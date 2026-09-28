# AI Marketing Agent

An agentic AI system for marketing workflows, built around LLM orchestration, retrieval-augmented generation, structured tools, and reusable AI infrastructure.

This repository shows selected parts of a larger implementation. Some internal workflow logic, prompts, integrations, configuration, and production-oriented components are intentionally not included in the public version.

## Overview

The system combines several layers:

- **Marketing Agent** — coordinates AI-assisted marketing workflows including planning, research, content generation, and structured outputs.
- **RAG Pipeline** — retrieves relevant knowledge from document collections and provides grounded context to AI workflows.
- **Shared Agent Utilities** — reusable abstractions for LLM access, tools, state, and common agent functionality.
- **Web Interface** — provides a user-facing interface for interacting with the system.

The complete project also contains additional private orchestration and integration components that are not part of the public showcase.

## Technology Stack

### Agentic AI

- LangGraph
- LangChain
- LangSmith
- Structured tool calling
- Multi-step agent workflows
- LLM orchestration
- State-based workflow management
- Validation and evaluation

### RAG & Knowledge Retrieval

- Retrieval-Augmented Generation (RAG)
- Document ingestion
- Embedding generation
- Semantic search
- Vector databases
- Metadata-based retrieval
- Context preparation
- Incremental document processing

### Models & AI Providers

The architecture supports both local and API-based language models and embedding models.

Provider and model selection is separated from the main workflow so the underlying models can be exchanged without redesigning the agent architecture.

### Backend & Data

- Python
- FastAPI
- Pydantic
- Chroma
- PostgreSQL / Supabase
- pgvector
- HTTP APIs

### Development & Operations

- Modular Python packages
- Typed data models
- Environment-based configuration
- Testing and validation
- Observability and tracing
- Docker-based development and deployment support

## Architecture

At a high level, the system follows this structure:

```text
User Interface
      │
      ▼
Marketing Agent
      │
      ├── LLM / Agent Workflow
      ├── Tools
      ├── Research
      └── RAG
             │
             ▼
      Knowledge Sources
      Embeddings
      Vector Search
```

Shared utilities provide common functionality used across the agent and retrieval layers.

The full implementation contains additional orchestration, evaluation, integrations, storage, and workflow logic that is intentionally omitted from the public repository.

## RAG Pipeline

The RAG layer is designed as an independent component rather than embedding retrieval logic directly inside the agent.

Its responsibilities include:

1. loading source documents,
2. preparing documents for retrieval,
3. generating embeddings,
4. storing and retrieving vector representations,
5. selecting relevant context,
6. providing structured evidence to downstream AI workflows.

The implementation supports multiple knowledge collections and interchangeable storage backends.

## Agent Architecture

Agent workflows are built with **LangGraph** and use **LangChain-compatible tools**.

The architecture separates:

- state,
- tools,
- retrieval,
- model access,
- workflow orchestration,
- validation,
- observability.

This separation allows individual parts of the system to evolve independently and makes tools reusable across different AI workflows.

## Observability & Evaluation

The complete project uses **LangSmith** and additional application-level evaluation mechanisms for tracing and analyzing AI workflows.

This includes monitoring model and tool interactions, inspecting multi-step execution, and evaluating workflow outputs.

Detailed evaluation logic and tracing configuration are not included in the public showcase.

## Public Repository Scope

This repository is intentionally a **selected technical showcase**, not a complete runnable distribution.

It includes representative implementation for parts of:

- the marketing system,
- RAG infrastructure,
- shared agent utilities,
- data models,
- LLM integration,
- tool abstractions,
- and the user interface.

Some files and directories are intentionally empty or incomplete to preserve the overall project structure without publishing private implementation details.

Not included publicly:

- proprietary prompts,
- core workflow intelligence,
- private integrations,
- credentials or environment configuration,
- internal data and vector stores,
- private automation,
- deployment-specific configuration,
- selected evaluation and orchestration logic.

The purpose of the repository is to demonstrate the system architecture, engineering approach, and technologies used without publishing the complete implementation.