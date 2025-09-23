"""Tests for MCP Atlassian integration."""

import pytest
from unittest.mock import patch, AsyncMock

from pointless.core.connectors.mcp_atlassian import (
    MCPAtlassianClient,
    JiraTicket,
    get_jira_ticket_info,
)
from pointless.core.models import EstimationRequest
from pointless.core.estimate import estimate_effort


class TestJiraTicket:
    """Test JiraTicket model."""

    def test_jira_ticket_creation(self):
        """Test basic JiraTicket creation."""
        ticket = JiraTicket(
            key="TEST-123",
            summary="Test ticket",
            description="Test description",
            status="In Progress",
            priority="High",
            issue_type="Bug"
        )
        
        assert ticket.key == "TEST-123"
        assert ticket.summary == "Test ticket"
        assert ticket.description == "Test description"
        assert ticket.status == "In Progress"
        assert ticket.priority == "High"
        assert ticket.issue_type == "Bug"


class TestMCPAtlassianClient:
    """Test MCP Atlassian client."""

    def test_client_initialization(self):
        """Test client initialization with default settings."""
        client = MCPAtlassianClient()
        
        # Should use settings from config
        assert hasattr(client, 'server_url')
        assert hasattr(client, 'api_token')
        assert hasattr(client, 'email')
        assert hasattr(client, 'timeout')
        assert hasattr(client, 'enabled')

    def test_is_configured_false_by_default(self):
        """Test that client is not configured by default."""
        client = MCPAtlassianClient()
        assert not client.is_configured()

    @patch('pointless.core.connectors.mcp_atlassian.settings')
    def test_is_configured_true_when_settings_provided(self, mock_settings):
        """Test that client is configured when all settings are provided."""
        mock_settings.MCP_ENABLED = True
        mock_settings.MCP_ATLASSIAN_SERVER_URL = "https://test.atlassian.net"
        mock_settings.MCP_ATLASSIAN_API_TOKEN = "test-token"
        mock_settings.MCP_ATLASSIAN_EMAIL = "test@example.com"
        mock_settings.MCP_TIMEOUT = 30
        
        client = MCPAtlassianClient()
        assert client.is_configured()

    @pytest.mark.asyncio
    async def test_get_ticket_returns_none_when_not_configured(self):
        """Test that get_ticket returns None when client is not configured."""
        client = MCPAtlassianClient()
        
        result = await client.get_ticket("TEST-123")
        assert result is None

    @pytest.mark.asyncio
    async def test_get_ticket_returns_none_for_empty_ticket_id(self):
        """Test that get_ticket returns None for empty ticket ID."""
        client = MCPAtlassianClient()
        
        result = await client.get_ticket("")
        assert result is None

    @pytest.mark.asyncio
    @patch('pointless.core.connectors.mcp_atlassian.settings')
    async def test_get_ticket_returns_mock_ticket(self, mock_settings):
        """Test that get_ticket returns a mock ticket when configured."""
        mock_settings.MCP_ENABLED = True
        mock_settings.MCP_ATLASSIAN_SERVER_URL = "https://test.atlassian.net"
        mock_settings.MCP_ATLASSIAN_API_TOKEN = "test-token"
        mock_settings.MCP_ATLASSIAN_EMAIL = "test@example.com"
        mock_settings.MCP_TIMEOUT = 30
        
        client = MCPAtlassianClient()
        
        result = await client.get_ticket("TEST-123")
        
        assert result is not None
        assert isinstance(result, JiraTicket)
        assert result.key == "TEST-123"
        assert "Mock ticket for TEST-123" in result.summary

    @pytest.mark.asyncio
    async def test_search_tickets_returns_empty_when_not_configured(self):
        """Test that search_tickets returns empty list when not configured."""
        client = MCPAtlassianClient()
        
        result = await client.search_tickets("project = TEST")
        assert result == []


class TestMCPIntegrationWithEstimation:
    """Test MCP integration with the estimation flow."""

    @pytest.mark.asyncio
    async def test_estimate_without_mcp(self):
        """Test estimation without MCP integration."""
        from pointless.core.estimate import estimate_effort_async
        
        request = EstimationRequest(
            title="Test task",
            description="Test description",
            use_mcp=False
        )
        
        result = await estimate_effort_async(request)
        
        assert result.estimated_hours > 0
        assert not result.mcp_data_used
        assert result.jira_ticket_summary is None

    @pytest.mark.asyncio
    @patch('pointless.core.connectors.mcp_atlassian.settings')
    async def test_estimate_with_mcp_enabled_but_no_ticket_id(self, mock_settings):
        """Test estimation with MCP enabled but no Jira ticket ID."""
        from pointless.core.estimate import estimate_effort_async
        
        mock_settings.MCP_ENABLED = True
        
        request = EstimationRequest(
            title="Test task",
            description="Test description",
            use_mcp=True
        )
        
        result = await estimate_effort_async(request)
        
        assert result.estimated_hours > 0
        assert not result.mcp_data_used
        assert result.jira_ticket_summary is None

    @pytest.mark.asyncio
    @patch('pointless.core.estimate.settings')
    @patch('pointless.core.connectors.mcp_atlassian.settings')
    async def test_estimate_with_mcp_and_ticket_id(self, mock_atlassian_settings, mock_estimate_settings):
        """Test estimation with MCP enabled and Jira ticket ID."""
        from pointless.core.estimate import estimate_effort_async
        
        # Mock settings for both modules
        for mock_settings in [mock_atlassian_settings, mock_estimate_settings]:
            mock_settings.MCP_ENABLED = True
            mock_settings.MCP_ATLASSIAN_SERVER_URL = "https://test.atlassian.net"
            mock_settings.MCP_ATLASSIAN_API_TOKEN = "test-token"
            mock_settings.MCP_ATLASSIAN_EMAIL = "test@example.com"
            mock_settings.MCP_TIMEOUT = 30
        
        request = EstimationRequest(
            title="Test task",
            description="Test description",
            jira_ticket_id="TEST-123",
            use_mcp=True
        )
        
        result = await estimate_effort_async(request)
        
        assert result.estimated_hours > 0
        assert result.mcp_data_used
        assert result.jira_ticket_summary is not None
        assert "Enhanced with Jira ticket data via MCP" in result.factors


@pytest.mark.asyncio
async def test_get_jira_ticket_info_convenience_function():
    """Test the convenience function for getting Jira ticket info."""
    # Test that it returns None when not configured (default settings)
    result = await get_jira_ticket_info("")
    
    # Should return None for empty ticket ID
    assert result is None