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


class EstimationResponse(BaseModel):
    """Minimal baseline output; we'll extend once LLM/retrieval lands."""
    estimated_hours: float = Field(..., gt=0)
    complexity: TaskComplexity
    confidence: float = Field(..., ge=0, le=1)
    reasoning: str
    factors: List[str] = Field(default_factory=list)


class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: str  # RFC3339/ISO8601 (UTC; ends with 'Z')
