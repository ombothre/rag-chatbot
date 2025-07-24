from langchain_google_genai import ChatGoogleGenerativeAI
from agent.config.settings import utils
from agent.services.tools import add, product

class LLM:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            api_key=utils.GEMINI_API_KEY
        )
        # LLM with tools
        self.llm_with_tools = self.llm.bind_tools([add, product])

    def get_llm(self):
        return self.llm
    
    def get_tools_llm(self):
        return self.llm_with_tools
