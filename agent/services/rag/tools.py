from langchain.tools import tool
from agent.services.rag.vectordb import vdb

@tool(response_format="content")
def rag(query: str):
    """Retrieve information related to a query."""
    retrieved = vdb.similarity_search(query)
    print(retrieved)
    data = "\n\n".join([f"Source: {doc.metadata}\nContent: {doc.page_content}" for doc in retrieved])
    
    return data

tools = {
    "rag": rag
}
