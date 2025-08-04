from fastapi import FastAPI
from config import supabase

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "hello world"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/test-supabase")
def test_supabase():
    # Just check if we can get the list of tables
    try:
        data = supabase.table("testTable").select("*").limit(1).execute()
        return {"status": "success", "data": data.data}
    except Exception as e:
        return {"status": "error", "message": str(e)}