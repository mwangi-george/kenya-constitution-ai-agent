# 🇰🇪 Katiba AI — Constitution of Kenya Assistant

Katiba AI is an AI-powered assistant that enables users to query **The Constitution of Kenya (2010)** and receive **precise, context-grounded answers with verifiable citations**.

The system combines retrieval-augmented generation (RAG), OpenAI models, and a modern React interface to deliver an intuitive, ChatGPT-like experience tailored for legal reference.

## ![](docs/frontend_ui.png)

## Project Structure

```
.
├── agent-backend   # FastAPI + Pydantic AI + pgvector (RAG pipeline)
└── agent-frontend  # React + Vite + Tailwind + shadcn UI (chat interface)
```

---

## Core Features

- **Context-aware Q&A** over the Constitution PDF
- **Citation-backed responses** (traceable to source text)
- **Streaming responses (SSE)** for real-time interaction
- **RAG architecture** (embeddings + vector search)
- **Modern UI**
- **Dockerized backend** with PostgreSQL + pgvector
- Modular, maintainable, OOP-based backend design

---

## Tech Stack

### Backend

- FastAPI
- Pydantic AI (agent orchestration)
- OpenAI (LLM + embeddings)
- PostgreSQL + pgvector
- SQLAlchemy (async)

### Frontend

- React + TypeScript (Vite)
- Tailwind CSS
- shadcn/ui components
- TanStack Query

---

## Getting Started

### 1. Backend Setup

```bash
cd agent-backend

# create env file
cp .env.example .env

```

### 2. Frontend Setup

```bash

cd agent-frontend

# create env file
cp .env.example .env
```

### 3 Start all services

```bash
docker compose up --build
```

Then index the Constitution:

```bash
docker compose exec api python -m app.scripts.index_constitution
```

Backend runs at:

```
http://localhost:8000
```

Frontend runs at

```
http://localhost:5173
```

---

## Usage

1.  Open the frontend UI
2.  Ask any question about the Constitution
3.  Receive:
    - Real-time streamed answer
    - Supporting citations from the document

---

## Architecture Overview

```
User → React UI → FastAPI → Retriever (pgvector)
                        ↓
                 Context Injection
                        ↓
                Pydantic AI Agent
                        ↓
              Streaming Response (SSE)
```

---

## Notes

- Ensure your OpenAI API key is set in the backend `.env`
- Embeddings must be indexed before querying
- Streaming uses **Server-Sent Events (SSE)**

---

## Future Improvements

- Structured article/section parsing
- Chat history & persistence
- Authentication & user sessions
- Mobile-first optimization
- Offline / local model support

---

## License

MIT License

---

## Author

[George Mwangi](github.com/mwangi-george)
