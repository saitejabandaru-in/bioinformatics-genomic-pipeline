"""Align paired or single-end reads with BWA-MEM2."""

from __future__ import annotations

import argparse
from pathlib import Path

from pipeline.common import add_common_flags, ensure_parent, path_arg, run_command


def build_bwa_mem2_command(reference: Path, read1: Path, read2: Path | None, output_sam: Path, threads: int = 4) -> list[str]:
    command = ["bwa-mem2", "mem", "-t", str(threads), str(reference), str(read1)]
    if read2:
        command.append(str(read2))
    return command + ["-o", str(output_sam)]


def align_reads(reference: Path, read1: Path, output_sam: Path, read2: Path | None = None, threads: int = 4, *, dry_run: bool = False):
    ensure_parent(output_sam)
    return run_command(build_bwa_mem2_command(reference, read1, read2, output_sam, threads), dry_run=dry_run)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", required=True, type=path_arg)
    parser.add_argument("--read1", required=True, type=path_arg)
    parser.add_argument("--read2", type=path_arg)
    parser.add_argument("--output-sam", required=True, type=path_arg)
    parser.add_argument("--threads", default=4, type=int)
    add_common_flags(parser)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = align_reads(args.reference, args.read1, args.output_sam, args.read2, args.threads, dry_run=args.dry_run)
    print(result.stdout or "Alignment complete")


if __name__ == "__main__":
    main()
