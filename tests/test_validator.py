from src.validator import validate_entry, missing_required_fields


def test_validate_entry_passes():
    fields = {
        "timestamp": "2022-10-10",
        "label": "Demo",
        "shard_count": 3,
        "seal": "abc",
        "distribution": ["hardware wallet"],
    }
    assert validate_entry(fields)


def test_missing_fields():
    entry = {"timestamp": "2022-10-10"}
    missing = missing_required_fields(entry)
    assert "label" in missing
    assert "seal" in missing
*** End Patch
PATCH
