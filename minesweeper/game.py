from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import random
from typing import Iterable


class GameState(str, Enum):
    READY = "ready"
    ACTIVE = "active"
    WON = "won"
    LOST = "lost"


@dataclass
class Cell:
    mine: bool = False
    revealed: bool = False
    flagged: bool = False
    adjacent_mines: int = 0


class Game:
    """Rules engine for a single Minesweeper board."""

    def __init__(
        self,
        rows: int = 9,
        columns: int = 9,
        mines: int = 10,
        rng: random.Random | None = None,
    ) -> None:
        if rows <= 0 or columns <= 0:
            raise ValueError("rows and columns must be positive")
        if mines <= 0:
            raise ValueError("mines must be positive")
        if mines >= rows * columns:
            raise ValueError("mines must leave at least one safe cell")

        self.rows = rows
        self.columns = columns
        self.mine_count = mines
        self._rng = rng or random.Random()
        self.state = GameState.READY
        self._mines_placed = False
        self.grid = [[Cell() for _ in range(columns)] for _ in range(rows)]

    @property
    def flags_left(self) -> int:
        return self.mine_count - sum(cell.flagged for row in self.grid for cell in row)

    @property
    def revealed_count(self) -> int:
        return sum(cell.revealed for row in self.grid for cell in row)

    def cell(self, row: int, column: int) -> Cell:
        self._validate_position(row, column)
        return self.grid[row][column]

    def neighbors(self, row: int, column: int) -> Iterable[tuple[int, int]]:
        self._validate_position(row, column)
        for next_row in range(max(0, row - 1), min(self.rows, row + 2)):
            for next_column in range(max(0, column - 1), min(self.columns, column + 2)):
                if (next_row, next_column) != (row, column):
                    yield next_row, next_column

    def toggle_flag(self, row: int, column: int) -> bool:
        self._validate_position(row, column)
        if self.state in {GameState.WON, GameState.LOST}:
            return False
        cell = self.grid[row][column]
        if cell.revealed:
            return False
        cell.flagged = not cell.flagged
        return True

    def reveal(self, row: int, column: int) -> set[tuple[int, int]]:
        self._validate_position(row, column)
        if self.state in {GameState.WON, GameState.LOST}:
            return set()

        if not self._mines_placed:
            self._place_mines(row, column)
            self.state = GameState.ACTIVE

        cell = self.grid[row][column]
        if cell.flagged or cell.revealed:
            return set()

        changed = self._reveal_area(row, column)
        if cell.mine:
            self.state = GameState.LOST
            self._reveal_all_mines()
            return changed

        if self._all_safe_cells_revealed():
            self.state = GameState.WON
        return changed

    def _place_mines(self, first_row: int, first_column: int) -> None:
        protected = {(first_row, first_column), *set(self.neighbors(first_row, first_column))}
        all_positions = {
            (row, column)
            for row in range(self.rows)
            for column in range(self.columns)
        }
        candidates = list(all_positions - protected)
        if len(candidates) < self.mine_count:
            candidates = list(all_positions - {(first_row, first_column)})

        for row, column in self._rng.sample(candidates, self.mine_count):
            self.grid[row][column].mine = True

        for row in range(self.rows):
            for column in range(self.columns):
                self.grid[row][column].adjacent_mines = sum(
                    1 for n_row, n_column in self.neighbors(row, column)
                    if self.grid[n_row][n_column].mine
                )
        self._mines_placed = True

    def _reveal_area(self, row: int, column: int) -> set[tuple[int, int]]:
        changed: set[tuple[int, int]] = set()
        pending = [(row, column)]

        while pending:
            current_row, current_column = pending.pop()
            cell = self.grid[current_row][current_column]
            if cell.revealed or cell.flagged:
                continue
            cell.revealed = True
            changed.add((current_row, current_column))

            if cell.mine or cell.adjacent_mines:
                continue
            for neighbor in self.neighbors(current_row, current_column):
                next_cell = self.grid[neighbor[0]][neighbor[1]]
                if not next_cell.revealed and not next_cell.flagged:
                    pending.append(neighbor)

        return changed

    def _reveal_all_mines(self) -> None:
        for row in self.grid:
            for cell in row:
                if cell.mine:
                    cell.revealed = True

    def _all_safe_cells_revealed(self) -> bool:
        safe_cells = self.rows * self.columns - self.mine_count
        return self.revealed_count == safe_cells

    def _validate_position(self, row: int, column: int) -> None:
        if not (0 <= row < self.rows and 0 <= column < self.columns):
            raise IndexError("cell position is outside the board")
