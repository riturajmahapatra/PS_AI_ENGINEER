"""Validation Agent -- ADVISORY ONLY. Does not run builds, tests, or lints;
that is checks/, which this agent may never import or call into.

Adds qualitative judgement (architectural fit, readability, documentation
quality) against a written rubric. Output is advisory evidence and defaults
to non-blocking -- it cannot turn a failing deterministic check green. See
agents/__init__.py and docs/02-generation-vs-acceptance.md."""

from typing import Any

from .base import BaseAgent


class ValidationAgent(BaseAgent):
    def __init__(self, config: dict[str, Any] = None):
        super().__init__(name="ValidationAgent", config=config)

    async def execute(self, state: dict[str, Any]) -> dict[str, Any]:
        # Advisory judgement against a rubric. Never a pass/fail verdict --
        # that belongs to checks/.
        return state
