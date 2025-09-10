"""Tests for FastAPI interface."""

from fastapi.testclient import TestClient

from pointless.interfaces.api import app

client = TestClient(app)


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/healthz")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "timestamp" in data


def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200

    data = response.json()
    assert "message" in data
    assert "version" in data
    assert data["docs"] == "/docs"
    assert data["health"] == "/healthz"


def test_estimate_endpoint_basic():
    """Test basic estimation endpoint."""
    request_data = {
        "title": "Fix login bug",
        "description": "Users cannot login on mobile",
    }

    response = client.post("/estimate", json=request_data)
    assert response.status_code == 200

    data = response.json()
    assert "estimated_hours" in data
    assert "complexity" in data
    assert "confidence" in data
    assert "reasoning" in data
    assert "factors" in data

    assert data["estimated_hours"] > 0
    assert 0 <= data["confidence"] <= 1


def test_estimate_endpoint_full():
    """Test estimation endpoint with full request."""
    request_data = {
        "title": "Implement user authentication",
        "description": "Add OAuth2 authentication with JWT tokens",
        "jira_ticket_id": "AUTH-123",
        "codebase_context": "Express.js API with MongoDB",
        "tags": ["feature", "security", "urgent"],
    }

    response = client.post("/estimate", json=request_data)
    assert response.status_code == 200

    data = response.json()
    assert data["estimated_hours"] > 0
    assert data["complexity"] in ["trivial", "simple", "moderate", "complex", "expert"]


def test_estimate_endpoint_empty_title():
    """Test estimation endpoint with empty title."""
    request_data = {"title": "", "description": "Some description"}

    response = client.post("/estimate", json=request_data)
    assert response.status_code == 400
    assert "cannot be empty" in response.json()["detail"]


def test_estimate_endpoint_missing_title():
    """Test estimation endpoint with missing title."""
    request_data = {"description": "Some description"}

    response = client.post("/estimate", json=request_data)
    assert response.status_code == 422  # Validation error


def test_estimate_endpoint_minimal():
    """Test estimation endpoint with minimal valid data."""
    request_data = {"title": "Simple task"}

    response = client.post("/estimate", json=request_data)
    assert response.status_code == 200

    data = response.json()
    assert data["estimated_hours"] > 0


def test_docs_endpoints():
    """Test that documentation endpoints are accessible."""
    docs_response = client.get("/docs")
    assert docs_response.status_code == 200

    redoc_response = client.get("/redoc")
    assert redoc_response.status_code == 200
