from langchain_core.messages import AIMessage, HumanMessage, messages_to_dict, messages_from_dict
import json

lst = [AIMessage(content="Hi"), HumanMessage(content="hello")]
a = messages_to_dict(lst)
b = json.dumps(a)

st = """[{"type": "ai", "data": {"content": "Hi", "additional_kwargs": {}, "response_metadata": {}, "type": "ai", "name": null, "id": null, "example": false, "tool_calls": [], "invalid_tool_calls": [], "usage_metadata": null}}, {"type": "human", "data": {"content": "hello", "additional_kwargs": {}, "response_metadata": {}, "type": "human", "name": null, "id": null, "example": false}}]"""

t = json.loads(st)

s = messages_from_dict(t)

print(s)

