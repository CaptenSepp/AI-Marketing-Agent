from langgraph.graph import MessagesState


class AgentState(MessagesState):
    step_count: int
    validation_error: str | None
    final_answer: str
