from typing import List, Dict
from typing import Optional, Dict, Any
from app.utils.embeddings import embed_text
from app.utils.openai_chat import get_openai_response
from app.services.vector_db import query_chunks
from app.utils.supabase_jwt import get_user_id_from_jwt
from fastapi import APIRouter, HTTPException, Header, Body



def build_context(chunks: List[Dict], max_chars: int = 8000) -> str:
    """
    Concatenate chunk texts with simple budget control.
    (You can swap to token-aware truncation later.)
    """
    parts, total = [], 0
    for i, ch in enumerate(chunks, start=1):
        # Tag each chunk so we can cite it later
        txt = ch.get("chunk_text", "") or ""
        block = f"[{i}] (id={ch['id']}, spec={ch.get('spec_id')}, score={ch.get('score'):.4f})\n{txt}\n"
        if total + len(block) > max_chars:
            break
        parts.append(block)
        total += len(block)
    return "\n".join(parts)

STRICT_SYSTEM = (
    "You are a helpful assistant that answers only using the provided context.\n"
    "If the context doesn’t fully answer, reply exactly: 'The provided documentation does not include information on this topic.'\n"
    "Do not use outside knowledge. Do not guess. Do not invent fields.\n"
    "Prefer concise, readable answers in plain English. Use bullet points when helpful."
)

def build_prompt(context: str, question: str) -> str:
    """
    Build a simple string prompt that includes the strict system instructions.
    This matches what your get_openai_response function expects.
    """
    prompt = f"""{STRICT_SYSTEM}

Context:
{context}

Question: {question}

Instructions:
- Answer using ONLY the context above.
- If insufficient, say "The provided documentation does not include information on this topic." 
-  Keep the answer easy to read (short paragraphs / bullets).
"""
    
    return prompt

def answer_question_strict_rag(
    user_id: str,
    question: str,
    spec_id: Optional[str] = None,
    top_k: Optional[int] = None,
    model: Optional[str] = None,  # stays nano to avoid temperature param injection
) -> Dict[str, Any]:
    # 1) Embed the query
    q_emb = embed_text(question)

    # 2) Retrieve relevant chunks (already thresholded inside query_chunks)
    hits = query_chunks(q_emb,user_id)

    if not hits:
        return {
            "answer": "The provided documentation does not include information on this topic."
        }

    # 3) Build context & prompt
    context = build_context(hits)
    prompt = build_prompt(context, question)

    # 4) Call your existing helper (no custom temperature/system here)
    answer = get_openai_response(prompt)

    # 5) Map labels -> chunk ids for UI
    citations = [
        {"label": i + 1, "id": h.get("id"), "spec_id": h.get("spec_id"), "score": h.get("score")}
        for i, h in enumerate(hits)
    ]

    return {
        "answer": answer,
        "citations": citations
    }


router = APIRouter()

@router.post("/ask")
def ask(
    question: str = Body(..., embed=True),
    spec_id: Optional[str] = Body(None),
    top_k: Optional[int] = Body(None),
    model: Optional[str] = Body(None),
    authorization: str = Header(...),
):
    try:
        # Extract token from Authorization header
        if not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid authorization header format")
        token = authorization.split(" ")[1]

        # Get user_id from Supabase
        user_id = get_user_id_from_jwt(token)

        # Call RAG service
        return answer_question_strict_rag(
            user_id=user_id,
            question=question,
            spec_id=spec_id,
            top_k=top_k,
            model=model
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))