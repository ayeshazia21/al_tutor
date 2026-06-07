#vector_memory.py
import chromadb
from chromadb.config import Settings
import uuid

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection("agent_memory")


# -----------------------------
# CLEAN METADATA (FIX)
# -----------------------------
def clean_metadata(metadata: dict):
    if not metadata:
        return {}

    cleaned = {}

    for k, v in metadata.items():
        if v is None:
            continue
        if isinstance(v, (str, int, float, bool)):
            cleaned[k] = v
        else:
            cleaned[k] = str(v)  # convert complex objects safely

    return cleaned


# -----------------------------
# STORE MEMORY
# -----------------------------
def store_memory(text, metadata=None):
    doc_id = str(uuid.uuid4())

    collection.add(
        documents=[text],
        metadatas=[clean_metadata(metadata)],
        ids=[doc_id]
    )


# -----------------------------
# SEARCH MEMORY
# -----------------------------
def search_memory(query, k=5):
    results = collection.query(
        query_texts=[query],
        n_results=k
    )

    return results.get("documents", [[]])[0]


# -----------------------------
# GET ALL MEMORY (for UI)
# -----------------------------
def get_all_memories(limit=20):
    data = collection.get(
        limit=limit,
        include=["documents", "metadatas"]
    )

    memories = []

    for doc, meta in zip(data.get("documents", []), data.get("metadatas", [])):
        memories.append({
            "text": doc,
            "metadata": meta
        })

    return memories