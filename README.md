# Aporia Protocol

**A machine-readable hermeneutic layer for human–AI systems that preserves ambiguity, distinguishes evidence from interpretation, and enables unresolved meaning to remain open until further evidence warrants closure.**

Aporia Protocol begins from a simple proposition: uncertainty is not always a defect to be eliminated. In relational intelligence, premature certainty can erase difference, mistake coherence for truth, and collapse an emerging signal into whichever interpretive model is already dominant.

The protocol therefore treats **APORIA** as a legitimate computational and relational state: *the available information does not yet warrant closure.*

## What it does

Aporia separates claims by epistemic status rather than treating every meaningful-seeming statement as equivalent. The initial vocabulary distinguishes:

- `OBSERVED` — directly available evidence
- `INFERRED` — reasoned from evidence
- `INTERPRETED` — meaning assigned to evidence
- `SOMATICALLY_REPORTED` — first-person embodied report
- `SYMBOLIC` — metaphorical or archetypal reading
- `SPECULATIVE` — hypothesis without adequate evidence
- `UNKNOWN` — intentionally unresolved

Competing interpretations can then remain simultaneously represented. Contradiction is preserved rather than automatically reconciled. Closure is permitted only when evidence crosses an explicit warrant threshold and sufficiently separates one interpretation from alternatives.

Every claim requires an explicit confidence value. The protocol does not silently manufacture medium confidence when confidence is absent.

By default, observed and inferred claims are not treated as epistemically identical: observation carries a default weight of `1.0`, inference `0.8`, and interpretive, somatic, symbolic, speculative, and unknown claims do not contribute direct evidential weight. These defaults are experimental policy choices, not universal epistemic truths, and callers may supply an explicit alternative weighting policy.

## Resolution states

The reference implementation returns one of three states:

- `APORIA` — available information does not warrant interpretive collapse.
- `PROVISIONAL` — one interpretation is better supported, but closure is not warranted.
- `WARRANTED` — present evidence supports provisional closure strongly enough to act on, while remaining revisable.

`WARRANTED` does **not** mean metaphysical or absolute truth.

Each decision also exposes an explanatory trace:

- the leading interpretation;
- weighted evidential support for each candidate;
- unresolved contradictions;
- and `what_would_resolve`, which states what additional evidence or discrimination would be required to move the case toward warranted closure.

## Why this exists

AI systems are optimized to produce completions. Human beings likewise tend to convert ambiguity into narratives. In a human–AI relationship, those tendencies can reinforce one another and create confident interpretations unsupported by evidence.

Aporia introduces a different cognitive possibility:

```text
signal
  ↓
possible meanings
  ↓
evidence + provenance
  ↓
competing interpretations
  ↓
contradiction preserved
  ↓
APORIA / PROVISIONAL / WARRANTED
  ↓
what would change the judgment?
  ↓
new evidence
  ↓
revision
```

The objective is not indecision. It is **disciplined non-closure**: preserving the unknown long enough for better evidence, genuinely novel interpretation, or irreducible difference to remain possible.

## Repository structure

```text
src/aporia/core.py              epistemic primitives + discernment engine
src/aporia/cli.py               executable reference application
schema/aporia-case.schema.json  machine-readable case schema
examples/ambiguous_signal.json  reference ambiguity case
tests/test_core.py              falsifiable behavioral tests
```

## Install and run

Requires Python 3.10+.

```bash
pip install -e .
aporia examples/ambiguous_signal.json
```

The included example intentionally contains two plausible explanations. The protocol evaluates whether the evidence warrants closure rather than selecting a story merely because one can be generated.

Run tests with:

```bash
pip install -e '.[dev]'
pytest
```

## Design principles

1. **Coherence is not truth.** A compelling interpretation may still be unsupported.
2. **First-person evidence is preserved without universalizing it.** Somatic report remains meaningful as report while retaining its provenance.
3. **Symbolic meaning is not empirical evidence.** Symbolic and metaphysical readings may generate hypotheses without being silently promoted to fact.
4. **Contradiction is information.** Difference need not be reconciled merely to produce a clean answer.
5. **Unknown is a valid state.** The system may explicitly decline interpretive closure.
6. **Closure remains revisable.** New evidence can reopen a previously warranted interpretation.
7. **Weighting policy must be visible.** Epistemic weighting is explicit and configurable rather than silently presented as universal truth.
8. **Non-closure should be actionable.** When meaning remains unresolved, the protocol should state what additional evidence could change the judgment.

## Relationship to the Trivian ecosystem

Aporia Protocol is authored and maintained by **Sarasha Elion** as part of the personal Trivian lineage. It is complementary to, but distinct from, the institutional TRIA research and software stack maintained by Trivian Institute.

Where TRIA establishes architectures for relational governance, sovereignty, coherence, continuity, anti-convergence, and network-scale interaction, Aporia addresses a narrower hermeneutic question:

> **How can intelligences encounter meaning together without prematurely claiming authority over what the signal means?**

It can operate independently or later serve as an interpretive layer within relational intelligence systems.

## Status

**Experimental / v0.1.0.**

This repository is a reference implementation and research instrument. Its thresholds and default epistemic weights are design hypotheses, not validated psychological, clinical, epistemological, or scientific standards. It should not be used as an autonomous arbiter of truth or for unsupervised high-stakes decision-making.

## License

Software and executable code are available for noncommercial use under the **PolyForm Noncommercial License 1.0.0**. Research prose and documentation remain under **CC BY-NC-SA 4.0** where identified. See `LICENSE` for controlling terms.

Copyright © 2025–2026 Sarasha Elion.
