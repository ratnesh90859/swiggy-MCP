import os
from google.adk.agents import Agent
from google.genai import types
from swiggy_concierge.instructions import DINEOUT_AGENT_INSTRUCTIONS
from swiggy_concierge.tools.mcp import dineout_mcp_toolset

model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

# Retry config to handle 429 RESOURCE_EXHAUSTED (per ADK docs)
_retry_config = types.GenerateContentConfig(
    http_options=types.HttpOptions(
        retry_options=types.HttpRetryOptions(initial_delay=2, attempts=3),
    ),
)

dineout_agent = Agent(
    name="DineoutAgent",
    model=model,
    instruction=DINEOUT_AGENT_INSTRUCTIONS,
    tools=[dineout_mcp_toolset()],
    generate_content_config=_retry_config,
)
