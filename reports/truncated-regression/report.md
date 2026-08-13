# Claim-by-claim audit — unknown-truncation linear regression

**Paper:** *Linear Regression with Unknown Truncation Beyond Gaussian Features* —
Alexandros Kouridakis, Anay Mehrotra, Alkis Kalavasis, and Constantine
Caramanis, ICML 2026 ([arXiv:2602.12534](https://arxiv.org/abs/2602.12534),
OpenReview `DsV89lJ58l`).

## Executive assessment

**Scoped gate: PASS. Paper-level reproduction: INCONCLUSIVE.** The author’s
released CPU simulation is reproduced at `R=10`, `T=4500`. Independent controls
support the positive-only interval learner and truncated-likelihood mechanism.
The theorem, assumption class, smoothness lemma, and asymptotic comparison are
not independently formalized from first principles.

## C1 — polynomial-time unknown-truncation regression

The primary source’s Theorem 3.1 is mapped in
[`docs/primary_source_map.md`](../../docs/primary_source_map.md). The pinned
author implementation is run with the documented 10D five-Gaussian-mixture,
five-interval setup. This verifies that the released finite protocol executes
and produces the expected comparison, not the universal polynomial-time theorem.

**Assessment:** `SOURCE_AUDITED_CONDITIONAL`, medium confidence.

## C2 — assumptions

The source map checks the survival probability, sub-Gaussian/bounded-feature,
and observed-covariance identifiability assumptions against
`upstream/config.yaml`. The finite configuration is compatible with the audited
conditions, but it cannot represent the full theorem’s distribution class.

**Assessment:** `SOURCE_AUDITED_CONDITIONAL`, medium confidence.

## C3 — positive-only Phase I

The independent producer `positive_only_intervals` in
[`repro/src/verify_mechanisms.py`](../../repro/src/verify_mechanisms.py) learns
intervals from positive samples and a reference sample without importing the
author implementation. It obtains symmetric-difference mass `0.007899` on the
matched reference. A deliberately disjoint reference produces `0.515311`, so
the control distinguishes the intended mechanism from a bad reference.

**Assessment:** `REPRODUCED_SCOPED`, medium confidence. This is a scalar
mechanism check, not a proof of the paper’s high-dimensional PAC guarantee.

## C4 — Phase II PSGD

The full unmodified author run reports:

| Method | Mean final error |
| --- | ---: |
| OLS | `9.852682` |
| Wrong-set PSGD | `7.170760` |
| True-set PSGD | `0.522706` |
| Full learned-set algorithm | `0.653189` |

The independent scalar truncated-likelihood control estimates `w*=1.25` with
error `0.007669` using the correct set and `0.099420` using a wrong set.

**Assessment:** `REPRODUCED_SCOPED`, medium/high confidence. The named finite
protocol and mechanism direction are reproduced; general convergence is not
claimed.

## C5 — smoothness lemma

Lemma 3.4 and its source equations are audited in the source map. The scalar
control exercises the conditional-normal CDF, density, and conditional-mean
calculations used by the likelihood producer. This supports formula-level
consistency only.

**Assessment:** `SOURCE_AUDITED_CONDITIONAL`, medium confidence.

## C6 — comparison with prior work

The related-work and Gaussian-case sections are recorded in the source map. The
comparison concerns asymptotic dependence, so the repository does not claim that
the finite source run or any local timing measurement proves it.

**Assessment:** `SOURCE_AUDITED_ONLY`, low confidence.

## Reproduction boundary

The source pin, file hashes, environment, and exact command are recorded in
[`docs/SOURCE_MANIFEST.md`](../../docs/SOURCE_MANIFEST.md). The ignored author
checkout is recreated from commit `a14732163158aff75113e3e1c50a90ecc27b4250`.
The current arXiv record is v2, while the pinned author README links to v1; the
audit preserves that version boundary.

## Citation and thanks

```bibtex
@article{kouridakis2026linear,
  title         = {Linear Regression with Unknown Truncation Beyond Gaussian Features},
  author        = {Kouridakis, Alexandros and Mehrotra, Anay and Kalavasis, Alkis and Caramanis, Constantine},
  journal       = {arXiv preprint arXiv:2602.12534},
  year          = {2026},
  note          = {ICML 2026, OpenReview DsV89lJ58l}
}
```

Thank you to Alexandros Kouridakis, Anay Mehrotra, Alkis Kalavasis, and
Constantine Caramanis for releasing the runnable CPU implementation and its
configuration. It made the finite protocol and the distinction between
mechanism evidence and asymptotic claims straightforward to audit.
