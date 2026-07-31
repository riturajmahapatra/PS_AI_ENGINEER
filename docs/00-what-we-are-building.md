# 00 · What we are building

Read this first. It has no code in it. When you finish it you should be able to
explain the product to someone else in two minutes.

## The problem in one paragraph

Ask a model to write a function and it does fine. Ask it to migrate a module,
add tests to reach 85% coverage, or replace a deprecated dependency across
forty files, and it will do most of the work and then tell you — warmly,
fluently, at length — that it is done. Sometimes it is. You cannot tell which
time this is without running the checks yourself. Writing the code was never
the hard part. **Knowing whether to trust it was.**

## What we build

A platform where an engineer:

1. Points at a repository and states an objective in prose.
2. Gets back a **contract** — a list of measurable success criteria, proposed by
   an agent, which the engineer edits and confirms before anything runs.
3. Watches a bounded loop work the task: plan → implement → validate → learn
   from the failure → plan again.
4. Sees a real verdict backed by real command output, not a model's summary.
5. Approves the diff, or lets the system stop safely and hand back a clean repo
   with an honest report.

The loop is not hardcoded. It is a **graph you edit on a canvas** — add a node,
rewire a failure path, swap the model on one agent, raise the retry budget,
insert a human approval before delivery. Save it, export it as YAML, commit that
YAML, rerun it tomorrow and get the same shape of run.

## The four roles

| Role | Input | Output | May it accept work? |
| --- | --- | --- | --- |
| **Success Criteria** | objective, repo | measurable criteria | no |
| **Planning** | objective, criteria, last failure's evidence | a plan naming real files | no |
| **Execution** | plan | file edits, via a real coding agent | no |
| **Validation** | the changed workspace | pass/fail + evidence | **the deterministic checks do** |

The Validation *node* is the interesting one. It runs commands — build, tests,
lint, types, coverage — and the exit codes decide. A model may attach a
qualitative opinion ("this follows the repo's conventions") but that opinion is
labelled advisory and cannot rescue a failing check.

## Five behaviours that are the actual assignment

Everything else is scaffolding around these. When you are deciding what to cut,
cut anything that is not in service of one of them.

**1. Plan against reality.** The planner reads the repo before planning. A plan
that says "modify `src/services/billing.py:L40-88`, following the pattern in
`src/services/invoicing.py`" is worth something. A plan that says "refactor the
billing logic" is worth nothing. Grounding the planner in actual file contents
is the difference.

**2. Separate generation from acceptance.** Covered above and in doc 02. This is
the single most heavily weighted idea in the brief.

**3. Feed failure forward.** When the tests fail, the next attempt must receive
*the failing test name, the assertion, and the traceback* — not "validation
failed". An attempt that starts from the same information as the last one is not
an iteration, it is a re-roll. The attempt counter must go up and the prompt must
get richer.

**4. Stay bounded; retreat cleanly.** A budget in attempts, wall-clock, and
dollars. When it runs out: roll back the worktree, leave the base repo exactly as
found, write a report that says *undelivered* and explains what was tried. A
half-finished branch left behind is worse than no attempt at all.

**5. Ask instead of guess.** If the objective contradicts itself — "keep the
public API stable" alongside "rename the exported client class" — the correct
behaviour is to stop and emit a structured clarification request naming the two
conflicting requirements. Confidently picking one earns nothing. Build a
deliberately contradictory objective into your demo and show the system catching
it; this is the cheapest point on the scorecard and most teams will skip it.

## What "done" looks like

An engineer opens the canvas, types an objective against a real repo, edits two
of the proposed criteria, hits Run, and watches attempt 1 fail on coverage with
the actual `pytest --cov` output visible in the console. Attempt 2 receives that
output, adds the missing tests, and passes. The engineer clicks the execution
node and sees the transcript, the commands run, and the files changed. They
approve the gate. The run is marked delivered, with a total of 11 model calls,
4 minutes 20 seconds, and $0.38 recorded against it.

Then they export the workflow as YAML, and someone else reruns it.

## What we are deliberately not building

- A chat interface. The canvas is the product.
- Nested graphs, auto-layout, multi-user collaboration, hundreds of node types.
  The brief explicitly excuses all of these.
- Our own agent harness. We adapt onto an existing one (Claude Agent SDK, Cursor
  CLI, Aider) — the brief requires integrating a real runner, not writing one.
- A general-purpose CI system. The checks we ship are the ones our demo repo
  needs, behind an interface that makes adding more trivial.

## Divide the work

Two people, roughly:

- **Engine** — graph executor, node types, workspace isolation, checks, ledger.
  This is the harder half and the half that gets judged.
- **Surface** — React Flow canvas, node inspector, run console, WebSocket
  streaming, YAML export/import.

They meet at the schemas in `engine/src/loopctl/schemas/`. Agree those types on
day one and you can work in parallel without blocking each other. Whoever
finishes first takes the demo repo and the demo script.
