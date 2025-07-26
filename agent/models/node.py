from enum import Enum

class Nodes(str, Enum):
    START = "__start__"
    END = "__end__"
    
    LLM_NODE = "llm_node"
    RAG_NODE = "rag_node"
    OUTPUT_NODE = "output_node"

    def __str__(self):
        return self.value