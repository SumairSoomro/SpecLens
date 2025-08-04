from pinecone import Pinecone
from app import config
from typing import List, Dict

pc = Pinecone(api_key=config.PINECONE_API_KEY)
specLensIndex = pc.index = pc.Index(config.PINECONE_INDEX_NAME)


def upsert_chunks(chunks: list[dict], namespace: str = ""):
    specLensIndex.upsert(vectors=chunks, namespace=namespace)

