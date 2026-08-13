# ICML 2026 — Unknown-Truncation Linear Regression

Independent reproduction and evidence audit for **“Linear Regression with Unknown Truncation Beyond Gaussian Features.”**

> **Current assessment: SCOPED GATE PASS; paper-level status INCONCLUSIVE.**
> The released CPU experiment is reproduced at its documented `R=10`, `T=4500`
> setting, and the positive-only and truncated-likelihood mechanisms have
> independent controls. This repository does not claim to re-prove the paper’s
> asymptotic theorem or its general sub-Gaussian guarantees.

## Paper

- **Authors:** Alexandros Kouridakis, Anay Mehrotra, Alkis Kalavasis, and Constantine Caramanis
- **Paper:** [arXiv:2602.12534](https://arxiv.org/abs/2602.12534) (current page: v2)
- **OpenReview record:** [DsV89lJ58l](https://openreview.net/forum?id=DsV89lJ58l)
- **Venue:** ICML 2026
- **Official code audited:** [`alexkouridakis/truncated-regression`](https://github.com/alexkouridakis/truncated-regression)
- **Pinned author commit:** `a14732163158aff75113e3e1c50a90ecc27b4250`
- **Suggested clean repository name:** `icml26-unknown-truncation-linear-regression`
- **Former repository name:** `icml26-repro-DsV89lJ58l-truncated-regression`

The paper studies linear regression when samples are observed only if the
response lies in an unknown survival set. Its released algorithm first learns a
union of intervals from positive examples, then applies projected stochastic
gradient descent (PSGD) to a truncated-likelihood objective.

## Claim-to-evidence ledger

| Claim | Paper result | Producer and evidence path | Current assessment | Boundary |
| --- | --- | --- | --- | --- |
| **C1 — Theorem 3.1** | Polynomial-time regression with unknown truncation beyond Gaussian features | [`docs/primary_source_map.md`](docs/primary_source_map.md) audits the theorem; pinned [`upstream/main.py`](https://github.com/alexkouridakis/truncated-regression/blob/a14732163158aff75113e3e1c50a90ecc27b4250/main.py) runs the documented synthetic protocol | **SOURCE_AUDITED_CONDITIONAL · MEDIUM** | The theorem is source-audited and its finite protocol is preserved; no independent proof of the universal runtime/accuracy theorem is claimed. |
| **C2 — assumptions** | Known survival-mass, sub-Gaussian/bounded-feature, and observed-covariance identifiability conditions | [`docs/primary_source_map.md`](docs/primary_source_map.md) maps assumptions to `upstream/config.yaml`; the source uses a 10D Gaussian mixture, identity covariance, and a five-interval survival set | **SOURCE_AUDITED_CONDITIONAL · MEDIUM** | One finite configuration cannot establish the full assumption class. |
| **C3 — Phase I** | Positive-only learning recovers a bounded union of survival intervals | [`repro/src/verify_mechanisms.py`](repro/src/verify_mechanisms.py) implements an independent gap-counting learner; `outputs/independent_mechanisms.json` records matched and disjoint-reference controls | **REPRODUCED_SCOPED · MEDIUM** | The scalar control supports the mechanism, not the full high-dimensional positive-only guarantee. |
| **C4 — Phase II PSGD** | Learned survival set followed by truncated-likelihood PSGD estimates `w*` | The unmodified author run in [`docs/SOURCE_MANIFEST.md`](docs/SOURCE_MANIFEST.md) produces [`outputs/source_r10.png`](outputs/source_r10.png) and the captured Trackio log; the independent scalar likelihood control is in `verify_mechanisms.py` | **REPRODUCED_SCOPED · MEDIUM/HIGH** | The documented 10D finite protocol is reproduced; this does not prove convergence for every allowed distribution. |
| **C5 — Lemma 3.4** | Smoothness/control of truncated-normal conditional quantities | [`docs/primary_source_map.md`](docs/primary_source_map.md) audits the lemma; `verify_mechanisms.py` exercises conditional-normal means in the scalar control | **SOURCE_AUDITED_CONDITIONAL · MEDIUM** | Numerical agreement is not a proof of the general smoothness lemma. |
| **C6 — comparison with prior work** | Improvement over prior Gaussian-feature runtime dependence | [`docs/primary_source_map.md`](docs/primary_source_map.md) records the related-work and Gaussian-case anchors | **SOURCE_AUDITED_ONLY · LOW** | This is an asymptotic/source comparison; no timing benchmark can establish the complexity separation. |

### What the labels mean

`SOURCE_AUDITED_CONDITIONAL` means the primary text, assumptions, or equation
anchor was checked and the finite implementation is consistent with the stated
protocol. `REPRODUCED_SCOPED` means a finite mechanism or experiment was
independently rerun with committed evidence and controls. `SOURCE_AUDITED_ONLY`
means that the evidence is textual/asymptotic and no independent numerical claim
is made. None of these labels is a foundational proof of a universal theorem.

## Results

### Pinned author protocol (`R=10`, `T=4500`)

The unmodified author implementation reports mean final parameter error:

| Method | Mean error |
| --- | ---: |
| OLS (no correction) | `9.852682` |
| PSGD with wrong survival set | `7.170760` |
| PSGD with true survival set (idealized reference) | `0.522706` |
| Full algorithm | `0.653189` |

The full source plot is [`outputs/source_r10.png`](outputs/source_r10.png). The
captured command, output, and environment are retained in the local Trackio
logbook; the ignored `upstream/` checkout is recreated from the pinned commit
using the source manifest.

### Independent mechanism controls

- Positive-only interval recovery: symmetric-difference mass `0.007899`.
- Deliberately disjoint reference negative control: mass `0.515311`.
- Correct-set scalar truncated-likelihood error: `0.007669`.
- Wrong-set control error: `0.099420`.

The first weaker shifted-reference control is retained as a failed control
design; it is not used as evidence. The corrected disjoint control is the one
credited by the gate.

## How each claim is produced

```text
arXiv/source audit ── docs/primary_source_map.md
        │
        ├── upstream/main.py + upstream/config.yaml
        │       └── R=10 source protocol ── source_r10.png + Trackio log
        │
        └── repro/src/verify_mechanisms.py
                ├── C3 positive-only gap-counting control
                ├── C4/C5 scalar truncated-normal likelihood control
                └── outputs/independent_mechanisms.json

repro/src/run_publication_gate.py
        └── source pin + output checks + pytest + claim manifest
                └── outputs/publication_gate.json
```

## Reproduce

The public repository intentionally ignores the author checkout and virtual
environment. Recreate them first:

```bash
git clone https://github.com/alexkouridakis/truncated-regression.git upstream
git -C upstream checkout --detach a14732163158aff75113e3e1c50a90ecc27b4250
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -r repro/requirements-cpu.txt
```

Run the source protocol, independent checks, tests, and fail-closed gate:

```bash
env MPLBACKEND=Agg OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  .venv/bin/python upstream/main.py --config upstream/config.yaml --R 10 \
  --output-plot outputs/source_r10.png

PYTHONPATH=. .venv/bin/python repro/src/verify_mechanisms.py \
  --output outputs/independent_mechanisms.json
PYTHONPATH=. .venv/bin/python -m pytest -q repro/tests
.venv/bin/python repro/src/run_publication_gate.py
```

The gate writes [`outputs/publication_gate.json`](outputs/publication_gate.json).
It is a documentation/evidence gate; `paper_claims_verified` is zero because
the universal theorem and asymptotic comparison are not independently
formalized here.

## Repository contents

| Path | Purpose |
| --- | --- |
| [`docs/SOURCE_MANIFEST.md`](docs/SOURCE_MANIFEST.md) | Author source pin, environment, and paper-scale command |
| [`docs/primary_source_map.md`](docs/primary_source_map.md) | Paper anchors, claim producers, and limitations |
| [`repro/src/verify_mechanisms.py`](repro/src/verify_mechanisms.py) | Independent positive-only and truncated-likelihood controls |
| [`repro/src/run_publication_gate.py`](repro/src/run_publication_gate.py) | Fail-closed source/evidence/test gate |
| [`repro/tests/test_mechanisms.py`](repro/tests/test_mechanisms.py) | Lightweight tests for control primitives |
| [`outputs/source_r10.png`](outputs/source_r10.png) | Full source-protocol plot |
| [`outputs/source_r1.png`](outputs/source_r1.png) | One-repetition calibration plot |
| [`outputs/independent_mechanisms.json`](outputs/independent_mechanisms.json) | Raw independent-control evidence |
| [`outputs/publication_gate.json`](outputs/publication_gate.json) | Machine-readable scoped gate and claim disposition |
| [`STATUS.md`](STATUS.md), [`GATE_READY.md`](GATE_READY.md) | Current status and publication contract |
| [`BRANCH_AUDIT.md`](BRANCH_AUDIT.md) | Branch/commit history and cleanup policy |

## Branch policy and history

The repository currently has one public branch, `main`. There are no active
research branches to preserve or rename. The three existing commits are
documented in [`BRANCH_AUDIT.md`](BRANCH_AUDIT.md); final cleanup keeps the
cumulative history on `main` and normalizes all reachable authors and committers
to MachineLearning-Nerd.

## Source provenance and version boundary

```text
Repository: https://github.com/alexkouridakis/truncated-regression
Commit:     a14732163158aff75113e3e1c50a90ecc27b4250
upstream/main.py     SHA-256 2877a8e00c36a3de8fcb489f7476524a6773f915dfe2167a9cf96446f36b81dc
upstream/config.yaml SHA-256 7a9332fa26e658c73fb6001689844af73cd8f30c4a65457bdadbe0c5012c3fc0
```

The current arXiv page is v2, while the pinned author README links to the v1
paper URL. This audit does not silently assume that the released code and every
v2 textual change are identical; the code commit and source-map anchors are the
authoritative reproduction boundary.

## Citation

```bibtex
@article{kouridakis2026linear,
  title         = {Linear Regression with Unknown Truncation Beyond Gaussian Features},
  author        = {Kouridakis, Alexandros and Mehrotra, Anay and Kalavasis, Alkis and Caramanis, Constantine},
  journal       = {arXiv preprint arXiv:2602.12534},
  year          = {2026},
  note          = {ICML 2026, OpenReview DsV89lJ58l}
}
```

## Thank you

Thank you to Alexandros Kouridakis, Anay Mehrotra, Alkis Kalavasis, and
Constantine Caramanis for releasing a runnable CPU implementation and a clear
configuration for the unknown-truncation problem. That release made it
possible to reproduce the finite protocol, inspect the positive-only and PSGD
mechanisms, and keep the asymptotic theorem boundary explicit. This repository
is an independent reproduction and evidence audit; it does not claim
authorship of the paper’s work.
