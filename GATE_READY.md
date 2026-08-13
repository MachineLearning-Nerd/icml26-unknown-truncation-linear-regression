# Publication gate readiness

**Paper:** arXiv:2602.12534 (`DsV89lJ58l`)<br>
**Repository target:** `MachineLearning-Nerd/icml26-unknown-truncation-linear-regression`<br>
**Overall paper-level status:** `INCONCLUSIVE`<br>
**Scoped documentation gate:** `PASS`

## Claim disposition

| Claim | Disposition | Confidence | Evidence |
| --- | --- | --- | --- |
| C1 | `SOURCE_AUDITED_CONDITIONAL` | Medium | Theorem 3.1 source anchor plus pinned full source protocol |
| C2 | `SOURCE_AUDITED_CONDITIONAL` | Medium | Assumption audit against the 10D mixture/configuration |
| C3 | `REPRODUCED_SCOPED` | Medium | Independent positive-only learner and disjoint-reference control |
| C4 | `REPRODUCED_SCOPED` | Medium/High | Unmodified author `R=10` run plus independent scalar likelihood control |
| C5 | `SOURCE_AUDITED_CONDITIONAL` | Medium | Lemma 3.4 source anchor and conditional-normal calculations |
| C6 | `SOURCE_AUDITED_ONLY` | Low | Related-work/source comparison; no asymptotic timing claim |

The finite gate passes, but `paper_claims_verified` is `0`: no universal paper
theorem is independently formalized here. The source code is pinned to commit
`a14732163158aff75113e3e1c50a90ecc27b4250`.

## Fixed command

See [`docs/SOURCE_MANIFEST.md`](docs/SOURCE_MANIFEST.md) and run the source
protocol, independent controls, tests, and gate described in [`README.md`](README.md).

The machine-readable result is [`outputs/publication_gate.json`](outputs/publication_gate.json).
The full producer map is [`docs/primary_source_map.md`](docs/primary_source_map.md).
