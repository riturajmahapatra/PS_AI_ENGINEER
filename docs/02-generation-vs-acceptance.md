# 02 · Generation vs acceptance

> "Language models are eloquent about code that does not work."

This is the highest-weighted idea in the brief and the one most submissions get
wrong — not by disagreeing with it, but by *saying* it in a README and then
building a system where a model still ultimately decides. This document is how
we avoid that.

## The rule

**Generation** — proposing criteria, writing plans, editing files — is where
models operate freely.

**Acceptance** — the verdict that a change may advance — belongs exclusively to
executable checks. Compiler, test suite, linter, type checker, coverage report,
file assertions, performance measurement against a baseline.

An LLM's opinion, however confident, must never turn a red check green.

## Three failure modes to design against

**1. The model summarises the checks.** An agent runs `pytest`, sees a failure,
and reports "tests pass with minor warnings." Fix: the *node* runs the check as a
subprocess and parses the exit code. The agent's transcript is evidence, never
input to the verdict.

**2. The model is asked to judge.** "Does this satisfy the criteria?" is a
generation question dressed as acceptance. Fix: every criterion carries a
`CheckSpec` describing how it is measured. A criterion with no `CheckSpec` is
`blocking: false` and cannot fail a run.

**3. The verdict drifts.** Same code, two runs, two answers — because a check
depended on wall-clock, network, `$PWD`, or test ordering. Fix: `determinism_key`,
plus a test that runs the full check suite twice against a fixed sha and asserts
the results are byte-identical.

## How we enforce it structurally

Rules that live in documentation get broken at 2am on day three. This one lives
in a test.

`engine/tests/test_acceptance_is_deterministic.py` should contain:

```python
FORBIDDEN = {"anthropic", "openai", "litellm", "langchain",
             "loopctl.agents", "loopctl.runners"}

def test_checks_package_imports_no_model_client():
    """Acceptance must be reproducible. A model client in checks/ makes it not."""
    for path in (SRC / "loopctl" / "checks").rglob("*.py"):
        tree = ast.parse(path.read_text())
        for node in ast.walk(tree):
            names = ...  # collect Import / ImportFrom module roots
            offending = names & FORBIDDEN
            assert not offending, f"{path.name} imports {offending}"
```

Walk the AST rather than grepping — grep misses `importlib` and trips on
comments. Run it transitively too: `checks/` importing a helper that imports
`anthropic` is the same violation one hop out.

When a judge asks "how do I know a model can't override your checks?", you open
this file. That answer is worth more than three paragraphs of prose.

## Where LLM-as-judge is legitimate

The brief does allow it — for qualitative areas a compiler cannot see:
architectural alignment, readability, documentation quality, adherence to
conventions. Our rules:

1. It runs as its own node type (`llm_judge`), never inside `checks/`.
2. It requires a written rubric checked into `docs/rubrics/`.
3. It returns structured output — per-criterion score plus quoted evidence from
   the diff — not a paragraph.
4. It defaults to `blocking: false`.
5. If a user sets `blocking: true` on the canvas, the run is stamped
   `llm_gated: true` in the ledger and the report says so. We do not forbid it;
   we make it impossible to do accidentally or invisibly.

That last point is the mature position, and worth saying out loud when you
present: we did not ban LLM judgement, we made it *legible*.

## The checks to actually ship

Match these to your demo repo. Breadth matters less than each one returning
evidence a planner can act on.

| Check | Deterministic signal | Evidence returned |
| --- | --- | --- |
| `build` | install/compile exit code | failing step, stderr |
| `tests` | pytest exit code | failing test ids, assertions, tracebacks |
| `lint` | ruff exit code | file, line, rule code, message |
| `types` | mypy exit code | file, line, error text |
| `coverage` | measured % vs threshold | per-file uncovered line ranges |
| `files` | path exists / path unchanged | which protected path was touched |
| `perf` | measured metric vs baseline | before, after, delta |
| `api_compat` | exported-symbol diff | symbols removed or re-signatured |

Notice the right-hand column. `CheckResult.evidence` is what makes attempt 2
smarter than attempt 1. "Tests failed" is a dead end; `test_client.py::test_retry
— AssertionError: expected 3 retries, got 1` is a plan.

**Bad:**
```
Validation failed. Please fix the issues and try again.
```

**Good:**
```
coverage: FAIL — 71.2% < 85% threshold
  src/client.py lines 44-58, 91-103 uncovered
  (the retry path and the timeout handler have no tests)
tests: PASS — 24 passed in 3.1s
lint:  PASS
```

Feed the second one to the planner and you get a targeted next attempt. Feed the
first and you get a re-roll.
