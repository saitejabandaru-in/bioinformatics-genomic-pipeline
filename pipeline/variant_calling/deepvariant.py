"""Run DeepVariant in a container-friendly command wrapper."""

from __future__ import annotations

import argparse
from pathlib import Path

from pipeline.common import add_common_flags, ensure_parent, path_arg, run_command


def build_deepvariant_command(reference: Path, input_bam: Path, output_vcf: Path, threads: int = 4) -> list[str]:
    return [
        "run_deepvariant",
        "--model_type=WGS",
        f"--ref={reference}",
        f"--reads={input_bam}",
        f"--output_vcf={output_vcf}",
        f"--num_shards={threads}",
    ]


def call_variants(reference: Path, input_bam: Path, output_vcf: Path, threads: int = 4, *, dry_run: bool = False):
    ensure_parent(output_vcf)
    return run_command(build_deepvariant_command(reference, input_bam, output_vcf, threads), dry_run=dry_run)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", required=True, type=path_arg)
    parser.add_argument("--input-bam", required=True, type=path_arg)
    parser.add_argument("--output-vcf", required=True, type=path_arg)
    parser.add_argument("--threads", default=4, type=int)
    add_common_flags(parser)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = call_variants(args.reference, args.input_bam, args.output_vcf, args.threads, dry_run=args.dry_run)
    print(result.stdout or "DeepVariant complete")


if __name__ == "__main__":
    main()
