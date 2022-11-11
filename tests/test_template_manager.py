from src import template_manager


def test_load_templates():
    templates = template_manager.load_templates()
    assert isinstance(templates, list)
    assert any(tpl.get("label") == "Ledger warmup" for tpl in templates)


def test_find_by_label():
    tpl = template_manager.find_by_label("API key backup")
    assert tpl is not None
    assert tpl.get("template") == "delta echo foxtrot"


def test_random_template(monkeypatch):
    monkeypatch.setattr(template_manager.random, "choice", lambda items: items[1])
    tpl = template_manager.random_template()
    assert tpl.get("label") == "API key backup"
*** End Patch
PATCH
