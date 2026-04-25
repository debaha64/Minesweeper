"""Core Minesweeper rules."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from enum import Enum
import random


class GameStatus(str, Enum):
    PLAYING = "playing"
    WON = "won"
    LOST = "lost"


@dataclass
class Cell:
    has_mine: bool = False
    adjacent_mines: int = 0
    revealed: bool = False
    flagged: bool = False


class Game:
    """A first-click-safe Minesweeper board."""

    def __init__(
        self,
        rows: int = 9,
        columns: int = 9,
        mines: int = 10,
        seed: int | None = None,
    ) -> None:
        if rows < 2 or columns < 2:
            raise ValueError("Board must be at least 2x2.")
        if mines < 1 or mines >= rows * columns:
            raise ValueError("Mine count must fit inside the board.")

        self.rows = rows
        self.columns = columns
        self.mine_count = mines
        self.status = GameStatus.PLAYING
        self._rng = random.Random(seed)
        self._mines_planted = False
        self._cells = [[Cell() for _ in range(columns)] for _ in range(rows)]

    @property
    def flags_left(self) -> int:
        return self.mine_count - sum(
            1 for row in self._cells for cell in row if cell.flagged
        )

    def cell(self, row: int, column: int) -> Cell:
        self._validate_position(row, column)
        return self._cells[row][column]

    def toggle_flag(self, row: int, column: int) -> None:
        self._validate_active_move(row, column)
        cell = self._cells[row][column]
        if not cell.revealed:
            cell.flagged = not cell.flagged

    def reveal(self, row: int, column: int) -> None:
        self._validate_active_move(row, column)
        if not self._mines_planted:
            self._plant_mines(exclude=(row, column))

        cell = self._cells[row][column]
        if cell.flagged or cell.revealed:
            return

        if cell.has_mine:
            cell.revealed = True
            self.status = GameStatus.LOST
            self._reveal_all_mines()
            return

        self._reveal_safe_area(row, column)
        if self._all_safe_cells_revealed():
            self.status = GameStatus.WON
            self._flag_all_mines()

    def render(self, reveal_all: bool = False) -> str:
        width = len(str(self.columns))
        header = " " * (width + 1) + " ".join(str(index + 1) for index in range(self.columns))
        lines = [header]
        for row_index, row in enumerate(self._cells):
            cells = [self._render_cell(cell, reveal_all) for cell in row]
            lines.append(f"{row_index + 1:>{width}} " + " ".join(cells))
        return "\n".join(lines)

    def _plant_mines(self, exclude: tuple[int, int]) -> None:
        positions = [
            (row, column)
            for row in range(self.rows)
            for column in range(self.columns)
            if (row, column) != exclude
        ]
        for row, column in self._rng.sample(positions, self.mine_count):
            self._cells[row][column].has_mine = True

        for row in range(self.rows):
            for column in range(self.columns):
                self._cells[row][column].adjacent_mines = sum(
                    1
                    for near_row, near_column in self._neighbors(row, column)
                    if self._cells[near_row][near_column].has_mine
                )
        self._mines_planted = True

    def _reveal_safe_area(self, start_row: int, start_column: int) -> None:
        queue: deque[tuple[int, int]] = deque([(start_row, start_column)])
        while queue:
            row, column = queue.popleft()
            cell = self._cells[row][column]
            if cell.revealed or cell.flagged:
                continue
            cell.revealed = True
            if cell.adjacent_mines != 0:
                continue
            for neighbor in self._neighbors(row, column):
                queue.append(neighbor)

    def _neighbors(self, row: int, column: int) -> list[tuple[int, int]]:
        positions: list[tuple[int, int]] = []
        for row_delta in (-1, 0, 1):
            for column_delta in (-1, 0, 1):
                if row_delta == 0 and column_delta == 0:
                    continue
                near_row = row + row_delta
                near_column = column + column_delta
                if 0 <= near_row < self.rows and 0 <= near_column < self.columns:
                    positions.append((near_row, near_column))
        return positions

    def _all_safe_cells_revealed(self) -> bool:
        return all(
            cell.revealed or cell.has_mine for row in self._cells for cell in row
        )

    def _reveal_all_mines(self) -> None:
        for row in self._cells:
            for cell in row:
                if cell.has_mine:
                    cell.revealed = True

    def _flag_all_mines(self) -> None:
        for row in self._cells:
            for cell in row:
                if cell.has_mine:
                    cell.flagged = True

    def _validate_active_move(self, row: int, column: int) -> None:
        if self.status is not GameStatus.PLAYING:
            raise ValueError("Game is already finished.")
        self._validate_position(row, column)

    def _validate_position(self, row: int, column: int) -> None:
        if not (0 <= row < self.rows and 0 <= column < self.columns):
            raise ValueError("Cell is outside the board.")

    @staticmethod
    def _render_cell(cell: Cell, reveal_all: bool) -> str:
        if cell.flagged and not reveal_all:
            return "F"
        if not cell.revealed and not reveal_all:
            return "."
        if cell.has_mine:
            return "*"
        if cell.adjacent_mines == 0:
            return " "
        return str(cell.adjacent_mines)
