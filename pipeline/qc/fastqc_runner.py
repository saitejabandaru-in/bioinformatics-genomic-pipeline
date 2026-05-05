"""Run FastQC for FASTQ inputs."""

from __future__ import annotations

import argparse
from pathlib import Path

from pipeline.common import add_common_flags, ensure_parent, path_arg, run_command


def build_fastqc_command(input_path: Path, output_dir: Path, threads: int = 2) -> list[str]:
    return ["fastqc", "--threads", str(threads), "--outdir", str(output_dir), str(input_path)]


def run_fastqc(input_path: Path, output_dir: Path, threads: int = 2, *, dry_run: bool = False):
    output_dir.mkdir(parents=True, exist_ok=True)
    command = build_fastqc_command(input_path, output_dir, threads)
    result = run_command(command, dry_run=dry_run)
    if dry_run:
        ensure_parent(output_dir / "fastqc_command.txt").write_text(result.stdout + "\n", encoding="utf-8")
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=path_arg, help="FASTQ/FASTQ.GZ input")
    parser.add_argument("--output-dir", default="output/qc", type=path_arg)
    parser.add_argument("--threads", default=2, type=int)
    add_common_flags(parser)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = run_fastqc(args.input, args.output_dir, args.threads, dry_run=args.dry_run)
    print(result.stdout or "FastQC complete")


if __name__ == "__main__":
    main()
