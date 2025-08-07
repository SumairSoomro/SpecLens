from fastapi import FastAPI
from app import config
from app.routes.upload_spec import router as upload_spec_router

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
        data = config.supabase.table("testTable").select("*").execute()
        return {"status": "success", "data": data.data}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    

app.include_router(upload_spec_router)