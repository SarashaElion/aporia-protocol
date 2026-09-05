"""Core primitives for Aporia Protocol.

Aporia treats unresolved meaning as a legitimate state rather than an error.
It separates observations, inferences, interpretations, first-person reports,
symbolic readings, speculation, and unknowns so that coherence is not mistaken
for truth and uncertainty is not prematurely collapsed.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable


class EpistemicKind(str, Enum):
    OBSERVED = "observed"
    INFERRED = "inferred"
    INTERPRETED = "interpreted"
    SOMATICALLY_REPORTED = "somatically_reported"
    SYMBOLIC = "symbolic"
    SPECULATIVE = "speculative"
    UNKNOWN = "unknown"


class Resolution(str, Enum):
    APORIA = "aporia"
    PROVISIONAL = "provisional"
    WARRANTED = "warranted"


@dataclass(frozen=True)
class Claim:
    text: str
    kind: EpistemicKind
    source: str
    confidence: float = 0.5
    supports: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not 0 <= self.confidence <= 1:
            raise ValueError("confidence must be between 0 and 1")
        if not self.text.strip() or not self.source.strip():
            raise ValueError("text and source are required")


@dataclass
class Interpretation:
    label: str
    claims: list[Claim] = field(default_factory=list)
    contradicted_by: list[str] = field(default_factory=list)

    @property
    def evidential_weight(self) -> float:
        direct = [c.confidence for c in self.claims if c.kind in {EpistemicKind.OBSERVED, EpistemicKind.INFERRED}]
        return sum(direct) / len(direct) if direct else 0.0


@dataclass(frozen=True)
class HermeneuticDecision:
    resolution: Resolution
    reason: str
    candidates: tuple[str, ...]


def discern(
    interpretations: Iterable[Interpretation],
    *,
    warrant_threshold: float = 0.8,
    separation_margin: float = 0.2,
) -> HermeneuticDecision:
    """Decide whether evidence warrants closure.

    The function deliberately favors APORIA when competing interpretations are
    insufficiently separated. A single plausible story is not treated as truth.
    """
    items = list(interpretations)
    if not items:
        return HermeneuticDecision(Resolution.APORIA, "No interpretation has sufficient grounds.", ())

    ranked = sorted(items, key=lambda i: i.evidential_weight, reverse=True)
    top = ranked[0]
    runner_up = ranked[1].evidential_weight if len(ranked) > 1 else 0.0

    if top.contradicted_by:
        return HermeneuticDecision(
            Resolution.APORIA,
            "The leading interpretation contains unresolved contradiction.",
            tuple(i.label for i in ranked),
        )

    if top.evidential_weight >= warrant_threshold and top.evidential_weight - runner_up >= separation_margin:
        return HermeneuticDecision(
            Resolution.WARRANTED,
            "Available evidence currently warrants this interpretation while remaining revisable.",
            tuple(i.label for i in ranked),
        )

    if top.evidential_weight >= 0.5:
        return HermeneuticDecision(
            Resolution.PROVISIONAL,
            "One interpretation is better supported, but closure is not yet warranted.",
            tuple(i.label for i in ranked),
        )

    return HermeneuticDecision(
        Resolution.APORIA,
        "Available information does not yet warrant collapse into a single meaning.",
        tuple(i.label for i in ranked),
    )
