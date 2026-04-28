from __future__ import annotations

import random
import unittest

from minesweeper import Game, GameState


class GameTests(unittest.TestCase):
    def test_first_reveal_places_mines_away_from_first_cell(self) -> None:
        game = Game(rows=9, columns=9, mines=10, rng=random.Random(1))

        game.reveal(4, 4)

        self.assertEqual(game.state, GameState.ACTIVE)
        self.assertFalse(game.cell(4, 4).mine)
        self.assertFalse(any(game.cell(row, column).mine for row, column in game.neighbors(4, 4)))

    def test_flagged_cell_cannot_be_revealed(self) -> None:
        game = Game(rows=4, columns=4, mines=2, rng=random.Random(2))

        self.assertTrue(game.toggle_flag(1, 1))
        changed = game.reveal(1, 1)

        self.assertEqual(changed, set())
        self.assertTrue(game.cell(1, 1).flagged)
        self.assertFalse(game.cell(1, 1).revealed)

    def test_revealing_all_safe_cells_wins(self) -> None:
        game = Game(rows=2, columns=2, mines=1, rng=random.Random(3))
        game.reveal(0, 0)

        for row in range(game.rows):
            for column in range(game.columns):
                if not game.cell(row, column).mine:
                    game.reveal(row, column)

        self.assertEqual(game.state, GameState.WON)

    def test_revealing_mine_loses(self) -> None:
        game = Game(rows=3, columns=3, mines=1, rng=random.Random(4))
        game.reveal(0, 0)
        mine_position = next(
            (row, column)
            for row in range(game.rows)
            for column in range(game.columns)
            if game.cell(row, column).mine
        )

        game.reveal(*mine_position)

        self.assertEqual(game.state, GameState.LOST)

    def test_invalid_board_rejected(self) -> None:
        with self.assertRaises(ValueError):
            Game(rows=1, columns=1, mines=1)


if __name__ == "__main__":
    unittest.main()
