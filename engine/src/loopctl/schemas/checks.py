"""What a check hands back. Evidence, not a boolean -- "pytest exited 1" is
useless to the planner; the failing test name, the assertion, and the
traceback are what make the next attempt smarter than the last one. See
docs/02-generation-vs-acceptance.md, "the checks to actually ship"."""

from typing import Any

from pydantic import BaseModel, Field


class Evidence(BaseModel):
    command: str | None = None
    exit_code: int | None = None
    stdout: str = ""
    stderr: str = ""
    # Parsed specifics a planner can act on: failing test ids and
    # assertions, uncovered line ranges, lint rule/file/line, etc.
    # Shape is check-type-specific, so it stays a dict here rather than a
    # a class per check type.
    detail: dict[str, Any] = Field(default_factory=dict)


class CheckResult(BaseModel):
    check_id: str
    passed: bool
    evidence: Evidence
    duration_ms: int
    # sha256(workspace_git_sha + canonical_json(check_config)). Same inputs,
    # same verdict, byte for byte -- this is what lets a verdict be cached
    # and lets you prove a re-run is not a re-roll. See docs/01 and
    # docs/02-generation-vs-acceptance.md.
    determinism_key: str
