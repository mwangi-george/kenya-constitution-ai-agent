# Constitution Frontend

A polished Vite + React + TypeScript frontend for querying The Constitution of Kenya, 2010.

## Stack

- Vite
- React
- TypeScript
- Tailwind CSS
- shadcn-style UI components
- TanStack Query

## Getting started

```bash
npm install
cp .env-example.example .env
npm run dev
```

Set `VITE_API_BASE_URL` to your FastAPI server URL.

## Suggested backend contract

The UI expects:

- `POST /chat` returning:

```json
{
  "answer": "...",
  "citations": [
    {
      "chunk_id": "abc123",
      "article_label": "Article 43",
      "page_number": 29,
      "excerpt": "..."
    }
  ]
}
```

- `POST /chat/stream` returning Server-Sent Events with messages shaped like:

```text
event: token
data: {"content":"..."}

event: complete
data: {"citations":[...]}
```

If your API uses a slightly different shape, update `src/services/chat-service.ts` only.
