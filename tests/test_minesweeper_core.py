import random
import unittest

from minesweeper.core import GameState, MinesweeperGame


class MinesweeperGameTest(unittest.TestCase):
    def test_first_reveal_is_safe(self) -> None:
        game = MinesweeperGame(width=4, height=4, mines=3, rng=random.Random(1))

        game.reveal(1, 1)

        self.assertFalse(game.cell(1, 1).mine)
        self.assertTrue(game.cell(1, 1).revealed)
        self.assertEqual(game.state, GameState.PLAYING)

    def test_flagged_cell_is_not_revealed(self) -> None:
        game = MinesweeperGame(width=3, height=3, mines=1, rng=random.Random(2))

        game.toggle_flag(0, 0)
        changed = game.reveal(0, 0)

        self.assertEqual(changed, set())
        self.assertTrue(game.cell(0, 0).flagged)
        self.assertFalse(game.cell(0, 0).revealed)

    def test_revealing_mine_loses_game(self) -> None:
        game = MinesweeperGame(width=2, height=2, mines=1, rng=random.Random(3))
        game.reveal(0, 0)
        mine = next((x, y) for y in range(game.height) for x in range(game.width) if game.cell(x, y).mine)

        game.reveal(*mine)

        self.assertEqual(game.state, GameState.LOST)

    def test_revealing_all_safe_cells_wins_game(self) -> None:
        game = MinesweeperGame(width=2, height=2, mines=1, rng=random.Random(4))

        for y in range(game.height):
            for x in range(game.width):
                if game.state == GameState.PLAYING and not game.cell(x, y).mine:
                    game.reveal(x, y)

        self.assertEqual(game.state, GameState.WON)


if __name__ == "__main__":
    unittest.main()
