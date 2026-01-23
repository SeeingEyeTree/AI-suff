"""Orchestrate the Hexcells agent pipeline."""

from __future__ import annotations

from .actuator import apply_move
from pathlib import Path
from typing import Optional, Tuple

from .capture import capture_screen, preprocess_image
from .parser import parse_board
from .solver import find_safe_move


def run_once(
    *,
    capture_region: Optional[Tuple[int, int, int, int]] = None,
    template_dir: Optional[Path] = None,
    state_out: Optional[Path] = None,
    dry_run: bool = False,
) -> None:
    """Run one capture → parse → solve → act cycle."""
    image = capture_screen(region=capture_region)
    processed = preprocess_image(image)
    state = parse_board(processed, template_dir=template_dir)
    if state_out is not None:
        state.save(state_out)
    move = find_safe_move(state)
    if move is None:
        return
    if not dry_run:
        apply_move(move)


def main() -> None:
    """Entry point for running the Hexcells agent."""
    run_once()


if __name__ == "__main__":
    main()
