# tools/

Shared infrastructure used by all agents. Two files — no more, no less.

---

## mcp.py — MCP Toolset Factory

Builds `McpToolset` connections for each Swiggy MCP server. Reads `SWIGGY_ENV` at import time and points agents at either the local mock stubs or the live Swiggy production endpoints.

### Environment switching

| `SWIGGY_ENV` | Food | Instamart | Dineout |
|-------------|------|-----------|---------|
| `local` (default) | `http://localhost:8001/sse` | `http://localhost:8002/sse` | `http://localhost:8003/sse` |
| `production` | `https://mcp.swiggy.com/food` | `https://mcp.swiggy.com/im` | `https://mcp.swiggy.com/dineout` |

### Usage

```python
from tools.mcp import get_food_server, get_instamart_server, get_dineout_server

food_agent.tools = [get_food_server()]
instamart_agent.tools = [get_instamart_server()]
dineout_agent.tools = [get_dineout_server()]
```

### Switching to production

```bash
# Windows PowerShell
$env:SWIGGY_ENV = "production"
$env:SWIGGY_TOKEN = "your_bearer_token_here"

# macOS / Linux
export SWIGGY_ENV=production
export SWIGGY_TOKEN=your_bearer_token_here
```

Restart `adk web` after setting these. No code changes needed.

---

## plugins.py — SwiggyGuardrailPlugin

A custom ADK plugin that enforces hard validation rules **before tool results reach the LLM**. This is different from instructions — instructions can drift; plugin-level filtering cannot be bypassed by the model.

### What it enforces

| Rule | Tool Intercepted | Action |
|------|-----------------|--------|
| 5 km delivery radius (Food) | `search_restaurants` | Strips restaurants beyond 5 km from the result before the LLM sees them |
| ₹1000 cart cap (Food) | `place_food_order` | `place_food_order` itself rejects the call; plugin provides a second layer |

### How it works

The plugin hooks into the ADK `after_tool_callback` lifecycle:

```
Tool runs → returns raw result → SwiggyGuardrailPlugin.after_tool_callback() → (filtered result) → LLM
```

By filtering at this layer, the LLM never reasons about restaurants that are too far away, which:
- Saves tokens (no irrelevant context)
- Prevents the model from recommending them anyway

### Registering the plugin

ADK's `Agent` doesn't have a `plugins` field — it exposes `after_tool_callback` directly. The plugin's method is assigned there in `agent.py`:

```python
from tools.plugins import SwiggyGuardrailPlugin

_guardrail = SwiggyGuardrailPlugin()

# Attach to whichever agent(s) need the filter
food_agent.after_tool_callback = _guardrail.after_tool_callback
```

Currently attached to `food_agent` only, because that's where `search_restaurants` lives.

### Adding new rules

Add a new `if tool_name == "your_tool":` block inside `after_tool_callback` in `plugins.py`. Modify `result["content"]` in-place and return the modified result. Attach to whichever agent runs that tool.
