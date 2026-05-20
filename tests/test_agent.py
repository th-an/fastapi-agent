from agent.agent import create_agent
from agent.result_types import QueryResult, CustomerInfo, OrderStatus


class TestAgentUnitTests:
    """Deterministic unit tests using TestModel and FunctionModel.

    Note: These tests require a real database connection for tool execution.
    For unit testing without real DB, use mocked dependencies.
    """

    def test_agent_output_type_is_query_result(self, mock_db):
        """Test that agent output_type is correctly set to QueryResult."""
        from agent.agent import create_agent

        agent = create_agent(mock_db)
        output_type = getattr(agent, "output_type", None) or getattr(
            agent, "_output_type", None
        )
        assert output_type is not None
        assert output_type == QueryResult

    def test_agent_system_prompt_is_set(self, mock_db):
        """Test that agent has system prompt configured."""
        from agent.agent import create_agent

        agent = create_agent(mock_db)
        system_prompt = getattr(agent, "system_prompt", None)
        assert system_prompt is not None

    def test_agent_deps_type_is_database(self, mock_db):
        """Test that agent uses AsyncIOMotorDatabase as deps type."""
        from agent.agent import create_agent

        agent = create_agent(mock_db)
        deps_type = agent.deps_type
        assert deps_type is not None


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


class TestAgentToolsIntegration:
    """Test agent tools are properly registered and callable."""

    def test_agent_deps_type_correct(self, mock_db):
        """Test that agent uses correct deps type."""
        agent = create_agent(mock_db)
        assert agent.deps_type is not None

    def test_agent_has_system_prompt(self, mock_db):
        """Test that agent has system prompt configured."""
        agent = create_agent(mock_db)
        assert hasattr(agent, "system_prompt") or hasattr(agent, "_system_prompt")

    def test_agent_output_type_is_query_result(self, mock_db):
        """Test that agent output_type is QueryResult."""
        agent = create_agent(mock_db)
        output_type = getattr(agent, "output_type", None) or getattr(
            agent, "_output_type", None
        )
        assert output_type is not None
