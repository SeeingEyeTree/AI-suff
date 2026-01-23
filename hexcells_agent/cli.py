"""Command-line interface for the Hexcells agent."""

from __future__ import annotations

import argparse
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple


@dataclass(frozen=True)
class CliOptions:
    """Container for parsed CLI arguments."""

    capture_region: Optional[Tuple[int, int, int, int]]
    template_dir: Optional[Path]
    state_out: Optional[Path]
    dry_run: bool
    debug: bool


def _parse_region(value: str) -> Tuple[int, int, int, int]:
    parts = [part for part in value.replace(" ", "").split(",") if part]
    if len(parts) != 4:
        raise argparse.ArgumentTypeError(
            "--capture-region must be four comma-separated integers: left,top,width,height"
        )
    try:
        left, top, width, height = (int(part) for part in parts)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("--capture-region values must be integers") from exc
    return left, top, width, height


def build_parser() -> argparse.ArgumentParser:
    """Create the argument parser for the CLI."""
    parser = argparse.ArgumentParser(description="Hexcells automation agent")
    parser.add_argument(
        "--capture-region",
        type=_parse_region,
        help="Optional capture region as left,top,width,height",
    )
    parser.add_argument(
        "--template-dir",
        type=Path,
        help="Directory containing image templates for board parsing",
    )
    parser.add_argument(
        "--state-out",
        type=Path,
        help="Path to write the parsed game state JSON",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run the pipeline without applying UI actions",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging",
    )
    return parser


def parse_args(argv: Optional[list[str]] = None) -> CliOptions:
    """Parse command-line arguments into a ``CliOptions`` object."""
    parser = build_parser()
    args = parser.parse_args(argv)
    return CliOptions(
        capture_region=args.capture_region,
        template_dir=args.template_dir,
        state_out=args.state_out,
        dry_run=args.dry_run,
        debug=args.debug,
    )


def configure_logging(debug: bool) -> None:
    """Configure application logging."""
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=level, format="%(message)s")
