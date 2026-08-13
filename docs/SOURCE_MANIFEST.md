# Source manifest

Paper: [arXiv:2602.12534](https://arxiv.org/abs/2602.12534)<br>
OpenReview: `DsV89lJ58l`<br>
Official repository: [`alexkouridakis/truncated-regression`](https://github.com/alexkouridakis/truncated-regression)

The author release is intentionally kept as a separately versioned, ignored
checkout. The exact audited commit is:

```text
a14732163158aff75113e3e1c50a90ecc27b4250
```

Recreate it with:

```bash
git clone https://github.com/alexkouridakis/truncated-regression.git upstream
git -C upstream checkout --detach a14732163158aff75113e3e1c50a90ecc27b4250
```

The pinned source-file hashes are:

```text
upstream/main.py     2877a8e00c36a3de8fcb489f7476524a6773f915dfe2167a9cf96446f36b81dc
upstream/config.yaml 7a9332fa26e658c73fb6001689844af73cd8f30c4a65457bdadbe0c5012c3fc0
```

## Environment

```bash
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -r repro/requirements-cpu.txt
```

## Paper-scale source experiment

The released default is a 10-dimensional mixture of five Gaussians, a
five-interval survival set, `R=10` outer repetitions, `T=4500` PSGD steps, and
batch size 128. Run it with single-threaded CPU BLAS for the committed output:

```bash
env MPLBACKEND=Agg OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  .venv/bin/python upstream/main.py --config upstream/config.yaml --R 10 \
  --output-plot outputs/source_r10.png
```

The captured source command and output are retained in the local Trackio
logbook under `source-replication-paper-scale`. The repository’s gate checks
the pinned commit, plot, and expected summary values.
