# 03 · Build order

Seven milestones. Each has a **definition of done that is demonstrable** — if you
cannot show it working, the milestone is not finished, regardless of how much
code exists.

The ordering principle is **inside-out**: the loop must work end to end, headless,
with no LLM and no UI, before either an LLM or a UI is attached. That way, when
something breaks later you always know which layer it broke in.

Two people can run milestones in parallel after M1. Suggested split noted per
milestone as **[E]** engine and **[S]** surface.

---

## M0 · Environment and a walking skeleton

**Goal:** `loopctl run examples/workflows/default-loop.yaml` executes a
three-node graph and prints a result. No LLM. No UI. No checks.

- [ ] Install Node.js 20+ and Docker (both currently missing on this machine).
- [ ] `engine/pyproject.toml` with `uv`; deps: `pydantic`, `fastapi`, `uvicorn`,
      `typer`, `pyyaml`, `pytest`, `ruff`, `mypy`.
- [ ] Define the schemas from [doc 01](01-architecture.md#core-contracts).
      **Do this jointly with your teammate and freeze it** — it is the interface
      the two halves meet at.
- [ ] `graph/` executor: load a workflow, walk nodes, follow edges, stop at a
      terminal node.
- [ ] Three node types only: `input`, `command`, `success`.
- [ ] A CLI (`typer`) that runs a workflow file.

**Done when:** a YAML file with input → command(`echo hi`) → success runs from the
CLI and reports success.

**Why first:** everything later is a node or a check. Get the walking skeleton
right and the rest is filling in.

---

## M1 · Choose and prepare the target repository

**Goal:** a real repo with a real, hard-but-demonstrable task, and a *baseline
that fails*.

Pick something where the first attempt will plausibly fail — that failure is the
centrepiece of your demo. Good candidates:

- A small service with an untested module → *"raise coverage on `src/client.py`
  to 85% without modifying `src/client.py` itself."* Coverage is a beautifully
  crisp, hard-to-fake criterion.
- A synchronous HTTP client → *"convert to async, keep the public API
  byte-compatible."* `api_compat` gives you a second independent check.
- A module using a deprecated dependency → *"migrate off it, all tests green."*

Put it in `examples/target-repo/` as its own git repo (not a submodule — you want
to be able to reset it freely). Also try one **external** repo late in the
project to prove you are not overfit to your own fixture.

- [ ] Repo committed, tests currently green.
- [ ] Every check from doc 02 runs against it by hand; write the exact commands
      into `examples/workflows/default-loop.yaml`.
- [ ] Record the baseline: coverage %, test count, timings.
- [ ] Write **two** objectives: one legitimate, one deliberately
      self-contradictory (for the clarification demo).

**Done when:** you can run the full check suite by hand and it is green, and you
know exactly which criterion your objective will initially fail.

---

## M2 · Deterministic acceptance **[E]**

**Goal:** `checks/` works, is reproducible, and returns actionable evidence.

- [ ] `CheckSpec` → `CheckResult` interface; subprocess execution with timeout,
      cwd pinned to the worktree, environment scrubbed.
- [ ] Implement `build`, `tests`, `lint`, `types`, `coverage`, `files`.
- [ ] **Parsers**, not just exit codes: pytest failures into test-id + assertion
      + traceback; coverage into per-file uncovered line ranges; ruff/mypy into
      file/line/rule/message.
- [ ] `determinism_key = sha256(workspace_git_sha + canonical_json(check_config))`
      and a verdict cache keyed on it.
- [ ] `tests/test_acceptance_is_deterministic.py`:
      - the AST import guard from [doc 02](02-generation-vs-acceptance.md)
      - run the full suite twice at a fixed sha, assert byte-identical results

**Done when:** both tests pass, and a failing check prints evidence you would be
happy to hand a junior engineer as their only instruction.

---

## M3 · Workspace isolation **[E]**

**Goal:** an attempt cannot touch the base repo, and rollback is total.

- [ ] `git worktree add` per attempt from the base ref; branch
      `loopctl/<run_id>/attempt-<n>`.
- [ ] Artifact tree under `.artifacts/runs/<run_id>/` as laid out in doc 01.
- [ ] `rollback()`: remove worktree, delete branch, verify base repo clean.
- [ ] Diff capture: `files_changed` with per-file patches.

**Done when:** you can start an attempt, have it delete half the repo, call
`rollback()`, and `git status` in the base repo is clean. Write that as a test —
it is the single most reassuring test in the project.

---

## M4 · The loop, headless, with `FakeRunner` **[E]**

**Goal:** the complete four-role loop with feedback, budget, and safe stop —
still zero tokens.

- [ ] All eight node types.
- [ ] `FakeRunner`: replays scripted file edits from a fixture. Script it so
      **attempt 1 fails coverage and attempt 2 passes.**
- [ ] The four agent roles, with their prompt templates — but wired through
      `FakeRunner` so they are deterministic for now.
- [ ] Failure evidence threaded into the planning prompt on retry; attempt
      counter increments; assert the two prompts differ.
- [ ] Budget: `max_attempts`, `max_wall_clock`, `max_usd`. Exhaustion →
      `StoppedSafely` → rollback → `report.md`.
- [ ] Human gate: run suspends, persists, resumes on a decision.
- [ ] `ledger/`: JSONL append-only, every event, every cost record.
- [ ] Clarification path: a `ClarificationRequest` halts the run.

**Done when:** one headless CLI run shows attempt 1 failing, attempt 2 passing,
and a second run with `max_attempts: 1` stops safely with a clean base repo and
an honest report. **This is the whole assignment working. Everything after is
attaching a model and a face to it.**

---

## M5 · Real agent runners **[E]**

**Goal:** swap `FakeRunner` for a real harness by changing one line of YAML.

- [ ] `ClaudeCodeRunner` via the Claude Agent SDK — filesystem tools, shell,
      transcript capture, token/cost capture.
- [ ] At least one second adapter (`CursorRunner` or `AiderRunner`) to prove the
      abstraction is real. The brief specifically asks that the backend not be
      welded to the orchestrator; two working adapters is the proof.
- [ ] Tool allowlists per agent role — the planner gets read and search, never
      write. Enforce it; do not just ask nicely in the prompt.
- [ ] Prompt engineering pass: ground the planner in real file contents, force
      structured output for criteria and clarifications.
- [ ] Retries and timeouts around provider errors, distinct from loop retries.

**Done when:** the same workflow YAML runs green on `runner: fake` in CI and on
`runner: claude_code` against the real repo, and `runner: aider` also completes.

**Watch out:** this is where cost and flakiness arrive. Keep `FakeRunner` as the
default in CI forever.

---

## M6 · The canvas **[S]** — start this in parallel from M2

**Goal:** the visual node editor that is the actual product surface.

- [ ] React + Vite + TypeScript + **React Flow**. Generate TS types from the
      pydantic schemas so the contract cannot drift.
- [ ] Five areas, per the brief: top bar (name, save/export, run/pause/stop, run
      status, attempt counter) · node library panel · canvas · node inspector ·
      collapsible run console.
- [ ] Node cards show name, type, status, config summary, ports, latest result.
- [ ] Inspector shows **only settings relevant to the selected node** — this is
      called out explicitly in the brief and is easy to fail by rendering one
      giant form.
- [ ] Live status over WebSocket; nodes light up as the run walks the graph.
- [ ] Console: agent messages, commands, files changed, validation evidence,
      errors, retry reasons, human feedback.
- [ ] Click a completed or failed node → inspect that execution: input, output,
      commands, files, check results, retry reason.
- [ ] Human gate renders as an approve/reject panel with the diff.

**Done when:** you can build the default loop from an empty canvas, run it, and
diagnose a failure without leaving the browser.

---

## M7 · Config as code, packaging, demo

- [ ] Export canvas → YAML. Import YAML → canvas. **Round-trip test:** export,
      import, export again, assert identical.
- [ ] Commit exported workflows to `examples/workflows/`.
- [ ] `infra/docker-compose.yml`: engine + web, one command to start.
- [ ] Run report: markdown + JSON — outcome, criteria table with evidence,
      attempts, cost, timings, why it ended.
- [ ] Rehearse the demo against [doc 04](04-demo-and-scoring.md). Time it.
- [ ] Write 2–3 ADRs in `docs/adr/` — why a graph executor over a hardcoded
      state machine, why worktrees over containers, why deterministic-only
      acceptance. **You will be asked to defend the architecture; ADRs mean you
      answer with a document instead of an improvisation.**

---

## Where teams lose this

- **Building the canvas first.** It demos well and proves nothing. The loop is
  the assignment.
- **Skipping `FakeRunner`.** Every subsequent milestone gets 100× slower to debug.
- **Vague evidence.** The whole feedback claim collapses if attempt 2 receives
  "validation failed".
- **No safe-stop demo.** It is a third of the brief and takes an hour to build
  once rollback works. Show it.
- **Forgetting the clarification case.** Cheap points, almost universally skipped.
- **Cost tracking bolted on at the end.** Put `CostRecord` in the schemas at M0
  and thread it through as you go; retrofitting it means touching every node.
