"""The workflow graph model and its executor.

A workflow is a directed graph of nodes with labelled edges (`on_success`,
`on_failure`, `on_clarification`). The executor walks it one node at a
time, recording every transition to the ledger.

Two invariants:

  1. The executor never decides anything itself. Nodes return outcomes;
     edges determine where control goes next. This is what makes the loop
     a configurable template rather than a hardcoded sequence.

  2. Every step is resumable. State lives in the store, not in Python
     locals, so a paused or crashed run can be picked back up.
"""
