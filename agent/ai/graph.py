from typing import Literal, cast
from collections.abc import Sequence
from langgraph.graph import StateGraph
from langchain_core.messages import AIMessage, AnyMessage
from agent.models.state import MessageState
from agent.models.node import Nodes
from agent.ai.prompts import system_prompt, output_prompt
from agent.services.helpers import has_tools, run_tools, view_graph
from agent.services.rag.tools import rag_tool
from agent.services.rag.vectordb import VectorDB
from agent.ai.llm import LLM


class AiGraph:
    def __init__(self, vector_db: VectorDB):
        self.vector_db = vector_db

        # Create tools
        self.rag = rag_tool(self.vector_db)
        self.tools = {
            "rag": self.rag
        }

        self.llm = LLM(self.tools)
        self.tool_llm = self.llm.get_tools_llm()
        self.output_llm = self.llm.get_llm()

        # Graph
        self.builder = StateGraph(MessageState)
        self._build_graph()
        self.graph = self.builder.compile()

    ## ---------------- Nodes ---------------- ##

    def llm_node(self, state: MessageState) -> MessageState:
        result = self.tool_llm.invoke(state["messages"])
        return {
            "messages": [cast(AnyMessage, result)]
        }

    def rag_node(self, state: MessageState) -> MessageState:
        curr_message = cast(AIMessage, state["messages"][-1])
        tools_list = run_tools(curr_message.tool_calls, self.tools)
        return {
            "messages": tools_list
        }

    def output_node(self, state: MessageState) -> MessageState:
        result = self.output_llm.invoke([*state["messages"], output_prompt])
        return {
            "messages": [cast(AnyMessage, result)]
        }

    ## --------------- Conditional --------------- ##
    def tools_condition(self, state: MessageState) -> Literal[Nodes.RAG_NODE, Nodes.END]:
        if has_tools(state["messages"][-1]):
            return Nodes.RAG_NODE
        return Nodes.END

    ## --------------- Build Graph --------------- ##
    def _build_graph(self):
        # Nodes
        self.builder.add_node(Nodes.LLM_NODE, self.llm_node)
        self.builder.add_node(Nodes.RAG_NODE, self.rag_node)
        self.builder.add_node(Nodes.OUTPUT_NODE, self.output_node)

        # Edges
        self.builder.add_edge(Nodes.START, Nodes.LLM_NODE)
        self.builder.add_conditional_edges(Nodes.LLM_NODE, self.tools_condition)
        self.builder.add_edge(Nodes.RAG_NODE, Nodes.OUTPUT_NODE)
        self.builder.add_edge(Nodes.OUTPUT_NODE, Nodes.END)

    ## --------------- Run --------------- ##
    def run(self, messages: Sequence[AnyMessage]):
        try:
            return self.graph.invoke({"messages": [system_prompt, *messages]})
        except Exception as e:
            print("Graph Failed:", str(e))

    def get(self):
        return self.graph

    def view(self):
        view_graph(self.graph)
        