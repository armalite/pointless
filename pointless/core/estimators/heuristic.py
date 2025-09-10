from __future__ import annotations

import hashlib
import logging
import os
import random
from typing import List

from pointless.core.models import EstimationRequest, EstimationResponse, TaskComplexity

log = logging.getLogger(__name__)


def _rng_from_title(title: str) -> random.Random:
    seed = int(hashlib.sha256((title or "pointless").encode()).hexdigest(), 16) % (2**32)
    return random.Random(seed)


def _find_relevant_files(root: str, text: str, limit: int = 10) -> List[str]:
    """
    Super-cheap path/name match (no parsing). Looks for keywords from the issue text.
    This is only to make the placeholder feel 'alive' until LLM retrieval lands.
    """
    if not root or not os.path.isdir(root):
        return []

    text = (text or "").lower()
    # crude keyword set
    kws = {w for w in ("client", "api", "monitor", "domain", "get", "list", "method") if w in text}
    if not kws:
        return []

    hits: List[str] = []
    for dirpath, _, filenames in os.walk(root):
        for fname in filenames:
            path = os.path.join(dirpath, fname)
            rel = os.path.relpath(path, root)
            low_rel = rel.lower()
            if any(kw in low_rel for kw in kws):
                hits.append(rel)
                if len(hits) >= limit:
                    return hits
    return hits


def estimate(req: EstimationRequest) -> EstimationResponse:
    """
    Deterministic, throwaway baseline. Adds a tiny repo 'sniff' if a local path is provided.
    """
    rnd = _rng_from_title(req.title)
    text = f"{req.title} {req.description or ''}".lower()

    base = 1.0
    factors: List[str] = []
    complexity = TaskComplexity.SIMPLE

    desc_len = len(req.description or "")
    if desc_len > 200:
        base += 3.0
        complexity = TaskComplexity.COMPLEX
        factors.append("Long description indicates richer requirements")
    elif desc_len > 50:
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

    # Optional: look at local repo path if provided.
    if req.codebase_context:
        hits = _find_relevant_files(req.codebase_context, text, limit=8)
        if hits:
            # nudge estimate a bit, bounded
            bump = min(0.3 * len(hits), 2.0)
            base += bump
            factors.append(f"Found {len(hits)} matching paths in repo (e.g. {hits[0]})")

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
        req.title, final, complexity.value, confidence,
    )

    return EstimationResponse(
        estimated_hours=round(final, 1),
        complexity=complexity,
        confidence=round(confidence, 2),
        reasoning=reasoning,
        factors=factors,
    )
