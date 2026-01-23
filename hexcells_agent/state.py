"""Data structures for representing Hexcells game state."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
import json
from pathlib import Path
from typing import Iterable, List, Optional, Tuple


@dataclass(frozen=True)
class Clue:
    """A clue attached to a revealed cell.

    Attributes:
        number: The numeric clue (0-6) if present.
        line: Optional line constraint descriptor (e.g., "---" or "- -").
    """

    number: Optional[int] = None
    line: Optional[str] = None


@dataclass
class Cell:
    """A single hex cell in axial coordinates.

    Attributes:
        q: Axial column coordinate.
        r: Axial row coordinate.
        revealed: Whether the cell is revealed.
        marked: Whether the cell is flagged as a mine.
        clue: Optional clue information for revealed cells.
        screen_pos: Optional (x, y) pixel position for click actions.
        s: Optional cube coordinate for hex grids (q + r + s == 0).
        inferred_mine: Whether the solver inferred this cell is a mine.
        inferred_safe: Whether the solver inferred this cell is safe.
    """

    q: int
    r: int
    revealed: bool = False
    marked: bool = False
    clue: Optional[Clue] = None
    screen_pos: Optional[Tuple[int, int]] = None
    s: Optional[int] = None
    inferred_mine: bool = False
    inferred_safe: bool = False


@dataclass(frozen=True)
class HexGridGeometry:
    """Metadata about the hex grid coordinate system."""

    coordinate_system: str = "axial"
    layout: str = "pointy"


@dataclass
class GameState:
    """Complete game state for the current Hexcells board."""

    cells: List[Cell] = field(default_factory=list)
    geometry: HexGridGeometry = field(default_factory=HexGridGeometry)
    image_shape: Optional[Tuple[int, int]] = None
    metadata: dict = field(default_factory=dict)

    def cell_at(self, q: int, r: int) -> Optional[Cell]:
        """Return the cell at axial coordinate (q, r) if it exists."""
        for cell in self.cells:
            if cell.q == q and cell.r == r:
                return cell
        return None

    def neighbors(self, cell: Cell) -> List[Cell]:
        """Return neighboring cells using axial hex directions."""
        directions = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]
        neighbors: List[Cell] = []
        for dq, dr in directions:
            neighbor = self.cell_at(cell.q + dq, cell.r + dr)
            if neighbor is not None:
                neighbors.append(neighbor)
        return neighbors

    def to_json(self) -> str:
        """Serialize the game state to a JSON string."""
        return json.dumps(asdict(self))

    @classmethod
    def from_json(cls, payload: str) -> "GameState":
        """Deserialize a game state from a JSON string."""
        data = json.loads(payload)
        cells = []
        for cell in data.get("cells", []):
            clue_data = cell.get("clue")
            clue = Clue(**clue_data) if isinstance(clue_data, dict) else None
            screen_pos = cell.get("screen_pos")
            if screen_pos is not None:
                screen_pos = tuple(screen_pos)
            cells.append(
                Cell(
                    q=cell["q"],
                    r=cell["r"],
                    revealed=cell.get("revealed", False),
                    marked=cell.get("marked", False),
                    clue=clue,
                    screen_pos=screen_pos,
                    s=cell.get("s"),
                    inferred_mine=cell.get("inferred_mine", False),
                    inferred_safe=cell.get("inferred_safe", False),
                )
            )
        geometry_data = data.get("geometry") or {}
        geometry = HexGridGeometry(**geometry_data) if isinstance(geometry_data, dict) else HexGridGeometry()
        image_shape = data.get("image_shape")
        if image_shape is not None:
            image_shape = tuple(image_shape)
        return cls(cells=cells, geometry=geometry, image_shape=image_shape, metadata=data.get("metadata", {}))

    def save(self, path: str | Path) -> None:
        """Save the game state to disk as JSON."""
        Path(path).write_text(self.to_json(), encoding="utf-8")

    @classmethod
    def load(cls, path: str | Path) -> "GameState":
        """Load a game state from disk."""
        return cls.from_json(Path(path).read_text(encoding="utf-8"))


@dataclass
class Move:
    """A safe move inferred by the solver.

    Attributes:
        action: One of "reveal", "flag", or "chord".
        cell: The target cell to act on.
        screen_pos: Optional (x, y) pixel coordinates for GUI interaction.
    """

    action: str
    cell: Cell
    screen_pos: Optional[Tuple[int, int]] = None

    def with_screen_pos(self) -> "Move":
        """Return a copy of the move using the cell's screen position if present."""
        screen_pos = self.screen_pos or self.cell.screen_pos
        return Move(action=self.action, cell=self.cell, screen_pos=screen_pos)


def iter_revealed_cells(cells: Iterable[Cell]) -> Iterable[Cell]:
    """Yield only revealed cells from an iterable."""
    return (cell for cell in cells if cell.revealed)
