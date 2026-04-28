from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import random
from typing import Iterable


class GameState(str, Enum):
    READY = "ready"
    PLAYING = "playing"
    WON = "won"
    LOST = "lost"


@dataclass(frozen=True)
class GameResult:
    state: GameState
    changed: tuple[tuple[int, int], ...]


@dataclass(frozen=True)
class CellView:
    row: int
    col: int
    revealed: bool
    flagged: bool
    mined: bool
    adjacent_mines: int


class GameBoard:
    def __init__(
        self,
        rows: int = 9,
        cols: int = 9,
        mines: int = 10,
        seed: int | None = None,
    ) -> None:
        if rows < 2 or cols < 2:
            raise ValueError("Board must be at least 2x2.")
        if mines < 1 or mines >= rows * cols:
            raise ValueError("Mine count must be between 1 and cell_count - 1.")
        self.rows = rows
        self.cols = cols
        self.mine_count = mines
        self._rng = random.Random(seed)
        self._mines: set[tuple[int, int]] = set()
        self._revealed: set[tuple[int, int]] = set()
        self._flags: set[tuple[int, int]] = set()
        self.state = GameState.READY

    @property
    def flags_left(self) -> int:
        return self.mine_count - len(self._flags)

    @property
    def revealed_count(self) -> int:
        return len(self._revealed)

    def in_bounds(self, row: int, col: int) -> bool:
        return 0 <= row < self.rows and 0 <= col < self.cols

    def has_mine(self, row: int, col: int) -> bool:
        self._require_bounds(row, col)
        return (row, col) in self._mines

    def adjacent_mines(self, row: int, col: int) -> int:
        self._require_bounds(row, col)
        return sum((nr, nc) in self._mines for nr, nc in self.neighbors(row, col))

    def neighbors(self, row: int, col: int) -> Iterable[tuple[int, int]]:
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr = row + dr
                nc = col + dc
                if self.in_bounds(nr, nc):
                    yield nr, nc

    def toggle_flag(self, row: int, col: int) -> GameResult:
        self._require_bounds(row, col)
        cell = (row, col)
        if self.state in {GameState.WON, GameState.LOST} or cell in self._revealed:
            return GameResult(self.state, ())
        if cell in self._flags:
            self._flags.remove(cell)
        else:
            self._flags.add(cell)
        return GameResult(self.state, (cell,))

    def reveal(self, row: int, col: int) -> GameResult:
        self._require_bounds(row, col)
        if self.state in {GameState.WON, GameState.LOST}:
            return GameResult(self.state, ())
        start = (row, col)
        if start in self._flags:
            return GameResult(self.state, ())
        if not self._mines:
            self._place_mines(avoid=start)
        self.state = GameState.PLAYING
        if start in self._mines:
            self._revealed.add(start)
            self.state = GameState.LOST
            return GameResult(self.state, tuple(sorted(self._mines | {start})))

        changed = self._reveal_safe_area(start)
        if self._is_complete():
            self.state = GameState.WON
            self._flags.update(self._mines)
            changed = tuple(sorted(set(changed) | self._mines))
        return GameResult(self.state, changed)

    def view(self, reveal_mines: bool = False) -> tuple[CellView, ...]:
        cells: list[CellView] = []
        for row in range(self.rows):
            for col in range(self.cols):
                cell = (row, col)
                mined = cell in self._mines
                cells.append(
                    CellView(
                        row=row,
                        col=col,
                        revealed=cell in self._revealed,
                        flagged=cell in self._flags,
                        mined=mined and (reveal_mines or self.state in {GameState.WON, GameState.LOST}),
                        adjacent_mines=self.adjacent_mines(row, col) if self._mines else 0,
                    )
                )
        return tuple(cells)

    def _place_mines(self, avoid: tuple[int, int]) -> None:
        candidates = [(row, col) for row in range(self.rows) for col in range(self.cols) if (row, col) != avoid]
        self._mines = set(self._rng.sample(candidates, self.mine_count))

    def _reveal_safe_area(self, start: tuple[int, int]) -> tuple[tuple[int, int], ...]:
        changed: set[tuple[int, int]] = set()
        pending = [start]
        while pending:
            cell = pending.pop()
            if cell in self._revealed or cell in self._flags:
                continue
            self._revealed.add(cell)
            changed.add(cell)
            row, col = cell
            if self.adjacent_mines(row, col) != 0:
                continue
            for neighbor in self.neighbors(row, col):
                if neighbor not in self._revealed and neighbor not in self._mines:
                    pending.append(neighbor)
        return tuple(sorted(changed))

    def _is_complete(self) -> bool:
        safe_cells = self.rows * self.cols - self.mine_count
        return len(self._revealed) == safe_cells

    def _require_bounds(self, row: int, col: int) -> None:
        if not self.in_bounds(row, col):
            raise IndexError(f"Cell out of bounds: {row}, {col}")
