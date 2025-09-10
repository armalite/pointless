"""Test configuration and fixtures."""

import pytest

from pointless.core.models import EstimationRequest


@pytest.fixture
def sample_estimation_request():
    """Sample estimation request for testing."""
    return EstimationRequest(
        title="Fix critical login bug",
        description="Users cannot log in on mobile devices when using 2FA",
        jira_ticket_id="PROJ-123",
        codebase_context="Authentication module, mobile app",
        tags=["urgent", "bug", "mobile"],
    )


@pytest.fixture
def simple_estimation_request():
    """Simple estimation request for testing."""
    return EstimationRequest(
        title="Update README", description="Add installation instructions"
    )
