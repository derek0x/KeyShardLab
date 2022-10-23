from src.shard import generate_shards, format_shard_pack


def test_generate_shards_count():
    shards = generate_shards("example-secret", 3, salt="steady")
    assert len(shards) == 3
    assert shards[0].startswith("SHARD-01-")


def test_format_shard_pack_contains_metadata():
    pack = format_shard_pack("value", "TestVault", 2, salt="steady")
    assert pack["label"] == "TestVault"
    assert pack["shard_count"] == 2
    assert "seal" in pack
    assert isinstance(pack["shards"], list)
