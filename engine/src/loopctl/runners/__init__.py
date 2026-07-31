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
"""
