from __future__ import annotations

import logging
from datetime import datetime, timezone

from fastapi import FastAPI

from .. import __version__
from ..core.estimate import estimate_effort
from ..core.models import EstimationRequest, EstimationResponse, HealthResponse
from ..core.config import settings

logging.basicConfig(level=logging.INFO)
app = FastAPI(title="Pointless API", version=__version__)


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "Pointless API - AI effort estimates",
        "version": __version__,
        "docs": "/docs",
        "health": "/healthz",
        "mcp_enabled": settings.MCP_ENABLED,
    }


@app.get("/healthz", response_model=HealthResponse)
def healthz() -> HealthResponse:
    ts = (
        datetime.now(timezone.utc)
        .isoformat(timespec="seconds")
        .replace("+00:00", "Z")
    )
    return HealthResponse(status="healthy", version=__version__, timestamp=ts)


@app.post("/estimate", response_model=EstimationResponse)
def estimate(req: EstimationRequest) -> EstimationResponse:
    return estimate_effort(req)
