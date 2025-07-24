from dotenv import load_dotenv
import os

class Utils:
    def __init__(self):
        load_dotenv()
        self.GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")
utils = Utils()