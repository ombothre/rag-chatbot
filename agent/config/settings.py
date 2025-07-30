from dotenv import load_dotenv
from pydantic import SecretStr
import os

class Utils:
    def __init__(self):
        load_dotenv()
        gemini_key = os.getenv("GEMINI_API_KEY")
        qdrant_url = os.getenv("QDRANT_URL")
        qdrant_db = os.getenv("QDRANT_DB_NAME")
        self.GEMINI_API_KEY = SecretStr(gemini_key) if gemini_key else None
        self.QDRANT_URL = qdrant_url if qdrant_url else None
        self.QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
        self.QDRANT_DB = qdrant_db if qdrant_db else "test"

utils = Utils()