from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
from scipy.cluster.hierarchy import dendrogram, fcluster, linkage
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import (
    calinski_harabasz_score,
    davies_bouldin_score,
    silhouette_score,
)
from sklearn.preprocessing import StandardScaler


BASE_DIR = Path(__file__).resolve().parent
GDP_FILE = BASE_DIR / "API_NY.GDP.PCAP.PP.CD_DS2_en_csv_v2_35.csv"
POP_FILE = BASE_DIR / "API_SP.POP.TOTL_DS2_en_csv_v2_61.csv"
URB_FILE = BASE_DIR / "API_SP.URB.TOTL.IN.ZS_DS2_en_csv_v2_249.csv"


def load_world_bank_series(file_path: Path) -> pd.DataFrame:
    """Carga un CSV de World Bank ignorando metadatos iniciales."""
    return pd.read_csv(file_path, skiprows=4)


def get_year_columns(df: pd.DataFrame) -> list[str]:
    return [c for c in df.columns if str(c).isdigit() and len(str(c)) == 4]


def clean_merge_for_year(
    gdp_df: pd.DataFrame, pop_df: pd.DataFrame, urb_df: pd.DataFrame, year: str
) -> pd.DataFrame:
    cols = ["Country Name", "Country Code", year]

    g = gdp_df[cols].rename(columns={year: "GDP_PC"})
    p = pop_df[cols].rename(columns={year: "POP"})
    u = urb_df[cols].rename(columns={year: "URB_PCT"})

    merged = (
        g.merge(p, on=["Country Name", "Country Code"], how="inner")
        .merge(u, on=["Country Name", "Country Code"], how="inner")
        .rename(columns={"Country Name": "CN", "Country Code": "CC"})
    )

    for col in ["GDP_PC", "POP", "URB_PCT"]:
        merged[col] = pd.to_numeric(merged[col], errors="coerce")

    merged = merged.replace([np.inf, -np.inf], np.nan).dropna(
        subset=["GDP_PC", "POP", "URB_PCT"]
    )

    merged = merged[
        (merged["GDP_PC"] > 0)
        & (merged["POP"] > 0)
        & (merged["URB_PCT"] >= 0)
        & (merged["URB_PCT"] <= 100)
    ].copy()

    # Intentamos quedarnos solo con países ISO-3166 alpha-3.
    try:
        import pycountry

        valid_codes = {c.alpha_3 for c in pycountry.countries if hasattr(c, "alpha_3")}
        merged = merged[merged["CC"].isin(valid_codes)].copy()
    except Exception:
        # Fallback simple si pycountry no está instalado.
        merged = merged[
            merged["CC"].str.fullmatch(r"[A-Z]{3}", na=False)
            & ~merged["CN"].str.contains(
                "income|world|union|OECD|IDA|IBRD|states|Europe|Asia|Africa|America",
                case=False,
                na=False,
            )
        ].copy()

    merged["GDP"] = merged["GDP_PC"] * merged["POP"]
    merged["URB"] = merged["POP"] * merged["URB_PCT"] / 100.0

    return merged[["CC", "CN", "GDP", "POP", "URB", "URB_PCT", "GDP_PC"]]


def choose_latest_valid_year(
    gdp_df: pd.DataFrame, pop_df: pd.DataFrame, urb_df: pd.DataFrame
) -> tuple[str, pd.DataFrame]:
    years = sorted(
        set(get_year_columns(gdp_df))
        & set(get_year_columns(pop_df))
        & set(get_year_columns(urb_df)),
        reverse=True,
    )

    best_year = None
    best_df = pd.DataFrame()

    for year in years:
        df_year = clean_merge_for_year(gdp_df, pop_df, urb_df, year)
        if len(df_year) > len(best_df):
            best_year = year
            best_df = df_year
        if len(df_year) >= 50:
            return year, df_year

    if best_year is None:
        raise ValueError("No se encontró ningún año con datos válidos.")
    return best_year, best_df


def evaluate_hierarchical_models(X_scaled: np.ndarray) -> pd.DataFrame:
    rows = []
    max_k = min(10, X_scaled.shape[0] - 1)

    for link in ["single", "complete", "ward"]:
        for k in range(2, max_k + 1):
            model = AgglomerativeClustering(n_clusters=k, linkage=link)
            labels = model.fit_predict(X_scaled)
            if len(np.unique(labels)) < 2:
                continue

            rows.append(
                {
                    "linkage": link,
                    "k": k,
                    "silhouette": silhouette_score(X_scaled, labels),
                    "calinski_harabasz": calinski_harabasz_score(X_scaled, labels),
                    "davies_bouldin": davies_bouldin_score(X_scaled, labels),
                }
            )

    metrics_df = pd.DataFrame(rows)
    metrics_df = metrics_df.sort_values(
        by=["silhouette", "calinski_harabasz", "davies_bouldin"],
        ascending=[False, False, True],
    ).reset_index(drop=True)
    return metrics_df


def plot_3d_scatter(df: pd.DataFrame, output_path: Path) -> None:
    fig = plt.figure(figsize=(11, 8))
    ax = fig.add_subplot(111, projection="3d")

    x = np.log10(df["GDP"])
    y = np.log10(df["POP"])
    z = np.log10(df["URB"])

    ax.scatter(x, y, z, alpha=0.75)

    if len(df) <= 80:
        for _, row in df.iterrows():
            ax.text(
                np.log10(row["GDP"]),
                np.log10(row["POP"]),
                np.log10(row["URB"]),
                row["CC"],
                fontsize=7,
            )

    ax.set_xlabel("log10(GDP)")
    ax.set_ylabel("log10(POP)")
    ax.set_zlabel("log10(URB)")
    ax.set_title("Nube 3D de paises")
    fig.tight_layout()
    fig.savefig(output_path, dpi=180)
    plt.close(fig)


def plot_dendrograms(
    X_scaled: np.ndarray,
    labels_cc: pd.Series,
    method: str,
    selected_k: int,
    output_full: Path,
    output_intermediate_distance: Path,
    output_intermediate_k: Path,
) -> None:
    Z = linkage(X_scaled, method=method, metric="euclidean")

    fig = plt.figure(figsize=(16, 8))
    dendrogram(Z, labels=labels_cc.tolist(), leaf_rotation=90, leaf_font_size=6)
    plt.title(f"Dendrograma completo ({method})")
    plt.xlabel("Pais")
    plt.ylabel("Distancia")
    plt.tight_layout()
    plt.savefig(output_full, dpi=180)
    plt.close(fig)

    dist_threshold = float(np.percentile(Z[:, 2], 70))
    fig = plt.figure(figsize=(14, 7))
    dendrogram(
        Z,
        labels=labels_cc.tolist(),
        color_threshold=dist_threshold,
        leaf_rotation=90,
        leaf_font_size=7,
    )
    plt.axhline(y=dist_threshold, c="red", ls="--", label=f"threshold={dist_threshold:.2f}")
    plt.legend()
    plt.title(f"Dendrograma intermedio por distancia ({method})")
    plt.xlabel("Pais")
    plt.ylabel("Distancia")
    plt.tight_layout()
    plt.savefig(output_intermediate_distance, dpi=180)
    plt.close(fig)

    fig = plt.figure(figsize=(14, 7))
    dendrogram(
        Z,
        labels=labels_cc.tolist(),
        truncate_mode="lastp",
        p=selected_k,
        show_leaf_counts=True,
        leaf_rotation=90,
    )
    plt.title(f"Dendrograma intermedio por numero de clusters (k={selected_k})")
    plt.xlabel("Cluster agrupado")
    plt.ylabel("Distancia")
    plt.tight_layout()
    plt.savefig(output_intermediate_k, dpi=180)
    plt.close(fig)


def main() -> None:
    gdp_df = load_world_bank_series(GDP_FILE)
    pop_df = load_world_bank_series(POP_FILE)
    urb_df = load_world_bank_series(URB_FILE)

    selected_year, merged = choose_latest_valid_year(gdp_df, pop_df, urb_df)

    final_df = merged[["CC", "CN", "GDP", "POP", "URB"]].copy()
    final_df = final_df.replace([np.inf, -np.inf], np.nan).dropna().reset_index(drop=True)

    output_csv = BASE_DIR / "actividad58_dataset_paises.csv"
    final_df.to_csv(output_csv, index=False)

    X = np.log1p(final_df[["GDP", "POP", "URB"]].values)
    X_scaled = StandardScaler().fit_transform(X)

    metrics_df = evaluate_hierarchical_models(X_scaled)
    if metrics_df.empty:
        raise ValueError("No se pudieron calcular metricas de clustering.")

    best = metrics_df.iloc[0]
    best_linkage = str(best["linkage"])
    best_k = int(best["k"])

    cluster_model = AgglomerativeClustering(n_clusters=best_k, linkage=best_linkage)
    labels = cluster_model.fit_predict(X_scaled)
    final_df["cluster"] = labels

    metrics_path = BASE_DIR / "actividad58_metricas_clustering.csv"
    metrics_df.to_csv(metrics_path, index=False)

    clusters_path = BASE_DIR / "actividad58_dataset_con_clusters.csv"
    final_df.to_csv(clusters_path, index=False)

    scatter_path = BASE_DIR / "actividad58_scatter3d.png"
    plot_3d_scatter(final_df, scatter_path)

    dendro_full = BASE_DIR / "actividad58_dendrograma_completo.png"
    dendro_mid_dist = BASE_DIR / "actividad58_dendrograma_intermedio_distancia.png"
    dendro_mid_k = BASE_DIR / "actividad58_dendrograma_intermedio_k.png"

    plot_dendrograms(
        X_scaled,
        final_df["CC"],
        best_linkage,
        best_k,
        dendro_full,
        dendro_mid_dist,
        dendro_mid_k,
    )

    clusters_by_distance = fcluster(
        linkage(X_scaled, method=best_linkage, metric="euclidean"),
        t=np.percentile(linkage(X_scaled, method=best_linkage, metric="euclidean")[:, 2], 70),
        criterion="distance",
    )
    n_clusters_distance = len(np.unique(clusters_by_distance))

    print(f"Ano seleccionado: {selected_year}")
    print(f"Numero de paises validos: {len(final_df)}")
    print(f"Mejor modelo: linkage={best_linkage}, k={best_k}")
    print(
        "Metricas mejor modelo: "
        f"silhouette={best['silhouette']:.4f}, "
        f"calinski_harabasz={best['calinski_harabasz']:.2f}, "
        f"davies_bouldin={best['davies_bouldin']:.4f}"
    )
    print(f"Clusters estimados con criterio de distancia intermedia: {n_clusters_distance}")
    print(f"CSV final: {output_csv}")
    print(f"CSV metricas: {metrics_path}")
    print(f"CSV con clusters: {clusters_path}")
    print(f"Scatter 3D: {scatter_path}")
    print(f"Dendrograma completo: {dendro_full}")
    print(f"Dendrograma intermedio (distancia): {dendro_mid_dist}")
    print(f"Dendrograma intermedio (k): {dendro_mid_k}")


if __name__ == "__main__":
    main()