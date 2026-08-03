# Contributing

One rule, because we've hit the cost of skipping it three times in one week:

## Never push directly to `main`. Always branch, then open a PR.

Every direct push to `main` so far has collided with work already in flight on
a PR — a README rewritten out from under a merge, a `requirements.txt` that
duplicated one already being built properly elsewhere, a `pyproject.toml`
edited on both sides at once. None of these were mistakes exactly — they were
two people moving fast without a shared signal for "this is in progress." A
branch + PR *is* that signal.

```bash
git checkout -b your-branch-name main
# ... make changes ...
git push -u origin your-branch-name
gh pr create --base main --head your-branch-name
```

Small changes still get a PR — a one-line fix takes thirty extra seconds this
way and costs nothing. What it buys: the other person sees it's happening
before it lands, instead of discovering it in a merge conflict.

## Before you branch, pull `main`

```bash
git fetch origin && git checkout -b your-branch-name origin/main
```

Every collision so far happened because a branch was cut from a `main` that
had already moved. Branching from `origin/main` explicitly, not a stale local
`main`, avoids the easy version of this mistake.

## If you're about to touch a file the other person is likely mid-edit on

Say so first — even just a one-line heads-up. `schemas/`, `config.py`, the
workflow YAML, and anything at the repo root (`pyproject.toml`,
`requirements.txt`) are the highest-collision files; see
[docs/05, Part 5](docs/05-tech-stack-and-ownership.md#part-5--ownership--two-tracks-both-full-stack)
for the fuller ownership breakdown.

## Enforcing this technically (not yet set up)

GitHub can reject direct pushes to `main` outright via branch protection —
Settings → Branches → Add rule → require a pull request before merging. This
needs repo **admin**, which the account driving these PRs doesn't have (only
`push`). Whoever owns the repo can turn it on in about thirty seconds; until
then this document is the only enforcement, so it only works if both of you
actually follow it.
