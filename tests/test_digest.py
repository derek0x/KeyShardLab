import json

from src.digest import build_digest, write_digest


def _fake_entry(label: str, stamp: str):
    return {
        "timestamp": stamp,
        "label": label,
        "shard_count": 3,
        "seal": "deadbeef",
        "distribution": ["hardware wallet"],
    }


def test_build_digest(tmp_path):
    log_path = tmp_path / "shard_history.log"
    entries = [json.dumps(_fake_entry("Vault A", "2022-10-20T18:00:00")), json.dumps(_fake_entry("Vault B", "2022-10-21T19:00:00"))]
    log_path.write_text("\n".join(entries) + "\n", encoding="utf-8")
    lines = build_digest(log_path, limit=2)
    assert len(lines) == 2
    assert "Vault B" in lines[0]


def test_write_digest(tmp_path):
    output = tmp_path / "digest.md"
    write_digest(["Line A"], output)
    content = output.read_text("utf-8")
    assert "Line A" in content
*** End Patch
PATCH
