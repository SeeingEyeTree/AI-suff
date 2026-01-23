"""Board parsing utilities for Hexcells automation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import cv2
import numpy as np

from .config import TemplateMatchingConfig
from .state import Cell, Clue, GameState


@dataclass(frozen=True)
class TemplateMatch:
    """A detected template match in screen coordinates."""

    center: Tuple[int, int]
    score: float
    label: str
    size: Tuple[int, int]


def parse_board(image: np.ndarray, config: Optional[TemplateMatchingConfig] = None) -> GameState:
    """Parse a Hexcells board image into a structured ``GameState``.

    Args:
        image: A BGR or grayscale image of the active Hexcells board.
        config: Optional template-matching configuration overrides.

    Returns:
        A ``GameState`` instance containing detected cells, clues, and metadata.
    """
    config = config or TemplateMatchingConfig()
    gray = image
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    offset = (0, 0)
    if config.screen_region is not None:
        x, y, w, h = config.screen_region
        gray = gray[y : y + h, x : x + w]
        offset = (x, y)

    cell_templates = _load_templates(config.cell_template_paths(), config.scale)
    digit_templates = _load_templates(config.digit_template_paths(), config.scale)
    cell_matches = _collect_cell_matches(
        gray, cell_templates, config.cell_match_threshold, config.nms_distance
    )
    grid_cells = _assign_grid_coordinates(cell_matches, config.row_group_tolerance)

    cells: List[Cell] = []
    for row_index, row in enumerate(grid_cells):
        for col_index, match in enumerate(row):
            is_revealed = match.label == "revealed"
            is_flagged = match.label == "flagged"
            clue = None
            if is_revealed:
                roi = _extract_center_roi(gray, match.center, match.size, config.digit_roi_scale)
                digit = _match_digit_in_roi(roi, digit_templates, config.digit_match_threshold)
                if digit is not None:
                    clue = Clue(number=digit)
            screen_pos = (match.center[0] + offset[0], match.center[1] + offset[1])
            cells.append(
                Cell(
                    q=col_index,
                    r=row_index,
                    revealed=is_revealed,
                    marked=is_flagged,
                    clue=clue,
                    screen_pos=screen_pos,
                    s=-(col_index + row_index),
                )
            )

    metadata = {
        "screen_region": config.screen_region,
        "cell_matches": len(cell_matches),
        "digit_templates": sorted(digit_templates.keys()),
    }
    return GameState(cells=cells, image_shape=gray.shape, metadata=metadata)


def _load_templates(paths: Dict[object, Path], scale: float) -> Dict[object, np.ndarray]:
    templates: Dict[object, np.ndarray] = {}
    for key, path in paths.items():
        if not path.exists():
            continue
        template = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
        if template is None:
            continue
        if scale != 1.0:
            new_size = (int(template.shape[1] * scale), int(template.shape[0] * scale))
            template = cv2.resize(template, new_size, interpolation=cv2.INTER_AREA)
        templates[key] = template
    return templates


def _match_template_locations(
    image: np.ndarray, template: np.ndarray, threshold: float
) -> List[Tuple[int, int, float]]:
    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    y_coords, x_coords = np.where(result >= threshold)
    matches = [(int(x), int(y), float(result[y, x])) for x, y in zip(x_coords, y_coords)]
    matches.sort(key=lambda item: item[2], reverse=True)
    return matches


def _collect_cell_matches(
    image: np.ndarray,
    templates: Dict[str, np.ndarray],
    threshold: float,
    nms_distance: int,
) -> List[TemplateMatch]:
    candidates: List[TemplateMatch] = []
    for label, template in templates.items():
        height, width = template.shape[:2]
        for x, y, score in _match_template_locations(image, template, threshold):
            center = (x + width // 2, y + height // 2)
            candidates.append(TemplateMatch(center=center, score=score, label=label, size=(width, height)))
    candidates.sort(key=lambda item: item.score, reverse=True)
    selected: List[TemplateMatch] = []
    for candidate in candidates:
        if all(_distance(candidate.center, chosen.center) > nms_distance for chosen in selected):
            selected.append(candidate)
    return selected


def _assign_grid_coordinates(
    matches: Sequence[TemplateMatch], row_tolerance: int
) -> List[List[TemplateMatch]]:
    if not matches:
        return []
    sorted_matches = sorted(matches, key=lambda item: item.center[1])
    rows: List[List[TemplateMatch]] = []
    row_centers: List[float] = []
    for match in sorted_matches:
        if not rows:
            rows.append([match])
            row_centers.append(float(match.center[1]))
            continue
        if abs(match.center[1] - row_centers[-1]) <= row_tolerance:
            rows[-1].append(match)
            row_centers[-1] = float(np.mean([m.center[1] for m in rows[-1]]))
        else:
            rows.append([match])
            row_centers.append(float(match.center[1]))
    for row in rows:
        row.sort(key=lambda item: item.center[0])
    return rows


def _extract_center_roi(
    image: np.ndarray, center: Tuple[int, int], size: Tuple[int, int], scale: float
) -> np.ndarray:
    width = max(1, int(size[0] * scale))
    height = max(1, int(size[1] * scale))
    x_center, y_center = center
    x0 = max(0, x_center - width // 2)
    x1 = min(image.shape[1], x_center + width // 2)
    y0 = max(0, y_center - height // 2)
    y1 = min(image.shape[0], y_center + height // 2)
    return image[y0:y1, x0:x1]


def _match_digit_in_roi(
    roi: np.ndarray, templates: Dict[int, np.ndarray], threshold: float
) -> Optional[int]:
    if roi.size == 0 or not templates:
        return None
    best_digit = None
    best_score = threshold
    for digit, template in templates.items():
        if roi.shape[0] < template.shape[0] or roi.shape[1] < template.shape[1]:
            continue
        result = cv2.matchTemplate(roi, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)
        if max_val > best_score:
            best_score = float(max_val)
            best_digit = digit
    return best_digit


def _distance(a: Tuple[int, int], b: Tuple[int, int]) -> float:
    return float(np.hypot(a[0] - b[0], a[1] - b[1]))


def _extract_clue_from_cell(cell_image: np.ndarray) -> Clue | None:
    """Extract a clue (number/line) from a single cell image.

    Args:
        cell_image: Cropped grayscale image of a single hex cell.

    Returns:
        A ``Clue`` instance when a clue is detected, otherwise ``None``.
    """
    _ = cell_image
    return None
