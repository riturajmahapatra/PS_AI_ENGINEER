"""Isolation and rollback. The reason a failed run cannot hurt you.

Each attempt gets its own git worktree cut from the base commit. The agent
edits only inside it. On success the branch is kept and surfaced as a diff;
on a safe stop the worktree is removed and the base repo is left exactly as
found.

"Leave the workspace green" is not a best-effort promise here -- it is
structural, because the agent never had write access to the base checkout
in the first place.
"""
