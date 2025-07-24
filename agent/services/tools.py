from langchain.tools import tool

@tool
def add(a: int, b: int) -> int:
    """Add two given numbers"""
    return a + b