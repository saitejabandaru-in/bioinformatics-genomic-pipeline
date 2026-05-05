"""Convert VCF records into a Parquet table."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Iterator

import pandas as pd

from pipeline.common import ensure_parent, path_arg
from transforms.normalization import normalize_variant


VCF_COLUMNS = ["#CHROM", "POS", "ID", "REF", "ALT", "QUAL", "FILTER", "INFO"]


def read_vcf_records(vcf_path: Path) -> Iterator[dict[str, str]]:
    with vcf_path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.startswith("##"):
                continue
            if line.startswith("#CHROM"):
                reader = csv.DictReader(handle, fieldnames=line.rstrip("\n").split("\t"), delimiter="\t")
                for row in reader:
                    yield row
                return
            if not line.startswith("#"):
                values = line.rstrip("\n").split("\t")
                yield dict(zip(VCF_COLUMNS, values[: len(VCF_COLUMNS)], strict=False))


def vcf_to_dataframe(vcf_path: Path) -> pd.DataFrame:
    return pd.DataFrame(normalize_variant(row) for row in read_vcf_records(vcf_path))


def convert(vcf_path: Path, output_path: Path) -> Path:
    ensure_parent(output_path)
    frame = vcf_to_dataframe(vcf_path)
    if output_path.suffix == ".csv":
        frame.to_csv(output_path, index=False)
    else:
        frame.to_parquet(output_path, index=False)
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-vcf", required=True, type=path_arg)
    parser.add_argument("--output", required=True, type=path_arg)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output = convert(args.input_vcf, args.output)
    print(output)


if __name__ == "__main__":
    main()
