"""Fail-closed publication gate for the DsV89lJ58l reproduction."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
UPSTREAM = ROOT / "upstream"
OUTPUT = ROOT / "outputs" / "publication_gate.json"


def check(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def main() -> None:
    failures: list[str] = []
    tests_passed = False
    try:
        subprocess.run(
            [str(ROOT / ".venv" / "bin" / "python"), "-m", "pytest", "-q", "repro/tests"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        tests_passed = True
    except (OSError, subprocess.CalledProcessError) as error:
        failures.append(f"claim verifier tests failed: {error}")
    try:
        commit = subprocess.check_output(
            ["git", "-C", str(UPSTREAM), "rev-parse", "HEAD"], text=True
        ).strip()
        dirty = subprocess.check_output(
            ["git", "-C", str(UPSTREAM), "status", "--porcelain"], text=True
        ).strip()
    except subprocess.CalledProcessError as error:
        commit, dirty = "", "unknown"
        failures.append(f"cannot inspect pinned author source: {error}")

    check(commit == "a14732163158aff75113e3e1c50a90ecc27b4250", "author commit differs from the audited pin", failures)
    check(not dirty, "author source worktree is dirty", failures)

    plot = ROOT / "outputs" / "source_r10.png"
    check(plot.is_file() and plot.stat().st_size > 1_000_000, "missing or implausibly small full-scale source plot", failures)
    source_log = ROOT / ".trackio" / "logbook" / "pages" / "source-replication-paper-scale" / "page.md"
    source_text = source_log.read_text() if source_log.is_file() else ""
    for expected in (
        "Number of outer reruns R: 10",
        "PSGD iterations T: 4500",
        "OLS (no correction)      : 9.852682 +/- 0.250369",
        "PSGD with wrong S        : 7.170760 +/- 0.149235",
        "PSGD with true S*        : 0.522706 +/- 0.080022",
        "Full algorithm           : 0.653189 +/- 0.110646",
    ):
        check(expected in source_text, f"source log lacks expected record: {expected}", failures)

    independent_path = ROOT / "outputs" / "independent_mechanisms.json"
    try:
        independent = json.loads(independent_path.read_text())
        positive = independent["positive_only"]
        likelihood = independent["truncated_likelihood"]
        check(positive["reference_symmetric_difference_mass"] < 0.01, "positive-only recovery error is not below 0.01", failures)
        check(positive["shifted_reference_negative_control_mass"] > 0.5, "disjoint-reference negative control did not fail strongly", failures)
        check(likelihood["true_set_error"] < likelihood["wrong_set_error"], "correct-set likelihood did not beat wrong-set control", failures)
    except (OSError, KeyError, TypeError, ValueError) as error:
        independent = None
        failures.append(f"cannot validate independent controls: {error}")

    source_map = ROOT / "docs" / "primary_source_map.md"
    check(source_map.is_file() and "C1" in source_map.read_text(), "primary-source claim map is missing", failures)
    claims = {
        "C1": "Primary Theorem 3.1 was source-audited; full source simulation is preserved.",
        "C2": "The three stated assumptions were audited against the primary source and CPU configuration.",
        "C3": "Independent positive-only recovery passes and a disjoint-reference control fails strongly.",
        "C4": "Pinned full Phase-I/II source run beats OLS and wrong-set PSGD; independent likelihood control agrees.",
        "C5": "Primary smoothness lemma was source-audited; independent conditional-normal calculations are exercised.",
        "C6": "Primary related-work comparison was source-audited (an asymptotic claim, not a timing benchmark).",
    }
    report = {
        "paper": "DsV89lJ58l",
        "pass": not failures,
        "tests_passed": tests_passed,
        "publication_gate_passed": not failures,
        "author_commit": commit,
        "author_dirty": bool(dirty),
        "full_scale": {"reruns": 10, "psgd_iterations": 4500, "plot": str(plot.relative_to(ROOT))},
        "source_summary": {
            "ols_mean_error": 9.852682,
            "wrong_set_mean_error": 7.170760,
            "true_set_mean_error": 0.522706,
            "full_algorithm_mean_error": 0.653189,
        },
        "independent_controls": independent,
        "claims": claims,
        "failures": failures,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, indent=2, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
