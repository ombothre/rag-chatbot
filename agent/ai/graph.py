from typing import Literal
from agent.ai.llm import LLM
from agent.ai.prompts import system_prompt, output_prompt
from langgraph.graph import StateGraph
from langchain_core.messages import AIMessage
from agent.models.state import MessageState
from langchain_core.messages import AnyMessage
from agent.services.helpers import has_tools, run_tools, view_graph
from agent.models.node import Nodes
from collections.abc import Sequence
from typing import cast

# State
## MessageState

# Nodes
## llm
llm = LLM()
tool_llm = llm.get_tools_llm()
output_llm = llm.get_llm()

def llm_node(state: MessageState) -> MessageState:
    result = tool_llm.invoke(state["messages"])
    return {
        "messages": [cast(AnyMessage, result)]
    }

## tool node
def rag_node(state: MessageState) -> MessageState:
    curr_message = cast(AIMessage, state["messages"][-1])
    tools_list = run_tools(curr_message.tool_calls)

    return {
        "messages": tools_list
    }

## output llm node
def output_node(state: MessageState) -> MessageState:
    result = output_llm.invoke([*state["messages"], output_prompt])
    return {
        "messages": [cast(AnyMessage, result)]
    }

# Edge
## conditional
def tools_condition(state: MessageState) -> Literal[Nodes.RAG_NODE, Nodes.END]:    # type: ignore # Replacing langgraph.prebuilt import tools_condition
    if has_tools(state["messages"][-1]):
        return Nodes.RAG_NODE
    return Nodes.END

# Graph
class AiGraph:

    def __init__(self):
        self.builder = StateGraph(MessageState)
        self._build_graph()
        self.graph = self.builder.compile()

    def _build_graph(self):
        # Nodes
        self.builder.add_node(Nodes.LLM_NODE, llm_node)
        self.builder.add_node(Nodes.RAG_NODE, rag_node)      # Replacing langgraph.prebuilt import ToolNode
        self.builder.add_node(Nodes.OUTPUT_NODE, output_node)

        # Edges
        self.builder.add_edge(Nodes.START, Nodes.LLM_NODE)
        self.builder.add_conditional_edges(Nodes.LLM_NODE, tools_condition)
        self.builder.add_edge(Nodes.RAG_NODE, Nodes.OUTPUT_NODE)
        self.builder.add_edge(Nodes.OUTPUT_NODE, Nodes.END)

    def run(self, messages: Sequence[AnyMessage]):
        # print([system_prompt, *messages])
        try:
            return self.graph.invoke({"messages": [system_prompt, *messages]})
        except Exception as e:
            print("Graph Failed: ",str(e))
    
    def get(self):
        return self.graph
    
    def view(self):
        view_graph(self.graph)