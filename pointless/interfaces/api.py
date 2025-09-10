"""FastAPI interface for pointless effort estimation."""

import logging
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .. import __version__
from ..core.estimate import estimate_effort
from ..core.models import EstimationRequest, EstimationResponse, HealthResponse

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Pointless API",
    description=(
        "AI-powered effort estimation for Jira tickets and codebases - "
        "because someone has to guess!"
    ),
    version=__version__,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthz", response_model=HealthResponse, tags=["Health"])
async def health_check() -> HealthResponse:
    """
    Health check endpoint to verify service is running.

    Returns basic service information and current timestamp.
    """
    logger.info("Health check requested")
    return HealthResponse(
        status="healthy",
        version=__version__,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


@app.post("/estimate", response_model=EstimationResponse, tags=["Estimation"])
async def create_estimate(request: EstimationRequest) -> EstimationResponse:
    """
    Create an effort estimation for a task.

    This endpoint accepts task details and returns an AI-generated effort estimate
    with confidence levels and reasoning. Perfect for when you need to pretend
    you know how long something will take!

    Args:
        request: Task details including title, description, and context

    Returns:
        Effort estimation with hours, complexity, confidence, and reasoning

    Raises:
        HTTPException: If estimation fails due to invalid input or processing error
    """
    try:
        logger.info(f"Estimation requested for task: {request.title}")

        # Validate request
        if not request.title.strip():
            raise HTTPException(status_code=400, detail="Task title cannot be empty")

        # Generate estimation
        result = estimate_effort(request)

        logger.info(
            f"Estimation completed: {result.estimated_hours}h with "
            f"{result.confidence:.2f} confidence"
        )
        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Estimation failed: {e}")
        raise HTTPException(
            status_code=500, detail=f"Internal error during estimation: {str(e)}"
        )


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with basic API information."""
    return {
        "message": (
            "Welcome to Pointless API - where effort estimation meets "
            "educated guessing!"
        ),
        "version": __version__,
        "docs": "/docs",
        "health": "/healthz",
    }


# For running with uvicorn directly
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
