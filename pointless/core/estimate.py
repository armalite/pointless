from __future__ import annotations

import os

from .estimators import heuristic
from .models import EstimationRequest, EstimationResponse


def estimate_effort(req: EstimationRequest) -> EstimationResponse:
    """
    Central dispatcher. For now we only support the heuristic baseline.
    Later we'll add: if EEAI_ESTIMATOR=llm -> call the LLM estimator.
    """
    mode = os.getenv("EEAI_ESTIMATOR", "heuristic").lower()
    if mode == "heuristic":
        return heuristic.estimate(req)
    # Fallback until LLM estimator is implemented:
    return heuristic.estimate(req)
