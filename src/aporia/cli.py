"""Small executable reference application for Aporia Protocol."""

import argparse
import json

from .core import Claim, EpistemicKind, Interpretation, discern


def evaluate(payload: dict) -> dict:
    interpretations = []
    for item in payload.get("interpretations", []):
        claims = [
            Claim(
                text=c["text"],
                kind=EpistemicKind(c["kind"]),
                source=c["source"],
                confidence=float(c["confidence"]),
                supports=tuple(c.get("supports", [])),
            )
            for c in item.get("claims", [])
        ]
        interpretations.append(
            Interpretation(
                label=item["label"],
                claims=claims,
                contradicted_by=list(item.get("contradicted_by", [])),
            )
        )
    decision = discern(interpretations)
    return {
        "resolution": decision.resolution.value,
        "reason": decision.reason,
        "candidates": list(decision.candidates),
        "leading_interpretation": decision.leading_interpretation,
        "evidential_weights": dict(decision.evidential_weights),
        "unresolved_contradictions": list(decision.unresolved_contradictions),
        "what_would_resolve": list(decision.what_would_resolve),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate whether meaning warrants closure or should remain in aporia.")
    parser.add_argument("input", help="Path to a JSON hermeneutic case")
    args = parser.parse_args()
    with open(args.input, "r", encoding="utf-8") as handle:
        print(json.dumps(evaluate(json.load(handle)), indent=2))


if __name__ == "__main__":
    main()
