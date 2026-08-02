"""Process-wide settings: model keys, workspace root, artifact root, limits.

Loaded from environment plus an optional .env. Nothing else in the package
reads os.environ directly -- keep that rule and the system stays testable.

Also holds the per-model token rates the ledger multiplies by. Keep them here,
not scattered at call sites, so repricing is a one-line change.

------------------------------------------------------------------
TERRITORY   SHARED -- both roles          OWNER      Role 1 + Role 2
LAYER       engine / Python               REVIEWER   the other one
------------------------------------------------------------------
"""
