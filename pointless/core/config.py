from __future__ import annotations
import os

# Optional: load .env if python-dotenv is installed; ignore if not.
try:  # noqa: SIM105
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()  # loads .env in cwd if present
except Exception:
    pass

def _getenv(key: str, default: str | None = None) -> str | None:
    return os.getenv(f"POINTLESS_{key}", default)

class Settings:
    # estimator mode: "heuristic" now, "llm" later
    ESTIMATOR: str = (_getenv("ESTIMATOR", "heuristic") or "heuristic").lower()

    # placeholders for upcoming features (unused today, but ready)
    JIRA_BASE_URL: str | None = _getenv("JIRA_BASE_URL")
    JIRA_TOKEN: str | None = _getenv("JIRA_TOKEN")
    GH_TOKEN: str | None = _getenv("GH_TOKEN")
    MODEL_PROVIDER: str = _getenv("MODEL_PROVIDER", "openai") or "openai"
    OPENAI_API_KEY: str | None = _getenv("OPENAI_API_KEY")
    CONFIDENCE_THRESHOLD: float = float(_getenv("CONFIDENCE_THRESHOLD", "0.7"))
    MAX_FILES: int = int(_getenv("MAX_FILES", "20"))

    # MCP (Model Context Protocol) settings for Atlassian integration
    MCP_ENABLED: bool = _getenv("MCP_ENABLED", "false").lower() == "true"
    MCP_ATLASSIAN_SERVER_URL: str | None = _getenv("MCP_ATLASSIAN_SERVER_URL")
    MCP_ATLASSIAN_API_TOKEN: str | None = _getenv("MCP_ATLASSIAN_API_TOKEN")
    MCP_ATLASSIAN_EMAIL: str | None = _getenv("MCP_ATLASSIAN_EMAIL")
    MCP_TIMEOUT: int = int(_getenv("MCP_TIMEOUT", "30"))
    
    # MCP GitHub integration settings
    MCP_GITHUB_ENABLED: bool = _getenv("MCP_GITHUB_ENABLED", "false").lower() == "true"
    MCP_GITHUB_SERVER_URL: str | None = _getenv("MCP_GITHUB_SERVER_URL")
    MCP_GITHUB_TOKEN: str | None = _getenv("MCP_GITHUB_TOKEN")
    MCP_GITHUB_TIMEOUT: int = int(_getenv("MCP_GITHUB_TIMEOUT", "30"))

settings = Settings()
