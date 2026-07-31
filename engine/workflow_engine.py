"""Workflow Engine managing the main AI agent loop state machine."""

from typing import Any, Dict
from .graph_executor import GraphExecutor

class WorkflowEngine:
    def __init__(self):
        self.executor = GraphExecutor()

    async def start_loop(self, task: str) -> Dict[str, Any]:
        """Start autonomous AI execution loop."""
        state = {"task": task, "status": "initialized"}
        return await self.executor.run(state)
