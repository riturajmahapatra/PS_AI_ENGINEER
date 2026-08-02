"""Receipts. Append-only, per run.

Every event carries: timestamp, run id, attempt number, node id, actor
(agent | check | human | system), event type, payload, duration, and cost
(input tokens, output tokens, model, dollars).

Written as JSONL so it is greppable and diffable, mirrored into the store
for querying, and streamed over WebSocket for the live console. When
someone asks "why did this run pass?", this file is the answer.

Append-only is enforced by shape: there is a write path and no update or
delete path.

Cost comes straight off the API response -- `usage.input_tokens`,
`output_tokens`, `cache_read_input_tokens`, `cache_creation_input_tokens` --
multiplied by the per-model rates in config. Never estimate; never keep a
running counter that can drift from the ledger.

------------------------------------------------------------------
TERRITORY   Acceptance & Evidence         OWNER      Role 2
LAYER       engine / Python               REVIEWER   Role 1
------------------------------------------------------------------
"""
