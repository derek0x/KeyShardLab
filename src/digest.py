"""Utilities for turning the log into a readable digest."""
from pathlib import Path
from typing import List

from .log_reader import read_log_entries, summarize


def build_digest(log_path: Path, limit: int = 4) -> List[str]:
    """Return bullet lines summarizing the most recent entries."""
    entries = read_log_entries(log_path)
    if not entries:
        return ["No shard bundles recorded yet."]
    return summarize(entries, limit)


def write_digest(digest_lines: List[str], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as handle:
        handle.write("# Daily digest\n\n")
        for line in digest_lines:
            handle.write(f"- {line}\n")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Render recent shard bundles as a digest.")
    parser.add_argument("--log", type=Path, default=Path("logs/shard_history.log"))
    parser.add_argument("--out", type=Path, default=Path("data/digest_summary.md"))
    parser.add_argument("--limit", type=int, default=4)
    args = parser.parse_args()
    lines = build_digest(args.log, args.limit)
    write_digest(lines, args.out)
    print(f"Digest written to {args.out}")
