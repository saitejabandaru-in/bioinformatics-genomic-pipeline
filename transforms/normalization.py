"""Normalize variant records into analytics-friendly dictionaries."""

from __future__ import annotations


def split_info_field(info: str) -> dict[str, str | bool]:
    if not info or info == ".":
        return {}
    values: dict[str, str | bool] = {}
    for item in info.split(";"):
        if "=" in item:
            key, value = item.split("=", 1)
            values[key] = value
        elif item:
            values[item] = True
    return values


def normalize_variant(row: dict[str, str]) -> dict[str, str | int | float | bool | None]:
    quality: float | None
    try:
        quality = None if row.get("QUAL") in (None, ".") else float(row["QUAL"])
    except ValueError:
        quality = None

    normalized: dict[str, str | int | float | bool | None] = {
        "chrom": row.get("#CHROM") or row.get("CHROM"),
        "pos": int(row["POS"]),
        "id": None if row.get("ID") == "." else row.get("ID"),
        "ref": row.get("REF"),
        "alt": row.get("ALT"),
        "qual": quality,
        "filter": row.get("FILTER"),
    }
    normalized.update({f"info_{key.lower()}": value for key, value in split_info_field(row.get("INFO", "")).items()})
    return normalized
