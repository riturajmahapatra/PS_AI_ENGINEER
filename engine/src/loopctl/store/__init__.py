"""Persistence. SQLite to start; the interface hides that choice.

Holds workflows, runs, attempts, node states, ledger events, and
human-gate decisions. Runs must survive a process restart -- a control
plane that forgets what it was doing when you redeploy is not a control
plane.

Shares its SQLite file with LangGraph's checkpointer, so a resumed run and its
receipts stay in one place.

------------------------------------------------------------------
TERRITORY   Acceptance & Evidence         OWNER      Role 2
LAYER       engine / Python               REVIEWER   Role 1
------------------------------------------------------------------
"""
