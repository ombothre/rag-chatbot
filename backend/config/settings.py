from dotenv import load_dotenv
import os

class Utils:
    def __init__(self):
        load_dotenv()
        redis_url = os.getenv("REDIS_URL")
        redis_port = os.getenv("REDIS_PORT")
        self.REDIS_URL: str =  redis_url if redis_url else "localhost"
        self.REDIS_PORT: str =  redis_port if redis_port else "6379"

utils = Utils()