from app import config
from openai import OpenAI

client = OpenAI(api_key=config.OPENAI_API_KEY)


def embed_text(text: str) -> list[float]: # convert string to list of vectors
    """
    Call OpenAI’s embedding API to get a vector for `text`.
    """
    resp = client.embeddings.create(model="text-embedding-3-small",
    input=text)
    return resp.data[0].embedding