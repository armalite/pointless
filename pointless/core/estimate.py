from __future__ import annotations
from .estimators import heuristic
from .models import EstimationRequest, EstimationResponse
from .config import settings

def estimate_effort(req: EstimationRequest) -> EstimationResponse:
    mode = settings.ESTIMATOR
    if mode == "heuristic":
        return heuristic.estimate(req)
    # LLM path will plug in here later
    return heuristic.estimate(req)
