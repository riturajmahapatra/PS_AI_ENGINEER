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

They are also the `output_format` passed to `client.messages.parse()`, so the
same class that defines the API contract constrains what the model may emit.

------------------------------------------------------------------
TERRITORY   SHARED -- both roles          OWNER      Role 1 + Role 2
LAYER       engine / Python               REVIEWER   the other one
------------------------------------------------------------------
Freeze this package together on day one and change it only by agreement.
It is the seam where the two tracks meet; unilateral edits here break the
other person's build.
------------------------------------------------------------------
"""
