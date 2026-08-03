"""Acceptance. Deterministic, executable, reproducible. No LLMs. Ever.

    build      - the project compiles / installs
    tests      - the suite passes (existing + newly added)
    lint       - linter and formatter are clean
    types      - static type check passes
    coverage   - coverage meets a threshold
    files      - a required path exists / a protected path is untouched
    perf       - a measured metric beats a recorded baseline
    api_compat - the public surface did not break

A check's verdict is a pure function of (workspace git sha, check config).
Same inputs, same verdict, byte for byte -- so verdicts are cached by that
hash and a re-run is provably not a re-roll.

Each check returns structured evidence, not just a boolean. "pytest exited
1" is useless to the planner; the failing test name, the assertion, and the
traceback are what make the next attempt smarter than the last one.

------------------------------------------------------------------
TERRITORY   Acceptance & Evidence         OWNER      Role 2
LAYER       engine / Python               REVIEWER   Role 1
------------------------------------------------------------------
No LLM client may be imported here, directly or transitively. Enforced by
engine/tests/test_acceptance_is_deterministic.py. If you need a model to
decide something, it does not belong in this package.
------------------------------------------------------------------
"""

from .build import BuildValidator
from .coverage import CoverageValidator
from .lint import LintValidator
from .tests import TestValidator

__all__ = ["BuildValidator", "CoverageValidator", "LintValidator", "TestValidator"]
