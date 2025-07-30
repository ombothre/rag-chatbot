from langchain_core.messages import AnyMessage, AIMessage
from collections.abc import Sequence
from agent.ai.graph import AiGraph
from agent.models.state import MessageState
from agent.services.helpers import ai_input
from agent.services.rag.processor import Processor
from pathlib import Path
from typing import cast

from agent.services.rag.vectordb import VectorDB

changi_txt_path = Path("agent/services/scraper/data/changi/visible_text")
changi_pdf_path = Path("agent/services/scraper/data/changi/pdfs")
jewel_txt_path = Path("agent/services/scraper/data/jewel/visible_text")
jewel_pdf_path = Path("agent/services/scraper/data/jewel/pdfs")

def rag_setup(vdb: VectorDB):
    if vdb.check_empty():
        rag_processor = Processor(
            txt_paths=[changi_txt_path, jewel_txt_path],
            pdf_paths=[changi_pdf_path, jewel_pdf_path]
        )
        rag_processor.add_documents()

def api_chat(history: Sequence[AnyMessage], vector: VectorDB) -> str:
    rag_setup(vector)
    ai = AiGraph()

    # Flatten message history
    flat_history: list[AnyMessage] = []
    for msg in history:
        if isinstance(msg, list):
            flat_history.extend(msg)
        else:
            flat_history.append(msg)

    result = cast(MessageState, ai.run(flat_history))
    response = cast(AIMessage, result["messages"][-1])

    if isinstance(response.content, list):
        return "\n".join(str(item) for item in response.content)
    return response.content
