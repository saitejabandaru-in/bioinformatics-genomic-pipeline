"""Annotate VCF files with SnpEff."""

from __future__ import annotations

import argparse
from pathlib import Path

from pipeline.common import add_common_flags, ensure_parent, path_arg, run_command


def build_snpeff_command(input_vcf: Path, output_vcf: Path, database: str = "GRCh38.99") -> list[str]:
    return ["snpEff", database, str(input_vcf), "-o", "vcf", "-csvStats", str(output_vcf.with_suffix(".csv"))]


def annotate(input_vcf: Path, output_vcf: Path, database: str = "GRCh38.99", *, dry_run: bool = False):
    ensure_parent(output_vcf)
    result = run_command(build_snpeff_command(input_vcf, output_vcf, database), dry_run=dry_run)
    if dry_run:
        return result
    output_vcf.write_text(result.stdout, encoding="utf-8")
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-vcf", required=True, type=path_arg)
    parser.add_argument("--output-vcf", required=True, type=path_arg)
    parser.add_argument("--database", default="GRCh38.99")
    add_common_flags(parser)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = annotate(args.input_vcf, args.output_vcf, args.database, dry_run=args.dry_run)
    print(result.stdout if args.dry_run else "SnpEff annotation complete")


if __name__ == "__main__":
    main()
