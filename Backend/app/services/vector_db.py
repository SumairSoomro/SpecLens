from pinecone import Pinecone
from app import config


pc = Pinecone(api_key=config.PINECONE_API_KEY)
specLensIndex = pc.Index(config.PINECONE_INDEX_NAME)

#each chunk is a vector object with key value pairs
def upsert_chunks(chunks, namespace: str):
    specLensIndex.upsert(vectors=chunks, namespace=namespace)

# namespace is like a folder of vectors
