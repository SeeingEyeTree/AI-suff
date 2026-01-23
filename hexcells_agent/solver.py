"""Deterministic solver logic for Hexcells."""

from __future__ import annotations

from typing import Optional

from .state import GameState, Move


def find_safe_move(state: GameState) -> Optional[Move]:
    """Find a deterministic safe move using constraint propagation.

    Args:
        state: Current ``GameState`` parsed from the board.

    Returns:
        A ``Move`` to execute (reveal/flag/chord), or ``None`` when no safe move
        can be deduced.
    """
    for cell in state.cells:
        if not cell.revealed or cell.clue is None or cell.clue.number is None:
            continue

        neighbors = state.neighbors(cell)
        flagged = [n for n in neighbors if n.marked]
        unknown = [n for n in neighbors if not n.revealed and not n.marked]
        target = cell.clue.number

        if target == len(flagged) and unknown:
            return Move(action="reveal", cell=unknown[0]).with_screen_pos()

        if target == len(flagged) + len(unknown) and unknown:
            return Move(action="flag", cell=unknown[0]).with_screen_pos()

    return None
