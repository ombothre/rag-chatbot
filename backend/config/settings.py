from dotenv import load_dotenv
import os

class Utils:
    def __init__(self):
        load_dotenv()
        redis_url = os.getenv("REDIS_URL")
        redis_port = os.getenv("REDIS_PORT")
        redis_user = os.getenv("REDIS_USER")
        redis_psw = os.getenv("REDIS_PASSWORD")
        self.REDIS_URL: str =  redis_url if redis_url else "localhost"
        self.REDIS_PORT: int =  int(redis_port) if redis_port else 6379
        self.REDIS_USER: str = redis_user if redis_user else "default"
        self.REDIS_PSW: str = redis_psw if redis_psw else ""

utils = Utils()