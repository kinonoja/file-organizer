"""Command-line interface for the file organizer."""

from __future__ import annotations

import logging
import sys
from pathlib import Path

import click

from src.organizer import organize_folder


def setup_logging(verbose: bool) -> None:
    """Configure logging to file + console."""
    level = logging.DEBUG if verbose else logging.INFO
    handlers: list[logging.Handler] = [logging.FileHandler("organizer.log")]

    if verbose:
        handlers.append(logging.StreamHandler(sys.stdout))

    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=handlers,
    )


@click.command()
@click.option(
    "--source",
    "-s",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    default=Path.home() / "Downloads",
    help="Folder to organize (default: ~/Downloads)",
)
@click.option("--dry-run", is_flag=True, help="Preview moves without doing them")
@click.option("--verbose", "-v", is_flag=True, help="Print progress to console")
def main(source: Path, dry_run: bool, verbose: bool) -> None:
    """Organize a messy folder into categorized subfolders."""
    setup_logging(verbose)

    mode = "DRY RUN" if dry_run else "LIVE"
    click.echo(f" Organizing: {source}")
    click.echo(f" Mode: {mode}\n")

    try:
        results = organize_folder(source, dry_run=dry_run)
    except (FileNotFoundError, NotADirectoryError) as e:
        click.secho(f" Error: {e}", fg="red")
        sys.exit(1)

    if not results:
        click.secho("** Nothing to organize — folder is already clean!", fg="green")
        return

    # Summary
    by_category: dict[str, int] = {}
    for r in results:
        by_category[r.category] = by_category.get(r.category, 0) + 1

    click.echo("\n Summary:")
    for cat, count in sorted(by_category.items()):
        click.echo(f"  • {cat}: {count} file(s)")

    action = "Would move" if dry_run else "Moved"
    click.secho(f"\n {action} {len(results)} file(s).", fg="green")


if __name__ == "__main__":
    main()