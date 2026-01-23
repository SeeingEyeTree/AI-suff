"""Apply solver moves to the Hexcells UI."""

from __future__ import annotations

from typing import Tuple

import pyautogui

from .state import Move


def apply_move(move: Move) -> None:
    """Apply a move using pyautogui.

    Args:
        move: The ``Move`` returned by ``find_safe_move``.

    Raises:
        ValueError: If the move has no screen position assigned.
    """
    move = move.with_screen_pos()
    if move.screen_pos is None:
        raise ValueError("Move has no screen coordinates for GUI interaction.")

    x, y = _normalize_position(move.screen_pos)

    if move.action == "reveal":
        pyautogui.click(x, y, button="left")
    elif move.action == "flag":
        pyautogui.click(x, y, button="right")
    elif move.action == "chord":
        pyautogui.click(x, y, button="middle")
    else:
        raise ValueError(f"Unsupported move action: {move.action}")


def _normalize_position(position: Tuple[int, int]) -> Tuple[int, int]:
    """Return integer pixel coordinates for a GUI click."""
    x, y = position
    return int(x), int(y)
