"""Sort and index alignment files with SAMtools."""

from __future__ import annotations

import argparse
from pathlib import Path

from pipeline.common import add_common_flags, ensure_parent, path_arg, run_command


def build_sort_command(input_sam: Path, output_bam: Path, threads: int = 4) -> list[str]:
    return ["samtools", "sort", "-@", str(threads), "-o", str(output_bam), str(input_sam)]


def sort_alignment(input_sam: Path, output_bam: Path, threads: int = 4, *, dry_run: bool = False):
    ensure_parent(output_bam)
    return run_command(build_sort_command(input_sam, output_bam, threads), dry_run=dry_run)


def index_bam(output_bam: Path, *, dry_run: bool = False):
    return run_command(["samtools", "index", str(output_bam)], dry_run=dry_run)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-sam", required=True, type=path_arg)
    parser.add_argument("--output-bam", required=True, type=path_arg)
    parser.add_argument("--threads", default=4, type=int)
    parser.add_argument("--index", action="store_true")
    add_common_flags(parser)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = sort_alignment(args.input_sam, args.output_bam, args.threads, dry_run=args.dry_run)
    if args.index:
        index_bam(args.output_bam, dry_run=args.dry_run)
    print(result.stdout or "SAMtools sort complete")


if __name__ == "__main__":
    main()
