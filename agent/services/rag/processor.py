from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_core.documents import Document
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from agent.services.rag.vectordb import vdb

# Documents
def get_text_loaders(paths: list[Path]) -> list[Document]:
    text_loaders = []
    for i in paths:
        for file in i.glob("*.txt"):
            text_loaders.extend(TextLoader(file_path=str(file), encoding="utf-8").load())
    return text_loaders
    
def get_pdf_loaders(paths: list[Path]) -> list[Document]:
    pdf_loaders = []
    for i in paths:
        for file in i.glob("*.pdf"):
            pdf_loaders.extend(PyPDFLoader(file_path=str(file)).load())
    return pdf_loaders

def get_documents(pdf_paths: list[Path], txt_paths: list[Path]) -> list[Document]:
        return get_pdf_loaders(pdf_paths) + get_text_loaders(txt_paths)

# Splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap = 100
)

class Processor():
    def __init__(self, pdf_paths: list[Path], txt_paths: list[Path]) -> None:
        self.documents: list[Document] = get_documents(pdf_paths, txt_paths)
        print("DOCUMENTS: ", len(self.documents))
        self.chunked_documents = text_splitter.split_documents(self.documents)
    
    def get_chunked_documents(self) -> list[Document]:
        return self.chunked_documents
    
    def add_documents(self) -> None:
        vdb.add_documents(self.chunked_documents)