from agent.services.helpers import ai_input, ai_print
from agent.models.state import MessageState
from agent.ai.graph import AiGraph
from typing import cast

def chat(message: str):
    ai = AiGraph()
    result = cast(MessageState, ai.run(ai_input(message)))

    # for i in result["messages"]:
    #     i.pretty_print()
    
    # print(result) 

    ai_print(result["messages"])

    # ai.view()