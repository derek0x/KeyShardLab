"""Tools to inspect the shard history log."""
import json
from pathlib import Path
from typing import List, Dict


def read_log_entries(log_path: Path) -> List[Dict]:
    """Return parsed JSON lines from the log file."""
    if not log_path.exists():
        return []
    entries = []
    with log_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return entries


def summarize(entries: List[Dict], limit: int = 3) -> List[str]:
    """Build human-readable summaries of the most recent entries."""
    recent = entries[-limit:][::-1]
    summary_lines = []
    for entry in recent:
        dist = entry.get("distribution", [])
        summary_lines.append(
            f"{entry.get('timestamp')} · {entry.get('label')} · {entry.get('shard_count')} shards · {', '.join(dist)}"
        )
    return summary_lines


def show_last_entries(log_path: Path, limit: int = 3) -> None:
    entries = read_log_entries(log_path)
    if not entries:
        print("No log entries yet.")
        return
    for line in summarize(entries, limit):
        print(line)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Summarize the most recent shard bundles from the log.")
    parser.add_argument("--limit", type=int, default=3, help="How many recent entries to show.")
    parser.add_argument("--log", type=Path, default=Path("logs/shard_history.log"))
    args = parser.parse_args()
    show_last_entries(args.log, args.limit)
