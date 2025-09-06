from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any

app = FastAPI(title="IntelliSupport API")

class QueryRequest(BaseModel):
    query: str
    context: Dict[str, Any] = None

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/query")
async def query_endpoint(req: QueryRequest):
    # This endpoint would call ManagerAgent in real implementation
    return {"response": "This is a stub response from the API", "query": req.query}
