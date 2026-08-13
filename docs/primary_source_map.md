# Primary-source claim map

Primary source: arXiv `2602.12534`, source snapshot `main.tex`. This is a
source audit plus a producer map, not a foundational theorem proof.

| Claim | Primary-source anchor | Local producer | Evidence | Assessment |
| --- | --- | --- | --- | --- |
| C1 — polynomial-time unknown-truncation regression | Theorem 3.1, informal statement (lines 128–139) and formal `thm:main` (lines 369–393) | Pinned `upstream/main.py`; source pin checks in `repro/src/run_publication_gate.py` | `outputs/source_r10.png`, Trackio source log | Source-audited conditional; finite protocol reproduced |
| C2 — assumptions | Survival probability, sub-Gaussianity/boundedness, and observed-covariance identifiability (lines 102–126) | `upstream/config.yaml` plus this source audit | 10D five-component Gaussian mixture and five-interval survival set | Source-audited conditional |
| C3 — positive-only Phase I | Contribution text (lines 36–38); positive-only setup and smooth reference construction (lines 691–723) | Independent `positive_only_intervals` in `repro/src/verify_mechanisms.py` | `outputs/independent_mechanisms.json`: `0.007899` matched error vs `0.515311` disjoint control | Reproduced scoped |
| C4 — Phase II PSGD | Algorithm overview, learn-set then optimize phases (lines 171–185) | Pinned source `main.py`; independent `likelihood_gradient_control` | Full source mean error `0.653189`; correct-set scalar error `0.007669` vs wrong-set `0.099420` | Reproduced scoped |
| C5 — sub-Gaussian smoothness | Lemma 3.4 / `lem:smoothness` (lines 705–723) | `conditional_normal_mean` and likelihood control in `verify_mechanisms.py` | Conditional-normal calculations and source anchor | Source-audited conditional |
| C6 — improvement over LMZ24a | Related work (lines 90–101, 278–280) and Gaussian-case comparison (lines 963–965) | Textual source audit only | Claim manifest in `outputs/publication_gate.json` | Source-audited only; no timing claim |

## Configuration boundary

The paper’s simulation uses a 10-dimensional mixture of five Gaussians with a
five-interval survival set (source lines 803–805). The pinned author config is
the authoritative finite reproduction protocol. The current arXiv page is v2,
whereas the pinned author README links to the v1 URL; this repository does not
silently treat those as identical source snapshots.

## Independent-control boundary

The independent producer imports no symbols from `upstream`. It checks the
mechanisms with scalar normal identities and a fresh positive-only gap learner.
Those checks support the mechanism path and negative-control behavior; they do
not establish the paper’s arbitrary sub-Gaussian theorem or asymptotic runtime.
