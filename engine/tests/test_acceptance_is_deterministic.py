"""Enforces the one rule the whole project is built around: acceptance
(checks/) must never be able to import a model client, directly or
transitively. See docs/02-generation-vs-acceptance.md.

This is a structural guard, not a style preference -- it is what lets us
answer "how do I know an LLM can't override your verdict?" with a file
instead of a promise."""

import ast
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"

FORBIDDEN = {
    "anthropic",
    "openai",
    "litellm",
    "langchain",
    "langchain_core",
    "langgraph",
    "claude_agent_sdk",
    "loopctl.agents",
    "loopctl.runners",
}


def _imported_module_roots(tree: ast.Module) -> set[str]:
    roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                roots.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module:
            # module is already dotted, e.g. "loopctl.agents.planning" --
            # check against both the full path and its root, so a
            # forbidden entry like "loopctl.agents" catches submodule
            # imports too.
            parts = node.module.split(".")
            for i in range(1, len(parts) + 1):
                roots.add(".".join(parts[:i]))
    return roots


def test_checks_package_imports_no_model_client() -> None:
    checks_dir = SRC / "loopctl" / "checks"
    assert checks_dir.is_dir(), f"expected {checks_dir} to exist"

    violations: dict[str, set[str]] = {}
    for path in sorted(checks_dir.rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        offending = _imported_module_roots(tree) & FORBIDDEN
        if offending:
            violations[str(path.relative_to(SRC))] = offending

    assert not violations, (
        "checks/ must never import a model client -- acceptance has to stay "
        f"deterministic. Offending imports: {violations}"
    )


def test_forbidden_set_is_not_accidentally_empty() -> None:
    # A guard that can never fail is not a guard. Sanity-check the test
    # itself catches something, so a future refactor can't silently hollow
    # it out by editing FORBIDDEN down to nothing.
    assert len(FORBIDDEN) >= 5
