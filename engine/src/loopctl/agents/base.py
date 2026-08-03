"""Base agent class for AI Loop Platform agents."""

from abc import ABC, abstractmethod
from typing import Any


class BaseAgent(ABC):
    """Abstract base class for platform agents."""
    
    def __init__(self, name: str, config: dict[str, Any] = None):
        self.name = name
        self.config = config or {}
        
    @abstractmethod
    async def execute(self, state: dict[str, Any]) -> dict[str, Any]:
        """Execute agent logic against current state."""
        pass
