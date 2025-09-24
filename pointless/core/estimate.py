from __future__ import annotations
import asyncio
from .estimators import heuristic
from .models import EstimationRequest, EstimationResponse
from .config import settings
from .connectors.mcp_atlassian import get_jira_ticket_info
from .connectors.mcp_github import analyze_github_codebase_for_estimation

async def estimate_effort_async(req: EstimationRequest) -> EstimationResponse:
    """Async version of estimate_effort that supports MCP integration."""
    # Try to enhance the request with MCP data if enabled and ticket ID provided
    enhanced_req = req
    jira_ticket_summary = None
    mcp_data_used = False
    github_data_used = False
    github_repository = None
    github_analysis_summary = None
    
    # Jira MCP integration
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
                    mcp_enhanced_context=f"Jira Status: {ticket.status}, Priority: {ticket.priority}, Type: {ticket.issue_type}",
                    # Preserve GitHub fields
                    github_owner=req.github_owner,
                    github_repo=req.github_repo,
                    use_github_mcp=req.use_github_mcp
                )
                jira_ticket_summary = ticket.summary
                mcp_data_used = True
        except Exception as e:
            # Log the error but continue with original request
            import logging
            logging.getLogger(__name__).warning(f"Failed to retrieve MCP data: {e}")
    
    # GitHub MCP integration
    if req.use_github_mcp and req.github_owner and req.github_repo and settings.MCP_GITHUB_ENABLED:
        try:
            task_description = f"{req.title} {req.description or ''}"
            github_analysis = await analyze_github_codebase_for_estimation(
                req.github_owner, req.github_repo, task_description
            )
            if github_analysis:
                # Enhance the request with GitHub codebase data
                github_context = f"GitHub Repository: {github_analysis.repository.full_name}"
                github_context += f"\nLanguages: {', '.join(github_analysis.languages)}"
                github_context += f"\nComplexity Indicators: {', '.join(github_analysis.complexity_indicators)}"
                github_context += f"\nArchitecture Patterns: {', '.join(github_analysis.architecture_patterns)}"
                github_context += f"\nRelevant Files: {len(github_analysis.relevant_files)} files found"
                
                # Update enhanced context
                existing_context = enhanced_req.mcp_enhanced_context or ""
                if existing_context:
                    existing_context += "\n\n"
                enhanced_context = existing_context + github_context
                
                # Create updated request with GitHub data
                enhanced_req = EstimationRequest(
                    title=enhanced_req.title,
                    description=enhanced_req.description,
                    acceptance_criteria=enhanced_req.acceptance_criteria,
                    jira_ticket_id=enhanced_req.jira_ticket_id,
                    codebase_context=enhanced_req.codebase_context,
                    tags=enhanced_req.tags,
                    use_mcp=enhanced_req.use_mcp,
                    mcp_enhanced_context=enhanced_context,
                    github_owner=req.github_owner,
                    github_repo=req.github_repo,
                    use_github_mcp=req.use_github_mcp
                )
                
                github_data_used = True
                github_repository = github_analysis.repository.full_name
                github_analysis_summary = f"Analyzed {len(github_analysis.relevant_files)} relevant files, detected {len(github_analysis.complexity_indicators)} complexity indicators"
                
        except Exception as e:
            # Log the error but continue with original request
            import logging
            logging.getLogger(__name__).warning(f"Failed to retrieve GitHub MCP data: {e}")
    
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
    result.github_data_used = github_data_used
    result.github_repository = github_repository
    result.github_analysis_summary = github_analysis_summary
    
    if mcp_data_used:
        result.factors.append("Enhanced with Jira ticket data via MCP")
    
    if github_data_used:
        result.factors.append("Enhanced with GitHub codebase analysis via MCP")
    
    return result

def estimate_effort(req: EstimationRequest) -> EstimationResponse:
    """Synchronous wrapper that runs the async estimation."""
    return asyncio.run(estimate_effort_async(req))
