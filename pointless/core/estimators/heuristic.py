from __future__ import annotations

import hashlib
import logging
import random
from typing import List

from ..models import EstimationRequest, EstimationResponse, TaskComplexity

log = logging.getLogger(__name__)


def _rng_from_title(title: str) -> random.Random:
    """Deterministic RNG based on the title so tests are stable."""
    seed = int(hashlib.sha256((title or "pointless").encode()).hexdigest(), 16) % (2**32)
    return random.Random(seed)


def estimate(req: EstimationRequest) -> EstimationResponse:
    """
    Deterministic, throwaway baseline.
    Keeps us unblocked while LLM + progressive retrieval are added.
    """
    rnd = _rng_from_title(req.title)
    text = f"{req.title} {req.description or ''}".lower()

    # Start simple and nudge by a few crude signals.
    base = 1.0
    factors: List[str] = []
    complexity = TaskComplexity.SIMPLE

    if len(req.description or "") > 200:
        base += 3.0
        complexity = TaskComplexity.COMPLEX
        factors.append("Long description indicates richer requirements")
    elif len(req.description or "") > 50:
        base += 1.0
        complexity = TaskComplexity.MODERATE
        factors.append("Moderate description length")

    for kw in ["refactor", "migrate", "architecture", "security", "performance", "integration"]:
        if kw in text:
            base += 3.0
            complexity = TaskComplexity.COMPLEX
            factors.append(f"Complex keyword: {kw}")
            break

    if req.tags and any(t.lower() == "urgent" for t in req.tags):
        base *= 0.9
        factors.append("Urgent tag—risk of optimistic sizing")

    # Deterministic jitter for not-all-the-same outputs.
    final = base * rnd.uniform(0.9, 1.3)

    conf_map = {
        TaskComplexity.TRIVIAL: 0.9,
        TaskComplexity.SIMPLE: 0.85,
        TaskComplexity.MODERATE: 0.7,
        TaskComplexity.COMPLEX: 0.55,
        TaskComplexity.EXPERT: 0.45,
    }
    confidence = conf_map.get(complexity, 0.7)

    reasoning = (
        "Heuristic baseline only; final implementation will use progressive retrieval "
        "over Jira/GitHub and an LLM (plan→size) with confidence & assumptions."
    )

    log.info(
        "Heuristic estimate for '%s': hours=%.1f, complexity=%s, confidence=%.2f",
        req.title,
        final,
        complexity.value,
        confidence,
    )

    return EstimationResponse(
        estimated_hours=round(final, 1),
        complexity=complexity,
        confidence=round(confidence, 2),
        reasoning=reasoning,
        factors=factors,
    )
