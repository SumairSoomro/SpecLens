from pinecone import Pinecone
from typing import List, Dict, Optional
from app import config

pc = Pinecone(api_key=config.PINECONE_API_KEY)
specLensIndex = pc.Index(config.PINECONE_INDEX_NAME)

#each chunk is a vector object with key value pairs
def upsert_chunks(chunks, namespace: str):
    specLensIndex.upsert(vectors=chunks, namespace=namespace)

# namespace is like a folder of vectors

# You should define this constant somewhere in your config or constants module
SIMILARITY_THRESHOLD = 0.1  # adjust this value as needed

def query_chunks(
    query_emb: List[float],
    user_id: str,
    spec_id: Optional[str] = None,
    top_k: int = 5
) -> List[Dict]:
    """
    Retrieve the top_k most similar chunks for a query embedding.

    Searches the namespace=user_id (all that user’s docs),
    optionally filters to a single spec_id, and applies a similarity cutoff.

    Args:
        query_emb:  The embedding vector of the user’s question.
        user_id:    The Pinecone namespace to search (all that user’s uploads).
        spec_id:    If provided, only return chunks from this spec.
        top_k:      Number of candidates to fetch before thresholding.

    Returns:
        A list of dicts, each with:
          - "id":         chunk ID
          - "score":      cosine similarity score
          - "spec_id":    which spec it came from
          - "chunk_text": the original text of the chunk
    """
    # Build metadata filter if spec_id is provided
    metadata_filter = {"spec_id": spec_id} if spec_id else None

    resp = specLensIndex.query(
        namespace=user_id,
        vector=query_emb,
        filter=metadata_filter,
        top_k=top_k,
        include_metadata=True  # make sure metadata is included in results
    )

    results = []
    for match in resp.matches:
        if match.score is not None and match.score >= SIMILARITY_THRESHOLD:
            results.append({
                "id":         match.id,
                "score":      match.score,
                "spec_id":    match.metadata.get("spec_id"),
                "chunk_text": match.metadata.get("chunk_text")
            })

    return results