"""HTTP + WebSocket surface consumed by the React canvas.

REST for CRUD on workflows and runs. WebSocket for the live run console:
the ledger emits events, this layer fans them out to connected clients.

The API owns no orchestration logic. It starts runs, relays human-gate
decisions, and reads the ledger. Business rules live below it.

FastAPI generates OpenAPI from the pydantic models in schemas/, and the web
build turns that into TypeScript. Change a schema and the frontend stops
compiling -- which is the point.

------------------------------------------------------------------
TERRITORY   Acceptance & Evidence         OWNER      Role 2
LAYER       engine / Python               REVIEWER   Role 1
------------------------------------------------------------------
"""
