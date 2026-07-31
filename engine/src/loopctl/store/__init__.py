"""Persistence. SQLite to start; the interface hides that choice.

Holds workflows, runs, attempts, node states, ledger events, and
human-gate decisions. Runs must survive a process restart -- a control
plane that forgets what it was doing when you redeploy is not a control
plane.
"""
