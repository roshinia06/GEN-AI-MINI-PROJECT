import os
import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
chroma_path = os.path.join(base_dir, "chroma_db")
client = chromadb.PersistentClient(path=chroma_path)
try:
    collection = client.get_collection(name="travel")
except:
    collection = client.create_collection(name="travel")


import uuid

def add_to_vector_store(texts):
    embeddings = model.encode(texts).tolist()

    for i, text in enumerate(texts):
        collection.add(
            documents=[text],
            embeddings=[embeddings[i]],
            ids=[str(uuid.uuid4())]
        )


def query_vector_store(query):
    query_embedding = model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=3
    )

    return results["documents"]
