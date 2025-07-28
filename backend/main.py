from fastapi import FastAPI, HTTPException, Header, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from backend.models.query import QueryRequest, QueryResponse
from langchain_core.messages import AnyMessage
from typing import Optional, Annotated
from agent.main import api_chat
from backend.helpers.messages import to_ai_msg, to_human_msg, deserialize_history, serialize_history
from backend.services.lifespan import lifespan
from backend.services.redis_client import RedisDB
import uuid

redis_db = RedisDB.create()

app = FastAPI(title="RAG Chatbot API", lifespan=lifespan)

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

# Dependency
async def get_redis_db(request: Request) -> RedisDB:
    if not hasattr(request.app.state, 'redis_db') or not request.app.state.redis_db:
        raise HTTPException(status_code=503, detail="Redis not connected")
    return request.app.state.redis_db

@app.post("/api/ask", response_model=QueryResponse, tags=["Chat"])
async def ask_question(
        payload: QueryRequest, 
        session_id: Annotated[Optional[str], Header()] = None,
        db: RedisDB = Depends(get_redis_db)
    ):
    
    if not session_id:
        session_id = str(uuid.uuid4())

    session_history_s = await db.get_history(session_id)
    if isinstance(session_history_s, list):
        session_history_s = "".join(session_history_s)  # flatten Redis list

    session_history = deserialize_history(session_history_s) if session_history_s else []
    human_msg = to_human_msg(payload.question)
    session_history.append(human_msg)

    response = api_chat(history=session_history)

    ai_msg = to_ai_msg(response)
    session_history.append(ai_msg)

    try:
        serialized_session_history = serialize_history(session_history)
        await db.add_message(session_id, serialized_session_history)
    except Exception as e:
        print("REDIS ADD ERROR: ", str(e))

    return QueryResponse(answer=response, session_id=session_id)
