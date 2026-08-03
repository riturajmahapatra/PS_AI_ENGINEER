"""The workflow graph, as authored and as exported. This is the schema
examples/workflows/default-loop.yaml parses against -- the canvas exports
this shape, the engine imports it, and it round-trips without loss. When
you're unsure what a field should be named, check that YAML file first;
it is the ground truth this schema follows, not the other way around.

`Node.config` is deliberately a loose dict, not a discriminated union per
node type. Modeling every node type's config precisely is M0-M4 work as
each type actually gets built (docs/03) -- forcing that out now would mean
guessing at shapes nobody has implemented against yet."""

from typing import Any, Literal

from pydantic import BaseModel, Field

# The eight node types. See nodes/__init__.py -- this list must stay in
# sync with it.
NodeType = Literal[
    "input",
    "agent",
    "command",
    "validator",
    "decision",
    "human_gate",
    "success",
    "stop",
]

# The four agent roles. See agents/__init__.py.
AgentRole = Literal["success_criteria", "planning", "execution", "validation"]


class Target(BaseModel):
    repo: str
    base_ref: str
    isolation: Literal["git-worktree", "container"] = "git-worktree"


class Budget(BaseModel):
    max_attempts: int
    max_wall_clock_minutes: int
    max_usd: float
    on_exhaustion: str = "stop_safely"  # rollback + honest report, always


class Defaults(BaseModel):
    provider: str
    model: str


class Node(BaseModel):
    id: str
    type: NodeType
    name: str | None = None
    role: AgentRole | None = None  # only meaningful when type == "agent"
    config: dict[str, Any] = Field(default_factory=dict)


class Edge(BaseModel):
    model_config = {"populate_by_name": True}

    from_: str = Field(alias="from")
    to: str
    on: str | None = None  # e.g. "success", "clarification", "approved"
    when: str | None = None  # e.g. "!verify.passed && attempts_remaining"


class WorkflowMetadata(BaseModel):
    name: str
    version: int
    description: str = ""


class WorkflowSpec(BaseModel):
    target: Target
    budget: Budget
    defaults: Defaults
    nodes: list[Node]
    edges: list[Edge]


class Workflow(BaseModel):
    apiVersion: str = "loopctl/v1"
    kind: Literal["Workflow"] = "Workflow"
    metadata: WorkflowMetadata
    spec: WorkflowSpec
