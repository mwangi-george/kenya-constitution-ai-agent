# Kenya Constitution Chatbot

A modular project for building a traceable chatbot over **THE CONSTITUTION OF KENYA, 2010** using:

- **FastAPI** for the API layer
- **Pydantic AI** for the answer-generation agent
- **OpenAI** for chat and embeddings
- **PostgreSQL + pgvector** for vector storage and retrieval
- **Docker Compose** for local development

The chatbot is designed to:
- answer only from the indexed constitution text,
- return concise mobile-friendly answers,
- include traceable citations back to stored chunks.

## Project structure

```text
app/
  ai/
    constitution_agent.py
    deps.py
  api/
    dependencies.py
    routes/chat.py
  core/
    config.py
  data/
    constitution.pdf
  db/
    initializer.py
    models.py
    session.py
  repositories/
    document_chunk_repository.py
  schemas/
    chat.py
  services/
    chatbot_service.py
    embedding_service.py
    indexing_service.py
    pdf_loader.py
    retriever.py
    text_chunker.py
  scripts/
    index_constitution.py
  main.py
Dockerfile
docker-compose.yml
requirements.txt
.env.example
```

## 1. Add environment variables

Copy the example file:

```bash
cp .env.example .env
```

Then set your OpenAI API key in `.env`.

## 2. Add the constitution PDF

Place your PDF here:

```text
app/data/constitution.pdf
```

## 3. Start the stack

```bash
docker compose up --build
```

This starts:
- `api` on port `8000`
- `db` on port `5432`

## 4. Index the constitution

In a new terminal:

```bash
docker compose exec api python -m app.scripts.index_constitution
```

## 5. Test the chatbot

### Standard response

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question":"What does the Constitution say about freedom of expression?"}'
```

### Streaming response

```bash
curl -N -X POST http://localhost:8000/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"question":"What does the Constitution say about the Bill of Rights?"}'
```

## Notes

- This project uses simple chunking with lightweight article detection.
- For stronger legal traceability, the next improvement is to parse the PDF into a richer hierarchy such as chapter -> article -> clause before embedding.
- `text-embedding-3-small` uses 1536 dimensions, so the vector column is configured to match that. OpenAI lists `text-embedding-3-small` and `text-embedding-3-large` on its pricing page, and Pydantic AI supports OpenAI chat models through `OpenAIChatModel`.
