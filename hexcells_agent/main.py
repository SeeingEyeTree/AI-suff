"""Orchestrate the Hexcells agent pipeline."""

from __future__ import annotations

from .actuator import apply_move
from .capture import capture_screen, preprocess_image
from .parser import parse_board
from .solver import find_safe_move


def run_once() -> None:
    """Run one capture → parse → solve → act cycle."""
    image = capture_screen()
    processed = preprocess_image(image)
    state = parse_board(processed)
    move = find_safe_move(state)
    if move is None:
        return
    apply_move(move)


def main() -> None:
    """Entry point for running the Hexcells agent."""
    run_once()


if __name__ == "__main__":
    main()
