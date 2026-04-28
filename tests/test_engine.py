import unittest

from minesweeper import GameBoard, GameState


class GameBoardTests(unittest.TestCase):
    def test_first_reveal_never_hits_mine(self) -> None:
        board = GameBoard(rows=4, cols=4, mines=5, seed=7)

        result = board.reveal(0, 0)

        self.assertNotEqual(result.state, GameState.LOST)
        self.assertFalse(board.has_mine(0, 0))
        self.assertGreater(board.revealed_count, 0)

    def test_flagged_cell_is_not_revealed(self) -> None:
        board = GameBoard(rows=3, cols=3, mines=1, seed=2)

        board.toggle_flag(1, 1)
        result = board.reveal(1, 1)

        self.assertEqual(result.changed, ())
        self.assertEqual(board.revealed_count, 0)
        self.assertEqual(board.flags_left, 0)

    def test_win_after_all_safe_cells_revealed(self) -> None:
        board = GameBoard(rows=2, cols=2, mines=1, seed=1)
        board.reveal(0, 0)

        for row in range(board.rows):
            for col in range(board.cols):
                if not board.has_mine(row, col):
                    board.reveal(row, col)

        self.assertEqual(board.state, GameState.WON)
        self.assertEqual(board.flags_left, 0)

    def test_out_of_bounds_raises(self) -> None:
        board = GameBoard()

        with self.assertRaises(IndexError):
            board.reveal(99, 99)


if __name__ == "__main__":
    unittest.main()
