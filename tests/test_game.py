import unittest

from minesweeper import Game, GameStatus


class GameTests(unittest.TestCase):
    def test_first_reveal_is_safe(self) -> None:
        game = Game(rows=4, columns=4, mines=3, seed=1)

        game.reveal(0, 0)

        self.assertFalse(game.cell(0, 0).has_mine)
        self.assertTrue(game.cell(0, 0).revealed)
        self.assertEqual(game.status, GameStatus.PLAYING)

    def test_flagged_cell_is_not_revealed(self) -> None:
        game = Game(rows=4, columns=4, mines=3, seed=2)

        game.toggle_flag(1, 1)
        game.reveal(1, 1)

        self.assertTrue(game.cell(1, 1).flagged)
        self.assertFalse(game.cell(1, 1).revealed)

    def test_revealing_all_safe_cells_wins(self) -> None:
        game = Game(rows=2, columns=2, mines=1, seed=3)
        game.reveal(0, 0)

        for row in range(game.rows):
            for column in range(game.columns):
                cell = game.cell(row, column)
                if not cell.has_mine:
                    game.reveal(row, column)

        self.assertEqual(game.status, GameStatus.WON)

    def test_hitting_mine_loses(self) -> None:
        game = Game(rows=3, columns=3, mines=1, seed=4)
        game.reveal(0, 0)
        mine_position = next(
            (row, column)
            for row in range(game.rows)
            for column in range(game.columns)
            if game.cell(row, column).has_mine
        )

        game.reveal(*mine_position)

        self.assertEqual(game.status, GameStatus.LOST)


if __name__ == "__main__":
    unittest.main()
