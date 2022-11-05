from pathlib import Path

from src import note_keeper


def test_append_and_read(tmp_path):
    test_path = tmp_path / "notes.md"
    note_keeper.NOTE_PATH = test_path
    note_keeper.append_note("Evening entry")
    notes = note_keeper.read_notes()
    assert any("Evening entry" in line for line in notes)


def test_read_empty(tmp_path):
    note_keeper.NOTE_PATH = tmp_path / "missing.md"
    assert note_keeper.read_notes() == []
*** End Patch
PATCH
