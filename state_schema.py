from typing import Annotated, TypedDict, List
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    messages: Annotated[List, add_messages]
    current_code: str
    error_log: str
    iteration: int
    use_local: bool