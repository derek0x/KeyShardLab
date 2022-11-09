"""Analytics for distribution coverage seen in the log."""
from collections import Counter
from pathlib import Path
from typing import Dict, List, Tuple

from .log_reader import read_log_entries


def tally_distribution(entries: List[Dict]) -> Dict[str, int]:
    counter = Counter()
    for entry in entries:
        for tier in entry.get("distribution", []):
            counter[tier] += 1
    return dict(counter)


def top_locations(counts: Dict[str, int], limit: int = 3) -> List[Tuple[str, int]]:
    return sorted(counts.items(), key=lambda pair: pair[1], reverse=True)[:limit]


def build_summary(log_path: Path, limit: int = 3) -> List[str]:
    entries = read_log_entries(log_path)
    if not entries:
        return ["No entries to count yet."]
    counts = tally_distribution(entries)
    summary_lines = [f"{tier}: {count}" for tier, count in top_locations(counts, limit)]
    return summary_lines


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Report where shards have been stored the most.")
    parser.add_argument("--log", type=Path, default=Path("logs/shard_history.log"))
    parser.add_argument("--limit", type=int, default=3)
    args = parser.parse_args()
    summary = build_summary(args.log, args.limit)
    for line in summary:
        print(line)
