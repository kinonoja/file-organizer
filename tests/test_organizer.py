"""Tests for the file organizer."""

from pathlib import Path

import pytest

from src.organizer import get_category, organize_folder, resolve_collision


@pytest.mark.parametrize(
    "filename,expected",
    [
        ("photo.jpg", "Images"),
        ("resume.pdf", "Documents"),
        ("script.py", "Code"),
        ("song.mp3", "Audio"),
        ("clip.mp4", "Videos"),
        ("archive.zip", "Archives"),
        ("notes.txt", "Text"),
        ("data.csv", "Data"),
        ("unknown.xyz", "Others"),
        ("NO_EXTENSION", "Others"),
    ],
)
def test_get_category(filename: str, expected: str) -> None:
    assert get_category(Path(filename)) == expected


def test_resolve_collision_no_conflict(tmp_path: Path) -> None:
    target = tmp_path / "photo.jpg"
    assert resolve_collision(target) == target


def test_resolve_collision_with_conflict(tmp_path: Path) -> None:
    (tmp_path / "photo.jpg").touch()
    resolved = resolve_collision(tmp_path / "photo.jpg")
    assert resolved.name == "photo_1.jpg"


def test_organize_dry_run_does_not_move(tmp_path: Path) -> None:
    (tmp_path / "photo.jpg").touch()
    (tmp_path / "doc.pdf").touch()

    results = organize_folder(tmp_path, dry_run=True)

    assert len(results) == 2
    assert all(not r.moved for r in results)
    assert (tmp_path / "photo.jpg").exists()  # still there
    assert not (tmp_path / "Images").exists()  # not created


def test_organize_moves_files(tmp_path: Path) -> None:
    (tmp_path / "photo.jpg").touch()
    (tmp_path / "doc.pdf").touch()

    results = organize_folder(tmp_path, dry_run=False)

    assert len(results) == 2
    assert (tmp_path / "Images" / "photo.jpg").exists()
    assert (tmp_path / "Documents" / "doc.pdf").exists()
    assert not (tmp_path / "photo.jpg").exists()


def test_organize_handles_name_collision(tmp_path: Path) -> None:
    (tmp_path / "photo.jpg").touch()
    (tmp_path / "Images").mkdir()
    (tmp_path / "Images" / "photo.jpg").touch()  # pre-existing

    organize_folder(tmp_path, dry_run=False)

    assert (tmp_path / "Images" / "photo_1.jpg").exists()


def test_organize_missing_source_raises(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        organize_folder(tmp_path / "does_not_exist")