import json
import yaml
from app.services.spec_ingestion import ingest_spec 
from uuid import uuid4
from fastapi import APIRouter, UploadFile, File, Header, HTTPException, status
from app.utils.supabase_jwt import get_user_id_from_jwt

async def handle_uploaded_spec(
    user_id: str,
    spec_id: str,
    file: UploadFile
) -> int:
    # 1) Read the raw bytes & decode
    raw = (await file.read()).decode('utf-8')

    # 2) (Optional) Normalize / pretty-print
    if file.filename.endswith((".yaml", ".yml")):
        # already YAML—just re-dump to ensure consistent formatting
        spec_dict = yaml.safe_load(raw)
        raw_text = yaml.safe_dump(spec_dict, sort_keys=False)
    elif file.filename.endswith(".json"):
        spec_dict = json.loads(raw)
        raw_text = json.dumps(spec_dict, indent=2)
    else:
        raise ValueError("Only .yaml/.yml or .json specs accepted")

    # 3) Hand off to your existing splitter → embedder → upserter
    total_chunks = ingest_spec(user_id, spec_id, raw_text)
    return total_chunks 



router = APIRouter()

@router.post("/upload_spec", status_code=status.HTTP_201_CREATED)
async def upload_spec(
    file: UploadFile = File(...),
    authorization: str = Header(..., description="Bearer <supabase-access-token>")
):
    # 1) Extract Bearer token
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise ValueError()
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization header. Use: Bearer <token>"
        )

    # 2) Verify JWT & get user_id
    try:
        user_id = get_user_id_from_jwt(token)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token validation failed: {e}"
        )

    # 3) Generate a new spec_id
    spec_id = str(uuid4())

    # 4) Ingest the spec (normalize → chunk → embed → upsert to Pinecone)
    try:
        total_chunks = await handle_uploaded_spec(user_id, spec_id, file)
    except ValueError as ve:
        # e.g. unsupported file extension
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except Exception as ioe:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to ingest spec into Pinecone"
        )

    # 5) Return the new spec_id and how many chunks were created
    return {
        "spec_id": spec_id,
        "chunks_created": total_chunks
    }