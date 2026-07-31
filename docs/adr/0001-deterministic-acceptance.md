# ADR 0001 · Acceptance is deterministic and models are excluded from it

**Status:** accepted · **Date:** 2026-07-31

Use this file as the template for the rest: Context, Decision, Consequences,
Alternatives. Keep each under a page. You will be asked to defend the
architecture, and an ADR turns that from an improvisation into a document.

## Context

The system must produce a verdict on model-written code that an engineer can
trust enough to merge. Language models produce confident, fluent claims of
completion that are frequently wrong, and their outputs are not reproducible —
the same input can yield different verdicts across calls.

The brief requires that "given the same state, the acceptance verdict must be
identical every time."

## Decision

Acceptance is computed exclusively by executable checks: subprocess exit codes
and parsed output from the build, test suite, linter, type checker, coverage
tool, and file assertions.

1. `loopctl/checks/` may not import any model client, directly or transitively.
   `engine/tests/test_acceptance_is_deterministic.py` walks the AST of every
   module in the package and fails the build on violation.
2. Every check's verdict is keyed by
   `sha256(workspace_git_sha + canonical_json(check_config))`. Verdicts are
   cached on this key, and a test asserts that running the full suite twice at a
   fixed sha yields byte-identical results.
3. LLM judgement is permitted only as a separate `llm_judge` node type, requires
   a checked-in rubric, returns structured per-criterion evidence, and is
   `blocking: false` by default. Making one blocking stamps the run `llm_gated`
   in the ledger and states it in the report.

## Consequences

**Good.** The verdict is reproducible and auditable. A judge asking "how do I
know a model can't override this?" gets a file, not an assurance. Our own CI can
run the loop with `FakeRunner` at zero cost and zero flakiness.

**Costly.** Qualitative criteria — architectural fit, naming, documentation
quality — cannot block delivery, so some genuinely bad code will pass. We accept
this: a system that reliably catches mechanical defects and defers taste to the
human gate is more useful than one that occasionally hallucinates either verdict.

Writing a check for a new criterion is real work. That is the intended pressure —
it forces criteria to be measurable, which is the whole point of the contract.

## Alternatives considered

**LLM-as-judge for everything.** Cheap to build, fails the reproducibility
requirement outright, and reintroduces exactly the problem the project exists to
solve.

**Deterministic checks with an LLM override for false positives.** Tempting —
real check suites do produce false positives. Rejected: an override path is a
red-check-to-green path, and once it exists every hard failure becomes
negotiable. The human gate is the override, and it is operated by a person.
