from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from enum import Enum
import random


class GameState(str, Enum):
    PLAYING = "playing"
    WON = "won"
    LOST = "lost"


@dataclass
class Cell:
    mine: bool = False
    adjacent: int = 0
    revealed: bool = False
    flagged: bool = False


class MinesweeperGame:
    def __init__(self, width: int = 9, height: int = 9, mines: int = 10, rng: random.Random | None = None) -> None:
        if width < 2 or height < 2:
            raise ValueError("width and height must be at least 2")
        if mines < 1 or mines >= width * height:
            raise ValueError("mines must be between 1 and the number of cells minus one")
        self.width = width
        self.height = height
        self.mines = mines
        self._rng = rng or random.Random()
        self.reset()

    def reset(self) -> None:
        self.state = GameState.PLAYING
        self._mines_placed = False
        self._cells = [[Cell() for _ in range(self.width)] for _ in range(self.height)]

    def cell(self, x: int, y: int) -> Cell:
        self._require_inside(x, y)
        return self._cells[y][x]

    def neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        self._require_inside(x, y)
        result: list[tuple[int, int]] = []
        for ny in range(max(0, y - 1), min(self.height, y + 2)):
            for nx in range(max(0, x - 1), min(self.width, x + 2)):
                if nx != x or ny != y:
                    result.append((nx, ny))
        return result

    def reveal(self, x: int, y: int) -> set[tuple[int, int]]:
        self._require_inside(x, y)
        if self.state != GameState.PLAYING:
            return set()

        cell = self.cell(x, y)
        if cell.flagged or cell.revealed:
            return set()
        if not self._mines_placed:
            self._place_mines(first_x=x, first_y=y)

        changed: set[tuple[int, int]] = set()
        if cell.mine:
            cell.revealed = True
            self.state = GameState.LOST
            return {(x, y)}

        queue: deque[tuple[int, int]] = deque([(x, y)])
        while queue:
            cx, cy = queue.popleft()
            current = self.cell(cx, cy)
            if current.revealed or current.flagged:
                continue
            current.revealed = True
            changed.add((cx, cy))
            if current.adjacent == 0:
                for nx, ny in self.neighbors(cx, cy):
                    neighbor = self.cell(nx, ny)
                    if not neighbor.revealed and not neighbor.flagged and not neighbor.mine:
                        queue.append((nx, ny))

        if self._all_safe_cells_revealed():
            self.state = GameState.WON
        return changed

    def toggle_flag(self, x: int, y: int) -> bool:
        self._require_inside(x, y)
        if self.state != GameState.PLAYING:
            return False
        cell = self.cell(x, y)
        if cell.revealed:
            return False
        cell.flagged = not cell.flagged
        return True

    @property
    def remaining_mines(self) -> int:
        flagged = sum(1 for row in self._cells for cell in row if cell.flagged)
        return self.mines - flagged

    def visible_value(self, x: int, y: int, reveal_mines: bool = False) -> str:
        cell = self.cell(x, y)
        if cell.flagged and not (reveal_mines and cell.mine):
            return "F"
        if cell.revealed:
            if cell.mine:
                return "*"
            return str(cell.adjacent) if cell.adjacent else ""
        if reveal_mines and cell.mine:
            return "*"
        return ""

    def _place_mines(self, first_x: int, first_y: int) -> None:
        candidates = [(x, y) for y in range(self.height) for x in range(self.width) if (x, y) != (first_x, first_y)]
        for x, y in self._rng.sample(candidates, self.mines):
            self.cell(x, y).mine = True
        for y in range(self.height):
            for x in range(self.width):
                current = self.cell(x, y)
                current.adjacent = sum(1 for nx, ny in self.neighbors(x, y) if self.cell(nx, ny).mine)
        self._mines_placed = True

    def _all_safe_cells_revealed(self) -> bool:
        return all(cell.revealed or cell.mine for row in self._cells for cell in row)

    def _require_inside(self, x: int, y: int) -> None:
        if not 0 <= x < self.width or not 0 <= y < self.height:
            raise IndexError("cell coordinates are outside the board")
