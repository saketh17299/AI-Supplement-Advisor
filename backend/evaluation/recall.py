# backend/evaluation/recall.py
from backend.rag import embedder, qdrant_client

def recall_at_k(query, relevant_docs, k=3):
    query_vec = list(embedder.embed([query]))[0]
    results = qdrant_client.search(
        collection_name="supplements",
        query_vector=query_vec,
        limit=k
    )

    retrieved = [r.payload["page_content"] for r in results]
    return any(doc in retrieved for doc in relevant_docs)
