from collections import defaultdict

from langchain_core.documents import Document


# Flow: Document chunks → source indexes → vector storage.
# Role: Assigns each chunk its index within the source document.
# Input: List of document chunks.
# Output: Enriched document chunks.
# Numbers chunks separately within each source file so retrieved evidence can be identified.
# The enriched documents are returned to ingestion and then stored in Chroma.
def assign_chunk_source_indexes(chunks: list[Document]) -> list[Document]:
    counts: defaultdict[str, int] = defaultdict(int)
    # Use the opaque document ID to maintain an independent counter per document.
    for chunk in chunks:
        document_id = str(chunk.metadata.get("document_id", "unknown"))
        chunk.metadata["chunk_index"] = counts[document_id]
        counts[document_id] += 1
    return chunks
