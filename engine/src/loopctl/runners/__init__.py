"""Adapters onto real coding-agent harnesses.

Every adapter satisfies one protocol: given a prompt, a workspace path, a
tool allowlist and a model id, produce a transcript, the set of files
changed, an exit status, and a cost record.

    ClaudeCodeRunner  - Claude Agent SDK / claude CLI
    CursorRunner      - cursor-agent headless
    AiderRunner       - aider --yes
    FakeRunner        - scripted, deterministic, zero tokens

FakeRunner is not a toy. It is how the loop gets tested in CI without
spending money or inheriting model nondeterminism, and it is how you
develop orchestration offline. Build it first, before any real adapter.

Because the protocol is narrow, model / provider / backend are all
configuration, not code -- which is exactly what the brief asks for.

ClaudeCodeRunner wraps the Claude Agent SDK (`claude-agent-sdk`), which is a
different package from the Messages API SDK the agents/ package uses: it ships
the whole Claude Code harness -- Read, Write, Edit, Bash, Glob, Grep, plus the
agent loop and permissions -- so we adapt onto it rather than rebuilding it.

------------------------------------------------------------------
TERRITORY   Generation & Control          OWNER      Role 1
LAYER       engine / Python               REVIEWER   Role 2
------------------------------------------------------------------
"""
