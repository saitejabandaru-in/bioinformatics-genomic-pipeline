from transforms.normalization import normalize_variant, split_info_field


def test_split_info_field_handles_flags_and_key_values():
    assert split_info_field("DP=10;SOMATIC;AF=0.4") == {"DP": "10", "SOMATIC": True, "AF": "0.4"}


def test_normalize_variant_casts_position_and_quality():
    row = {
        "#CHROM": "chr1",
        "POS": "123",
        "ID": ".",
        "REF": "A",
        "ALT": "G",
        "QUAL": "99.7",
        "FILTER": "PASS",
        "INFO": "DP=42",
    }

    assert normalize_variant(row) == {
        "chrom": "chr1",
        "pos": 123,
        "id": None,
        "ref": "A",
        "alt": "G",
        "qual": 99.7,
        "filter": "PASS",
        "info_dp": "42",
    }
