from agent.services.helpers import ai_input, ai_print
from agent.models.state import MessageState
from agent.ai.graph import AiGraph
from typing import cast
from agent.services.rag.processor import Processor
from pathlib import Path
from agent.services.rag.vectordb import vdb

changi_txt_path = Path("agent/services/scraper/data/changi/visible_text")
changi_pdf_path = Path("agent/services/scraper/data/changi/pdfs")

jewel_txt_path = Path("agent/services/scraper/data/jewel/visible_text")
jewel_pdf_path = Path("agent/services/scraper/data/jewel/pdfs")

def rag_setup():
    if vdb.check_empty():
        rag_processor = Processor(
            txt_paths=[changi_txt_path, jewel_txt_path], 
            pdf_paths=[changi_pdf_path, jewel_pdf_path]
        )
        rag_processor.add_documents()

def chat(message: str):
    ai = AiGraph()
    ai.view()
    result = cast(MessageState, ai.run(ai_input(message)))

    for msg in result["messages"]:
        msg.pretty_print()
    # ai_print(result["messages"])