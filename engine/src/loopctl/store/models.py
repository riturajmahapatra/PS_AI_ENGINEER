"""Persistence row models.

Named to match the vocabulary the rest of the docs use throughout --
Workflow / Run / Attempt, not Project / Execution. store/__init__.py's own
docstring promises "workflows, runs, attempts, node states, ledger events,
and human-gate decisions"; these are the first three of those."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class WorkflowRecord:
    id: str
    name: str
    created_at: datetime

@dataclass
class RunRecord:
    id: str
    workflow_id: str
    status: str

@dataclass
class AttemptRecord:
    id: str
    run_id: str
    attempt_number: int
    status: str
