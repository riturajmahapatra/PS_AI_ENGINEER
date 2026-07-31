"""Process-wide settings: model keys, workspace root, artifact root, limits.

Loaded from environment plus an optional .env. Nothing else in the package
reads os.environ directly -- keep that rule and the system stays testable.
"""
