"""examples/workflows/default-loop.yaml is the contract every part of the
system is built against -- if it stops parsing, or stops round-tripping,
that is not a documentation problem, it's a schema-drift problem.

This also guards a real bug that shipped once: an unquoted `on:` key in
YAML is parsed as the boolean True (YAML 1.1's bareword-boolean rules
cover on/off/yes/no/true/false), not the string "on". Every conditional
edge in this file silently lost its condition until this test caught it.
See the comment above `edges:` in the YAML file itself."""

from pathlib import Path

import yaml

from loopctl.schemas import Workflow

WORKFLOW_PATH = (
    Path(__file__).resolve().parents[2] / "examples" / "workflows" / "default-loop.yaml"
)


def _load() -> Workflow:
    raw = yaml.safe_load(WORKFLOW_PATH.read_text(encoding="utf-8"))
    return Workflow.model_validate(raw)


def test_default_workflow_parses() -> None:
    wf = _load()
    assert wf.metadata.name == "default-four-agent-loop"
    assert len(wf.spec.nodes) == 10
    assert len(wf.spec.edges) == 14


def test_on_key_is_a_string_not_a_bool() -> None:
    # The regression this test exists for: a bare `on:` key in YAML parses
    # as the boolean True, not the string "on". If this ever comes back,
    # every conditional edge silently reverts to "always take this path".
    wf = _load()
    conditional_edges = [e for e in wf.spec.edges if e.on is not None]
    assert len(conditional_edges) == 9
    assert all(isinstance(e.on, str) for e in conditional_edges)

    decide_node = next(n for n in wf.spec.nodes if n.id == "decide")
    assert decide_node.config == {"on": "verify.status"}


def test_round_trips_through_dump_and_reparse() -> None:
    wf = _load()
    dumped = wf.model_dump(by_alias=True, mode="json")
    reparsed = Workflow.model_validate(dumped)
    assert reparsed == wf


def test_no_dangling_edges() -> None:
    wf = _load()
    node_ids = {n.id for n in wf.spec.nodes}
    for edge in wf.spec.edges:
        assert edge.from_ in node_ids, f"edge references unknown node {edge.from_!r}"
        assert edge.to in node_ids, f"edge references unknown node {edge.to!r}"
