from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from backend.models.query import QueryRequest, QueryResponse
from agent.main import api_chat

app = FastAPI(title="RAG Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

# Chatbot Endpoint
@app.post("/api/ask", response_model=QueryResponse, tags=["Chat"])
async def ask_question(payload: QueryRequest):
    try:
        response = api_chat(payload.question)
        return QueryResponse(answer=response)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
