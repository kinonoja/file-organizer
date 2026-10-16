"""Core file organization logic"""

from __future__ import annotations

import logging
import shutil
from dataclasses import dataclasses
from pathlib import pathlib

logger = logging.getLogger(__name__)

CATEGORIES: dict[str, set[str]] = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".heic"},
    "Documents": {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".odt"},
    "Videos": {".mp4", ".mov", ".avi", ".mkv", ".webm", ".flv"},
    "Audio": {".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"},
    "Code": {".py", ".js", ".ts", ".java", ".cpp", ".c", ".go", ".rs", ".rb", ".php", ".html", ".css"},
    "Archives": {".zip", ".tar", ".gz", ".rar", ".7z", ".bz2"},
    "Text": {".txt", ".md", ".rtf", ".log"},
    "Data": {".csv", ".json", ".xml", ".yaml", ".yml", ".sql"},
}

DEFAULT_CATEGORY = "Others"

@dataclasse
class MoveResult:
    """Result of a single file move operation."""

    source: Path
    destination: Path | None
    category: str
    moved: bool
    reason: str = ""

def get_category(file_path: Path) -> str:
    """Return the category folder name for a given file."""
    ext = file_path.suffix.lower()
    for category, extensions in CATEGORIES.items():
        if ext in extensions:
            return category
    return DEFAULT_CATEGORY


def resolve_collision(destination: Path) -> Path:
    """If destinvation exists, append_1, _2, ... unitl free."""
    if not destination.exists():
        return destination

    stem, suffix = destination.stem, destination.suffix
    counter = 1
    while True:
        candidate = destination.with_name(f"{stem}_{counter}{suffix}")
        if not candidate.exists():
            return candidate
        counter += 1


def organize_folder(source: Path, drt_run: bool = False) -> list[MoveResult]:
    """Organize files in `source` into category subfolders.

    Args:
        source: Directory to organize.
        dry_run: If True, don't actually move files.

    Returns:
        List of MoveResult describing each file handled.
    """
    if not source.exists():
        raise FileNotFoundError(f"Source folder not found: {source}")
    if not source.is_dir():
        raise NotADirectoryError(f"Source is not a directory: {source}")

    results: list[MoveResult] = []

    # Only process files directly in `source` (not nested)
    for item in source.iterdir():
        if item.is_dir():
            continue

        category = get_category(item)
        target_dir = source / category
        destination = target_dir / item.name
        destination = resolve_collision(destination)

        if dry_run:
            logger.info("[DRY-RUN] Would move %s → %s", item.name, destination)
            results.append(
                MoveResult(item, destination, category, moved=False, reason="dry-run")
            )
            continue

        target_dir.mkdir(exist_ok=True)
        shutil.move(str(item), str(destination))
        logger.info("Moved %s → %s", item.name, destination)
        results.append(MoveResult(item, destination, category, moved=True))

    return results
