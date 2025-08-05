from typing import List
from uuid import uuid4
from app.utils.embeddings import embed_text
from app.utils.text_splitter import split_into_chunks
from app.services.vector_db import upsert_chunks

def ingest_spec(user_id: str, spec_id: str, raw_text: str) -> int:
    chunks = split_into_chunks(raw_text)
    total = 0

    # build all embeddings 
    # a payload is a list of vector objects with key values below
    payload = [
      {
        "id":       f"{user_id}_{spec_id}_chunk_{i}",
        "values":   embed_text(text),
        "metadata":{
          "user_id": user_id,
          "spec_id": spec_id
        }
      }
      for i, text in enumerate(chunks)
    ]

    # upsert in batches of 200 to avoid chance to limit
    for i in range(0, len(payload), 200):
        batch = payload[i : i + 200]
        upsert_chunks(batch, namespace=user_id)
        total += len(batch)

    return total