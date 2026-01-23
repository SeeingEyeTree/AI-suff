"""Board parsing utilities for Hexcells automation."""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional

import cv2
import numpy as np

from .state import Cell, Clue, GameState


def parse_board(image: np.ndarray, template_dir: Optional[Path] = None) -> GameState:
    """Parse a Hexcells board image into a structured ``GameState``.

    Args:
        image: A BGR or grayscale image of the active Hexcells board.
        template_dir: Optional directory of templates to aid parsing.

    Returns:
        A ``GameState`` instance containing detected cells, clues, and metadata.
    """
    gray = image
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Placeholder detection logic: real implementation would detect hex contours,
    # classify clues, and map them into axial coordinates.
    cells: List[Cell] = []

    metadata = {}
    if template_dir is not None:
        metadata["template_dir"] = str(template_dir)

    return GameState(cells=cells, image_shape=gray.shape, metadata=metadata)


def _extract_clue_from_cell(cell_image: np.ndarray) -> Clue | None:
    """Extract a clue (number/line) from a single cell image.

    Args:
        cell_image: Cropped grayscale image of a single hex cell.

    Returns:
        A ``Clue`` instance when a clue is detected, otherwise ``None``.
    """
    _ = cell_image
    return None
