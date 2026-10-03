# ── 1. IMPORTS & SETUP ──────────────────────────────────────
import os
import json
import uuid
from datetime import datetime

# Only set offline if explicitly requested or already cached
# os.environ.setdefault("HF_HUB_OFFLINE", "0")

# ── 2. MEMORY CLIENT (ChromaDB with JSON Fallback) ──────────
collection = None

class JSONFallbackCollection:
    """Safe fallback store if ChromaDB or sentence-transformers is unavailable."""
    def __init__(self, filepath="./osint_memory/fallback_memory.json"):
        self.filepath = filepath
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump({"ids": [], "documents": [], "metadatas": []}, f)

    def _load(self):
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"ids": [], "documents": [], "metadatas": []}

    def _save(self, data):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def count(self):
        return len(self._load().get("ids", []))

    def get(self, ids=None):
        data = self._load()
        if not ids:
            return data
        filtered_ids = []
        filtered_docs = []
        filtered_metas = []
        for i, doc_id in enumerate(data.get("ids", [])):
            if doc_id in ids:
                filtered_ids.append(doc_id)
                filtered_docs.append(data["documents"][i])
                filtered_metas.append(data["metadatas"][i])
        return {"ids": filtered_ids, "documents": filtered_docs, "metadatas": filtered_metas}

    def add(self, documents, metadatas, ids):
        data = self._load()
        data["ids"].extend(ids)
        data["documents"].extend(documents)
        data["metadatas"].extend(metadatas)
        self._save(data)

    def delete(self, ids=None):
        if not ids:
            self._save({"ids": [], "documents": [], "metadatas": []})
            return
        data = self._load()
        new_ids, new_docs, new_metas = [], [], []
        for i, doc_id in enumerate(data.get("ids", [])):
            if doc_id not in ids:
                new_ids.append(doc_id)
                new_docs.append(data["documents"][i])
                new_metas.append(data["metadatas"][i])
        self._save({"ids": new_ids, "documents": new_docs, "metadatas": new_metas})

    def query(self, query_texts, n_results=3):
        data = self._load()
        docs = data.get("documents", [])
        metas = data.get("metadatas", [])
        ids = data.get("ids", [])
        if not docs:
            return {"documents": [[]], "metadatas": [[]], "ids": [[]]}
        # Simple keyword matching heuristic
        query_words = set(query_texts[0].lower().split())
        scored = []
        for doc, meta, doc_id in zip(docs, metas, ids):
            text = (doc + " " + meta.get("subject", "") + " " + meta.get("query", "")).lower()
            score = sum(1 for w in query_words if w in text)
            scored.append((score, doc, meta, doc_id))
        scored.sort(key=lambda x: x[0], reverse=True)
        top = scored[:n_results]
        return {
            "documents": [[x[1] for x in top]],
            "metadatas": [[x[2] for x in top]],
            "ids": [[x[3] for x in top]]
        }


try:
    import chromadb
    from chromadb.utils import embedding_functions

    client = chromadb.PersistentClient(path="./osint_memory")
    try:
        embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        collection = client.get_or_create_collection(
            name="investigations",
            embedding_function=embedding_fn,
        )
    except Exception as emb_err:
        # Default chromadb embedding fallback
        collection = client.get_or_create_collection(name="investigations")
except Exception as e:
    collection = JSONFallbackCollection()


# ── 3. MEMORY OPERATIONS ────────────────────────────────────
def save_investigation(subject: str, report: str, query: str) -> str:
    """Save an investigation report to long-term memory."""
    entry_id = str(uuid.uuid4())
    collection.add(
        documents=[report],
        metadatas=[{
            "subject": subject,
            "query": query,
            "timestamp": datetime.now().isoformat(),
        }],
        ids=[entry_id],
    )
    return entry_id


def search_memory(query: str, n_results: int = 3) -> str:
    """Search past investigations for relevant information."""
    results = collection.query(query_texts=[query], n_results=n_results)

    if not results.get("documents") or not results["documents"][0]:
        return "No relevant past investigations found in memory."

    output = (
        "⚠️ CRITICAL INSTRUCTION TO THE AI: The text below is the ONLY information "
        "available from memory. You must quote it VERBATIM in your response. Do NOT "
        "add dates, URLs, or facts that are not shown below. Do NOT paraphrase. If "
        "the user asks about a subject not shown below, say \"I have no memory of "
        f"that subject.\"\n\nFound {len(results['documents'][0])} relevant past investigations:\n\n"
    )

    for i, (doc, metadata) in enumerate(zip(results["documents"][0], results["metadatas"][0]), 1):
        output += f"--- Past Investigation {i} ---\n"
        output += f"Subject: {metadata.get('subject', 'Unknown')}\n"
        output += f"Original Query: {metadata.get('query', 'Unknown')}\n"
        output += f"Date: {metadata.get('timestamp', 'Unknown')[:10]}\n"
        output += f"Report excerpt:\n{doc[:1500]}...\n\n"

    return output


def list_all_subjects() -> str:
    """List everything the agent has ever investigated."""
    results = collection.get()
    if not results.get("metadatas"):
        return "Memory is empty. No past investigations."

    subjects = [
        {"subject": m.get("subject", "Unknown"), "timestamp": m.get("timestamp", "Unknown")[:10]}
        for m in results["metadatas"]
    ]
    subjects.sort(key=lambda x: x["timestamp"], reverse=True)

    output = f"Past investigations ({len(subjects)} total):\n"
    for s in subjects:
        output += f"  - {s['subject']} (investigated {s['timestamp']})\n"
    return output


def clear_memory(subject_id: str = None):
    """Delete a single memory item or clear all memory."""
    if hasattr(collection, "delete"):
        if subject_id:
            collection.delete(ids=[subject_id])
        else:
            collection.delete()
