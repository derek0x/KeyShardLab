"""Load sample secrets or vault templates for quick prototyping."""
import json
import random
from pathlib import Path
from typing import Dict, List, Optional

TEMPLATE_FILE = Path(__file__).resolve().parents[1] / "data" / "template_secrets.json"


def load_templates() -> List[Dict[str, str]]:
    """Return every template defined under the data folder."""
    if not TEMPLATE_FILE.exists():
        return []
    with TEMPLATE_FILE.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def random_template() -> Optional[Dict[str, str]]:
    """Pick a random template for a quick start."""
    templates = load_templates()
    if not templates:
        return None
    return random.choice(templates)


def find_by_label(label: str) -> Optional[Dict[str, str]]:
    return next((tpl for tpl in load_templates() if tpl.get("label") == label), None)


if __name__ == "__main__":
    tpl = random_template()
    if not tpl:
        print("No templates available.")
    else:
        print("Random template:")
        for key, value in tpl.items():
            print(f"{key}: {value}")
