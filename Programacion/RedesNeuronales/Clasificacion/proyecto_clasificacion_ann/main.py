import argparse
import datetime as dt
import io
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import tensorflow as tf
from sklearn.compose import ColumnTransformer
from sklearn.datasets import load_breast_cancer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from tensorflow.keras import Sequential
from tensorflow.keras.callbacks import EarlyStopping, TensorBoard
from tensorflow.keras.layers import BatchNormalization, Dense, Dropout, Input
from tensorflow.keras.regularizers import l2


def parse_args():
    parser = argparse.ArgumentParser(description="Clasificación binaria con ANN + baseline")
    parser.add_argument("--data", type=str, default=None, help="Ruta a CSV opcional")
    parser.add_argument(
        "--dataset-source",
        type=str,
        default="owid",
        choices=["owid", "local", "sklearn"],
        help="Fuente del dataset si no se quiere usar CSV local",
    )
    parser.add_argument("--target-col", type=str, default="target", help="Nombre de la columna objetivo")
    parser.add_argument("--id-cols", type=str, nargs="*", default=[], help="Columnas ID a eliminar")
    parser.add_argument(
        "--owid-target-threshold",
        type=float,
        default=1.0,
        help="Umbral para target binario en OWID: new_deaths_per_million >= umbral",
    )
    parser.add_argument(
        "--owid-max-rows",
        type=int,
        default=120000,
        help="Máximo de filas OWID a usar (muestreo aleatorio estratificado simple por recorte)",
    )
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--learning-rate", type=float, default=1e-3)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output-dir", type=str, default="results")
    return parser.parse_args()


def load_owid_dataset(threshold=1.0, max_rows=120000, seed=42):
    urls = [
        "https://covid.ourworldindata.org/data/owid-covid-data.csv",
        "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv",
    ]
    last_error = None
    response = None
    used_url = None
    for url in urls:
        try:
            response = requests.get(url, timeout=60)
            response.raise_for_status()
            used_url = url
            break
        except Exception as exc:
            last_error = str(exc)

    if response is None:
        raise RuntimeError(
            "No se pudo descargar OWID (sin conectividad o DNS). "
            f"Último error: {last_error}. "
            "Puedes reintentar luego o ejecutar con --dataset-source sklearn temporalmente."
        )

    df = pd.read_csv(io.StringIO(response.text))

    df = df[~df["iso_code"].astype(str).str.startswith("OWID_")].copy()

    selected_cols = [
        "location",
        "continent",
        "new_cases_per_million",
        "total_cases_per_million",
        "reproduction_rate",
        "icu_patients_per_million",
        "hosp_patients_per_million",
        "people_vaccinated_per_hundred",
        "stringency_index",
        "population_density",
        "median_age",
        "aged_65_older",
        "cardiovasc_death_rate",
        "diabetes_prevalence",
        "gdp_per_capita",
        "new_deaths_per_million",
    ]
    selected_cols = [c for c in selected_cols if c in df.columns]
    df = df[selected_cols].copy()

    df = df.dropna(subset=["new_deaths_per_million"])
    df["target"] = (df["new_deaths_per_million"] >= threshold).astype(int)
    df = df.drop(columns=["new_deaths_per_million"])

    if max_rows is not None and len(df) > max_rows:
        df = df.sample(n=max_rows, random_state=seed)

    metadata = {
        "source": "Our World in Data COVID-19 dataset",
        "target": "target",
        "target_definition": f"new_deaths_per_million >= {threshold}",
        "url": used_url,
    }
    return df, "target", metadata


def load_dataset(csv_path, target_col, dataset_source="owid", owid_threshold=1.0, owid_max_rows=120000, seed=42):
    if csv_path is not None:
        df = pd.read_csv(csv_path)
        if target_col not in df.columns:
            raise ValueError(f"No existe la columna objetivo '{target_col}' en el dataset")
        metadata = {
            "source": str(csv_path),
            "target": target_col,
        }
        return df, target_col, metadata

    if dataset_source == "owid":
        return load_owid_dataset(threshold=owid_threshold, max_rows=owid_max_rows, seed=seed)

    if dataset_source == "sklearn":
        ds = load_breast_cancer(as_frame=True)
        df = ds.frame.copy()
        if "target" not in df.columns:
            df[target_col] = ds.target
        metadata = {
            "source": "sklearn.datasets.load_breast_cancer (dataset similar, binario)",
            "target": "target",
        }
        return df, "target", metadata

    if dataset_source == "local":
        raise ValueError("Para dataset-source='local' debes indicar --data con la ruta del CSV")

    raise ValueError("dataset-source no válido. Usa: owid, local o sklearn")


def encode_target_binary(y_series):
    y = y_series.copy()
    if pd.api.types.is_numeric_dtype(y):
        unique = sorted(pd.Series(y).dropna().unique().tolist())
        if len(unique) != 2:
            raise ValueError(f"La variable objetivo debe ser binaria. Valores encontrados: {unique}")
        y = y.astype(int)
        return y.to_numpy()

    y = y.astype(str).str.strip().str.lower()
    mapping = {
        "0": 0,
        "1": 1,
        "false": 0,
        "true": 1,
        "no": 0,
        "yes": 1,
        "negativo": 0,
        "positivo": 1,
        "low": 0,
        "high": 1,
    }
    if set(y.unique()).issubset(set(mapping.keys())):
        return y.map(mapping).astype(int).to_numpy()

    values = sorted(y.unique().tolist())
    if len(values) != 2:
        raise ValueError(f"La variable objetivo debe ser binaria. Valores encontrados: {values}")
    value_to_int = {values[0]: 0, values[1]: 1}
    return y.map(value_to_int).astype(int).to_numpy()


def split_data(df, target_col, id_cols, seed):
    clean_df = df.drop_duplicates().copy()
    cols_to_drop = [c for c in id_cols if c in clean_df.columns]
    if cols_to_drop:
        clean_df = clean_df.drop(columns=cols_to_drop)

    y = encode_target_binary(clean_df[target_col])
    X = clean_df.drop(columns=[target_col])

    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=0.30, random_state=seed, stratify=y
    )
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.50, random_state=seed, stratify=y_temp
    )

    return X_train, X_val, X_test, y_train, y_val, y_test


def build_preprocessor(X_train):
    num_cols = X_train.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = [c for c in X_train.columns if c not in num_cols]

    numeric_pipe = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_pipe = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    pre = ColumnTransformer(
        transformers=[
            ("num", numeric_pipe, num_cols),
            ("cat", categorical_pipe, cat_cols),
        ],
        remainder="drop",
    )

    return pre


def to_dense(arr):
    return arr.toarray() if hasattr(arr, "toarray") else np.asarray(arr)


def build_mlp(input_dim, regularized=False, learning_rate=1e-3):
    reg = l2(1e-4) if regularized else None
    model = Sequential()
    model.add(Input(shape=(input_dim,)))
    model.add(Dense(64, activation="relu", kernel_regularizer=reg))
    if regularized:
        model.add(BatchNormalization())
        model.add(Dropout(0.30))
    model.add(Dense(32, activation="relu", kernel_regularizer=reg))
    if regularized:
        model.add(Dropout(0.20))
    model.add(Dense(1, activation="sigmoid"))

    optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
    model.compile(
        optimizer=optimizer,
        loss="binary_crossentropy",
        metrics=[
            tf.keras.metrics.BinaryAccuracy(name="accuracy"),
            tf.keras.metrics.Recall(name="recall"),
            tf.keras.metrics.AUC(name="auc"),
        ],
    )
    return model


def compute_metrics(y_true, y_prob):
    y_pred = (y_prob >= 0.5).astype(int)
    acc = accuracy_score(y_true, y_pred)
    rec = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    auc = roc_auc_score(y_true, y_prob)
    cm = confusion_matrix(y_true, y_pred)
    if cm.shape == (2, 2):
        tn, fp, fn, tp = cm.ravel()
        spec = tn / (tn + fp) if (tn + fp) > 0 else 0.0
    else:
        spec = np.nan
    return {
        "accuracy": acc,
        "recall": rec,
        "specificity": spec,
        "f1": f1,
        "auc_roc": auc,
        "cm": cm,
    }


def plot_history(history, out_path, title):
    hist = pd.DataFrame(history.history)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    axes[0].plot(hist["loss"], label="train")
    axes[0].plot(hist["val_loss"], label="val")
    axes[0].set_title(f"Loss - {title}")
    axes[0].set_xlabel("epoch")
    axes[0].legend()

    axes[1].plot(hist["accuracy"], label="train")
    axes[1].plot(hist["val_accuracy"], label="val")
    axes[1].set_title(f"Accuracy - {title}")
    axes[1].set_xlabel("epoch")
    axes[1].legend()

    fig.tight_layout()
    fig.savefig(out_path, dpi=140, bbox_inches="tight")
    plt.close(fig)


def plot_confusion(cm, out_path, title):
    fig, ax = plt.subplots(figsize=(4.5, 4.5))
    im = ax.imshow(cm, cmap="Blues")
    ax.set_title(title)
    ax.set_xlabel("Predicción")
    ax.set_ylabel("Real")
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, str(cm[i, j]), ha="center", va="center")
    fig.colorbar(im, ax=ax)
    fig.tight_layout()
    fig.savefig(out_path, dpi=140, bbox_inches="tight")
    plt.close(fig)


def plot_roc(y_true, y_prob, out_path, title):
    fpr, tpr, _ = roc_curve(y_true, y_prob)
    auc = roc_auc_score(y_true, y_prob)
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.plot(fpr, tpr, label=f"AUC={auc:.4f}")
    ax.plot([0, 1], [0, 1], linestyle="--")
    ax.set_xlabel("FPR")
    ax.set_ylabel("TPR")
    ax.set_title(title)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_path, dpi=140, bbox_inches="tight")
    plt.close(fig)


def train_and_eval_mlp(
    X_train,
    y_train,
    X_val,
    y_val,
    X_test,
    y_test,
    regularized,
    args,
    tb_dir,
    fig_dir,
    name,
):
    model = build_mlp(X_train.shape[1], regularized=regularized, learning_rate=args.learning_rate)
    model.summary()

    callbacks = [
        EarlyStopping(monitor="val_loss", patience=10, restore_best_weights=True),
        TensorBoard(log_dir=str(tb_dir), histogram_freq=1),
    ]

    history = model.fit(
        X_train,
        y_train,
        validation_data=(X_val, y_val),
        epochs=args.epochs,
        batch_size=args.batch_size,
        callbacks=callbacks,
        verbose=0,
    )

    val_prob = model.predict(X_val, verbose=0).ravel()
    test_prob = model.predict(X_test, verbose=0).ravel()

    val_metrics = compute_metrics(y_val, val_prob)
    test_metrics = compute_metrics(y_test, test_prob)

    plot_history(history, fig_dir / f"history_{name}.png", name)
    plot_confusion(val_metrics["cm"], fig_dir / f"cm_val_{name}.png", f"CM Val - {name}")
    plot_confusion(test_metrics["cm"], fig_dir / f"cm_test_{name}.png", f"CM Test - {name}")
    plot_roc(y_val, val_prob, fig_dir / f"roc_val_{name}.png", f"ROC Val - {name}")
    plot_roc(y_test, test_prob, fig_dir / f"roc_test_{name}.png", f"ROC Test - {name}")

    return model, val_metrics, test_metrics


def train_and_eval_logreg(X_train, y_train, X_val, y_val, X_test, y_test):
    clf = LogisticRegression(max_iter=2000)
    clf.fit(X_train, y_train)

    val_prob = clf.predict_proba(X_val)[:, 1]
    test_prob = clf.predict_proba(X_test)[:, 1]

    val_metrics = compute_metrics(y_val, val_prob)
    test_metrics = compute_metrics(y_test, test_prob)
    return val_metrics, test_metrics


def flatten_metrics(model_name, split_name, m):
    return {
        "model": model_name,
        "split": split_name,
        "accuracy": m["accuracy"],
        "recall": m["recall"],
        "specificity": m["specificity"],
        "f1": m["f1"],
        "auc_roc": m["auc_roc"],
        "tn": int(m["cm"][0, 0]),
        "fp": int(m["cm"][0, 1]),
        "fn": int(m["cm"][1, 0]),
        "tp": int(m["cm"][1, 1]),
    }


def main():
    args = parse_args()
    np.random.seed(args.seed)
    tf.random.set_seed(args.seed)

    out_root = Path(args.output_dir)
    tb_root = out_root / "tensorboard"
    fig_root = out_root / "graficas"
    tb_root.mkdir(parents=True, exist_ok=True)
    fig_root.mkdir(parents=True, exist_ok=True)

    df, target_col, metadata = load_dataset(
        csv_path=args.data,
        target_col=args.target_col,
        dataset_source=args.dataset_source,
        owid_threshold=args.owid_target_threshold,
        owid_max_rows=args.owid_max_rows,
        seed=args.seed,
    )
    X_train_df, X_val_df, X_test_df, y_train, y_val, y_test = split_data(
        df=df,
        target_col=target_col,
        id_cols=args.id_cols,
        seed=args.seed,
    )

    pre = build_preprocessor(X_train_df)
    X_train = to_dense(pre.fit_transform(X_train_df))
    X_val = to_dense(pre.transform(X_val_df))
    X_test = to_dense(pre.transform(X_test_df))

    run_id = dt.datetime.now().strftime("%Y%m%d_%H%M%S")

    print("Fuente dataset:", metadata["source"])
    print("Variable objetivo:", metadata["target"])
    if "target_definition" in metadata:
        print("Definición del target:", metadata["target_definition"])
    if "url" in metadata:
        print("URL dataset:", metadata["url"])
    print("Tamaños -> train/val/test:", X_train.shape[0], X_val.shape[0], X_test.shape[0])
    print("Features tras preprocesado:", X_train.shape[1])

    model_base, val_base, test_base = train_and_eval_mlp(
        X_train,
        y_train,
        X_val,
        y_val,
        X_test,
        y_test,
        regularized=False,
        args=args,
        tb_dir=tb_root / f"mlp_base_{run_id}",
        fig_dir=fig_root,
        name="mlp_base",
    )

    model_reg, val_reg, test_reg = train_and_eval_mlp(
        X_train,
        y_train,
        X_val,
        y_val,
        X_test,
        y_test,
        regularized=True,
        args=args,
        tb_dir=tb_root / f"mlp_reg_{run_id}",
        fig_dir=fig_root,
        name="mlp_reg",
    )

    val_lr, test_lr = train_and_eval_logreg(X_train, y_train, X_val, y_val, X_test, y_test)

    rows = [
        flatten_metrics("mlp_base", "val", val_base),
        flatten_metrics("mlp_base", "test", test_base),
        flatten_metrics("mlp_reg", "val", val_reg),
        flatten_metrics("mlp_reg", "test", test_reg),
        flatten_metrics("logreg", "val", val_lr),
        flatten_metrics("logreg", "test", test_lr),
    ]

    res_df = pd.DataFrame(rows)
    res_df.to_csv(out_root / "metrics_summary.csv", index=False)

    with open(out_root / "model_info.txt", "w", encoding="utf-8") as f:
        f.write("MLP base params: " + str(model_base.count_params()) + "\n")
        f.write("MLP reg params: " + str(model_reg.count_params()) + "\n")

    print("\nResumen métricas:")
    print(res_df)
    print("\nGuardado en:", out_root.resolve())
    print("TensorBoard logs en:", tb_root.resolve())


if __name__ == "__main__":
    main()
