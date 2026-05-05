"""Evaluate FastQC summary files and emit pass/fail metadata."""

from __future__ import annotations

import argparse
from pathlib import Path

from pipeline.common import path_arg, write_json


def parse_fastqc_summary(summary_path: Path) -> dict[str, str]:
    checks: dict[str, str] = {}
    for line in summary_path.read_text(encoding="utf-8").splitlines():
        parts = line.split("\t")
        if len(parts) >= 2:
            checks[parts[1]] = parts[0]
    return checks


def evaluate_quality(checks: dict[str, str], max_failed_checks: int = 2) -> dict:
    failed = sorted(name for name, status in checks.items() if status.upper() == "FAIL")
    warnings = sorted(name for name, status in checks.items() if status.upper() == "WARN")
    return {
        "passed": len(failed) <= max_failed_checks,
        "failed_checks": failed,
        "warning_checks": warnings,
        "total_checks": len(checks),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary", required=True, type=path_arg, help="FastQC summary.txt file")
    parser.add_argument("--output", default="output/qc/quality_gate.json", type=path_arg)
    parser.add_argument("--max-failed-checks", default=2, type=int)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = evaluate_quality(parse_fastqc_summary(args.summary), args.max_failed_checks)
    write_json(args.output, result)
    print("PASS" if result["passed"] else "FAIL")


if __name__ == "__main__":
    main()
