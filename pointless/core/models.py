from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class TaskComplexity(str, Enum):
    TRIVIAL = "trivial"
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    EXPERT = "expert"


class EstimationRequest(BaseModel):
    """Input to the estimator. Jira/GitHub wiring comes later."""
    title: str = Field(default="", description="Short task title")
    description: Optional[str] = ""
    acceptance_criteria: List[str] = Field(default_factory=list)
    jira_ticket_id: Optional[str] = None
    codebase_context: Optional[str] = None  # placeholder until retrieval is wired
    tags: List[str] = Field(default_factory=list)
    
    # MCP integration fields
    use_mcp: bool = Field(default=False, description="Whether to use MCP for data retrieval")
    mcp_enhanced_context: Optional[str] = Field(default=None, description="Additional context from MCP sources")
    
    # GitHub integration fields
    github_owner: Optional[str] = Field(default=None, description="GitHub repository owner")
    github_repo: Optional[str] = Field(default=None, description="GitHub repository name")
    use_github_mcp: bool = Field(default=False, description="Whether to use GitHub MCP for codebase analysis")


class EstimationResponse(BaseModel):
    """Minimal baseline output; we'll extend once LLM/retrieval lands."""
    estimated_hours: float = Field(..., gt=0)
    complexity: TaskComplexity
    confidence: float = Field(..., ge=0, le=1)
    reasoning: str
    factors: List[str] = Field(default_factory=list)
    
    # MCP integration fields
    mcp_data_used: bool = Field(default=False, description="Whether MCP data was used in estimation")
    jira_ticket_summary: Optional[str] = Field(default=None, description="Summary of Jira ticket if retrieved via MCP")
    
    # GitHub integration fields
    github_data_used: bool = Field(default=False, description="Whether GitHub MCP data was used in estimation")
    github_repository: Optional[str] = Field(default=None, description="GitHub repository analyzed if GitHub MCP was used")
    github_analysis_summary: Optional[str] = Field(default=None, description="Summary of GitHub codebase analysis")


class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: str  # RFC3339/ISO8601 (UTC; ends with 'Z')
