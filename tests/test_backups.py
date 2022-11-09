import json

from src.backups import build_summary, tally_distribution


def test_tally_distribution_counts():
    entries = [
        {"distribution": ["hardware wallet", "trusted friend"]},
        {"distribution": ["hardware wallet"]},
    ]
    counts = tally_distribution(entries)
    assert counts["hardware wallet"] == 2
    assert counts["trusted friend"] == 1


def test_build_summary(tmp_path):
    log_path = tmp_path / "shard_history.log"
    data = {"timestamp": "2022-11-07", "label": "Sample", "shard_count": 2, "seal": "a", "distribution": ["hardware wallet"]}
    log_path.write_text(json.dumps(data) + "\n", encoding="utf-8")
    summary = build_summary(log_path, limit=2)
    assert summary[0].startswith("hardware wallet")
*** End Patch
PATCH
