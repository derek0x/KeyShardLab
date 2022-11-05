"""Record tiny journal entries for each work session."""
from datetime import datetime
from pathlib import Path
from typing import List

NOTE_PATH = Path(__file__).resolve().parents[1] / "data" / "lab_notes.md"


def _ensure_note_dir() -> None:
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)


def append_note(note: str) -> None:
    """Add a timestamped note to the shared data file."""
    _ensure_note_dir()
    stamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M")
    with NOTE_PATH.open("a", encoding="utf-8") as handle:
        handle.write(f"{stamp} · {note}\n")


def read_notes() -> List[str]:
    """Read every note that has been recorded so far."""
    if not NOTE_PATH.exists():
        return []
    return [line.strip() for line in NOTE_PATH.read_text("utf-8").splitlines() if line.strip()]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Log a quick Lab note.")
    parser.add_argument("note", help="The text to add to the journal.")
    args = parser.parse_args()
    append_note(args.note)
    print("Note recorded.")
