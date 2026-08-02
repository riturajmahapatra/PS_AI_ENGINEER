# AI Loop Platform

An autonomous, multi-agent engine and execution loop platform for AI engineering workflows.

**Problem Statement 1, Track B: Loop Engineering Platform.**

An engineer points the platform at a repository, states an engineering objective,
and approves a contract of measurable success criteria. Four agent roles then work
the task in a bounded loop — criteria, plan, execute, validate — while deterministic
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

This is enforced structurally, not by good intentions: the acceptance package is
forbidden from importing any model client, and a test fails the build if it ever
does. See [docs/02-generation-vs-acceptance.md](docs/02-generation-vs-acceptance.md).

## Read these in order

| Doc | What it answers |
| --- | --- |
| [docs/00-what-we-are-building.md](docs/00-what-we-are-building.md) | What the product is, in plain terms. **Start here.** |
| [docs/01-architecture.md](docs/01-architecture.md) | The components, the state machine, how data flows |
| [docs/02-generation-vs-acceptance.md](docs/02-generation-vs-acceptance.md) | The core principle and how it is enforced |
| [docs/03-build-order.md](docs/03-build-order.md) | Milestone-by-milestone build plan with definitions of done |
| [docs/04-demo-and-scoring.md](docs/04-demo-and-scoring.md) | The nine required demo beats, mapped to what to build |
| [docs/05-tech-stack-and-ownership.md](docs/05-tech-stack-and-ownership.md) | The stack, the API rules that will bite you, and **who writes which file** |

## ⚠️ Two layouts currently coexist — pick one before M0

This branch carries **both** an early flat scaffold and a package layout, because
they were written in parallel. Same architecture, different physical shape. They
need reconciling before real implementation starts; until then, treat the layout
below as a description of what exists, not as a decision.

### Flat scaffold

- **`agents/`**: Autonomous AI agent modules.
  - `base_agent.py`: Base abstract class for agents.
  - `planning_agent.py`: Task decomposition and plan generation.
  - `success_agent.py`: Goal verification and quality evaluation.
  - `execution_agent.py`: Code editing and tool execution.
  - `validation_agent.py`: Build, lint, and test validation.
- **`engine/`**: Core execution engine and state machine.
  - `graph_executor.py`: Dynamic agent node DAG executor.
  - `workflow_engine.py`: Agent execution loop orchestration.
  - `state.py`: Execution state models.
- **`runner/`**: Execution environment runners.
  - `repository.py`: Workspace filesystem manager.
  - `shell.py`: Subprocess & shell runner.
  - `git.py`: Git operations integration.
- **`validator/`**: Automated verification and quality gates.
  - `build.py`: Build system validator.
  - `tests.py`: Test suite execution validator.
  - `lint.py`: Code quality & linter validator.
  - `coverage.py`: Test coverage threshold validator.
- **`db/`**: Database models and data schemas.
  - `models.py`: ORM & data models.
  - `schemas.py`: Validation & API schemas.
- **`api/`**: Backend API endpoints.
- **`backend/`**: Core backend services.
- **`frontend/`**: Web canvas & visual interface components.
  - `canvas/`: Graph canvas workspace.
  - `nodes/`: Custom flow node components.
  - `console/`: Output terminal & execution logs interface.
  - `inspector/`: Node & agent property inspector.
  - `topbar/`: Navigation & toolbar controls.
  - `projects/`: Project list & workspace manager.
  - `settings/`: Platform & agent configuration panel.
- **`docker/`**: Container definitions & docker-compose configurations.
- **`logs/`**: Execution logs & audit records.
- **`artifacts/`**: Generated build artifacts & outputs.

### Package layout

```
engine/                  Python: the loop engine and its API
  pyproject.toml         uv-managed, Python 3.12
  src/loopctl/
    api/                 FastAPI REST + WebSocket for the canvas
    graph/               workflow graph model and executor (LangGraph)
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

Each package's `__init__.py` carries a docstring explaining that package's job,
its constraints, and its owner. Read it before writing into a package.

## Stack

LangGraph drives the executor (`interrupt()` is a human gate; the SQLite
checkpointer is pause/resume). The **Claude Agent SDK** is the execution agent's
harness. The **Messages API** with `messages.parse()` backs the three reasoning
roles, so criteria and clarification requests arrive as validated objects rather
than prose. FastAPI serves REST + WebSocket, and its OpenAPI schema generates the
frontend's TypeScript types — so a Pydantic change breaks the frontend build
instead of silently drifting. The canvas is React + Vite + React Flow.

Full rationale, model choices with current pricing, and the six API rules that
each cost an afternoon if you don't know them: [docs/05](docs/05-tech-stack-and-ownership.md).

## Prerequisites

```bash
cd engine
uv python install 3.12 && uv venv --python 3.12 .venv
uv sync --all-groups
```

Try 3.12 first — it's what the project targets. **If `uv python install 3.12`
or `uv venv --python 3.12` fails with an "Application Control" / "os error
4551" style message**, a Windows security policy on that machine is blocking
uv's own downloaded interpreters (this happened during development; both
uv-managed 3.12 and a pre-existing uv-managed 3.11 were blocked, while the
officially-installed system 3.14 was not). Don't try to work around that
policy — fall back to the trusted interpreter instead:

```bash
cd engine
uv venv --python "<path to your system python.exe>" .venv
uv sync --all-groups
```

Then check `requires-python` in `engine/pyproject.toml` matches the Python you
actually used, and re-run `uv sync --all-groups` to regenerate `uv.lock` for
that version if it doesn't. Verify before trusting it — don't assume a newer
Python "probably" has wheels for everything:

```bash
uv sync --all-groups && .venv/Scripts/python.exe -c "import langgraph, anthropic, claude_agent_sdk, fastapi; print('imports OK')"
```

No `uv`? `pip install -r engine/requirements.txt` into your own venv works too
— that file is generated from `uv.lock`, so it's exact versions, not floors.
See the comment at the top of `requirements.txt` for how to regenerate it.

Also required: **Node.js 20+** (canvas, from M2) and **Docker** (packaging, M7).
Neither is installed yet.

## Who writes what

Two capability tracks, each spanning Python *and* React so both engineers work
full-stack. Every module states its owner in a banner at the bottom of its
docstring; `schemas/` and `config.py` are jointly owned and frozen by agreement.
See [docs/05, Part 5](docs/05-tech-stack-and-ownership.md#part-5--ownership--two-tracks-both-full-stack).

## Status

Scaffolding and design. No implementation yet — see
[docs/03-build-order.md](docs/03-build-order.md) for what to build first.
