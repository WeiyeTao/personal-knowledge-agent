import chromadb
from chromadb.utils import embedding_functions

def build_vector_store(texts, embeddings, persist_dir="./vector_store"):
    client = chromadb.PersistentClient(path=persist_dir)
    collection = client.get_or_create_collection(name="personal_knowledge")
    for i, (t, e) in enumerate(zip(texts, embeddings)):
        collection.add(documents=[t], embeddings=[e], ids=[f"id_{i}"])
    return collection


def query(collection, query_text, embedder):
    query_vec = embedder([query_text])[0]
    results = collection.query(query_embeddings=[query_vec], n_results=3)
    return results["documents"]
