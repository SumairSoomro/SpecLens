# app/config.py
import os
from supabase import create_client, Client
from dotenv import load_dotenv
from openai import OpenAI



load_dotenv()


PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
JWKS_URL = f"{SUPABASE_URL}/auth/v1/.well-known/jwks.json"


supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
OpenAIclient = OpenAI(api_key=OPENAI_API_KEY)
