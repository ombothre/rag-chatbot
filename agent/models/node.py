from enum import Enum

class Nodes(str, Enum):
    START = "__start__"
    END = "__end__"
    
    LLM_NODE = "tool_llm_node"
    TOOL_NODE = "tool_call_node"

    def __str__(self):
        return self.value