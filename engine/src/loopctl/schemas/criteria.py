"""The success-criteria contract and the ask-don't-guess escape hatch.

A SuccessCriterion with no CheckSpec is advisory by construction (blocking
defaults to True only when a check exists to back it -- see the validator
in SuccessCriterion). This is what keeps "the model says it's fine" from
ever being able to pass a run: a criterion the system cannot measure
cannot block delivery."""

from typing import Literal

from pydantic import BaseModel, Field


class CheckSpec(BaseModel):
    """How a criterion is measured. `type` matches a check implementation
    under checks/ (build, tests, lint, types, coverage, files, perf,
    api_compat) or the advisory `llm_judge`. Type-specific fields
    (`min_percent`, `must_not_change`, `public_surface`, `rubric`, ...)
    are accepted but not individually modeled yet -- see
    examples/workflows/default-loop.yaml for the shapes in use today."""

    model_config = {"extra": "allow"}

    id: str
    type: str
    run: str | None = None
    blocking: bool = True


class SuccessCriterion(BaseModel):
    id: str
    statement: str  # "coverage on src/client.py is at least 85%"
    check: CheckSpec | None = None  # how it is measured; None = advisory only
    blocking: bool = True  # can this alone fail the run?
    priority: Literal["must", "should"] = "must"
    source: Literal["user", "agent", "hybrid"] = "hybrid"


class ClarificationRequest(BaseModel):
    """What an agent emits instead of guessing when the objective is
    ambiguous or self-contradictory. Halts the run at a human gate."""

    question: str
    conflicting_requirements: list[str]
    options: list[str] = Field(default_factory=list)
    blocking: bool = True
