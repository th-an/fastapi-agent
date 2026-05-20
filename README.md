# FastAPI Agentic Workflow

AI-powered agent with FastAPI, MongoDB, and PydanticAI.

## Features

- **Phase 1**: FastAPI + MongoDB Motor + Pydantic models
- **Phase 2**: PydanticAI agent with database tools
- **Phase 3**: Streaming SSE chat + invoice file upload
- **Phase 4**: Pytest tests, Logfire telemetry, Azure CI/CD

## Setup

```bash
cp .env.example .env
# Edit .env with your credentials

pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `MONGODB_URL` | MongoDB connection string |
| `ANTHROPIC_API_KEY` | Anthropic API key |
| `LOGFIRE_TOKEN` | Logfire observability (optional) |

## Endpoints

- `GET /health` - Health check
- `POST /agent/query` - Query AI agent
- `POST /api/v1/chat/` - Streaming chat
- `POST /api/v1/invoices` - Upload invoice document

## Azure Deployment

Deployed via GitHub Actions to Azure Container Apps.