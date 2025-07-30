from redis import asyncio as aioredis
from backend.config.settings import utils
from typing import List, cast, Awaitable

class RedisDB:
    """Asynchronous Redis Database client for managing chat history."""
    
    def __init__(self, client):
        self.r: aioredis.Redis = client

    @classmethod
    async def create(cls):
        try:
            # Create an async client
            client = aioredis.Redis(
                host=utils.REDIS_URL,
                port=utils.REDIS_PORT,
                username=utils.REDIS_USER,
                password=utils.REDIS_PSW,
                ssl=False,
                decode_responses=True
            )
            await client.ping()
            print("Successfully connected to Redis!")
            return cls(client)
        except Exception as e:
            print(f"Cannot connect to Redis: {str(e)}")
            return None

    async def add_message(self, key: str, value: str):
        if self.r:
            await cast(Awaitable, self.r.set(key, value))
        
    async def get_history(self, key: str) -> List[str]:
        if self.r:
            return await cast(Awaitable, self.r.get(key))
        return []
    
    async def delete_session(self, key: str):
        if self.r:
            return await self.r.delete(key)