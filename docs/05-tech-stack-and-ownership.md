# 05 · Tech stack and ownership

Two halves: **what we build with**, and **who writes which file**. Read both —
the ownership split only makes sense once you know what the pieces are.

---

# Part 1 · The stack

| Layer | Choice | Why this and not the obvious alternative |
| --- | --- | --- |
| Engine language | **Python 3.12** | Where the agent ecosystem lives. **Not 3.14** — see the warning below. |
| Package manager | **uv** | Already installed. Fast, lockfile-first, manages the interpreter too. |
| Graph executor | **LangGraph** | `interrupt()` is exactly a human gate; the SQLite checkpointer is exactly pause/resume. Both are things we'd otherwise hand-roll, and one is a listed bonus capability. |
| Reasoning agents | **Anthropic SDK — Messages API** | Criteria, Planning, and the advisory judge need *schema-valid structured output*, not filesystem access. `messages.parse()` gives that by construction. |
| Execution agent | **Claude Agent SDK** (`claude-agent-sdk`) | The brief requires a real coding-agent harness with file + shell capability. This *is* one — Read/Write/Edit/Bash/Glob/Grep, the agent loop, permissions, transcripts. We adapt onto it; we don't rebuild it. |
| Contracts | **Pydantic v2** | One class is simultaneously the API schema, the OpenAPI source, and the model's `output_format`. |
| API | **FastAPI + uvicorn** | REST + WebSocket in one process; auto-generates the OpenAPI the frontend types are built from. |
| Persistence | **SQLite** | Single-node control plane. Same file as the LangGraph checkpointer, so a resumed run and its receipts live together. |
| Our own quality bar | **pytest, ruff, mypy** | We ship a tool that enforces deterministic acceptance. Failing to run our own checks would be embarrassing. |
| Canvas | **React + Vite + TypeScript + React Flow** (`@xyflow/react`) | React Flow is the node-graph library the Rivet-style canvas needs. |
| Frontend state | **Zustand** (client) + **TanStack Query** (server) | Graph edits are client state; runs are server state. Don't conflate them. |
| UI kit | **Tailwind + shadcn/ui** | The inspector and console are dense forms and log views. Don't hand-roll them. |
| Type bridge | **openapi-typescript** | Generates TS types from FastAPI's OpenAPI. Change a Pydantic model, the frontend stops compiling. |
| Packaging | **Docker Compose** | `docker compose up` → engine + web. One command for the demo. |

### ⚠️ Do not build on Python 3.14

You have 3.14.6 installed. LangGraph, LangChain, and much of the scientific
stack won't have wheels for it yet — you will spend a day fighting C
extensions that have nothing to do with this project. Pin 3.12:

```bash
uv python install 3.12 && uv venv --python 3.12
```

`uv` manages the interpreter, so this doesn't touch your system Python.

### The type chain — set this up at M0 and never think about it again

```
Pydantic model  →  FastAPI OpenAPI  →  openapi-typescript  →  React props
      ↑
      └── also the model's output_format
```

One definition, four consumers. This is why `schemas/` is jointly owned and
frozen early: it is the single point where a careless edit breaks the other
person's build. That's a feature — silent drift is the alternative.

---

# Part 2 · Models, and the API rules that will bite you

| Role | Model | $/MTok in → out | Why |
| --- | --- | --- | --- |
| Success Criteria | `claude-opus-5` | $5 → $25 | Reads the repo, writes the contract. Getting this wrong poisons the whole run. |
| Planning | `claude-opus-5` | $5 → $25 | Must turn failure evidence into a targeted next attempt. The hardest reasoning in the loop. |
| Execution | `claude-sonnet-5` | $3 → $15 (intro $2 → $10 through 2026-08-31) | Highest token volume by far. Near-Opus quality on coding. |
| Advisory judge | `claude-opus-5` | $5 → $25 | Runs once per attempt, non-blocking. Cheap in aggregate. |
| Cheap labelling | `claude-haiku-4-5` | $1 → $5 | Only if you find a genuine use. Don't reach for it reflexively. |

Model IDs are complete as written — **never append a date suffix**.

### Six API facts that will cost you an afternoon each if you don't know them

1. **Thinking is ON by default on Opus 5.** Omitting the `thinking` parameter
   runs adaptive thinking. And `max_tokens` caps thinking *plus* response text
   together — so a tight `max_tokens` truncates mid-answer. Size generously
   (start at 64000 for the planner).
2. **`temperature`, `top_p`, `top_k` return 400** on Opus 5 and Sonnet 5. Steer
   with prompting. If you wanted determinism, note it was never guaranteed anyway.
3. **Assistant prefill returns 400.** The old "force JSON by prefilling `{`"
   trick is gone. Use structured outputs — which we want regardless.
4. **`effort` lives inside `output_config`**, not top-level:
   `output_config={"effort": "xhigh"}`. Start at `xhigh` for the coding and
   planning agents, then sweep down — `low` and `medium` are unusually strong
   on these models and are your main cost lever.
5. **Structured output is `client.messages.parse()`**, and the result is on
   `.parsed_output`. This is how `SuccessCriterion` and `ClarificationRequest`
   arrive as validated objects instead of prose you regex:

   ```python
   response = client.messages.parse(
       model="claude-opus-5",
       max_tokens=16000,
       output_format=CriteriaProposal,   # a Pydantic model from schemas/
       messages=[{"role": "user", "content": prompt}],
   )
   proposal = response.parsed_output     # CriteriaProposal, already validated
   ```

6. **Cost comes off `response.usage`** — `input_tokens`, `output_tokens`,
   `cache_read_input_tokens`, `cache_creation_input_tokens`. Multiply by the
   rates in `config.py`. Never estimate, never count tokens client-side.

**Prompt caching is your cost lever.** The repo context you feed the planner is
large and identical across attempts — cache it. Minimum cacheable prefix is 512
tokens on Opus 5. Verify with `usage.cache_read_input_tokens`; if it's zero
across attempts, something volatile (a timestamp, an unsorted dict) is at the
front of your prompt.

---

# Part 3 · Agent SDK vs Messages API — the split that matters

These are **two different packages**, and choosing wrong for a role costs you
either capability or control:

| | Claude Agent SDK | Messages API |
| --- | --- | --- |
| Package | `claude-agent-sdk` | `anthropic` |
| Gives you | The whole Claude Code harness — built-in Read/Write/Edit/Bash/Glob/Grep, the agent loop, context management, permissions | One request, one response (plus your own tools if you define them) |
| Use for | **Execution** — it needs to read, edit, and run things across a repo | **Criteria, Planning, Judge** — they need a validated object back, not filesystem access |
| Why not the other one | Overkill and unsteerable for "give me a list of criteria" | You'd be rebuilding a coding agent by hand, which the brief explicitly says not to do |

The planner is worth dwelling on. It gets read-only tools — and that's
*enforced*, not requested in the prompt. A planner that can write files is an
execution agent wearing a hat, and you've lost the separation the whole design
rests on.

---

# Part 4 · Where your existing skills actually fit

Honest answers, because forcing a technology in because you know it is how
projects get worse.

**LangGraph — core.** Load-bearing, and you'll learn it properly. The one
non-obvious part: our graph is defined by *user-edited YAML*, not by Python
decorators. So you compile YAML → `StateGraph` at load time, building nodes as
closures and `add_conditional_edges` from the `when:` expressions. Less
idiomatic than the tutorials, and exactly the right use of the library.

**LangChain — barely.** LangGraph pulls in `langchain-core`, but you won't
write chains. Calling the Anthropic SDK directly is clearer and gives you the
`usage` object you need for the ledger. Don't add `langchain` to please a
checklist.

**RAG and vector DBs (Chroma / pgvector) — not on the critical path, and I'd
rather you heard that from me than discovered it at 2am.** For a demo repo,
ripgrep plus targeted file reads beats embeddings on both precision and
latency, and the Agent SDK already does that natively.

There is exactly one place a vector store earns its keep here, and it's a good
one: **cross-run failure memory.** Embed the failure evidence from every
attempt of every run. When the planner starts attempt *N*, retrieve the
*k* most similar past failures and include them: *"three runs ago, a coverage
failure on this module was caused by an untested exception path."* That is
retrieval doing something ripgrep genuinely cannot, it improves with use, and
it demos well.

Build it at M7 as an optional node. Two hard rules: it informs the **planner**
only, and it never touches `checks/` — retrieved context must not be able to
influence a verdict.

---

# Part 5 · Ownership — two tracks, both full-stack

You both asked to learn both halves, so the split is **not** backend/frontend.
It's two capability verticals, each running from Python through to React.

## Track A — Generation & Control (Role 1)

*"What runs, and how the engineer configures it."*

| Engine (Python) | Surface (React) |
| --- | --- |
| `graph/` — LangGraph executor, YAML → StateGraph | Canvas, node rendering, edge wiring |
| `nodes/` — the eight node types | Node library panel |
| `agents/` — the four roles and their prompts | Node inspector (per-type settings) |
| `runners/` — Agent SDK, Cursor, Aider, Fake | Top bar: run / pause / stop, attempt counter |

You will own the loop's behaviour and the surface that configures it. You'll
learn LangGraph, structured outputs, prompt design, and React Flow.

## Track B — Acceptance & Evidence (Role 2)

*"What actually happened, and whether it's acceptable."*

| Engine (Python) | Surface (React) |
| --- | --- |
| `checks/` — deterministic acceptance + parsers | Run console (streamed events) |
| `workspace/` — worktrees, diffs, rollback | Evidence viewer (raw check output, diffs) |
| `ledger/` — append-only receipts, cost | Cost and timing panel |
| `store/` + `api/` — persistence, REST, WebSocket | Node drill-down: click a node, see its execution |

You will own the half that makes the system trustworthy. You'll learn
subprocess orchestration, git plumbing, determinism, WebSocket streaming, and
data-dense UI.

## Shared, and frozen by agreement

`schemas/`, `config.py`, `loopctl/__init__.py`, `examples/workflows/*.yaml`,
`infra/`. Both names on them. **Neither of you edits these alone** — they're
the seam, and a unilateral change breaks the other person's build.

## Cross-training rules (this is the point)

1. **Review every PR** in the other track. Not a rubber stamp — if you can't
   explain what it does, ask before approving.
2. **At M5, swap one thing.** Role 1 writes one deterministic check
   (`api_compat` is a good one). Role 2 writes one agent prompt (the
   clarification detector). Small, real, and it means neither of you is blind
   in half the codebase.
3. **Whoever finishes a milestone first takes the demo script.** Rotate it.

## Per-milestone split

Milestone numbering follows [doc 03](03-build-order.md).

| Milestone | Role 1 (Generation & Control) | Role 2 (Acceptance & Evidence) |
| --- | --- | --- |
| **M0** Skeleton | Executor, node registry, CLI | **Together: write `schemas/` first, then freeze it** |
| **M1** Target repo | Write the two objectives (one contradictory) | Stand up the repo, record the baseline |
| **M2** Acceptance | Scaffold the React app + type generation | `checks/`, parsers, the two determinism tests |
| **M3** Isolation | `agents/` prompt templates | `workspace/` worktrees + the rollback test |
| **M4** Headless loop | `FakeRunner`, all 8 nodes, feedback threading | `ledger/`, budget enforcement, safe-stop report |
| **M5** Real runners | Agent SDK + a second adapter, tool allowlists | `api/` REST + WebSocket, `store/` — **swap task here** |
| **M6** Canvas | Canvas, node library, inspector, top bar | Run console, evidence viewer, node drill-down |
| **M7** Polish | YAML round-trip test, optional failure-memory RAG | Docker Compose, run report, ADRs |

Notice M2 and M3: Role 1 is on the frontend while Role 2 is deep in Python,
then they swap. That's deliberate — it's the fastest way for both of you to
touch both stacks without blocking each other.
