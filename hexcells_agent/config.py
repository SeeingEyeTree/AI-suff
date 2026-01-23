"""Configuration for template-matching based board parsing."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Optional, Tuple


@dataclass(frozen=True)
class TemplateMatchingConfig:
    """Settings for CV template matching and region selection."""

    template_dir: Path = Path(__file__).resolve().parent.parent / "assets" / "templates"
    cell_templates: Dict[str, str] = field(
        default_factory=lambda: {
            "hidden": "cells/hidden.png",
            "revealed": "cells/revealed.png",
            "flagged": "cells/flagged.png",
        }
    )
    digit_templates: Dict[int, str] = field(
        default_factory=lambda: {digit: f"digits/{digit}.png" for digit in range(7)}
    )
    cell_match_threshold: float = 0.82
    digit_match_threshold: float = 0.78
    scale: float = 1.0
    screen_region: Optional[Tuple[int, int, int, int]] = None
    nms_distance: int = 8
    row_group_tolerance: int = 14
    digit_roi_scale: float = 0.55

    def cell_template_paths(self) -> Dict[str, Path]:
        """Return resolved file paths for cell templates."""
        return {name: self.template_dir / path for name, path in self.cell_templates.items()}

    def digit_template_paths(self) -> Dict[int, Path]:
        """Return resolved file paths for digit templates."""
        return {digit: self.template_dir / path for digit, path in self.digit_templates.items()}
