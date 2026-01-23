from typing import Dict, List, Optional, Tuple
from collections import deque
from typing import Set
from pyautogui import click, moveTo
from math import floor
from time import sleep

Action = Tuple[str, Tuple[int, int]]  # ('clear' or 'flag', (x, y))
Board = List[List[int]]


def add_to_board(board, x_positions, y_positions, value):
    #thing = [x_positions,y_positions]
    for i in range(len(x_positions)):
        board[x_positions[i]][y_positions[i]] = value
    return board


def detect_enclosed_regions(board: Board) -> List[Tuple[int, int]]:
    height = len(board)
    width = len(board[0]) if height > 0 else 0
    visited = [[False for _ in range(width)] for _ in range(height)]
    safe_to_clear = []

    def touches_edge(x, y):
        return x == 0 or y == 0 or x == width - 1 or y == height - 1

    for y in range(height):
        for x in range(width):
            if board[y][x] != 0 or visited[y][x]:
                continue

            region = []
            queue = deque([(x, y)])
            enclosed = True

            while queue:
                cx, cy = queue.popleft()
                if visited[cy][cx]:
                    continue
                visited[cy][cx] = True
                region.append((cx, cy))

                if touches_edge(cx, cy):
                    enclosed = False

                for nx, ny in get_neighbors(cx, cy, width, height):
                    if board[ny][nx] == 0 and not visited[ny][nx]:
                        queue.append((nx, ny))

            if enclosed:
                safe_to_clear.extend(region)

    return safe_to_clear


def get_neighbors(x: int, y: int, width: int, height: int) -> List[Tuple[int, int]]:
    neighbors = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height:
                neighbors.append((nx, ny))
    return neighbors


UNKNOWN = 0
FLAGGED = 9


def _is_number(cell: int) -> bool:
    return 1 <= cell <= 8


def _collect_constraints(board: Board) -> List[Tuple[Set[Tuple[int, int]], int]]:
    height = len(board)
    width = len(board[0]) if height > 0 else 0
    constraints = []

    for y in range(height):
        for x in range(width):
            cell = board[y][x]
            if not _is_number(cell):
                continue

            neighbors = get_neighbors(x, y, width, height)
            flagged = [(nx, ny) for (nx, ny) in neighbors if board[ny][nx] == FLAGGED]
            unknown = [(nx, ny) for (nx, ny) in neighbors if board[ny][nx] == UNKNOWN]

            remaining = cell - len(flagged)
            if remaining < 0 or not unknown:
                continue

            constraints.append((set(unknown), remaining))

    return constraints


def find_next_move(board: Board) -> Optional[Action]:
    height = len(board)
    width = len(board[0]) if height > 0 else 0

    for y in range(height):
        for x in range(width):
            cell = board[y][x]
            if not _is_number(cell):
                continue

            neighbors = get_neighbors(x, y, width, height)
            flagged = [(nx, ny) for (nx, ny) in neighbors if board[ny][nx] == FLAGGED]
            unknown = [(nx, ny) for (nx, ny) in neighbors if board[ny][nx] == UNKNOWN]

            remaining = cell - len(flagged)

            # If number of flags == cell value -> all unknown are safe
            if remaining == 0 and unknown:
                return ('left', unknown[0])

            # If number of flags + unknown == cell value -> all unknown are mines
            if remaining == len(unknown) and unknown:
                return ('right', unknown[0])

    return None  # No safe move found


def find_safe_tile_recursive(board: Board) -> Optional[Action]:
    immediate_move = find_next_move(board)
    if immediate_move:
        return immediate_move

    constraints = _collect_constraints(board)

    # Subset inference: if constraint A is subset of B, use the difference.
    for i, (a_tiles, a_remaining) in enumerate(constraints):
        for b_tiles, b_remaining in constraints[i + 1:]:
            if not a_tiles or not b_tiles:
                continue

            if a_tiles.issubset(b_tiles):
                diff = b_tiles - a_tiles
                if not diff:
                    continue
                if a_remaining == b_remaining:
                    return ('left', sorted(diff)[0])
                if b_remaining - a_remaining == len(diff):
                    return ('right', sorted(diff)[0])
            elif b_tiles.issubset(a_tiles):
                diff = a_tiles - b_tiles
                if not diff:
                    continue
                if a_remaining == b_remaining:
                    return ('left', sorted(diff)[0])
                if a_remaining - b_remaining == len(diff):
                    return ('right', sorted(diff)[0])

    # No guaranteed moves: pick the lowest-risk unknown tile.
    height = len(board)
    width = len(board[0]) if height > 0 else 0
    unknown_tiles = [
        (x, y)
        for y in range(height)
        for x in range(width)
        if board[y][x] == UNKNOWN
    ]
    if not unknown_tiles:
        return None

    tile_probabilities: Dict[Tuple[int, int], List[float]] = {
        tile: [] for tile in unknown_tiles
    }
    for tiles, remaining in constraints:
        if not tiles:
            continue
        probability = remaining / len(tiles)
        for tile in tiles:
            if tile in tile_probabilities:
                tile_probabilities[tile].append(probability)

    best_tile = None
    best_score = None
    for tile, probs in tile_probabilities.items():
        if probs:
            score = sum(probs) / len(probs)
        else:
            score = 1.0  # no info, assume worst
        if best_score is None or score < best_score:
            best_score = score
            best_tile = tile

    if best_tile is None:
        return None

    return ('left', best_tile)

def check_tile(x,y,rl,board):
    x = floor(831 + 19 + x * 37.4583333333)
    y = floor(522 + 19 + y * 37.55)
    click(x = x, y = y, button=rl)
    sleep(0.8)
    return board
    #moveTo(500,500)



if __name__ == "__main__":
    board = [9, 1, 8, 8, 8, 1, 1, 1, 8, 1, 9, 1, 8, 1, 9, 9, 1, 1, 1, 3, 9, 3, 1, 1],
    [1, 1, 1, 1, 1, 1, 9, 1, 8, 1, 1, 1, 1, 3, 4, 3, 1, 2, 9, 4, 9, 3, 9, 1],
    [8, 8, 2, 9, 3, 2, 2, 2, 1, 8, 8, 8, 1, 9, 9, 1, 8, 2, 9, 4, 3, 4, 2, 1],
    [8, 8, 2, 9, 9, 2, 1, 9, 3, 2, 1, 8, 1, 3, 3, 3, 1, 2, 2, 3, 9, 9, 1, 8],
    [8, 8, 1, 3, 9, 2, 1, 2, 9, 9, 2, 1, 1, 2, 9, 2, 9, 1, 1, 9, 3, 3, 3, 2],
    [8, 8, 1, 3, 3, 2, 8, 1, 2, 3, 9, 1, 1, 9, 2, 2, 2, 2, 2, 1, 1, 1, 9, 9],
    [1, 1, 2, 9, 9, 3, 1, 2, 1, 2, 1, 1, 2, 3, 3, 1, 2, 9, 2, 8, 8, 1, 3, 3],
    [9, 2, 3, 9, 9, 3, 9, 2, 9, 1, 8, 8, 1, 9, 9, 2, 3, 9, 2, 8, 8, 8, 2, 9],
    [2, 4, 9, 4, 3, 3, 2, 2, 1, 1, 8, 8, 1, 2, 3, 3, 9, 2, 1, 8, 8, 8, 2, 9],
    [9, 3, 9, 2, 1, 9, 2, 1, 1, 8, 8, 8, 8, 8, 1, 9, 2, 1, 1, 2, 2, 1, 1, 1],
    [1, 2, 1, 1, 1, 1, 3, 9, 4, 2, 1, 8, 8, 8, 1, 1, 2, 1, 2, 9, 9, 4, 2, 1],
    [8, 8, 8, 1, 1, 1, 2, 9, 9, 9, 1, 8, 1, 1, 1, 8, 1, 9, 3, 5, 9, 9, 9, 1],
    [8, 8, 8, 1, 9, 1, 1, 3, 0, 3, 1, 8, 1, 9, 2, 1, 3, 3, 0, 0, 0, 4, 2, 1],
    [1, 1, 1, 2, 2, 1, 8, 1, 0, 1, 1, 2, 3, 2, 0, 0, 0, 0, 0, 0, 0, 2, 8, 8],
    [9, 1, 1, 9, 2, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 8, 8],
    [2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 8],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 9, 1, 8],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 2, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 3, 9],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    print(find_safe_tile_recursive(board))
