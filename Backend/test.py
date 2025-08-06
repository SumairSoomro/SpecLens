#!/usr/bin/env python3
import os

# adjust these imports to match your project layout
from app.services.vector_db import specLensIndex
from app.services.spec_ingestion import ingest_spec
from app.utils.embeddings import embed_text

def main():
    # Make sure these env vars are set in your shell:
    #   export PINECONE_API_KEY=…
    #   export PINECONE_INDEX_NAME=…
    
    user_id = "test_user"
    spec_id = "test_spec"

    # 1) Ingest some sample text
    raw_text = (
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
        "Vivamus lacinia odio vitae vestibulum vestibulum. "
        "Cras venenatis euismod malesuada. "
    ) * 30

    count = ingest_spec(user_id, spec_id, raw_text)
    print(f"Ingested {count} chunks into namespace '{user_id}' for spec '{spec_id}'")
    
    user_id = "test_user"
    spec_id = "test_spec"
   
    
    # 2) Query Pinecone with a snippet of that text
    query_text = "vestibulum"
    qvec = embed_text(query_text)
    resp = specLensIndex.query(
        namespace=user_id,
        vector=qvec,
        top_k=3,
        include_metadata=True

    )


    print("\nTop 3 matches for query 'vestibulum':")
    for match in resp.matches:
        print(f"  id={match.id}  score={match.score:.4f}  metadata={match.metadata}")

if __name__ == "__main__":
    main()
