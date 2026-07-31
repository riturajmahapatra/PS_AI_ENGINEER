"""HTTP + WebSocket surface consumed by the React canvas.

REST for CRUD on workflows and runs. WebSocket for the live run console:
the ledger emits events, this layer fans them out to connected clients.

The API owns no orchestration logic. It starts runs, relays human-gate
decisions, and reads the ledger. Business rules live below it.
"""
