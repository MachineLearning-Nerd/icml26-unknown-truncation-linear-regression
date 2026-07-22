# Primary-source claim map

Primary source: arXiv `2602.12534` source snapshot, `main.tex`.  This is a
source audit, not a numerical claim verdict.

| Anchored claim | Primary-source anchor | Reproduction evidence still required |
| --- | --- | --- |
| C1 — polynomial-time unknown-truncation regression beyond Gaussian features | Theorem 3.1 (informal statement, lines 128–139) and formal Theorem 3.1 / `thm:main` (lines 369–393) | Verify the released Phase-I/Phase-II implementation on the paper's full synthetic protocol and independently check its mechanisms. |
| C2 — assumptions | Survival probability, sub-Gaussianity/boundedness, and observed-covariance identifiability assumptions (lines 102–126) | Read the source configuration and simulated distribution against these conditions. |
| C3 — positive-only union-of-interval learning | Contribution text (lines 36–38); the positive-only setup and smooth reference construction (lines 691–723) | Independent gap-counting recovery plus a deliberately shifted-reference negative control. |
| C4 — Phase-II PSGD | Algorithm overview explicitly describes learn-set then optimize phases (lines 171–185) | Full unmodified source R=10 run, then an independent scalar truncated-likelihood gradient control. |
| C5 — sub-Gaussian smoothness | Lemma 3.4 / `lem:smoothness` (lines 705–723) | Numeric control checks the conditional-normal quantities used by the independent Phase-I/II controls. |
| C6 — improvement over LMZ24a | Related-work comparison (lines 90–101, 278–280) and Gaussian-case comparison (lines 963–965) | Source-level comparison only; no runtime benchmark can prove an asymptotic claim. |

The paper's own simulation specification is a 10-dimensional mixture of five
Gaussians with a five-interval survival set (lines 803–805). The pinned author
configuration uses that setup and its documented ten outer repetitions.
