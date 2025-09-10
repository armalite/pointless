"""Pydantic models for pointless effort estimation."""

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class TaskComplexity(str, Enum):
    """Enumeration of task complexity levels."""

    TRIVIAL = "trivial"
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    EXPERT = "expert"


class EstimationRequest(BaseModel):
    """Request model for effort estimation."""

    title: str = Field(..., description="Task title or summary")
    description: Optional[str] = Field(None, description="Detailed task description")
    jira_ticket_id: Optional[str] = Field(None, description="Jira ticket identifier")
    codebase_context: Optional[str] = Field(
        None, description="Relevant codebase context"
    )
    tags: List[str] = Field(default_factory=list, description="Task tags or labels")


class EstimationResponse(BaseModel):
    """Response model for effort estimation."""

    estimated_hours: float = Field(..., description="Estimated effort in hours", gt=0)
    complexity: TaskComplexity = Field(..., description="Assessed task complexity")
    confidence: float = Field(..., description="Confidence level (0-1)", ge=0, le=1)
    reasoning: str = Field(..., description="Explanation of the estimation")
    factors: List[str] = Field(
        default_factory=list, description="Key factors considered"
    )


class HealthResponse(BaseModel):
    """Health check response model."""

    status: str = Field(..., description="Service status")
    version: str = Field(..., description="Service version")
    timestamp: str = Field(..., description="Current timestamp")
