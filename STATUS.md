# Status — ICML 2026 unknown-truncation linear regression

Paper: [arXiv:2602.12534](https://arxiv.org/abs/2602.12534)<br>
OpenReview: `DsV89lJ58l`<br>
Target repository: `MachineLearning-Nerd/icml26-unknown-truncation-linear-regression`

## Current scientific status

**Scoped gate: PASS. Paper-level reproduction: INCONCLUSIVE.**

- The pinned author source protocol is reproduced with `R=10`, `T=4500`, and
  the documented 10-dimensional, five-mixture, five-interval configuration.
- The full algorithm’s mean error is `0.653189`, compared with `9.852682` for
  OLS and `7.170760` for wrong-set PSGD; true-set PSGD is an idealized
  `0.522706` reference.
- Independent positive-only and scalar truncated-likelihood controls pass with
  a deliberately disjoint negative control.
- C1, C2, and C5 are source-audited conditional claims; C3 and C4 are scoped
  finite reproductions; C6 is source-audited only. No universal paper claim is
  independently formalized from first principles.

## Evidence snapshot

- Positive-only symmetric-difference mass: `0.007899`.
- Disjoint-reference negative control: `0.515311`.
- Correct-set likelihood error: `0.007669`; wrong-set error: `0.099420`.
- Full source plot: [`outputs/source_r10.png`](outputs/source_r10.png).
- Pinned author commit: `a14732163158aff75113e3e1c50a90ecc27b4250`.

## Reproduce

See [`docs/SOURCE_MANIFEST.md`](docs/SOURCE_MANIFEST.md), then run the commands
in [`README.md`](README.md). The fail-closed gate writes
[`outputs/publication_gate.json`](outputs/publication_gate.json).

## Cleanup status

- Former name: `icml26-repro-DsV89lJ58l-truncated-regression`.
- Clean name: `icml26-unknown-truncation-linear-regression`.
- Historical branch/commit record: [`BRANCH_AUDIT.md`](BRANCH_AUDIT.md).
- Final public branch policy: `main` only.
- Final reachable commit attribution: `MachineLearning-Nerd`.
- Citation and author thank-you note: [`README.md`](README.md).
