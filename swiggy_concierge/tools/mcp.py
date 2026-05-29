# Toolset factory — reads SWIGGY_ENV to switch between local stubs and production.
import os
from google.adk.tools.mcp_tool import McpToolset, SseConnectionParams

_ENV = os.getenv("SWIGGY_ENV", "local")
_TOKEN = os.getenv("SWIGGY_TOKEN", "mock-token-local")

# Local ports match mock_servers/main.py. Production URLs need a valid SWIGGY_TOKEN.
_URLS = {
    "local": {
        "food": "http://localhost:8001/sse",
        "im": "http://localhost:8002/sse",
        "dineout": "http://localhost:8003/sse",
    },
    "production": {
        "food": "https://mcp.swiggy.com/food",
        "im": "https://mcp.swiggy.com/im",
        "dineout": "https://mcp.swiggy.com/dineout",
    },
}


def _make_toolset(server_key: str) -> McpToolset:
    url = _URLS[_ENV][server_key]
    # Auth header only needed for production — local stubs don't check it
    headers = {"Authorization": f"Bearer {_TOKEN}"} if _ENV == "production" else {}
    return McpToolset(connection_params=SseConnectionParams(url=url, headers=headers))


def food_mcp_toolset() -> McpToolset:
    """Food MCP: 14 tools — Discover, Cart, Order, Track, Support."""
    return _make_toolset("food")


def instamart_mcp_toolset() -> McpToolset:
    """Instamart MCP: 13 tools — Discover, Cart, Order, Track, Support."""
    return _make_toolset("im")


def dineout_mcp_toolset() -> McpToolset:
    """Dineout MCP: 8 tools — Find, Reserve, Manage, Support."""
    return _make_toolset("dineout")
