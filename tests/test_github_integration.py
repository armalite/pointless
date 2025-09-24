"""Tests for GitHub MCP integration."""

import pytest
from unittest.mock import AsyncMock, patch

from pointless.core.models import EstimationRequest, EstimationResponse
from pointless.core.estimate import estimate_effort_async
from pointless.core.connectors.mcp_github import (
    GitHubRepository, 
    GitHubFile, 
    GitHubCodebaseAnalysis,
    MCPGitHubClient,
    get_github_mcp_client,
    get_github_repository_info,
    analyze_github_codebase_for_estimation
)
from pointless.core.config import settings


class TestGitHubRepository:
    """Test GitHubRepository dataclass."""
    
    def test_github_repository_creation(self):
        """Test creating a GitHubRepository instance."""
        repo = GitHubRepository(
            name="test-repo",
            full_name="owner/test-repo",
            description="A test repository",
            language="Python",
            size=1024,
            stars=42,
            forks=7,
            open_issues=3
        )
        
        assert repo.name == "test-repo"
        assert repo.full_name == "owner/test-repo"
        assert repo.description == "A test repository"
        assert repo.language == "Python"
        assert repo.size == 1024
        assert repo.stars == 42
        assert repo.forks == 7
        assert repo.open_issues == 3
        assert repo.default_branch == "main"


class TestGitHubFile:
    """Test GitHubFile dataclass."""
    
    def test_github_file_creation(self):
        """Test creating a GitHubFile instance."""
        file = GitHubFile(
            path="src/api/routes.py",
            content="def hello(): return 'world'",
            size=500,
            language="Python",
            complexity_score=0.6
        )
        
        assert file.path == "src/api/routes.py"
        assert file.content == "def hello(): return 'world'"
        assert file.size == 500
        assert file.language == "Python"
        assert file.complexity_score == 0.6


class TestGitHubCodebaseAnalysis:
    """Test GitHubCodebaseAnalysis dataclass."""
    
    def test_codebase_analysis_creation(self):
        """Test creating a GitHubCodebaseAnalysis instance."""
        repo = GitHubRepository(name="test", full_name="owner/test")
        analysis = GitHubCodebaseAnalysis(
            repository=repo,
            total_files=100,
            languages=["Python", "JavaScript"],
            complexity_indicators=["Large codebase", "Multiple languages"],
            relevant_files=[],
            architecture_patterns=["REST API", "MVC"]
        )
        
        assert analysis.repository == repo
        assert analysis.total_files == 100
        assert analysis.languages == ["Python", "JavaScript"]
        assert analysis.complexity_indicators == ["Large codebase", "Multiple languages"]
        assert analysis.architecture_patterns == ["REST API", "MVC"]


class TestMCPGitHubClient:
    """Test MCPGitHubClient."""
    
    def test_client_initialization(self):
        """Test GitHub MCP client initialization."""
        client = MCPGitHubClient()
        
        assert client.server_url == settings.MCP_GITHUB_SERVER_URL
        assert client.token == settings.MCP_GITHUB_TOKEN
        assert client.timeout == settings.MCP_GITHUB_TIMEOUT
        assert client.enabled == settings.MCP_GITHUB_ENABLED
    
    def test_is_configured_false_by_default(self):
        """Test client is not configured by default."""
        client = MCPGitHubClient()
        assert not client.is_configured()
    
    @patch('pointless.core.config.settings.MCP_GITHUB_ENABLED', True)
    @patch('pointless.core.config.settings.MCP_GITHUB_SERVER_URL', 'http://localhost:8080')
    @patch('pointless.core.config.settings.MCP_GITHUB_TOKEN', 'test-token')
    def test_is_configured_true_when_settings_provided(self):
        """Test client is configured when all settings provided."""
        client = MCPGitHubClient()
        assert client.is_configured()
    
    @pytest.mark.asyncio
    async def test_get_repository_returns_none_when_not_configured(self):
        """Test get_repository returns None when not configured."""
        client = MCPGitHubClient()
        result = await client.get_repository("owner", "repo")
        assert result is None
    
    @pytest.mark.asyncio
    async def test_get_repository_returns_none_for_empty_params(self):
        """Test get_repository returns None for empty parameters."""
        client = MCPGitHubClient()
        
        result = await client.get_repository("", "repo")
        assert result is None
        
        result = await client.get_repository("owner", "")
        assert result is None
    
    @pytest.mark.asyncio
    @patch('pointless.core.config.settings.MCP_GITHUB_ENABLED', True)
    @patch('pointless.core.config.settings.MCP_GITHUB_SERVER_URL', 'http://localhost:8080')
    @patch('pointless.core.config.settings.MCP_GITHUB_TOKEN', 'test-token')
    async def test_get_repository_returns_mock_repository(self):
        """Test get_repository returns mock repository when configured."""
        client = MCPGitHubClient()
        result = await client.get_repository("owner", "repo")
        
        assert result is not None
        assert isinstance(result, GitHubRepository)
        assert result.name == "repo"
        assert result.full_name == "owner/repo"
        assert result.language == "Python"
    
    @pytest.mark.asyncio
    async def test_analyze_codebase_returns_none_when_not_configured(self):
        """Test analyze_codebase_for_task returns None when not configured."""
        client = MCPGitHubClient()
        result = await client.analyze_codebase_for_task("owner", "repo", "test task")
        assert result is None
    
    @pytest.mark.asyncio
    @patch('pointless.core.config.settings.MCP_GITHUB_ENABLED', True)
    @patch('pointless.core.config.settings.MCP_GITHUB_SERVER_URL', 'http://localhost:8080')
    @patch('pointless.core.config.settings.MCP_GITHUB_TOKEN', 'test-token')
    async def test_analyze_codebase_returns_analysis_for_api_task(self):
        """Test codebase analysis returns relevant data for API-related task."""
        client = MCPGitHubClient()
        result = await client.analyze_codebase_for_task("owner", "repo", "Add API endpoint for users")
        
        assert result is not None
        assert isinstance(result, GitHubCodebaseAnalysis)
        assert result.repository.name == "repo"
        assert "api" in " ".join(result.complexity_indicators).lower() or len(result.relevant_files) > 0
        
    @pytest.mark.asyncio
    async def test_search_code_returns_empty_when_not_configured(self):
        """Test search_code returns empty list when not configured."""
        client = MCPGitHubClient()
        result = await client.search_code("test query")
        assert result == []


class TestGitHubIntegrationWithEstimation:
    """Test GitHub integration with the estimation process."""
    
    @pytest.mark.asyncio
    async def test_estimate_without_github_mcp(self):
        """Test estimation without GitHub MCP integration."""
        request = EstimationRequest(
            title="Add API endpoint",
            description="Simple endpoint",
            use_github_mcp=False
        )
        
        result = await estimate_effort_async(request)
        
        assert isinstance(result, EstimationResponse)
        assert not result.github_data_used
        assert result.github_repository is None
        assert result.github_analysis_summary is None
    
    @pytest.mark.asyncio
    async def test_estimate_with_github_mcp_but_no_repo_params(self):
        """Test estimation with GitHub MCP enabled but no repository parameters."""
        request = EstimationRequest(
            title="Add API endpoint",
            description="Simple endpoint",
            use_github_mcp=True
        )
        
        result = await estimate_effort_async(request)
        
        assert isinstance(result, EstimationResponse)
        assert not result.github_data_used  # Should be False because no repo params
    
    @pytest.mark.asyncio
    @patch('pointless.core.config.settings.MCP_GITHUB_ENABLED', True)
    @patch('pointless.core.config.settings.MCP_GITHUB_SERVER_URL', 'http://localhost:8080')
    @patch('pointless.core.config.settings.MCP_GITHUB_TOKEN', 'test-token')
    @patch('pointless.core.estimate.analyze_github_codebase_for_estimation')
    async def test_estimate_with_github_mcp_and_repo_params(self, mock_analyze):
        """Test estimation with GitHub MCP enabled and repository parameters."""
        # Mock the GitHub analysis
        mock_repo = GitHubRepository(name="test-repo", full_name="owner/test-repo")
        mock_analysis = GitHubCodebaseAnalysis(
            repository=mock_repo,
            languages=["Python", "JavaScript"],
            complexity_indicators=["REST API endpoints present"],
            relevant_files=[GitHubFile(path="api/routes.py", language="Python")],
            architecture_patterns=["REST API"]
        )
        mock_analyze.return_value = mock_analysis
        
        request = EstimationRequest(
            title="Add API endpoint",
            description="Create new user endpoint",
            github_owner="owner",
            github_repo="test-repo",
            use_github_mcp=True
        )
        
        result = await estimate_effort_async(request)
        
        assert isinstance(result, EstimationResponse)
        assert result.github_data_used
        assert result.github_repository == "owner/test-repo"
        assert "Enhanced with GitHub codebase analysis via MCP" in result.factors
        
        # Verify the analyze function was called
        mock_analyze.assert_called_once_with("owner", "test-repo", "Add API endpoint Create new user endpoint")


@pytest.mark.asyncio
async def test_get_github_repository_info_convenience_function():
    """Test the convenience function for getting GitHub repository info."""
    with patch('pointless.core.connectors.mcp_github.get_github_mcp_client') as mock_client_getter:
        mock_client = AsyncMock()
        mock_client.get_repository = AsyncMock(return_value=GitHubRepository(name="test", full_name="owner/test"))
        mock_client_getter.return_value = mock_client
        
        result = await get_github_repository_info("owner", "test")
        
        assert result is not None
        assert result.name == "test"
        mock_client.get_repository.assert_called_once_with("owner", "test")


@pytest.mark.asyncio
async def test_analyze_github_codebase_convenience_function():
    """Test the convenience function for analyzing GitHub codebase."""
    with patch('pointless.core.connectors.mcp_github.get_github_mcp_client') as mock_client_getter:
        mock_client = AsyncMock()
        mock_repo = GitHubRepository(name="test", full_name="owner/test")
        mock_analysis = GitHubCodebaseAnalysis(repository=mock_repo)
        mock_client.analyze_codebase_for_task = AsyncMock(return_value=mock_analysis)
        mock_client_getter.return_value = mock_client
        
        result = await analyze_github_codebase_for_estimation("owner", "test", "task description")
        
        assert result is not None
        assert result.repository.name == "test"
        mock_client.analyze_codebase_for_task.assert_called_once_with("owner", "test", "task description")