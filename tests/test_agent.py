from agent.result_types import (
    QueryResult,
    CustomerInfo,
    OrderStatus,
    DocumentProcessingResult,
)


class TestAgentModule:
    """Test agent module structure without requiring API key."""

    def test_agent_module_exists(self):
        """Test that agent module and functions exist."""
        from agent.agent import create_agent, create_chat_agent

        assert callable(create_agent)
        assert callable(create_chat_agent)

    def test_result_types_importable(self):
        """Test that all result types are importable."""
        from agent.result_types import (
            QueryResult,
            CustomerInfo,
            OrderStatus,
            DocumentProcessingResult,
        )

        assert QueryResult is not None
        assert CustomerInfo is not None
        assert OrderStatus is not None
        assert DocumentProcessingResult is not None


class TestCustomerInfoSchema:
    """Tests for CustomerInfo Pydantic schema validation."""

    def test_customer_info_valid(self):
        """Test valid CustomerInfo creation."""
        customer = CustomerInfo(
            customer_id="CUST-001",
            name="John Doe",
            email="john@example.com",
            account_status="active",
        )
        assert customer.customer_id == "CUST-001"
        assert customer.name == "John Doe"

    def test_customer_info_optional_fields(self):
        """Test CustomerInfo with optional fields."""
        customer = CustomerInfo(
            customer_id="CUST-002",
            name="Jane Smith",
            email="jane@example.com",
            account_status="inactive",
        )
        assert customer.account_status == "inactive"


class TestOrderStatusSchema:
    """Tests for OrderStatus Pydantic schema validation."""

    def test_order_status_valid(self):
        """Test valid OrderStatus creation."""
        from datetime import datetime

        order = OrderStatus(
            order_id="ORD-001",
            status="shipped",
            customer_id="CUST-001",
            items=[{"name": "Widget", "qty": 2}],
            total=49.98,
            created_at=datetime.utcnow(),
        )
        assert order.order_id == "ORD-001"
        assert order.status == "shipped"
        assert order.total == 49.98

    def test_order_status_empty_items(self):
        """Test OrderStatus with empty items list."""
        from datetime import datetime

        order = OrderStatus(
            order_id="ORD-002",
            status="pending",
            customer_id="CUST-002",
            items=[],
            total=0.0,
            created_at=datetime.utcnow(),
        )
        assert len(order.items) == 0


class TestQueryResultSchema:
    """Tests for QueryResult Pydantic schema validation."""

    def test_query_result_valid(self):
        """Test valid QueryResult creation."""
        from datetime import datetime

        result = QueryResult(
            query="Test query",
            response="Test response",
            confidence=0.95,
            sources=["test_source"],
            timestamp=datetime.utcnow(),
        )
        assert result.confidence == 0.95
        assert "test_source" in result.sources

    def test_query_result_confidence_bounds(self):
        """Test confidence score is bounded 0-1."""
        from datetime import datetime

        result = QueryResult(
            query="Test",
            response="Test",
            confidence=0.5,
            sources=[],
            timestamp=datetime.utcnow(),
        )
        assert 0.0 <= result.confidence <= 1.0

    def test_query_result_default_sources(self):
        """Test default empty sources list."""
        from datetime import datetime

        result = QueryResult(
            query="Test", response="Test", confidence=0.5, timestamp=datetime.utcnow()
        )
        assert result.sources == []


class TestDocumentProcessingResultSchema:
    """Tests for DocumentProcessingResult Pydantic schema validation."""

    def test_document_processing_result_valid(self):
        """Test valid DocumentProcessingResult creation."""
        result = DocumentProcessingResult(
            filename="invoice.pdf",
            document_type="invoice",
            extracted_text="Invoice #12345",
            confidence=0.9,
            processing_status="success",
        )
        assert result.filename == "invoice.pdf"
        assert result.document_type == "invoice"
        assert result.processing_status == "success"

    def test_document_processing_result_with_error(self):
        """Test DocumentProcessingResult with error."""
        result = DocumentProcessingResult(
            filename="unreadable.pdf",
            document_type="unknown",
            extracted_text="",
            confidence=0.0,
            processing_status="failed",
            error_message="Could not parse document",
        )
        assert result.error_message == "Could not parse document"
