from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class AgentDependencies:
    """Runtime data supplied to the constitution agent."""

    question: str
    context_block: str
