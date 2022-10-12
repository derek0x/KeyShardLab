"""CLI layers for building shard packs."""
import argparse
import json
from pathlib import Path
from typing import Optional

from .shard import format_shard_pack


DEFAULT_LOG = Path("logs/shard_history.log")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a small shard bundle for a secret phrase.")
    parser.add_argument("--secret", required=True, help="The secret material that will be split into shards.")
    parser.add_argument("--label", default="Unnamed Vault", help="Friendly label for the secret.")
    parser.add_argument("--count", type=int, default=3, help="The number of shards to emit.")
    parser.add_argument("--log", type=Path, default=DEFAULT_LOG, help="File used to record shard releases.")
    parser.add_argument("--salt", help="Optional salt if you want deterministic results.")
    return parser.parse_args()


def save_pack(pack: dict, log_path: Path) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "timestamp": pack["created_at"],
        "label": pack["label"],
        "shard_count": pack["shard_count"],
        "seal": pack["seal"],
    }
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry) + "\n")


def main() -> None:
    args = parse_args()
    pack = format_shard_pack(args.secret, args.label, args.count, args.salt)
    print("Shard bundle ready:\n")
    for shard in pack["shards"]:
        print(shard)
    print(f"Seal: {pack['seal']}")
    print(f"Risk advice: {pack['risk_level']}")
    save_pack(pack, args.log)


if __name__ == "__main__":
    main()
