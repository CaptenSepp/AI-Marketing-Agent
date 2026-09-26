from pydantic import BaseModel, Field


class Source(BaseModel):
    path: str
    chunk_index: int


class Evidence(Source):
    text: str
    distance: float


class RagAnswer(BaseModel):
    answer: str = Field(min_length=1)
    sources: list[Source]
    retrieved_evidence: list[Evidence] = []
    evidence: list[Evidence] = []


class IngestionResult(BaseModel):
    documents: int
    chunks: int
