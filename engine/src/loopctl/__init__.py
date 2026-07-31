"""loopctl - a control plane for long-running AI coding work.

The package is split along one axis that matters more than any other:
packages that may call a language model, and packages that may not.

    MAY call an LLM        MUST NOT call an LLM
    ---------------        --------------------
    agents/                checks/
    runners/               graph/
                           workspace/
                           ledger/

`checks/` is where acceptance lives. If a model can reach into it, the
system's verdicts stop being reproducible and the whole premise collapses.
`engine/tests/test_acceptance_is_deterministic.py` enforces this by import
inspection, so the boundary fails a test rather than resting on convention.
"""
