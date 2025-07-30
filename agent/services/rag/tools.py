from langchain.tools import tool, Tool
from agent.services.rag.vectordb import VectorDB
from typing import cast


def rag_tool(vector: VectorDB) -> Tool:
    @tool(response_format="content")
    def rag(query: str):
        """Retrieve information related to a query."""
        retrieved = vector.similarity_search(query)
        print(retrieved)
        data = "\n\n".join([f"Source: {doc.metadata}\nContent: {doc.page_content}" for doc in retrieved])
        
        return data
    return cast(Tool, rag)