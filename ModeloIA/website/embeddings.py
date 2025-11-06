from sentence_transformers import SentenceTransformer

# Modelo de embeddings (hay muchos, este es muy usado)
model = SentenceTransformer('all-MiniLM-L6-v2')

# Generar embeddings
frases = [
    "El edificio tiene aislamiento térmico",
    "Medidas para mejorar eficiencia energética",
    "Instalación de extintores contra incendios"
]

embeddings = model.encode(frases)

print(f"Forma del vector: {embeddings.shape}")
# Output: (3, 384) → 3 frases, 384 dimensiones cada una

print(f"Primer embedding: {embeddings[0][:5]}...")
# Output: [-0.04521887  0.08234156 -0.01923441  0.03441223  0.05123456]...

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Comparar las 3 frases
similarities = cosine_similarity(embeddings)

print("Matriz de similitud:")
print(similarities)

import chromadb
from chromadb.utils import embedding_functions

# Cliente (en memoria para el tutorial)
client = chromadb.Client()

# Embedder explícito (mismo modelo que antes)
embedder = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# Crear colección con función de embeddings
collection = client.create_collection(
    name="normativas",
    embedding_function=embedder
)

# Añadir documentos
collection.add(
    ids=["doc1", "doc2", "doc3"],
    documents=[
        "El aislamiento térmico debe cumplir U ≤ 0,75 W/m²K en zona D",
        "La eficiencia energética se mide por transmitancia térmica",
        "Los extintores deben ubicarse cada 15 metros máximo"
    ],
    metadatas=[
        {"tipo": "CTE-HE", "articulo": "3.1"},
        {"tipo": "CTE-HE", "articulo": "3.2"},
        {"tipo": "CTE-SI", "articulo": "9.1"}
    ]
)

# Buscar por similitud semántica
results = collection.query(
    query_texts=["¿Qué dice sobre aislar fachadas?"],
    n_results=2,
    include=["documents", "metadatas", "distances"]
)

print("Documentos encontrados:")
for i, doc in enumerate(results['documents'][0]):
    print(f"\n{i+1}. {doc}")
    print(f"   Metadata: {results['metadatas'][0][i]}")
    print(f"   Distancia: {results['distances'][0][i]:.3f}")

    # Búsqueda tradicional (como en el sistema actual de NormaConsult)
texto = "El aislamiento térmico debe cumplir U ≤ 0,75 W/m²K"

query = "eficiencia energética"

# ❌ NO encuentra nada porque no hay coincidencia exacta
if query.lower() in texto.lower():
    print("Encontrado")
else:
    print("No encontrado")  # ← Esto pasa

    # ✅ SÍ encuentra porque captura el significado
results = collection.query(
    query_texts=["eficiencia energética"],
    n_results=1,
    include=["documents"]
)

print(results['documents'][0][0])
# → "El aislamiento térmico debe cumplir..."

# Nueva colección para el ejemplo
collection = client.create_collection(
    name="normativas_filtrado",
    embedding_function=embedder
)

# Añadir documentos con metadata
collection.add(
    ids=["1", "2", "3"],
    documents=[
        "CTE DB-HE Art. 3.1: Aislamiento térmico en zona D",
        "La eficiencia energética mejora con aislamiento",
        "DB-SI Art. 9: Extintores cada 15m"
    ],
    metadatas=[
        {"db": "DB-HE"},
        {"db": "DB-HE"},
        {"db": "DB-SI"}
    ]
)

# Búsqueda con filtro por metadata
results = collection.query(
    query_texts=["aislamiento"],
    n_results=2,
    where={"db": "DB-HE"},
    include=["documents", "metadatas"]
)