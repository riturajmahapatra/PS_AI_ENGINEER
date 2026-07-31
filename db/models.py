"""Database models for AI Loop Platform."""

from dataclasses import dataclass
from datetime import datetime

@dataclass
class ProjectModel:
    id: str
    name: str
    created_at: datetime

@dataclass
class ExecutionModel:
    id: str
    project_id: str
    status: str
