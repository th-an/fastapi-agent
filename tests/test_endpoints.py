import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import connect_to_mongo, close_mongo_connection


class TestHealthEndpoints:
    """Test health and status endpoints."""

    def test_root_health(self):
        """Test root /health endpoint."""
        client = TestClient(app)
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

    def test_api_v1_health(self):
        """Test /api/v1/health endpoint with phase info."""
        client = TestClient(app)
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "phase" in data


class TestAgentEndpoints:
    """Test agent query endpoints."""

    @pytest.fixture
    def setup_db(self):
        """Setup test database connection."""
        import asyncio

        asyncio.run(connect_to_mongo())
        yield
        asyncio.run(close_mongo_connection())

    def test_agent_query_endpoint_health(self, setup_db):
        """Test agent query endpoint responds correctly."""
        client = TestClient(app)
        response = client.get("/agent/result-types")
        assert response.status_code == 200
        data = response.json()
        assert "QueryResult" in data


class TestAPIEndpoints:
    """Test API v1 endpoints."""

    @pytest.fixture
    def setup_db(self):
        """Setup test database connection."""
        import asyncio

        asyncio.run(connect_to_mongo())
        yield
        asyncio.run(close_mongo_connection())

    def test_api_v1_health_has_phase_info(self, setup_db):
        """Test API v1 health returns phase info."""
        client = TestClient(app)
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert "phase" in data

    def test_openapi_schema_available(self):
        """Test OpenAPI schema is accessible."""
        client = TestClient(app)
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert "paths" in schema
        assert "/health" in schema["paths"]


class TestConfigSettings:
    """Test configuration settings."""

    def test_settings_model_config(self):
        """Test Settings model accepts extra fields."""
        from app.config import Settings

        settings = Settings(APP_NAME="Test", ANTHROPIC_API_KEY="key123")
        assert settings.APP_NAME == "Test"
        assert settings.ANTHROPIC_API_KEY == "key123"

    def test_settings_defaults(self):
        """Test Settings default values."""
        from app.config import Settings

        settings = Settings()
        assert settings.APP_NAME == "FastAPI MongoDB App"
        assert settings.DATABASE_NAME == "myapp"

    def test_settings_env_loading(self, monkeypatch):
        """Test settings load from environment."""
        monkeypatch.setenv("APP_NAME", "CustomApp")
        from importlib import reload
        import app.config as config_module

        reload(config_module)
        settings = config_module.Settings()
        assert settings.APP_NAME == "CustomApp"
