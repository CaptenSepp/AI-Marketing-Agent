from pydantic import BaseModel, Field
from rag_pipeline.models import Evidence, Source

_COLLECTION_PATTERN = r"^[A-Za-z0-9_-]+$"


class IngestRequest(BaseModel):
    # Existing clients may omit the body entirely; routes.py then uses the same default collection.
    collection_name: str = Field(default="agentic", pattern=_COLLECTION_PATTERN)


class QueryRequest(BaseModel):
    question: str = Field(min_length=1, max_length=10_000)
    include_evidence: bool = False
    # Selecting a collection keeps core, marketing, application, or future knowledge isolated.
    collection_name: str = Field(default="agentic", pattern=_COLLECTION_PATTERN)


class QueryResponse(BaseModel):
    answer: str
    sources: list[Source]
    retrieved_evidence: list[Evidence]
    evidence: list[Evidence]
    evaluation: dict | None = None
    run_id: str | None = None
