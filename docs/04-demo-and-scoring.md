# 04 · Demo and scoring

The brief lists nine things the Track B demo must show, in 5–7 minutes. Treat
this as the acceptance test for the *project*: if a milestone does not move one
of these nine forward, it is not on the critical path.

## The nine beats, mapped

| # | Required beat | Built in | Demo action |
| --- | --- | --- | --- |
| 1 | A coding objective being entered | M6 | Type it into the Input node |
| 2 | Success criteria generated or edited | M4/M5 | Agent proposes; you edit one live |
| 3 | The four-agent loop being configured | M6 | Open the planner node, change its model |
| 4 | Workflow saved or exported | M7 | Click Export, show the YAML |
| 5 | An execution attempt against a repo | M5 | Hit Run; console streams |
| 6 | A real validation result with evidence | M2 | Show the actual `pytest --cov` output |
| 7 | A failed attempt feeding into another iteration | M4 | Attempt 1 fails coverage; show the retry prompt containing the failure |
| 8 | A later success, or safe stop after exhaustion | M4 | Attempt 2 passes → gate → delivered |
| 9 | Agent sessions and file changes inspectable | M6 | Click the execution node: transcript, commands, diff |

## Suggested 6-minute script

**0:00 — The claim.** One sentence: *"Models generate; deterministic checks
accept. Nothing advances on a model's say-so."* Then stop talking and show it.

**0:20 — Objective.** Type the real objective into the canvas against
`examples/target-repo`. State the budget out loud: 4 attempts, $5, 45 minutes.

**0:50 — The contract.** Criteria agent proposes. **Edit one in front of them** —
raise coverage from 80 to 85. This demonstrates hybrid mode and the human
contract gate in one move. Confirm.

**1:30 — Configuration.** Open the planning node in the inspector; show model,
tools, retry limit, failure path. Change the model. Point out the tool allowlist:
*"the planner physically cannot write files."*

**2:00 — Run.** Console streams. Planning names real files. Execution edits.

**3:00 — The failure. This is your best 45 seconds.** Attempt 1 fails coverage at
71%. Show the raw command output, not a summary. Then open the attempt-2 planning
prompt and show the uncovered line ranges embedded in it. Say: *"attempt 2 is not
a re-roll — it starts from evidence attempt 1 did not have."*

**3:45 — Success.** Attempt 2 passes. Every check green with its evidence
attached.

**4:15 — The gate.** Human approval with the diff. Approve. Delivered. Show the
receipt: 11 model calls, 4m20s, $0.38.

**4:45 — Inspection.** Click nodes: agent input, output, commands, files changed,
validation results, retry reason.

**5:10 — Two things they will not have seen elsewhere.**
- *Safe stop:* rerun with `max_attempts: 1`. It fails, rolls back, writes an
  honest undelivered report. `git status` on the base repo: clean.
- *Clarification:* paste the self-contradictory objective. The system halts and
  emits a structured question instead of guessing.

**5:50 — Config as code.** Export the YAML. Show it in the repo. *"Rerun it
tomorrow and get the same shape of run."*

## Questions you will be asked

Have an answer ready. These are the obvious probes for this brief.

**"How do I know a model can't override your checks?"**
Open `tests/test_acceptance_is_deterministic.py`. Show the AST import guard and
the twice-run byte-identical assertion. This is the single best answer in your
project — make sure you can find the file in three seconds.

**"What if the model just claims the tests pass?"**
It cannot — the validator node runs the subprocess itself and reads the exit
code. The agent transcript is evidence, never input to the verdict.

**"Why a graph executor instead of a hardcoded state machine?"**
Because the brief requires a configurable template. Demonstrate: rewire the
failure edge on the canvas to go straight to a human gate instead of back to
planning, and rerun. If you cannot do that live, your loop is hardcoded.

**"What did this cost?"**
Point at the ledger. Per run, per attempt, per node.

**"Show me it not working."**
Have the safe-stop run ready to go. Wanting to see the failure path is a good
sign — it means they believe the success path.

## Judgement calls worth defending out loud

Say these before you are asked; volunteering a limitation reads as engineering
maturity, while being caught by it reads as an oversight.

- **We allow LLM-as-judge, but never blocking by default.** Advisory, rubric-
  backed, structured evidence. If a user makes one blocking, the run is stamped
  `llm_gated` and the report says so. We made it legible rather than banning it.
- **Worktrees, not containers.** Isolation sufficient for the threat model
  (accidental damage, not hostile code), with far less operational weight.
  Containers are the next step, and the interface is ready for them.
- **`FakeRunner` in CI, real runners in the demo.** Our own test suite must be
  deterministic and free. A CI pipeline whose results depend on a model's mood
  is not a CI pipeline.
- **SQLite, not Postgres.** Single-node control plane. The store interface hides
  it; swapping is a day's work when there is a second node to justify it.
