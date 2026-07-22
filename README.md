# Linear Regression with Unknown Truncation Beyond Gaussian Features

Reproduction workspace for ICML 2026 OpenReview `DsV89lJ58l`.

Pinned author source: `alexkouridakis/truncated-regression` at
`a14732163158aff75113e3e1c50a90ecc27b4250`.

This project reproduces the released CPU-only synthetic protocol and audits
the positive-only survival-set learning and projected-SGD components with
independent numerical controls.

## Result

The unmodified author protocol (`R=10`, `T=4500`) reports mean parameter error
`0.653189` for the full algorithm, compared with `9.852682` for OLS and
`7.170760` for the deliberately wrong survival-set PSGD baseline. The
idealized true-set PSGD reference is `0.522706`. The output plot, complete
captured source log, and independent controls are retained locally.

The independent controls do not import `upstream`: positive-only interval
recovery has symmetric-difference mass `0.007899`, while a deliberately
disjoint reference distribution yields `0.515311`; the correct-set scalar
truncated-likelihood estimate has error `0.007669`, versus `0.099420` for a
wrong-set control.

## Re-run and gate

Follow [the source manifest](docs/SOURCE_MANIFEST.md), then run:

```bash
PYTHONPATH=. .venv/bin/python repro/src/verify_mechanisms.py --output outputs/independent_mechanisms.json
PYTHONPATH=. .venv/bin/python -m pytest -q repro/tests
.venv/bin/python repro/src/run_publication_gate.py
```

The gate is fail-closed and records its result in `outputs/publication_gate.json`.
It distinguishes primary-source audits of the theorem/asymptotic statements
from the executed numerical evidence; see [the claim map](docs/primary_source_map.md).
