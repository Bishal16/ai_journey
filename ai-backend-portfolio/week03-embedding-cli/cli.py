import os
import sys
from sentence_transformers import SentenceTransformer
import chromadb

DOCS_DIR = "docs"
model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.Client()
collection = client.get_or_create_collection("documents")

def ingest():
  for filename in os.listdir(DOCS_DIR):
    if not filename.endswith(".txt"):
      continue

    filepath = os.path.join(DOCS_DIR, filename)
    with open(filepath, "r") as f:
      text = f.read()

    chunks = [text[i:i+500] for i in range(0, len(text), 500)]

    for i, chunk in enumerate(chunks):
      embedding = model.encode(chunk).tolist()
      collection.add(
        ids=[f"{filename}-chunk-{i}"],
        embeddings=[embedding],
        documents=[chunk],
        metadatas=[{"source": filename}])

  print(f"Ingested {collection.count()} chunks into ChromaDB")

def search(query):
  query_embedding = model.encode(query).tolist()

  results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3
  )

  print(f"\nTop 3 results for: '{query}'\n")
  for i, (doc, meta) in enumerate(zip(results["documents"][0], results["metadatas"][0])):
    print(f"--- Result {i+1} (source: {meta['source']}) ---")
    print(doc)
    print()


if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("Usage: python cli.py <your search query>")
    sys.exit(1)

  ingest()
  query = " ".join(sys.argv[1:])
  search(query)