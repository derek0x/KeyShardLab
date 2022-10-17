"""Helper utilities for deciding where to stash shards."""
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


def recommend_distribution(shard_count: int, risk_level: str) -> List[str]:
    """Pick devices or locations based on the risk level."""
    weight = RISK_FOCUS.get(risk_level, 0.5)
    emphasis = max(1, int(shard_count * weight))
    suggestions = []
    for idx in range(len(DEVICE_TIERS)):
        if len(suggestions) >= emphasis:
            break
        suggestions.append(DEVICE_TIERS[idx])
    if len(suggestions) < emphasis:
        suggestions.extend(DEVICE_TIERS[: (emphasis - len(suggestions))])
    return suggestions


def build_plan(shard_count: int, risk_level: str, note: str = "Keep everything offline") -> Dict[str, object]:
    """Provide a mini plan that can be stored alongside logs."""
    distribution = recommend_distribution(shard_count, risk_level)
    return {
        "shard_count": shard_count,
        "risk_level": risk_level,
        "distribution": distribution,
        "note": note,
    }
