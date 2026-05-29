import os
from google.adk.agents import Agent
from google.genai import types
from swiggy_concierge.instructions import FOOD_AGENT_INSTRUCTIONS
from swiggy_concierge.tools.mcp import food_mcp_toolset
from swiggy_concierge.tools.plugins import SwiggyGuardrailPlugin

model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
guardrail = SwiggyGuardrailPlugin()

# Retry config to handle 429 RESOURCE_EXHAUSTED (per ADK docs)
_retry_config = types.GenerateContentConfig(
    http_options=types.HttpOptions(
        retry_options=types.HttpRetryOptions(initial_delay=2, attempts=3),
    ),
)

food_agent = Agent(
    name="FoodAgent",
    model=model,
    instruction=FOOD_AGENT_INSTRUCTIONS,
    tools=[food_mcp_toolset()],
    after_tool_callback=guardrail.after_tool_callback,
    generate_content_config=_retry_config,
)
