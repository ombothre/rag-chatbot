from fastapi import FastAPI
from contextlib import asynccontextmanager
from backend.services.redis_client import RedisDB
from agent.services.rag.vectordb import VectorDB

@asynccontextmanager
async def lifespan(app: FastAPI):
    # On startup:
    app.state.redis_db = await RedisDB.create()    # redis
    app.state.vector_db = VectorDB.create()        # qdrant vector db
     
    yield
    # On shutdown:
    if app.state.redis_db and app.state.redis_db.r:
        await app.state.redis_db.r.close()
        print("Redis connection closed.")
