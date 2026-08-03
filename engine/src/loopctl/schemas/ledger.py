"""The receipt shape. One LedgerEvent per thing that happened -- written
append-only, JSONL, never updated or deleted. See ledger/__init__.py."""

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field

from .cost import CostRecord


class LedgerEvent(BaseModel):
    ts: datetime
    run_id: str
    attempt: int
    node_id: str
    actor: Literal["agent", "check", "human", "system"]
    type: str
    payload: dict[str, Any] = Field(default_factory=dict)
    duration_ms: int
    cost: CostRecord | None = None
