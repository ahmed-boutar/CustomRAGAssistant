# app/services/pinecone_client.py
import pinecone
import os
from ..config import PINECONE_API_KEY, PINECONE_INDEX_NAME
from uuid import uuid4
from datetime import datetime

pc = pinecone.Pinecone(PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)

def upsert_documents(user_id: str, chunks: list[str], embeddings: list[list[float]], metadata: dict):
    namespace = f"user-{user_id}"
    now = datetime.utcnow().isoformat()
    vectors = []
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        vector_id = str(uuid4())
        chunk_metadata = metadata.copy()
        chunk_metadata.update({
            "chunk_index": i,
            "text": chunk,
            "timestamp": now
        })
        vectors.append({"id": vector_id, "values": embedding, "metadata": chunk_metadata})

    index.upsert(vectors=vectors, namespace=namespace)
    return namespace


def query_similar_chunks(user_id: str, query_embedding: list[float], top_k: int = 5):
    namespace = f"user-{user_id}"
    results = index.query(vector=query_embedding, top_k=top_k, include_metadata=True, namespace=namespace)
    return results["matches"]
