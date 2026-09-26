from langchain_core.language_models.chat_models import BaseChatModel
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

from agent_utilities.config.settings import AgentSettings
from agent_utilities.llm.fallback import FallbackChatModel
from agent_utilities.llm.groq_client import create_groq_chat_model


# Flow: Agent settings → provider selection → chat model.
# Role: Creates the configured reasoning model.
# Input: AgentSettings.
# Output: BaseChatModel.
# Creates the chat-model client selected in the settings so the graph is provider-independent.
# The returned LangChain model is passed to the decision node for all agent reasoning.
# Flow: Agent settings → provider selection & fallback chaining → resilient chat model.
# Role: Creates the configured reasoning model with zero-wait Ollama fallback.
# Junior-level note: Provides Groq as primary, falling back to local Ollama with a strict timeout.
# Junior-level note: Uses Groq/OpenAI as primary if keys are present, falling back to local Ollama.
def create_agent_chat_model(settings: AgentSettings) -> BaseChatModel:
    ollama_model = ChatOllama(
        model=settings.ollama_chat_model,
        base_url=settings.ollama_base_url,
        timeout=settings.ollama_timeout_seconds,
    )
    if settings.model_provider == "groq" and settings.groq_api_key:
        groq_model = create_groq_chat_model(settings)
        return FallbackChatModel(groq_model, ollama_model)
    if settings.model_provider == "openai" and settings.openai_api_key:
        openai_model = ChatOpenAI(
            model=settings.openai_model,
            api_key=settings.openai_api_key,
            use_responses_api=True,
        )
        return FallbackChatModel(openai_model, ollama_model)
    return ollama_model
