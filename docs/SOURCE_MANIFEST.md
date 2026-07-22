# Source manifest

The author release is intentionally kept as a separately versioned checkout.

```bash
git clone https://github.com/alexkouridakis/truncated-regression.git upstream
git -C upstream checkout --detach a14732163158aff75113e3e1c50a90ecc27b4250
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -r repro/requirements-cpu.txt
```

Run the documented paper-scale source experiment from this workspace:

```bash
env MPLBACKEND=Agg OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  .venv/bin/python upstream/main.py --config upstream/config.yaml --R 10 \
  --output-plot outputs/source_r10.png
```
