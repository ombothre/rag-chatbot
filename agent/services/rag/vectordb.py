from langchain_google_genai import GoogleGenerativeAIEmbeddings
from agent.config.settings import utils
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from langchain_core.documents import Document

def setup_qdrant(url: str, embeddings: GoogleGenerativeAIEmbeddings) -> QdrantVectorStore:
    client = QdrantClient(url=url, api_key=utils.QDRANT_API_KEY, timeout=120, prefer_grpc=True)
    collection_found = False
    for collection in client.get_collections().collections:
        if collection.name == 'rag':
            collection_found = True

    if not collection_found:
        print("Creating new collection 'rag'")
        client.create_collection(
            collection_name="rag",
            vectors_config=VectorParams(size=768, distance=Distance.COSINE),
        )
    else:
        print("Collection 'rag' already exists")

    vector_store = QdrantVectorStore(
        client=client,
        collection_name="rag",
        embedding=embeddings
    )
    return vector_store

class VectorDB:

    @classmethod
    def create(cls, model: str = "models/embedding-001"):
        try:
            embeddings = GoogleGenerativeAIEmbeddings(model=model, google_api_key=utils.GEMINI_API_KEY)
            qdrant_url = utils.QDRANT_URL if utils.QDRANT_URL else ":memory:"
            vector_store = setup_qdrant(qdrant_url, embeddings)

            return cls(vector_store)
        
        except Exception as e:
             print(f"Error adding docs: {str(e)}")

    def __init__(self, vector_store: QdrantVectorStore) -> None:
        self.vector_store = vector_store
    
    def get_vector_db(self) -> QdrantVectorStore:
        return self.vector_store
    
    def check_empty(self) -> bool:
        stats = self.vector_store.client.get_collection("rag")
        return stats.points_count == 0
    
    def add_documents(self, documents: list[Document]) -> None:
        try:
            ids = self.vector_store.add_documents(documents=documents)
            print("IDs: ", ids)
        except Exception as e:
            print(f"Error adding docs: {str(e)}")
    
    def similarity_search(self, query: str, k: int = 3) -> list[Document]:
        return self.vector_store.similarity_search(query=query, k=k)