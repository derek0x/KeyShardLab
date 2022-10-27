from src.planner import build_plan, recommend_distribution


def test_recommend_distribution_length():
    dist = recommend_distribution(5, "high")
    assert len(dist) >= 1


def test_build_plan_fields():
    plan = build_plan(4, "moderate")
    assert plan["shard_count"] == 4
    assert plan["risk_level"] == "moderate"
    assert isinstance(plan["distribution"], list)
    assert "guideline" in plan


def test_guideline_note_applies():
    plan = build_plan(2, "very low")
    assert "back" in plan["note"]
