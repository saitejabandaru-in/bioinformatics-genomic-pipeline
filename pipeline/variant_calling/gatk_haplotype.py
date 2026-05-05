"""Call variants with GATK HaplotypeCaller."""

from __future__ import annotations

import argparse
from pathlib import Path

from pipeline.common import add_common_flags, ensure_parent, path_arg, run_command


def build_gatk_command(reference: Path, input_bam: Path, output_vcf: Path) -> list[str]:
    return [
        "gatk",
        "HaplotypeCaller",
        "-R",
        str(reference),
        "-I",
        str(input_bam),
        "-O",
        str(output_vcf),
    ]


def call_variants(reference: Path, input_bam: Path, output_vcf: Path, *, dry_run: bool = False):
    ensure_parent(output_vcf)
    return run_command(build_gatk_command(reference, input_bam, output_vcf), dry_run=dry_run)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", required=True, type=path_arg)
    parser.add_argument("--input-bam", required=True, type=path_arg)
    parser.add_argument("--output-vcf", required=True, type=path_arg)
    add_common_flags(parser)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = call_variants(args.reference, args.input_bam, args.output_vcf, dry_run=args.dry_run)
    print(result.stdout or "GATK HaplotypeCaller complete")


if __name__ == "__main__":
    main()
