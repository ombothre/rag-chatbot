from langchain_core.messages import HumanMessage, AIMessage, AnyMessage, messages_from_dict, messages_to_dict
import json
from typing import cast

def to_human_msg(message: str) -> HumanMessage:
    return HumanMessage(content=message)

def to_ai_msg(message: str) -> AIMessage:
    return AIMessage(content=message)

def serialize_history(history: list[AnyMessage]) -> str:
    flat = []
    for msg in history:
        if isinstance(msg, list):
            flat.extend(msg)
        else:
            flat.append(msg)
    return json.dumps(messages_to_dict(flat))

def deserialize_history(serialized: str) -> list[AnyMessage]:
    return cast(list[AnyMessage],messages_from_dict(json.loads(serialized)))