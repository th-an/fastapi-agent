# FastAPI Agentic Workflow

AI-powered agent with FastAPI, MongoDB, PydanticAI, and Anthropic Claude.

## Features

- **Phase 1**: FastAPI + MongoDB Motor + Pydantic models
- **Phase 2**: PydanticAI agent with database tools (customer info, order status, invoice validation)
- **Phase 3**: Streaming SSE chat + multimodal invoice document processing
- **Phase 4**: Pytest tests, Logfire telemetry, Azure CI/CD

## Use Case: Autonomous Accounts Payable (AP) Invoice Pipeline

This application implements an AI-powered invoice processing pipeline that:

1. **Ingests** invoice documents (PDF, PNG, JPEG) via multipart file upload
2. **Extracts** structured data using multimodal AI (no OCR needed)
3. **Validates** data against strict Pydantic schemas
4. **Stores** processed invoices in MongoDB Atlas

### Architecture

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

### Invoice Schema

```python
InvoiceSchema:
  - invoice_id: str           # Unique invoice number
  - vendor_name: str           # Supplier name
  - tax_id: str                # Vendor tax identification
  - billing_date: date         # Invoice date (YYYY-MM-DD)
  - line_items: List[LineItem] # Itemized products
  - subtotal: float            # Pre-tax total
  - tax_amount: float         # Tax charged
  - total_amount: float        # Final total
```

## Setup

```bash
# Clone and setup virtual environment
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials:
#   - MONGODB_URL: MongoDB Atlas connection string
#   - ANTHROPIC_API_KEY: Anthropic API key
#   - LOGFIRE_TOKEN: (optional) for observability

# Run locally
uvicorn app.main:app --port 8000
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `MONGODB_URL` | Yes | MongoDB Atlas connection string (e.g., `mongodb+srv://user:pass@cluster.mongodb.net`) |
| `DATABASE_NAME` | No | MongoDB database name (default: `myapp`) |
| `ANTHROPIC_API_KEY` | Yes | Anthropic API key for Claude AI |
| `LOGFIRE_TOKEN` | No | Pydantic Logfire observability token |

## Endpoints

### Core Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/agent/query` | Query AI agent with customer/order tools |
| `POST` | `/api/v1/chat/` | Streaming SSE chat |
| `POST` | `/api/v1/invoices` | Upload invoice for processing |

### Invoice Upload Example

```bash
curl -X POST http://localhost:8000/api/v1/invoices \
  -F "file=@/path/to/invoice.pdf"
```

**Response:**

```json
{
  "filename": "invoice.pdf",
  "document_type": "invoice",
  "extracted_data": {
    "invoice_id": "HYD8-4046154",
    "vendor_name": "CLICKTECH RETAIL PRIVATE LIMITED",
    "tax_id": "36AAJCC9783E1Z8",
    "billing_date": "2025-11-01",
    "line_items": [
      {"description": "Apple EarPods", "quantity": 1, "unit_price": 1355.08, "total_price": 1355.08}
    ],
    "subtotal": 1355.08,
    "tax_amount": 243.92,
    "total_amount": 1599.0
  },
  "confidence": 0.95,
  "processing_status": "success"
}
```

## AI Agent Tools

The `/agent/query` endpoint provides a customer service agent with these tools:

- `get_customer_info` - Look up customer details by ID
- `get_order_status` - Check order status and details
- `validate_invoice` - Validate invoice format

## Deployment

Deployed via GitHub Actions to Azure Container Apps.

### Required GitHub Secrets

| Secret | Description |
|--------|-------------|
| `ANTHROPIC_API_KEY` | Anthropic API key |
| `MONGODB_URL` | MongoDB Atlas connection string |
| `LOGFIRE_TOKEN` | (optional) Logfire observability |
| `AZURE_CREDENTIALS` | Azure service principal |
| `AZURE_CONTAINER_APP_NAME` | Azure Container App name |
| `AZURE_RESOURCE_GROUP` | Azure resource group |

## Project Structure

```
Stack/
├── app/
│   ├── main.py          # FastAPI app entry point
│   ├── config.py        # Settings (Pydantic BaseSettings)
│   └── database.py      # MongoDB connection (Motor async driver)
├── agent/
│   ├── agent.py         # Customer service agent
│   ├── document_agent.py # Invoice processing agent
│   ├── tools.py         # Database tool functions
│   └── result_types.py  # Pydantic models (InvoiceSchema, etc.)
├── routers/
│   └── api_v1.py        # API routes (/invoices, /chat)
├── .env                 # Environment variables (not committed)
├── .env.example         # Example environment variables
└── requirements.txt     # Python dependencies
```

## Technology Stack

- **FastAPI** - Async web framework
- **Motor** - Async MongoDB driver
- **PydanticAI** - AI agent framework
- **Anthropic Claude** - AI model (claude-sonnet-4-20250514)
- **Pydantic v2** - Data validation
- **Logfire** - Observability (Pydantic's telemetry)
- **Azure Container Apps** - Cloud deployment