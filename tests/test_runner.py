import asyncio
import os
import sys
import logging
from dotenv import load_dotenv

# Path Setup
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)
agent_dir = os.path.join(root_dir, "swiggy_concierge")
if agent_dir not in sys.path:
    sys.path.insert(0, agent_dir)

load_dotenv(os.path.join(agent_dir, ".env"))

# ADK and Project Imports
from swiggy_concierge.agent import root_agent
from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.genai import types

from tests.test_cases import TEST_SCENARIOS
from tests.result_manager import ResultManager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("TestRunner")

async def run_scenario(runner, scenario, result_manager):
    logger.info(f"\n--- SCENARIO: {scenario['name']} ---")
    session_id = f"test_{scenario['id']}"
    
    for i, turn in enumerate(scenario["turns"]):
        turn_id = f"{scenario['id']}-T{i+1}"
        logger.info(f"Turn {i+1}: {turn['query']}")
        
        found_tools = []
        error = ""
        status = "FAIL"
        
        try:
            msg = types.Content(role="user", parts=[types.Part(text=turn["query"])])
            async for event in runner.run_async(
                user_id="tester",
                session_id=session_id,
                new_message=msg
            ):
                fcs = event.get_function_calls()
                if fcs:
                    for fc in fcs:
                        found_tools.append(fc.name)
                        logger.info(f"  [Tool] {fc.name}")
            
            # Basic turn validation
            missing = [t for t in turn["expected_tools"] if t not in found_tools]
            if not missing:
                status = "PASS"
            elif found_tools:
                status = "PARTIAL"
                
        except Exception as e:
            status = "ERROR"
            error = str(e)
            logger.error(f"  [Error] {error}")

        result_manager.add_result(turn_id, scenario["name"], turn["query"], status, found_tools, error)

async def main():
    if not os.getenv("GOOGLE_API_KEY"):
        logger.error("API Key missing.")
        return

    res_mgr = ResultManager()
    runner = Runner(
        app_name="swiggy_test_suite",
        agent=root_agent,
        session_service=InMemorySessionService(),
        memory_service=InMemoryMemoryService(),
        auto_create_session=True
    )

    for scenario in TEST_SCENARIOS:
        await run_scenario(runner, scenario, res_mgr)

    res_mgr.save()
    logger.info("Test execution complete.")

if __name__ == "__main__":
    asyncio.run(main())
