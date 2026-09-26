from langchain_openai import ChatOpenAI

from agent_utilities.config.settings import AgentSettings


# Flow: Groq settings → API client → agent model.
# Role: Creates the Groq-compatible chat model.
# Input: AgentSettings.
# Output: ChatOpenAI.
def create_groq_chat_model(settings: AgentSettings) -> ChatOpenAI:
    if not settings.groq_api_key:
        raise ValueError("GROQ_API_KEY is required when MODEL_PROVIDER=groq")
    return ChatOpenAI(
        model=settings.groq_model,
        api_key=settings.groq_api_key,
        base_url="https://api.groq.com/openai/v1",
        use_responses_api=False,
    )
