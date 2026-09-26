from langchain_core.embeddings import Embeddings
from rag_pipeline.config.settings import RagSettings
from rag_pipeline.llm.embeddings import create_ollama_embeddings


# Flow: RAG settings → embedding client → ingestion pipeline.
# Role: Creates the embedding service used during ingestion.
# Input: RagSettings.
# Output: Embeddings.
# Provides the embedding client used during ingestion without exposing provider setup here.
# The returned service converts chunks into vectors when the vector store adds documents.
def create_ingestion_embedding_service(settings: RagSettings) -> Embeddings:
    return create_ollama_embeddings(settings)
