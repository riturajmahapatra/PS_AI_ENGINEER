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

Ownership runs along a second axis, orthogonal to that one -- two capability
tracks, each spanning Python and React, so both engineers write both. See
docs/05-tech-stack-and-ownership.md; every module states its owner in the
banner at the bottom of its docstring.

------------------------------------------------------------------
TERRITORY   SHARED -- both roles          OWNER      Role 1 + Role 2
LAYER       engine / Python               REVIEWER   the other one
------------------------------------------------------------------
"""
