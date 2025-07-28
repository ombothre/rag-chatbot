from fastapi import FastAPI
from contextlib import asynccontextmanager
from backend.services.redis_client import RedisDB

@asynccontextmanager
async def lifespan(app: FastAPI):
    # On startup:
    app.state.redis_db = await RedisDB.create()
    yield
    # On shutdown:
    if app.state.redis_db and app.state.redis_db.r:
        await app.state.redis_db.r.close()
        print("Redis connection closed.")
