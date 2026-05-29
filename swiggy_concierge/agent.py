import os
from google.adk.agents import Agent
from google.genai import types
from swiggy_concierge.subagents.food_agent import food_agent
from swiggy_concierge.subagents.instamart_agent import instamart_agent
from swiggy_concierge.subagents.dineout_agent import dineout_agent
from swiggy_concierge.instructions import ORCHESTRATOR_INSTRUCTIONS

model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

# Retry config to handle 429 RESOURCE_EXHAUSTED (per ADK docs)
_retry_config = types.GenerateContentConfig(
    http_options=types.HttpOptions(
        retry_options=types.HttpRetryOptions(
            initial_delay=2,   # seconds before first retry
            attempts=3,        # total attempts (1 original + 2 retries)
        ),
    ),
)

root_agent = Agent(
    name="SwiggyConcierge",
    model=model,
    instruction=ORCHESTRATOR_INSTRUCTIONS,
    sub_agents=[food_agent, instamart_agent, dineout_agent],
    generate_content_config=_retry_config,
)
