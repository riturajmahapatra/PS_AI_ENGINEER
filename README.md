# loopctl — a control plane for AI coding work

**Problem Statement 1, Track B: Loop Engineering Platform.**

An engineer points `loopctl` at a repository, states an engineering objective, and
approves a contract of measurable success criteria. Four agent roles then work the
task in a bounded loop — criteria, plan, execute, validate — while deterministic
checks, not the model, decide whether anything advances. Every run leaves an
inspectable trail of what each agent did, what it cost, and why the run ended the
way it did. If the budget runs out, the workspace is rolled back and the run is
reported honestly as undelivered.

It is not a chat interface. The primary surface is a node canvas where the loop
itself is the artifact you edit, save, export, and rerun.

## The one idea this project is built around

> Generation is where models are free. Acceptance is where they are forbidden.

A language model can propose criteria, write a plan, and edit files. It cannot
declare its own work finished. That verdict belongs to the compiler, the test
suite, the linter, the type checker, and the coverage report. An LLM's opinion —
however confident — must never turn a red check green.

This is enforced structurally, not by good intentions: `loopctl/checks/` is
forbidden from importing any model client, and a test fails the build if it ever
does. See [docs/02-generation-vs-acceptance.md](docs/02-generation-vs-acceptance.md).

## Read these in order

| Doc | What it answers |
| --- | --- |
| [docs/00-what-we-are-building.md](docs/00-what-we-are-building.md) | What the product is, in plain terms. **Start your teammate here.** |
| [docs/01-architecture.md](docs/01-architecture.md) | The components, the state machine, how data flows |
| [docs/02-generation-vs-acceptance.md](docs/02-generation-vs-acceptance.md) | The core principle and how it is enforced |
| [docs/03-build-order.md](docs/03-build-order.md) | Milestone-by-milestone build plan with definitions of done |
| [docs/04-demo-and-scoring.md](docs/04-demo-and-scoring.md) | The nine required demo beats, mapped to what to build |

## Repository layout

```
engine/                  Python: the loop engine and its API
  src/loopctl/
    api/                 FastAPI REST + WebSocket for the canvas
    graph/               workflow graph model and executor
    nodes/               the eight node types
    agents/              the four LLM roles           [LLM allowed]
    runners/             coding-agent harness adapters [LLM allowed]
    checks/              deterministic acceptance      [LLM FORBIDDEN]
    workspace/           git worktree isolation + rollback
    ledger/              append-only receipts and cost accounting
    schemas/             pydantic contracts, shared with the exported YAML
    store/               persistence
  tests/                 tests for loopctl itself

web/                     React + React Flow node canvas
examples/
  workflows/             exported workflow YAML (config as code)
  target-repo/           the repository the loop operates on for the demo
infra/                   docker compose, Dockerfiles
docs/                    design and learning documentation
  adr/                   architecture decision records
.artifacts/              run outputs — gitignored, never committed
```

Each package's `__init__.py` carries a docstring explaining that package's job
and its constraints. Read them before writing into a package.

## Prerequisites

Confirmed present on this machine: Python 3.14, `uv`, git.
**Missing and required:** Node.js 20+ (for the canvas) and Docker (for packaging).
Install those before starting Milestone 4.

## Status

Scaffolding and design. No implementation yet — see
[docs/03-build-order.md](docs/03-build-order.md) for what to build first.
