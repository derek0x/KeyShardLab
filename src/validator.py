"""Simple shape checks for log entries and shard plans."""
from pathlib import Path
from typing import Dict, List

from .log_reader import read_log_entries

REQUIRED_FIELDS = {"timestamp", "label", "shard_count", "seal", "distribution"}


def missing_required_fields(entry: Dict) -> List[str]:
    """Return the set of required fields missing from a log entry."""
    return [field for field in REQUIRED_FIELDS if field not in entry]


def validate_entry(entry: Dict) -> bool:
    """Check that an entry contains all mandatory fields."""
    return not missing_required_fields(entry)


def inspect_log(path: Path, limit: int = 5) -> None:
    """Print the most recent entries along with any missing fields."""
    entries = read_log_entries(path)
    if not entries:
        print("Log is empty.")
        return
    for entry in entries[-limit:]:
        missing = missing_required_fields(entry)
        label = entry.get("label", "(no label)")
        print(f"{entry.get('timestamp', 'no timestamp')} · {label}")
        if missing:
            print("  missing:", ", ".join(missing))
        else:
            print("  ok")
        print()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Validate shard log entries.")
    parser.add_argument("--log", type=Path, default=Path("logs/shard_history.log"))
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()
    inspect_log(args.log, args.limit)
