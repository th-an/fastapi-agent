from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class QueryResult(BaseModel):
    query: str = Field(description="The original user query")
    response: str = Field(description="The agent's structured response")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence score")
    sources: list[str] = Field(default_factory=list, description="Data sources used")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class CustomerInfo(BaseModel):
    customer_id: str
    name: str
    email: str
    account_status: str


class InvoiceValidationResult(BaseModel):
    valid: bool
    invoice_id: str
    errors: list[str] = Field(default_factory=list)
    amount: Optional[float] = None
    currency: str = "USD"


class OrderStatus(BaseModel):
    order_id: str
    status: str
    customer_id: str
    items: list[dict]
    total: float
    created_at: datetime


class DocumentProcessingResult(BaseModel):
    filename: str = Field(description="Original filename of uploaded document")
    document_type: str = Field(description="Type of document (invoice, receipt, etc.)")
    extracted_text: str = Field(description="Text extracted from the document")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence in extraction")
    processing_status: str = Field(description="Status: success, failed, partial")
    error_message: Optional[str] = Field(
        default=None, description="Error details if failed"
    )
