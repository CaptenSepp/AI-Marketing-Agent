# Agentic prototype

Two Python services in one repository. They use one shared Python environment and are installed together:

- `rag_pipeline`: standalone LangChain ingestion, retrieval, and answer service.
- `agent_harness`: standalone LangGraph tool-calling agent.

The agent can run with only its calculator tool or optionally call the RAG service through HTTP. Both services support Ollama `qwen3.5:9b`; the chat model can be switched to OpenAI with environment configuration. RAG embeddings remain local with `qwen3-embedding:0.6b`.

## Shared installation

Use one virtual environment at the repository root. It gives both services one resolved version of every shared dependency.

Prerequisite: install Python 3.11 or newer with the Windows Python Launcher (`py`).

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".\rag_pipeline[test]" -e ".\agent_harness[test]"
```

`-e` installs both local projects in editable mode: source-code changes are used without reinstalling. `[test]` adds the test dependencies. The virtual environment is a local `.venv` folder; keep it while developing and recreate it only if you need a clean install.

Each service still has its own `.env` file because their service settings differ. See the project READMEs for configuration and run commands.

## Start instructions

Configure each service once before first use:

```powershell
Copy-Item rag_pipeline\.env.example rag_pipeline\.env
Copy-Item agent_harness\.env.example agent_harness\.env
```

Use either browser interfaces or terminal chat:

```powershell
.\scripts\agent-ui.ps1
```

This starts the shared Agent Harness, Marketing, and Application interface at
`http://localhost:8002/docs` and the RAG page at `http://localhost:8001/`.
The shared interface package must already be installed. Keep the terminal open for logs;
Ctrl+C stops services started by this launcher. An already-running RAG service is reused.

On the RAG page, select a collection and click **Ingest with progress**.
Source files belong in `rag_pipeline/data/documents/<collection>`.
For Marketing books, use `rag_pipeline/data/documents/marketing/books`.
To ingest Marketing from PowerShell while RAG is running:

```powershell
Invoke-RestMethod -Method Post -Uri http://localhost:8001/ingest -ContentType "application/json" -Body '{"collection_name":"marketing"}'
```

Ingestion never clears unchanged data.
Ollama starts when needed and loads the installed embedding model.
Select a local or configured API answer model and collection on the same page; both selections are saved in `rag_pipeline/data/interface_settings.json` and restored after refresh or RAG restart.
RAG API documentation remains at `http://localhost:8001/docs`.

```powershell
.\scripts\agent-tui.ps1
```

This opens core-agent terminal chat, starts/reuses RAG and Ollama when needed,
and stops only processes it started when chat exits.

## Open feature PRs

These features are implemented in open pull requests and are not yet part of `development`:

- **TUI layout:** Refines the terminal UI with a left sidebar, saved sessions, session details, inline sources, and compact command aliases without changing backend logic.
- **RAG reranking:** Retrieves 10 chunks, reranks them by query-term overlap with vector distance as a tiebreaker, and keeps the best 4.
- **Generic tool system:** Adds a shared typed tool definition and registry used by the existing calculator and RAG tools while keeping the LangGraph tool flow unchanged.
- **Marketing agent:** Independent [Python workflow](marketing-agent/README.md) reusing Agent Harness utilities. One shared text/image result serves the selected channels; LinkedIn publishing is separate.
- **Web search tool:** Adds reusable current-web search through OpenAI web search and registers it in the shared tool system.
- **Application preparation tool:** Adds a tool that researches a target job, adapts an existing CV, and creates a cover letter using supported facts only.
- **Forced tool control:** Adds a TUI tool selector and direct runner so a selected tool can run without the LLM choosing the tool first.
- **Codex access tool:** Adds a reusable local Codex CLI adapter for answer, web-search, and image tasks with a stable result schema and local image artifacts.

## RAG collections and incremental ingestion

The project keeps one physical Chroma database at `rag_pipeline/data/vector_store_updated` and separates knowledge with named collections.

- Default knowledge uses collection `agentic` with source files in `rag_pipeline/data/documents/agentic`.
- New collections use `rag_pipeline/data/documents/<collection_name>`.
- Marketing books use `rag_pipeline/data/documents/marketing/books`.
- `POST /ingest` with `{"collection_name":"marketing"}` ingests only the `marketing` collection.
- `POST /query` with `collection_name` queries only that collection.
- Every source document gets a stable path-based ID and a content hash.
- Ingestion skips unchanged files before embedding and updates only new or changed files.
- Adding a new collection does not re-ingest existing collections.
- Adding one document does not re-ingest unchanged documents in its collection.
- The previous collection-wide `reset_collection()` behavior is removed.

The first ingestion of the existing `documents` collection after this change re-indexes its current files once because the old vectors do not contain the new stable ID/hash metadata. Later ingestion runs are incremental.


## Optional Supabase runtime storage

Source prompts, templates, and books stay in the repository/local source folders.
When `SUPABASE_ENABLED=true`, Marketing and RAG runtime results are mirrored to Supabase.
Marketing source files, uploaded images, and generated images are uploaded to the private `agent-artifacts` bucket.

Apply `database_setup/supabase/shared_agentic_storage.sql` to the linked Supabase project.
Set `SUPABASE_URL`, `SUPABASE_SECRET_KEY`, and `SUPABASE_DB_URL` in the root `.env`.
Set `VECTOR_BACKEND=supabase` to use Supabase pgvector for RAG; leave `chroma` to keep the local backend.
On the first Supabase ingestion, existing Chroma vectors are copied when possible; later ingestion remains document-hash incremental.
