"""Helper utilities for deciding where to stash shards."""
import json
from pathlib import Path
from typing import List, Dict

DEVICE_TIERS = [
    "hardware wallet",
    "air-gapped laptop",
    "safety deposit box",
    "trusted friend",
    "personal vault app",
]

RISK_FOCUS = {
    "very low": 0.2,
    "low": 0.4,
    "moderate": 0.6,
    "medium": 0.8,
    "high": 1.0,
}

DEFAULT_RISK_GUIDELINES = {
    "very low": {
        "note": "Keep shards close but back them up monthly.",
        "preferred": ["personal vault app", "hardware wallet"],
    },
    "low": {
        "note": "Pair a hot wallet with a hardware wallet and check quarterly.",
        "preferred": ["hardware wallet", "air-gapped laptop"],
    },
    "moderate": {
        "note": "Spread shards across trusted hands and offline storage.",
        "preferred": ["hardware wallet", "air-gapped laptop", "trusted friend"],
    },
    "medium": {
        "note": "Keep copies in a box and on an air-gapped host; avoid network exposures.",
        "preferred": ["hardware wallet", "safety deposit box"],
    },
    "high": {
        "note": "Treat shards as ultra-sensitive and keep them off-network.",
        "preferred": ["safety deposit box", "air-gapped laptop"],
    },
}

DATA_PATH = Path(__file__).resolve().parents[1] / "data"
RISK_GUIDELINES_FILE = DATA_PATH / "risk_guidelines.json"


def _load_risk_guidelines() -> Dict[str, Dict[str, List[str]]]:
    try:
        with RISK_GUIDELINES_FILE.open("r", encoding="utf-8") as handle:
            candidate = json.load(handle)
    except (OSError, ValueError):
        candidate = DEFAULT_RISK_GUIDELINES
    normalized = {}
    for key, value in candidate.items():
        normalized[key.lower()] = value
    return normalized


RISK_GUIDELINES = _load_risk_guidelines()


def recommend_distribution(shard_count: int, risk_level: str) -> List[str]:
    """Pick devices or locations based on the risk level."""
    weight = RISK_FOCUS.get(risk_level, 0.5)
    emphasis = max(1, int(shard_count * weight))
    normalized = risk_level.lower()
    guideline = RISK_GUIDELINES.get(normalized, {})
    suggestions = list(guideline.get("preferred", []))
    for tier in DEVICE_TIERS:
        if len(suggestions) >= emphasis:
            break
        if tier not in suggestions:
            suggestions.append(tier)
    return suggestions


def build_plan(shard_count: int, risk_level: str, note: str = "Keep everything offline") -> Dict[str, object]:
    """Provide a mini plan that can be stored alongside logs."""
    distribution = recommend_distribution(shard_count, risk_level)
    guideline = RISK_GUIDELINES.get(risk_level.lower(), {})
    guideline_note = guideline.get("note")
    return {
        "shard_count": shard_count,
        "risk_level": risk_level,
        "distribution": distribution,
        "note": guideline_note or note,
        "guideline": guideline,
    }
