# supabase_jwt.py
import json, requests
from jose import jwt, JWTError
from app.config import SUPABASE_KEY,SUPABASE_URL



def get_user_id_from_jwt(token: str) -> str:
    """
    Verify a Supabase-issued JWT and return the unique user ID (sub claim).
    Raises JWTError on failure.
    """
    response = requests.get(
        f"{SUPABASE_URL}/auth/v1/user",
        headers={
            'Authorization': f'Bearer {token}',
            'apikey': SUPABASE_KEY  # Service key bypasses RLS
        },
        timeout=10
    )
    
    if response.status_code != 200:
        raise Exception(f"Invalid token: {response.status_code}")
    
    user_data = response.json()
    return user_data['id']