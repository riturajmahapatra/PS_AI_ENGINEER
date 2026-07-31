"""Pydantic models -- the contracts every other package speaks in.

    Workflow, Node, Edge          - the graph, as authored and as exported
    SuccessCriterion              - one measurable, checkable condition
    RunContext, NodeOutcome       - what flows through the executor
    CheckResult                   - verdict + structured evidence
    ClarificationRequest          - the "ask, do not guess" payload
    LedgerEvent, CostRecord       - receipts

These same models serialise to the exported YAML, so the file an engineer
downloads from the canvas is the file the engine imports and reruns. One
schema, not two that drift.
"""
