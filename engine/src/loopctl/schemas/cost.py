"""Cost accounting. One shape, filled straight from an API response's
`usage` block or a subprocess's wall-clock -- never estimated, never a
separately-tracked counter that can drift from the ledger. See
docs/01-architecture.md "Where cost is captured" and
docs/05-tech-stack-and-ownership.md Part 2, fact 6."""

from pydantic import BaseModel


class CostRecord(BaseModel):
    model: str | None = None
    input_tokens: int = 0
    output_tokens: int = 0
    cache_read_input_tokens: int = 0
    cache_creation_input_tokens: int = 0
    usd: float = 0.0
    wall_clock_ms: int = 0
