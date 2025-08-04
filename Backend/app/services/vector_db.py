from pinecone import Pinecone
from app import config

pc = Pinecone(api_key=config.PINECONE_API_KEY)
print(pc.list_indexes().names())