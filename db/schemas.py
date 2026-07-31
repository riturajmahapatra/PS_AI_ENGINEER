"""API and persistence schemas."""

from typing import Any, Dict, Optional

class ProjectSchema:
    name: str
    description: Optional[str] = None
