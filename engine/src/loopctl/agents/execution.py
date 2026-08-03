"""Execution Agent: turns a plan into file edits.

Does not touch the filesystem itself -- delegates to an AgentRunner from
runners/ (ClaudeCodeRunner, CursorRunner, AiderRunner, FakeRunner). This
class is the thin role wrapper; the runner is what actually holds file and
shell access. See runners/__init__.py."""

from typing import Any

from .base import BaseAgent


class ExecutionAgent(BaseAgent):
    def __init__(self, config: dict[str, Any] = None):
        super().__init__(name="ExecutionAgent", config=config)

    async def execute(self, state: dict[str, Any]) -> dict[str, Any]:
        # Hand the plan to a runner (runners/) and return its RunResult.
        return state
