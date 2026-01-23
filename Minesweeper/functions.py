from typing import List, Tuple, Optional
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


def find_next_move(board: Board) -> Optional[Action]:
    height = len(board)
    width = len(board[0]) if height > 0 else 0

    for y in range(height):
        for x in range(width):
            cell = board[y][x]
            if 1 <= cell <= 8:  # A revealed number
                neighbors = get_neighbors(x, y, width, height)
                flagged = [(nx, ny) for (nx, ny) in neighbors if board[ny][nx] == 9]
                unknown = [(nx, ny) for (nx, ny) in neighbors if board[ny][nx] == 0]

                # If number of flags == cell value -> all unknown are safe
                if len(flagged) == cell and unknown:
                    return ('left', unknown[0])

                # If number of flags + unknown == cell value -> all unknown are mines
                if len(flagged) + len(unknown) == cell and unknown:
                    return ('right', unknown[0])

    return None  # No safe move found


def find_safe_tile_recursive(board: Board) -> Optional[Action]:
    height = len(board)
    width = len(board[0]) if height > 0 else 0

    for y in range(height):
        for x in range(width):
            cell = board[y][x]
            if not (1 <= cell <= 8):
                continue

            neighbors = get_neighbors(x, y, width, height)
            flagged = [(nx, ny) for (nx, ny) in neighbors if board[ny][nx] == 9]
            unknown = [(nx, ny) for (nx, ny) in neighbors if board[ny][nx] == 0]

            # If we've flagged all mines, the rest must be safe
            if len(flagged) == cell and unknown:
                return ('left', unknown[0])

            # If remaining mines match unknowns, all unknowns must be mines
            if len(unknown) + len(flagged) == cell:
                return ('right', unknown[0])

            # Try chaining to a neighbor
            for (ux, uy) in unknown:
                # Find other numbers that see (ux, uy)
                for (sx, sy) in get_neighbors(ux, uy, width, height):
                    s_val = board[sy][sx]
                    if not (1 <= s_val <= 8):
                        continue

                    s_neighbors = get_neighbors(sx, sy, width, height)
                    s_flagged = [(nx, ny) for (nx, ny) in s_neighbors if board[ny][nx] == 9]
                    s_unknown = [(nx, ny) for (nx, ny) in s_neighbors if board[ny][nx] == 0]

                    if len(s_flagged) == s_val and (ux, uy) in s_unknown:
                        return ('left', (ux, uy))

                    if len(s_flagged) + len(s_unknown) == s_val and (ux, uy) in s_unknown:
                        return ('right', (ux, uy))

    return None

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