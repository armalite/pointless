"""Tests for core estimation logic."""

from pointless.core.estimate import estimate_effort
from pointless.core.models import EstimationRequest, TaskComplexity


def test_estimate_effort_basic(simple_estimation_request):
    """Test basic effort estimation."""
    result = estimate_effort(simple_estimation_request)

    assert isinstance(result.estimated_hours, float)
    assert result.estimated_hours > 0
    assert isinstance(result.complexity, TaskComplexity)
    assert 0 <= result.confidence <= 1
    assert isinstance(result.reasoning, str)
    assert len(result.reasoning) > 0
    assert isinstance(result.factors, list)


def test_estimate_effort_complex_task(sample_estimation_request):
    """Test estimation for a complex task."""
    result = estimate_effort(sample_estimation_request)

    assert result.estimated_hours > 0
    assert isinstance(result.complexity, TaskComplexity)
    assert 0 <= result.confidence <= 1
    # Check that the estimation contains keywords from the task
    reasoning_content = result.reasoning.lower()
    factors_content = " ".join(result.factors).lower()

    # Either the reasoning or factors should mention task characteristics
    assert (
        "login" in reasoning_content
        or "login" in factors_content
        or "critical" in reasoning_content
        or "critical" in factors_content
        or "urgent" in reasoning_content
        or "urgent" in factors_content
    )


def test_estimate_effort_empty_title():
    """Test estimation with empty title."""
    request = EstimationRequest(title="")
    result = estimate_effort(request)

    # Should still work, just with minimal estimation
    assert result.estimated_hours > 0
    assert isinstance(result.complexity, TaskComplexity)


def test_estimate_effort_long_description():
    """Test estimation considers description length."""
    long_desc = "This is a very long description " * 20  # > 200 chars
    request = EstimationRequest(title="Complex task", description=long_desc)

    result = estimate_effort(request)
    assert result.estimated_hours > 1.0  # Should be higher due to long description


def test_estimate_effort_complex_keywords():
    """Test that complex keywords affect estimation."""
    request = EstimationRequest(
        title="Refactor authentication architecture for better security",
        description="Complete refactor of the authentication system",
    )

    result = estimate_effort(request)
    # Should detect complexity from keywords
    assert result.complexity in [TaskComplexity.COMPLEX, TaskComplexity.EXPERT]
    assert any("refactor" in factor.lower() for factor in result.factors)


def test_estimate_effort_simple_keywords():
    """Test that simple keywords are detected."""
    request = EstimationRequest(
        title="Fix typo in documentation", description="Simple typo fix"
    )

    result = estimate_effort(request)
    assert any("simple" in factor.lower() for factor in result.factors)


def test_estimate_effort_urgent_tag():
    """Test that urgent tag affects estimation."""
    request = EstimationRequest(
        title="Important task", tags=["urgent", "high-priority"]
    )

    result = estimate_effort(request)
    assert any("urgent" in factor.lower() for factor in result.factors)


def test_estimate_effort_consistency():
    """Test that estimation is reasonably consistent for same input."""
    request = EstimationRequest(title="Test task", description="Test description")

    results = [estimate_effort(request) for _ in range(10)]
    hours = [r.estimated_hours for r in results]

    # Should have some variation but not be wildly different
    min_hours, max_hours = min(hours), max(hours)
    assert max_hours / min_hours < 3.0  # Within 3x range


def test_estimate_effort_with_codebase_context():
    """Test estimation with codebase context."""
    request = EstimationRequest(
        title="Update API endpoint",
        codebase_context="Legacy REST API with complex authentication",
    )

    result = estimate_effort(request)
    assert any("codebase" in factor.lower() for factor in result.factors)
