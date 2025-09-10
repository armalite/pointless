"""Tests for core models."""

import pytest

from pointless.core.models import (
    EstimationRequest,
    EstimationResponse,
    HealthResponse,
    TaskComplexity,
)


def test_estimation_request_creation():
    """Test EstimationRequest model creation."""
    request = EstimationRequest(
        title="Test task",
        description="Test description",
        jira_ticket_id="TEST-123",
        tags=["test", "example"],
    )

    assert request.title == "Test task"
    assert request.description == "Test description"
    assert request.jira_ticket_id == "TEST-123"
    assert request.tags == ["test", "example"]


def test_estimation_request_minimal():
    """Test EstimationRequest with minimal data."""
    request = EstimationRequest(title="Minimal task")

    assert request.title == "Minimal task"
    assert request.description is None
    assert request.jira_ticket_id is None
    assert request.codebase_context is None
    assert request.tags == []


def test_estimation_response_creation():
    """Test EstimationResponse model creation."""
    response = EstimationResponse(
        estimated_hours=5.5,
        complexity=TaskComplexity.MODERATE,
        confidence=0.75,
        reasoning="Based on task analysis",
        factors=["Factor 1", "Factor 2"],
    )

    assert response.estimated_hours == 5.5
    assert response.complexity == TaskComplexity.MODERATE
    assert response.confidence == 0.75
    assert response.reasoning == "Based on task analysis"
    assert response.factors == ["Factor 1", "Factor 2"]


def test_estimation_response_validation():
    """Test EstimationResponse validation."""
    # Test positive hours validation
    with pytest.raises(ValueError):
        EstimationResponse(
            estimated_hours=0,
            complexity=TaskComplexity.SIMPLE,
            confidence=0.8,
            reasoning="Test",
        )

    # Test confidence range validation
    with pytest.raises(ValueError):
        EstimationResponse(
            estimated_hours=1.0,
            complexity=TaskComplexity.SIMPLE,
            confidence=1.5,  # Invalid: > 1
            reasoning="Test",
        )


def test_health_response_creation():
    """Test HealthResponse model creation."""
    response = HealthResponse(
        status="healthy", version="0.1.0", timestamp="2024-01-01T00:00:00Z"
    )

    assert response.status == "healthy"
    assert response.version == "0.1.0"
    assert response.timestamp == "2024-01-01T00:00:00Z"


def test_task_complexity_enum():
    """Test TaskComplexity enum values."""
    assert TaskComplexity.TRIVIAL == "trivial"
    assert TaskComplexity.SIMPLE == "simple"
    assert TaskComplexity.MODERATE == "moderate"
    assert TaskComplexity.COMPLEX == "complex"
    assert TaskComplexity.EXPERT == "expert"
