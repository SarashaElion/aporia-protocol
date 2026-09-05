"""Core primitives for Aporia Protocol.

Aporia treats unresolved meaning as a legitimate state rather than an error.
It separates observations, inferences, interpretations, first-person reports,
symbolic readings, speculation, and unknowns so that coherence is not mistaken
for truth and uncertainty is not prematurely collapsed.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable, Mapping


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


DEFAULT_KIND_WEIGHTS: dict[EpistemicKind, float] = {
    EpistemicKind.OBSERVED: 1.0,
    EpistemicKind.INFERRED: 0.8,
    EpistemicKind.INTERPRETED: 0.0,
    EpistemicKind.SOMATICALLY_REPORTED: 0.0,
    EpistemicKind.SYMBOLIC: 0.0,
    EpistemicKind.SPECULATIVE: 0.0,
    EpistemicKind.UNKNOWN: 0.0,
}


@dataclass(frozen=True)
class Claim:
    text: str
    kind: EpistemicKind
    source: str
    confidence: float
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

    def evidential_weight(self, kind_weights: Mapping[EpistemicKind, float] | None = None) -> float:
        weights = kind_weights or DEFAULT_KIND_WEIGHTS
        weighted: list[float] = []
        for claim in self.claims:
            kind_weight = float(weights.get(claim.kind, 0.0))
            if kind_weight < 0:
                raise ValueError("epistemic kind weights must be non-negative")
            if kind_weight > 0:
                weighted.append(claim.confidence * kind_weight)
        return sum(weighted) / len(weighted) if weighted else 0.0


@dataclass(frozen=True)
class HermeneuticDecision:
    resolution: Resolution
    reason: str
    candidates: tuple[str, ...]
    leading_interpretation: str | None
    evidential_weights: tuple[tuple[str, float], ...]
    unresolved_contradictions: tuple[str, ...]
    what_would_resolve: tuple[str, ...]


def _resolution_requirements(
    top_weight: float,
    runner_up_weight: float,
    *,
    warrant_threshold: float,
    separation_margin: float,
    contradictions: Iterable[str],
) -> tuple[str, ...]:
    requirements: list[str] = []
    contradictions = tuple(contradictions)
    if contradictions:
        requirements.append("Resolve or account for the listed contradictions with new evidence or a revised interpretation.")
    if top_weight < 0.5:
        requirements.append("Add stronger provenance-bearing observed or inferred evidence before preferring any interpretation.")
    if top_weight < warrant_threshold:
        requirements.append(
            f"Raise the leading interpretation's weighted evidential support to at least {warrant_threshold:.2f}."
        )
    if top_weight - runner_up_weight < separation_margin:
        requirements.append(
            f"Obtain discriminating evidence that separates the leading interpretation from the nearest alternative by at least {separation_margin:.2f}."
        )
    if not requirements:
        requirements.append("Continue monitoring for counterevidence; warranted closure remains revisable.")
    return tuple(requirements)


def discern(
    interpretations: Iterable[Interpretation],
    *,
    warrant_threshold: float = 0.8,
    separation_margin: float = 0.2,
    kind_weights: Mapping[EpistemicKind, float] | None = None,
) -> HermeneuticDecision:
    """Decide whether evidence warrants closure.

    The function deliberately favors APORIA when competing interpretations are
    insufficiently separated. A single plausible story is not treated as truth.
    Default evidence weights distinguish observation from inference, but callers
    may supply their own explicit weighting policy.
    """
    items = list(interpretations)
    if not items:
        return HermeneuticDecision(
            Resolution.APORIA,
            "No interpretation has sufficient grounds.",
            (),
            None,
            (),
            (),
            ("Add at least one explicit interpretation supported by provenance-bearing evidence.",),
        )

    scored = [(item, item.evidential_weight(kind_weights)) for item in items]
    ranked = sorted(scored, key=lambda pair: pair[1], reverse=True)
    top, top_weight = ranked[0]
    runner_up_weight = ranked[1][1] if len(ranked) > 1 else 0.0
    candidate_labels = tuple(item.label for item, _ in ranked)
    weight_trace = tuple((item.label, round(weight, 6)) for item, weight in ranked)
    contradictions = tuple(top.contradicted_by)
    requirements = _resolution_requirements(
        top_weight,
        runner_up_weight,
        warrant_threshold=warrant_threshold,
        separation_margin=separation_margin,
        contradictions=contradictions,
    )

    if contradictions:
        return HermeneuticDecision(
            Resolution.APORIA,
            "The leading interpretation contains unresolved contradiction.",
            candidate_labels,
            top.label,
            weight_trace,
            contradictions,
            requirements,
        )

    if top_weight >= warrant_threshold and top_weight - runner_up_weight >= separation_margin:
        return HermeneuticDecision(
            Resolution.WARRANTED,
            "Available evidence currently warrants this interpretation while remaining revisable.",
            candidate_labels,
            top.label,
            weight_trace,
            (),
            requirements,
        )

    if top_weight >= 0.5:
        return HermeneuticDecision(
            Resolution.PROVISIONAL,
            "One interpretation is better supported, but closure is not yet warranted.",
            candidate_labels,
            top.label,
            weight_trace,
            (),
            requirements,
        )

    return HermeneuticDecision(
        Resolution.APORIA,
        "Available information does not yet warrant collapse into a single meaning.",
        candidate_labels,
        top.label,
        weight_trace,
        (),
        requirements,
    )
