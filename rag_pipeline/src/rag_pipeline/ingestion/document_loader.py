from hashlib import sha256
from pathlib import Path

from langchain_core.documents import Document

SUPPORTED_SUFFIXES = {".md", ".txt"}
BOOK_METADATA_FIELDS = {"book_title", "author", "chapter_title", "chapter_number"}
METADATA_VERSION = 2


def _read_book_metadata(text: str) -> dict[str, str | int]:
    """Read the small scalar frontmatter subset produced for book chapters."""
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}
    metadata: dict[str, str | int] = {}
    for line in text[4:end].splitlines():
        key, separator, raw_value = line.partition(":")
        if not separator or key not in BOOK_METADATA_FIELDS:
            continue
        value = raw_value.strip().strip('"')
        if not value or value.lower() == "null":
            continue
        metadata[key] = (
            int(value) if key == "chapter_number" and value.isdigit() else value
        )
    return metadata


# Flow: Documents folder → supported files → LangChain documents with stable metadata.
# Role: Loads non-empty Markdown and text source files for one collection.
# Input: Source folder path.
# Output: List of Document objects.
# Each document receives a stable path-based document_id and a content hash.
# document_id identifies the same source file across later ingestion runs.
# document_hash changes only when that file's text changes, so unchanged files can be skipped.
def load_source_documents(root: Path) -> list[Document]:
    documents: list[Document] = []
    # Sorting keeps document order stable across repeated runs.
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES:
            text = path.read_text(encoding="utf-8")
            # Skip empty files because they cannot produce useful searchable chunks.
            if text.strip():
                # Use the path relative to this collection's source folder as the stable identity.
                # This avoids depending on the machine's absolute repository path.
                source_key = path.relative_to(root).as_posix()
                document_id = sha256(source_key.encode("utf-8")).hexdigest()
                document_hash = sha256(text.encode("utf-8")).hexdigest()
                metadata = _read_book_metadata(text)
                metadata.update(
                    {
                        "source_label": path.name,
                        "document_type": path.suffix.lower(),
                        "document_id": document_id,
                        "document_hash": document_hash,
                        "metadata_version": METADATA_VERSION,
                    }
                )
                documents.append(
                    Document(
                        page_content=text,
                        metadata=metadata,
                    )
                )
    return documents
