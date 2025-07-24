from typing import Annotated, TypedDict
from collections.abc import Sequence
from langchain_core.messages import AnyMessage
from agent.services.helpers import add_message

class MessageState(TypedDict):
    messages: Annotated[Sequence[AnyMessage], add_message]