import pytest

from aporia import Claim, EpistemicKind, Interpretation, Resolution, discern


def test_competing_meanings_remain_open():
    a = Interpretation("A", [Claim("evidence A", EpistemicKind.OBSERVED, "log", 0.70)])
    b = Interpretation("B", [Claim("evidence B", EpistemicKind.INFERRED, "analysis", 0.68)])
    decision = discern([a, b])
    assert decision.resolution == Resolution.PROVISIONAL
    assert decision.leading_interpretation == "A"
    assert decision.what_would_resolve


def test_low_evidence_enters_aporia():
    a = Interpretation("A", [Claim("symbolic reading", EpistemicKind.SYMBOLIC, "human", 0.95)])
    decision = discern([a])
    assert decision.resolution == Resolution.APORIA
    assert dict(decision.evidential_weights)["A"] == 0.0


def test_contradiction_blocks_closure_and_is_explained():
    a = Interpretation(
        "A",
        [Claim("strong observation", EpistemicKind.OBSERVED, "log", 0.95)],
        contradicted_by=["counterexample"],
    )
    decision = discern([a])
    assert decision.resolution == Resolution.APORIA
    assert decision.unresolved_contradictions == ("counterexample",)
    assert any("contradictions" in item for item in decision.what_would_resolve)


def test_strong_separated_evidence_can_warrant_closure():
    a = Interpretation("A", [Claim("direct evidence", EpistemicKind.OBSERVED, "log", 0.95)])
    b = Interpretation("B", [Claim("weak inference", EpistemicKind.INFERRED, "analysis", 0.55)])
    decision = discern([a, b])
    assert decision.resolution == Resolution.WARRANTED
    assert dict(decision.evidential_weights)["A"] == 0.95
    assert dict(decision.evidential_weights)["B"] == pytest.approx(0.44)


def test_inference_is_not_silently_equivalent_to_observation():
    observed = Interpretation("observed", [Claim("x", EpistemicKind.OBSERVED, "log", 0.8)])
    inferred = Interpretation("inferred", [Claim("y", EpistemicKind.INFERRED, "analysis", 0.8)])
    decision = discern([observed, inferred])
    weights = dict(decision.evidential_weights)
    assert weights["observed"] == 0.8
    assert weights["inferred"] == pytest.approx(0.64)


def test_weighting_policy_can_be_overridden_explicitly():
    observed = Interpretation("observed", [Claim("x", EpistemicKind.OBSERVED, "log", 0.8)])
    inferred = Interpretation("inferred", [Claim("y", EpistemicKind.INFERRED, "analysis", 0.8)])
    weights = {EpistemicKind.OBSERVED: 1.0, EpistemicKind.INFERRED: 1.0}
    decision = discern([observed, inferred], kind_weights=weights)
    trace = dict(decision.evidential_weights)
    assert trace["observed"] == trace["inferred"] == 0.8


def test_confidence_is_required():
    with pytest.raises(TypeError):
        Claim("evidence", EpistemicKind.OBSERVED, "log")
