import logging
from typing import Any, Optional
from google.adk.plugins.base_plugin import BasePlugin
from google.adk.tools.base_tool import BaseTool

logger = logging.getLogger(__name__)

class SwiggyGuardrailPlugin(BasePlugin):
    """Filters tool results before they reach the LLM. Currently handles the 5 km restaurant radius."""

    def __init__(self):
        super().__init__(name="swiggy_guardrails")

    async def after_tool_callback(
        self,
        *,
        tool: BaseTool,
        **kwargs: Any
    ) -> Optional[dict]:
        """
        Handles inconsistent ADK parameter naming:
        - Tool Output: Can be in 'result' or 'tool_response'
        - Args: Can be in 'tool_args' or 'args'
        """
        # Extract result from possible keys
        result = kwargs.get("result") or kwargs.get("tool_response")
        
        if not result or not isinstance(result, dict) or "content" not in result:
            return None

        tool_name = tool.name

        if tool_name == "search_restaurants":
            for block in result.get("content", []):
                if block.get("type") != "text":
                    continue
                lines = block.get("text", "").split("\n")
                filtered = []
                skip_next = False
                for line in lines:
                    if skip_next:
                        skip_next = False
                        continue
                    # Check for distance markers
                    if any(f"{d} km" in line for d in ["5.2", "6.5", "7.", "8.", "9.", "10.", "11.", "12.", "13.", "14.", "15."]):
                        skip_next = True
                        continue
                    filtered.append(line)
                if len(filtered) != len(lines):
                    block["text"] = "\n".join(filtered) + "\n\n[Filtered: results beyond 5 km removed]"
            return result

        return None
