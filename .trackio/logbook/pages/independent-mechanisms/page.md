# Independent mechanisms


---
<!-- trackio-cell
{"type": "code", "id": "cell_d98e8c0319cb", "created_at": "2026-07-22T11:25:08+00:00", "title": "Run: env verify_mechanisms.py (exit -2)", "command": ["env", "PYTHONPATH=.", "OPENBLAS_NUM_THREADS=1", "OMP_NUM_THREADS=1", "MKL_NUM_THREADS=1", ".venv/bin/python", "repro/src/verify_mechanisms.py", "--output", "outputs/independent_mechanisms.json"], "exit_code": -2, "duration_s": 49.357}
-->
````bash
$ env PYTHONPATH=. OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 .venv/bin/python repro/src/verify_mechanisms.py --output outputs/independent_mechanisms.json
````

exit -2 · 49.4s


````python title=verify_mechanisms.py
"""Independent numeric controls for the two released algorithmic mechanisms.

No symbols are imported from ``upstream``.  The checks use scalar truncated
normal identities and a fresh positive-only gap-counting interval learner.
"""

from __future__ import annotations

import argparse
import json
from math import erf, sqrt
from pathlib import Path

import numpy as np


def normal_cdf(x: np.ndarray | float) -> np.ndarray | float:
    return 0.5 * (1.0 + np.vectorize(erf)(np.asarray(x) / sqrt(2.0)))


def normalize(intervals: list[tuple[float, float]]) -> list[tuple[float, float]]:
    answer: list[tuple[float, float]] = []
    for left, right in sorted(intervals):
        if right <= left:
            continue
        if answer and left <= answer[-1][1]:
            answer[-1] = (answer[-1][0], max(answer[-1][1], right))
        else:
            answer.append((left, right))
    return answer


def mass(intervals: list[tuple[float, float]], mean: float = 0.0, scale: float = 1.0) -> float:
    return float(sum(normal_cdf((right - mean) / scale) - normal_cdf((left - mean) / scale) for left, right in normalize(intervals)))


def interval_symmetric_difference_mass(first: list[tuple[float, float]], second: list[tuple[float, float]]) -> float:
    # Exact under N(0,1): split at all interval endpoints and test midpoints.
    endpoints = sorted({edge for interval in first + second for edge in interval})
    total = 0.0
    for left, right in zip(endpoints[:-1], endpoints[1:]):
        mid = (left + right) / 2.0
        in_first = any(a <= mid <= b for a, b in first)
        in_second = any(a <= mid <= b for a, b in second)
        if in_first != in_second:
            total += mass([(left, right)])
    return total


def positive_only_intervals(rng: np.random.Generator, positives: np.ndarray, reference: np.ndarray, remove_gaps: int) -> list[tuple[float, float]]:
    """Fresh gap-counting estimator matching the paper's stated mechanism."""
    positive = np.sort(np.asarray(positives, dtype=float))
    reference = np.sort(np.asarray(reference, dtype=float))
    left = np.searchsorted(reference, positive[:-1], side="right")
    right = np.searchsorted(reference, positive[1:], side="left")
    counts = right - left
    removed = np.zeros(counts.size, dtype=bool)
    removed[np.argpartition(counts, -remove_gaps)[-remove_gaps:]] = True
    intervals: list[tuple[float, float]] = []
    start = float(positive[0])
    for index, remove in enumerate(removed):
        if remove:
            intervals.append((start, float(positive[index])))
            start = float(positive[index + 1])
    intervals.append((start, float(positive[-1])))
    return normalize(intervals)


def conditional_normal_mean(mean: np.ndarray, intervals: list[tuple[float, float]]) -> np.ndarray:
    numerator = np.zeros_like(mean, dtype=float)
    denominator = np.zeros_like(mean, dtype=float)
    for left, right in intervals:
        alpha, beta = left - mean, right - mean
        pdf_alpha = np.exp(-0.5 * alpha**2) / sqrt(2.0 * np.pi)
        pdf_beta = np.exp(-0.5 * beta**2) / sqrt(2.0 * np.pi)
        numerator += pdf_alpha - pdf_beta
        denominator += normal_cdf(beta) - normal_cdf(alpha)
    return mean + numerator / np.maximum(denominator, 1e-14)


def observed_samples(rng: np.random.Generator, w_star: float, intervals: list[tuple[float, float]], count: int) -> tuple[np.ndarray, np.ndarray]:
    xs, ys = [], []
    while len(xs) < count:
        x = rng.normal(size=max(1000, 3 * (count - len(xs))))
        y = w_star * x + rng.normal(size=x.size)
        keep = np.zeros(y.size, dtype=bool)
        for left, right in intervals:
            keep |= (left <= y) & (y <= right)
        xs.extend(x[keep].tolist())
        ys.extend(y[keep].tolist())
    return np.asarray(xs[:count]), np.asarray(ys[:count])


def likelihood_gradient_control(rng: np.random.Generator) -> dict[str, float]:
    true_set = [(-2.0, -0.8), (0.6, 1.8)]
    wrong_set = [(-3.0, 3.0)]
    x, y = observed_samples(rng, w_star=1.25, intervals=true_set, count=30_000)

    def fit(intervals: list[tuple[float, float]]) -> float:
        w = 0.0
        for _ in range(2_000):
            predicted = conditional_normal_mean(w * x, intervals)
            gradient = float(np.mean(x * (predicted - y)))
            w -= 0.04 * gradient
        return w

    true_estimate = fit(true_set)
    wrong_estimate = fit(wrong_set)
    return {
        "w_star": 1.25,
        "true_set_estimate": true_estimate,
        "wrong_set_estimate": wrong_estimate,
        "true_set_error": abs(true_estimate - 1.25),
        "wrong_set_error": abs(wrong_estimate - 1.25),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rng = np.random.default_rng(260212534)
    truth = [(-2.0, -0.8), (0.6, 1.8)]
    raw = rng.normal(size=200_000)
    positive = raw[np.logical_or((raw >= -2.0) & (raw <= -0.8), (raw >= 0.6) & (raw <= 1.8))][:10_000]
    reference = rng.normal(size=100_000)
    learned = positive_only_intervals(rng, positive, reference, remove_gaps=30)
    shifted_reference = rng.normal(loc=2.5, size=100_000)
    negative = positive_only_intervals(rng, positive, shifted_reference, remove_gaps=30)
    recovered_error = interval_symmetric_difference_mass(truth, learned)
    negative_error = interval_symmetric_difference_mass(truth, negative)
    likelihood = likelihood_gradient_control(rng)
    if not recovered_error < negative_error:
        raise AssertionError((recovered_error, negative_error))
    if not likelihood["true_set_error"] < likelihood["wrong_set_error"]:
        raise AssertionError(likelihood)
    report = {
        "method": "independent scalar normal controls; no upstream imports",
        "positive_only": {
            "truth_mass": mass(truth),
            "learned_interval_count": len(learned),
            "reference_symmetric_difference_mass": recovered_error,
            "shifted_reference_negative_control_mass": negative_error,
        },
        "truncated_likelihood": likelihood,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()

````


````output
Traceback (most recent call last):
  File "/home/dineshai/Drives/Code/AllCode/ReproduceICML/papers/icml26-repro-DsV89lJ58l-truncated-regression/repro/src/verify_mechanisms.py", line 153, in <module>
    main()
  File "/home/dineshai/Drives/Code/AllCode/ReproduceICML/papers/icml26-repro-DsV89lJ58l-truncated-regression/repro/src/verify_mechanisms.py", line 132, in main
    likelihood = likelihood_gradient_control(rng)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/dineshai/Drives/Code/AllCode/ReproduceICML/papers/icml26-repro-DsV89lJ58l-truncated-regression/repro/src/verify_mechanisms.py", line 108, in likelihood_gradient_control
    wrong_estimate = fit(wrong_set)
                     ^^^^^^^^^^^^^^
  File "/home/dineshai/Drives/Code/AllCode/ReproduceICML/papers/icml26-repro-DsV89lJ58l-truncated-regression/repro/src/verify_mechanisms.py", line 102, in fit
    predicted = conditional_normal_mean(w * x, intervals)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/dineshai/Drives/Code/AllCode/ReproduceICML/papers/icml26-repro-DsV89lJ58l-truncated-regression/repro/src/verify_mechanisms.py", line 78, in conditional_normal_mean
    return mean + numerator / np.maximum(denominator, 1e-14)
                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
KeyboardInterrupt

````


---
<!-- trackio-cell
{"type": "code", "id": "cell_35b7f640e4d2", "created_at": "2026-07-22T11:46:00+00:00", "title": "Run: env verify_mechanisms.py (exit 1)", "command": ["env", "PYTHONPATH=.", "OPENBLAS_NUM_THREADS=1", "OMP_NUM_THREADS=1", "MKL_NUM_THREADS=1", ".venv/bin/python", "repro/src/verify_mechanisms.py", "--output", "outputs/independent_mechanisms.json"], "exit_code": 1, "duration_s": 11.437}
-->
````bash
$ env PYTHONPATH=. OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 .venv/bin/python repro/src/verify_mechanisms.py --output outputs/independent_mechanisms.json
````

exit 1 · 11.4s


````python title=verify_mechanisms.py
"""Independent numeric controls for the two released algorithmic mechanisms.

No symbols are imported from ``upstream``.  The checks use scalar truncated
normal identities and a fresh positive-only gap-counting interval learner.
"""

from __future__ import annotations

import argparse
import json
from math import sqrt
from pathlib import Path

import numpy as np
from scipy.special import ndtr


def normal_cdf(x: np.ndarray | float) -> np.ndarray | float:
    return ndtr(np.asarray(x, dtype=float))


def normalize(intervals: list[tuple[float, float]]) -> list[tuple[float, float]]:
    answer: list[tuple[float, float]] = []
    for left, right in sorted(intervals):
        if right <= left:
            continue
        if answer and left <= answer[-1][1]:
            answer[-1] = (answer[-1][0], max(answer[-1][1], right))
        else:
            answer.append((left, right))
    return answer


def mass(intervals: list[tuple[float, float]], mean: float = 0.0, scale: float = 1.0) -> float:
    return float(sum(normal_cdf((right - mean) / scale) - normal_cdf((left - mean) / scale) for left, right in normalize(intervals)))


def interval_symmetric_difference_mass(first: list[tuple[float, float]], second: list[tuple[float, float]]) -> float:
    # Exact under N(0,1): split at all interval endpoints and test midpoints.
    endpoints = sorted({edge for interval in first + second for edge in interval})
    total = 0.0
    for left, right in zip(endpoints[:-1], endpoints[1:]):
        mid = (left + right) / 2.0
        in_first = any(a <= mid <= b for a, b in first)
        in_second = any(a <= mid <= b for a, b in second)
        if in_first != in_second:
            total += mass([(left, right)])
    return total


def positive_only_intervals(rng: np.random.Generator, positives: np.ndarray, reference: np.ndarray, remove_gaps: int) -> list[tuple[float, float]]:
    """Fresh gap-counting estimator matching the paper's stated mechanism."""
    positive = np.sort(np.asarray(positives, dtype=float))
    reference = np.sort(np.asarray(reference, dtype=float))
    left = np.searchsorted(reference, positive[:-1], side="right")
    right = np.searchsorted(reference, positive[1:], side="left")
    counts = right - left
    removed = np.zeros(counts.size, dtype=bool)
    removed[np.argpartition(counts, -remove_gaps)[-remove_gaps:]] = True
    intervals: list[tuple[float, float]] = []
    start = float(positive[0])
    for index, remove in enumerate(removed):
        if remove:
            intervals.append((start, float(positive[index])))
            start = float(positive[index + 1])
    intervals.append((start, float(positive[-1])))
    return normalize(intervals)


def conditional_normal_mean(mean: np.ndarray, intervals: list[tuple[float, float]]) -> np.ndarray:
    numerator = np.zeros_like(mean, dtype=float)
    denominator = np.zeros_like(mean, dtype=float)
    for left, right in intervals:
        alpha, beta = left - mean, right - mean
        pdf_alpha = np.exp(-0.5 * alpha**2) / sqrt(2.0 * np.pi)
        pdf_beta = np.exp(-0.5 * beta**2) / sqrt(2.0 * np.pi)
        numerator += pdf_alpha - pdf_beta
        denominator += normal_cdf(beta) - normal_cdf(alpha)
    return mean + numerator / np.maximum(denominator, 1e-14)


def observed_samples(rng: np.random.Generator, w_star: float, intervals: list[tuple[float, float]], count: int) -> tuple[np.ndarray, np.ndarray]:
    xs, ys = [], []
    while len(xs) < count:
        x = rng.normal(size=max(1000, 3 * (count - len(xs))))
        y = w_star * x + rng.normal(size=x.size)
        keep = np.zeros(y.size, dtype=bool)
        for left, right in intervals:
            keep |= (left <= y) & (y <= right)
        xs.extend(x[keep].tolist())
        ys.extend(y[keep].tolist())
    return np.asarray(xs[:count]), np.asarray(ys[:count])


def likelihood_gradient_control(rng: np.random.Generator) -> dict[str, float]:
    true_set = [(-2.0, -0.8), (0.6, 1.8)]
    wrong_set = [(-3.0, 3.0)]
    x, y = observed_samples(rng, w_star=1.25, intervals=true_set, count=30_000)

    def fit(intervals: list[tuple[float, float]]) -> float:
        w = 0.0
        for _ in range(2_000):
            predicted = conditional_normal_mean(w * x, intervals)
            gradient = float(np.mean(x * (predicted - y)))
            w -= 0.04 * gradient
        return w

    true_estimate = fit(true_set)
    wrong_estimate = fit(wrong_set)
    return {
        "w_star": 1.25,
        "true_set_estimate": true_estimate,
        "wrong_set_estimate": wrong_estimate,
        "true_set_error": abs(true_estimate - 1.25),
        "wrong_set_error": abs(wrong_estimate - 1.25),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rng = np.random.default_rng(260212534)
    truth = [(-2.0, -0.8), (0.6, 1.8)]
    raw = rng.normal(size=200_000)
    positive = raw[np.logical_or((raw >= -2.0) & (raw <= -0.8), (raw >= 0.6) & (raw <= 1.8))][:10_000]
    reference = rng.normal(size=100_000)
    learned = positive_only_intervals(rng, positive, reference, remove_gaps=30)
    shifted_reference = rng.normal(loc=2.5, size=100_000)
    negative = positive_only_intervals(rng, positive, shifted_reference, remove_gaps=30)
    recovered_error = interval_symmetric_difference_mass(truth, learned)
    negative_error = interval_symmetric_difference_mass(truth, negative)
    likelihood = likelihood_gradient_control(rng)
    if not recovered_error < negative_error:
        raise AssertionError((recovered_error, negative_error))
    if not likelihood["true_set_error"] < likelihood["wrong_set_error"]:
        raise AssertionError(likelihood)
    report = {
        "method": "independent scalar normal controls; no upstream imports",
        "positive_only": {
            "truth_mass": mass(truth),
            "learned_interval_count": len(learned),
            "reference_symmetric_difference_mass": recovered_error,
            "shifted_reference_negative_control_mass": negative_error,
        },
        "truncated_likelihood": likelihood,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()

````


````output
Traceback (most recent call last):
  File "/home/dineshai/Drives/Code/AllCode/ReproduceICML/papers/icml26-repro-DsV89lJ58l-truncated-regression/repro/src/verify_mechanisms.py", line 154, in <module>
    main()
  File "/home/dineshai/Drives/Code/AllCode/ReproduceICML/papers/icml26-repro-DsV89lJ58l-truncated-regression/repro/src/verify_mechanisms.py", line 135, in main
    raise AssertionError((recovered_error, negative_error))
AssertionError: (0.007898979615557723, 0.005853615260001888)

````
