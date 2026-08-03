"""The four LLM roles and their prompts. Generation lives here.

    SuccessCriteriaAgent - objective -> measurable, checkable criteria
    PlanningAgent        - objective + criteria + failure evidence -> plan
    ExecutionAgent       - plan -> file edits, via a runner
    ValidationAgent      - ADVISORY ONLY (see below)

Note the asymmetry on the last one. The Validator *node* runs deterministic
checks. A validation *agent* may add qualitative judgement (readability,
architectural fit, documentation quality) against a written rubric, but its
output is recorded as advisory evidence and cannot flip a failing
deterministic check to passing. That rule is the whole point of the system;
see docs/02-generation-vs-acceptance.md.

Agents also own the clarification path: when an objective is ambiguous or
self-contradictory, an agent returns a structured ClarificationRequest
instead of guessing, and the run halts at a human gate.

Criteria, Planning, and the advisory judge call the Messages API directly via
`client.messages.parse(output_format=SomePydanticModel)`, so their output is
schema-valid by construction rather than by parsing prose. Execution goes
through a runner instead -- see runners/.

------------------------------------------------------------------
TERRITORY   Generation & Control          OWNER      Role 1
LAYER       engine / Python               REVIEWER   Role 2
------------------------------------------------------------------
"""

from .base import BaseAgent
from .execution import ExecutionAgent
from .planning import PlanningAgent
from .success_criteria import SuccessCriteriaAgent
from .validation import ValidationAgent

__all__ = [
    "BaseAgent",
    "ExecutionAgent",
    "PlanningAgent",
    "SuccessCriteriaAgent",
    "ValidationAgent",
]
