import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from unittest.mock import AsyncMock, MagicMock
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic_ai import Agent
from pydantic_ai.models.test import TestModel
from agent.agent import create_agent
from agent.result_types import QueryResult
from app.config import Settings, get_settings


@pytest.fixture
def mock_db():
    """Mock MongoDB database for testing."""
    from unittest.mock import AsyncMock, MagicMock
    
    mock_customers = MagicMock()
    mock_customers.find_one = AsyncMock(return_value={
        "customer_id": "CUST-001",
        "name": "Test User",
        "email": "test@example.com",
        "account_status": "active"
    })
    mock_customers.insert_many = AsyncMock(return_value=MagicMock())
    mock_customers.count_documents = AsyncMock(return_value=1)
    mock_customers.delete_many = AsyncMock(return_value=MagicMock())
    
    mock_orders = MagicMock()
    mock_orders.find_one = AsyncMock(return_value={
        "order_id": "ORD-001",
        "status": "shipped",
        "customer_id": "CUST-001",
        "items": [{"name": "Widget", "qty": 2}],
        "total": 49.98
    })
    mock_orders.insert_many = AsyncMock(return_value=MagicMock())
    mock_orders.count_documents = AsyncMock(return_value=1)
    mock_orders.delete_many = AsyncMock(return_value=MagicMock())
    
    db = MagicMock()
    db.customers = mock_customers
    db.orders = mock_orders
    db.admin = MagicMock()
    db.admin.command = AsyncMock(return_value={"ok": 1})
    
    return db


@pytest.fixture
def mock_settings():
    """Mock settings for testing."""
    return Settings(
        APP_NAME="Test App",
        MONGODB_URL="mongodb://localhost:27017",
        DATABASE_NAME="testdb",
        ANTHROPIC_API_KEY="test-key"
    )


@pytest.fixture
def test_agent(mock_db):
    """Create agent with TestModel for deterministic testing."""
    agent = create_agent(mock_db)
    return agent


@pytest.fixture
def test_model():
    """Create TestModel for deterministic unit testing."""
    return TestModel()


@pytest.fixture
def capture_logfire():
    """Skip Logfire telemetry tests if testing utilities not available."""
    pytest.skip("Logfire CaptureLogfire requires explicit exporter configuration")