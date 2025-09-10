"""Core effort estimation logic."""

import logging
import random

from .models import EstimationRequest, EstimationResponse, TaskComplexity

logger = logging.getLogger(__name__)


def estimate_effort(request: EstimationRequest) -> EstimationResponse:
    """
    Estimate effort for a given task.

    This is a stub implementation that provides pseudo-realistic estimates
    based on basic heuristics and some randomness to simulate AI estimation.

    Args:
        request: The estimation request containing task details

    Returns:
        EstimationResponse with estimated effort, complexity, and reasoning
    """
    logger.info(f"Estimating effort for task: {request.title}")

    # Basic heuristics for estimation (this is the "pointless" part!)
    base_hours = 1.0
    complexity = TaskComplexity.SIMPLE
    factors = []

    # Analyze title length (longer titles = more complex?)
    if len(request.title) > 50:
        base_hours += 2.0
        complexity = TaskComplexity.MODERATE
        factors.append("Long task title suggests complexity")

    # Analyze description
    if request.description:
        desc_length = len(request.description)
        if desc_length > 200:
            base_hours += 3.0
            complexity = TaskComplexity.COMPLEX
            factors.append("Detailed description indicates complex requirements")
        elif desc_length > 50:
            base_hours += 1.0
            factors.append("Moderate description length")
    else:
        factors.append("No description provided - assuming simple task")

    # Check for keywords that indicate complexity
    text_to_analyze = f"{request.title} {request.description or ''}".lower()
    complex_keywords = [
        "refactor",
        "migrate",
        "architecture",
        "security",
        "performance",
        "integration",
    ]
    simple_keywords = ["fix", "typo", "update", "add", "remove"]

    for keyword in complex_keywords:
        if keyword in text_to_analyze:
            base_hours += 4.0
            complexity = (
                TaskComplexity.EXPERT if base_hours > 10 else TaskComplexity.COMPLEX
            )
            factors.append(f"Complex keyword detected: {keyword}")
            break

    for keyword in simple_keywords:
        if keyword in text_to_analyze:
            factors.append(f"Simple keyword detected: {keyword}")
            break

    # Factor in codebase context
    if request.codebase_context:
        base_hours += 1.5
        factors.append("Codebase context requires additional investigation")

    # Factor in tags
    if "urgent" in [tag.lower() for tag in request.tags]:
        base_hours *= 0.8  # Urgent tasks get underestimated (realistic!)
        factors.append("Urgent tag - estimate may be optimistic")

    # Add some realistic randomness (because estimation is never perfect)
    randomness_factor = random.uniform(0.8, 1.4)
    final_hours = base_hours * randomness_factor

    # Calculate confidence (lower for complex tasks, higher for simple ones)
    if complexity == TaskComplexity.TRIVIAL:
        confidence = random.uniform(0.85, 0.95)
    elif complexity == TaskComplexity.SIMPLE:
        confidence = random.uniform(0.75, 0.9)
    elif complexity == TaskComplexity.MODERATE:
        confidence = random.uniform(0.6, 0.8)
    elif complexity == TaskComplexity.COMPLEX:
        confidence = random.uniform(0.4, 0.7)
    else:  # EXPERT
        confidence = random.uniform(0.2, 0.5)

    # Generate reasoning
    reasoning = f"Based on task analysis, estimated {complexity.value} complexity. "
    if factors:
        reasoning += (
            f"Key factors: {', '.join(factors[:3])}."  # Limit to first 3 factors
        )
    reasoning += (
        f" Applied {randomness_factor:.1f}x adjustment for estimation uncertainty."
    )

    logger.info(f"Estimated {final_hours:.1f} hours with {confidence:.2f} confidence")

    return EstimationResponse(
        estimated_hours=round(final_hours, 1),
        complexity=complexity,
        confidence=round(confidence, 2),
        reasoning=reasoning,
        factors=factors,
    )
