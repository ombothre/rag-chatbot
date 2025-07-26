from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from backend.models.query import QueryRequest, QueryResponse
from agent.main import api_chat

app = FastAPI(title="RAG Chatbot API")

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

# health check
@app.get("/api/health")
def health():
    return {"status": "ok"}

# Chatbot Endpoint
@app.post("/api/ask", response_model=QueryResponse)
async def ask_question(payload: QueryRequest):
    try:
        response = api_chat(payload.question)
        return QueryResponse(answer=response)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
