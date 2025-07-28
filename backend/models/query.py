from pydantic import BaseModel

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    session_id: str