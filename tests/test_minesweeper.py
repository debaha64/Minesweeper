import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from minesweeper import adjacent_mines


class MinesweeperTests(unittest.TestCase):
    def test_adjacent_mines(self):
        self.assertEqual(adjacent_mines(["*.", ".."], 1, 1), 1)


if __name__ == "__main__":
    unittest.main()
