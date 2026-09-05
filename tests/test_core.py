from aporia import Claim, EpistemicKind, Interpretation, Resolution, discern


def test_competing_meanings_remain_open():
    a = Interpretation("A", [Claim("evidence A", EpistemicKind.OBSERVED, "log", 0.70)])
    b = Interpretation("B", [Claim("evidence B", EpistemicKind.INFERRED, "analysis", 0.68)])
    decision = discern([a, b])
    assert decision.resolution == Resolution.PROVISIONAL


def test_low_evidence_enters_aporia():
    a = Interpretation("A", [Claim("symbolic reading", EpistemicKind.SYMBOLIC, "human", 0.95)])
    decision = discern([a])
    assert decision.resolution == Resolution.APORIA


def test_contradiction_blocks_closure():
    a = Interpretation(
        "A",
        [Claim("strong observation", EpistemicKind.OBSERVED, "log", 0.95)],
        contradicted_by=["counterexample"],
    )
    assert discern([a]).resolution == Resolution.APORIA


def test_strong_separated_evidence_can_warrant_provisional_closure():
    a = Interpretation("A", [Claim("direct evidence", EpistemicKind.OBSERVED, "log", 0.95)])
    b = Interpretation("B", [Claim("weak inference", EpistemicKind.INFERRED, "analysis", 0.55)])
    assert discern([a, b]).resolution == Resolution.WARRANTED
