"""Annotate VCF files with Ensembl VEP."""

from __future__ import annotations

import argparse
from pathlib import Path

from pipeline.common import add_common_flags, ensure_parent, path_arg, run_command


def build_vep_command(input_vcf: Path, output_vcf: Path, cache_dir: Path | None = None) -> list[str]:
    command = ["vep", "--vcf", "--input_file", str(input_vcf), "--output_file", str(output_vcf), "--force_overwrite"]
    if cache_dir:
        command.extend(["--cache", "--dir_cache", str(cache_dir)])
    return command


def annotate(input_vcf: Path, output_vcf: Path, cache_dir: Path | None = None, *, dry_run: bool = False):
    ensure_parent(output_vcf)
    return run_command(build_vep_command(input_vcf, output_vcf, cache_dir), dry_run=dry_run)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-vcf", required=True, type=path_arg)
    parser.add_argument("--output-vcf", required=True, type=path_arg)
    parser.add_argument("--cache-dir", type=path_arg)
    add_common_flags(parser)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = annotate(args.input_vcf, args.output_vcf, args.cache_dir, dry_run=args.dry_run)
    print(result.stdout or "VEP annotation complete")


if __name__ == "__main__":
    main()
