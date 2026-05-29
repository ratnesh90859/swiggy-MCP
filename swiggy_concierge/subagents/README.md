# subagents/

Sub-agents for the Swiggy Autonomous Commerce Orchestrator. Each file defines one domain-specific agent that the root orchestrator delegates to.

---

## Overview

| File | Agent Name | MCP Server | Tools |
|------|-----------|------------|-------|
| `food_agent.py` | `FoodAgent` | Food MCP `:8001` | 14 |
| `instamart_agent.py` | `InstamartAgent` | Instamart MCP `:8002` | 13 |
| `dineout_agent.py` | `DineoutAgent` | Dineout MCP `:8003` | 8 |

Tools are injected at runtime — the agent files themselves just define the agent identity and instructions.

---

## How agents are wired

In `agent.py`:

```python
from subagents.food_agent import food_agent
...

root_agent = Agent(
    name="SwiggyOrchestrator",
    agents=[food_agent, instamart_agent, dineout_agent],
    ...
)
```

---

## FoodAgent
Handles food discovery and ordering. Enforces the 5 km delivery radius via a plugin.

## InstamartAgent
Handles grocery shopping and predictive restocking.

## DineoutAgent
Handles restaurant discovery and free table booking.

---

## Adding a new sub-agent

1. Create `subagents/your_agent.py` following the same pattern.
2. Add its instructions to `instructions.py`.
3. Add a toolset factory to `tools/mcp.py`.
4. Import and wire it in `agent.py`.
