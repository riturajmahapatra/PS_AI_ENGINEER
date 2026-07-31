"""Implementations of the node library.

    Input      - the coding objective and constraints entering the graph
    Agent      - an LLM role: criteria / planning / execution
    Command    - runs a shell command in the attempt workspace
    Validator  - evaluates success criteria, returns pass/fail + evidence
    Decision   - branches on a prior node's result
    HumanGate  - suspends the run until a human approves or rejects
    Success    - terminal: task delivered
    Stop       - terminal: stopped safely (always rolls the workspace back)

Every node implements the same contract: given a RunContext, return a
NodeOutcome carrying a status, a payload, and its cost. Adding a node type
means adding a file here and registering it -- nothing in graph/ changes.
"""
