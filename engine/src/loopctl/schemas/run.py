"""What flows through the executor on each pass, and what a node hands
back when it finishes. Both evolve as the eight node types get built out
(docs/03, M0-M4) -- treat these as the day-one shape, not the final one."""

from typing import Any, Literal

from pydantic import BaseModel, Field

from .checks import CheckResult
from .cost import CostRecord
from .criteria import SuccessCriterion


class RunContext(BaseModel):
    """Carried through the graph for one run. `prior_evidence` is what
    makes attempt N+1 different from a re-roll of attempt N -- it is the
    failing CheckResults from the previous attempt, threaded into the next
    planning prompt. See docs/00, "feed failure forward"."""

    run_id: str
    workflow_name: str
    attempt: int = 1
    max_attempts: int = 1
    criteria: list[SuccessCriterion] = Field(default_factory=list)
    prior_evidence: list[CheckResult] = Field(default_factory=list)


class NodeOutcome(BaseModel):
    """What every node type returns, regardless of what it did. The
    executor reads `status` to decide where to go next -- it never
    inspects `payload` to make that decision itself. See
    graph/__init__.py."""

    status: Literal["success", "failure", "clarification", "awaiting_human"]
    payload: dict[str, Any] = Field(default_factory=dict)
    cost: CostRecord = Field(default_factory=CostRecord)
