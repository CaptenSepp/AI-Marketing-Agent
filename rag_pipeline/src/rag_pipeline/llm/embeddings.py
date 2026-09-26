from langchain_core.embeddings import Embeddings
from langchain_ollama import OllamaEmbeddings
from rag_pipeline.config.settings import RagSettings


# Flow: RAG settings → Ollama embedding client → vectors.
# Role: Creates the local embedding model client.
# Input: RagSettings.
# Output: Embeddings.
# Connects to the local Ollama embedding model through LangChain's standard interface.
# Chroma uses the returned object for both stored chunks and incoming search questions.
def create_ollama_embeddings(settings: RagSettings) -> Embeddings:
    return OllamaEmbeddings(
        model=settings.ollama_embedding_model,
        base_url=settings.ollama_base_url,
    )
