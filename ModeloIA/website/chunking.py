def chunk_by_chars(text, chunk_size=500, overlap=50):
    """Divide texto en chunks de tamaño fijo con overlap"""
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap  # overlap para mantener contexto

    return chunks

# Ejemplo
texto = "Lorem ipsum " * 100
chunks = chunk_by_chars(texto, chunk_size=200, overlap=20)

print(f"Total chunks: {len(chunks)}")
print(f"Chunk 1: {chunks[0][:50]}...")
print(f"Chunk 2: {chunks[1][:50]}...")

