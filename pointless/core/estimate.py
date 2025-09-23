from __future__ import annotations
import asyncio
from .estimators import heuristic
from .models import EstimationRequest, EstimationResponse
from .config import settings
from .connectors.mcp_atlassian import get_jira_ticket_info

async def estimate_effort_async(req: EstimationRequest) -> EstimationResponse:
    """Async version of estimate_effort that supports MCP integration."""
    # Try to enhance the request with MCP data if enabled and ticket ID provided
    enhanced_req = req
    jira_ticket_summary = None
    mcp_data_used = False
    
    if req.use_mcp and req.jira_ticket_id and settings.MCP_ENABLED:
        try:
            ticket = await get_jira_ticket_info(req.jira_ticket_id)
            if ticket:
                # Enhance the request with Jira ticket data
                enhanced_description = req.description or ""
                if ticket.description:
                    enhanced_description += f"\n\nJira Description: {ticket.description}"
                
                enhanced_req = EstimationRequest(
                    title=req.title or ticket.summary,
                    description=enhanced_description,
                    acceptance_criteria=req.acceptance_criteria,
                    jira_ticket_id=req.jira_ticket_id,
                    codebase_context=req.codebase_context,
                    tags=req.tags,
                    use_mcp=req.use_mcp,
                    mcp_enhanced_context=f"Jira Status: {ticket.status}, Priority: {ticket.priority}, Type: {ticket.issue_type}"
                )
                jira_ticket_summary = ticket.summary
                mcp_data_used = True
        except Exception as e:
            # Log the error but continue with original request
            import logging
            logging.getLogger(__name__).warning(f"Failed to retrieve MCP data: {e}")
    
    # Get the base estimation
    mode = settings.ESTIMATOR
    if mode == "heuristic":
        result = heuristic.estimate(enhanced_req)
    else:
        # LLM path will plug in here later
        result = heuristic.estimate(enhanced_req)
    
    # Add MCP information to the response
    result.mcp_data_used = mcp_data_used
    result.jira_ticket_summary = jira_ticket_summary
    
    if mcp_data_used:
        result.factors.append("Enhanced with Jira ticket data via MCP")
    
    return result

def estimate_effort(req: EstimationRequest) -> EstimationResponse:
    """Synchronous wrapper that runs the async estimation."""
    return asyncio.run(estimate_effort_async(req))
