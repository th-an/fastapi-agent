# AP Invoice Pipeline - Implementation Status

## Use Case: Autonomous Accounts Payable (AP) Invoice Pipeline

This use case automates the ingestion, validation, parsing, and structured storage of incoming corporate invoices and receipts. Rather than relying on traditional, fragile Optical Character Recognition (OCR) templates, this system uses a multimodal agent to directly extract structured schema from document images.

---

## Implementation Report

### Component Status

| Component | Status | Notes |
|-----------|--------|-------|
| **FastAPI multipart upload** | ✅ Working | `POST /api/v1/invoices` accepts PDF/image |
| **InvoiceSchema (Pydantic)** | ✅ Working | `LineItem`, `InvoiceSchema` properly defined |
| **PydanticAI + Claude** | ✅ Working | Multimodal extraction with Claude Sonnet 4 |
| **MongoDB Atlas Storage** | ⚠️ Partial | Data stored but using raw dicts |
| **Logfire FastAPI** | ✅ Working | HTTP requests traced |
| **Logfire PydanticAI** | ✅ Working | Agent spans visible |
| **Logfire MongoDB tracing** | ❌ Not working | Dependency conflict with opentelemetry packages |

---

## Architecture

```
Invoice Upload (PDF/Image)
       ↓
FastAPI Route: POST /api/v1/invoices
       ↓
PydanticAI Agent (Claude Sonnet 4)
       ↓
Structured Extraction: InvoiceSchema
       ↓
MongoDB Atlas Storage
```

---

## Known Issues

### 1. MongoDB Storage - Date Serialization

**Problem:** `DBInvoiceRecord` fails when storing because MongoDB's BSON encoder cannot handle `datetime.date` objects directly.

**Current workaround:** Using raw dicts with manual date conversion (`billing_date.isoformat()`).

**Fix needed:** Create proper serialization layer or use a BSON-compatible date type.

### 2. Logfire MongoDB Instrumentation

**Problem:** `opentelemetry-instrumentation-pymongo` conflicts with other OpenTelemetry packages:
- Requires `opentelemetry-instrumentation==0.63b1`
- Conflicts with `opentelemetry-instrumentation-httpx==0.60b1`

**Current workaround:** Using only FastAPI and manual PydanticAI spans.

**Fix needed:** Either resolve dependency conflicts or use manual instrumentation for MongoDB.

---

## Project Structure

```
Stack/
├── app/
│   ├── main.py              # FastAPI app with Logfire instrumentation
│   ├── config.py            # Settings (Pydantic BaseSettings)
│   └── database.py          # MongoDB connection (Motor async driver)
├── agent/
│   ├── agent.py             # Customer service agent
│   ├── document_agent.py    # Invoice processing agent
│   ├── tools.py             # Database tool functions
│   └── result_types.py      # Pydantic models
│       ├── LineItem
│       ├── InvoiceSchema
│       ├── DBInvoiceRecord
│       ├── DocumentProcessingResult
│       └── QueryResult
├── routers/
│   └── api_v1.py            # API routes (/invoices, /chat)
└── requirements.txt
```

---

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/agent/query` | Query AI agent with customer/order tools |
| `POST` | `/api/v1/chat/` | Streaming SSE chat |
| `POST` | `/api/v1/invoices` | Upload invoice document |

---

## Environment Variables

| Variable | Status | Description |
|----------|--------|-------------|
| `MONGODB_URL` | ✅ Set | MongoDB Atlas connection string |
| `ANTHROPIC_API_KEY` | ✅ Set | Anthropic API key for Claude |
| `LOGFIRE_TOKEN` | ✅ Set | Logfire write token for observability |

---

## Next Steps

1. **Fix MongoDB date serialization** - Properly handle date types when storing to MongoDB
2. **Resolve OpenTelemetry dependency conflicts** - Install compatible versions or use manual instrumentation
3. **Add invoice query endpoint** - Endpoint to retrieve stored invoices
4. **Add invoice validation workflow** - Process to validate and approve extracted invoices

---

*Generated: 2026-05-22*