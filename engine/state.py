"""State management models for workflow execution context."""

from dataclasses import dataclass, field
from typing import Any, Dict, List

@dataclass
class LoopState:
    task_id: str
    status: str = "pending"
    context: Dict[str, Any] = field(default_factory=dict)
    history: List[Dict[str, Any]] = field(default_factory=list)
