"""Success Criteria Agent: reads the objective and the repo, proposes
measurable, checkable success criteria. See docs/00 and agents/__init__.py."""

from typing import Any

from .base import BaseAgent


class SuccessCriteriaAgent(BaseAgent):
    def __init__(self, config: dict[str, Any] = None):
        super().__init__(name="SuccessCriteriaAgent", config=config)

    async def execute(self, state: dict[str, Any]) -> dict[str, Any]:
        # Propose criteria from the objective + repo context, or emit a
        # ClarificationRequest if the objective is ambiguous/contradictory.
        return state
