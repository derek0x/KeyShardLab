"""Standalone utilities for creating shard descriptions."""
import hashlib
from datetime import datetime
from typing import List, Dict, Optional


def _hash_chunk(secret: str, index: int, salt: str) -> str:
    """Create a deterministic chunk fingerprint."""
    marker = f"{index}-{salt}".encode("utf-8")
    digest = hashlib.blake2b(secret.encode("utf-8") + marker, digest_size=16)
    return digest.hexdigest().upper()


def generate_shards(secret: str, shard_count: int, salt: Optional[str] = None) -> List[str]:
    """Split a secret into simple deterministic shards."""
    if shard_count < 1:
        raise ValueError("shard_count must be positive")

    salt = salt or datetime.utcnow().isoformat()
    shard_list = []
    for idx in range(shard_count):
        shard_hash = _hash_chunk(secret, idx, salt)
        shard_list.append(f"SHARD-{idx + 1:02d}-{shard_hash}")
    return shard_list


def new_metadata(secret_label: str, shard_count: int) -> Dict[str, object]:
    """Create descriptive metadata for a shard bundle."""
    risk_levels = ["very low", "low", "moderate", "medium", "high"]
    index = min(shard_count, 4)
    return {
        "label": secret_label,
        "created_at": datetime.utcnow().isoformat(),
        "shard_count": shard_count,
        "risk_level": risk_levels[index],
        "storage_hint": "Spread shards across at least two device types.",
    }


def format_shard_pack(secret: str, label: str, shard_count: int, salt: Optional[str] = None) -> Dict[str, object]:
    """Assemble a digestable pack that can be logged."""
    shards = generate_shards(secret, shard_count, salt)
    metadata = new_metadata(label, shard_count)
    metadata["seal"] = hashlib.sha256(("".join(shards)).encode("utf-8")).hexdigest()
    metadata["shards"] = shards
    metadata["note"] = "Store shards offline; mark who has each shard in your private notes."
    return metadata
