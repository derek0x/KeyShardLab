from src.planner import build_plan, recommend_distribution


def test_recommend_distribution_length():
    dist = recommend_distribution(5, "high")
    assert len(dist) >= 1


def test_build_plan_fields():
    plan = build_plan(4, "moderate", note="Keep in mind")
    assert plan["shard_count"] == 4
    assert plan["risk_level"] == "moderate"
    assert plan["note"] == "Keep in mind"
    assert isinstance(plan["distribution"], list)
