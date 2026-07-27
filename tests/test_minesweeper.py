import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "src" / "minesweeper.py"

sys.path.insert(0, str(ROOT / "src"))
from minesweeper import adjacent_mines


class MinesweeperTests(unittest.TestCase):
    def run_cli(self, *arguments):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *arguments],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_adjacent_mines_center(self):
        self.assertEqual(adjacent_mines(["*.*", "...", "*.*"], 1, 1), 4)

    def test_adjacent_mines_edge(self):
        self.assertEqual(adjacent_mines(["...", "***", "..."], 0, 1), 3)

    def test_adjacent_mines_corner(self):
        self.assertEqual(adjacent_mines([".*", "*."], 0, 0), 2)

    def test_count_cli_prints_one_line(self):
        completed = self.run_cli("count", "--row", "1", "--column", "1", "*.", "..")

        self.assertEqual(completed.returncode, 0)
        self.assertEqual(completed.stdout, "1\n")
        self.assertEqual(completed.stderr, "")

    def test_invalid_coordinates(self):
        for row, column in (("-1", "0"), ("2", "0"), ("0", "2")):
            with self.subTest(row=row, column=column):
                completed = self.run_cli(
                    "count", "--row", row, "--column", column, "*.", ".."
                )

                self.assertEqual(completed.returncode, 2)
                self.assertEqual(completed.stdout, "")
                self.assertIn("coordinates", completed.stderr)

    def test_invalid_board(self):
        boards = (
            ("*.", "."),
            ("*x", ".."),
            ("",),
        )
        for board in boards:
            with self.subTest(board=board):
                completed = self.run_cli(
                    "count", "--row", "0", "--column", "0", *board
                )

                self.assertEqual(completed.returncode, 2)
                self.assertEqual(completed.stdout, "")
                self.assertTrue(completed.stderr.startswith("error: board"))

    def test_smoke_is_preserved(self):
        completed = self.run_cli("--smoke")

        self.assertEqual(completed.returncode, 0)
        self.assertEqual(completed.stdout, "Minesweeper smoke: PASS\n")
        self.assertEqual(completed.stderr, "")


if __name__ == "__main__":
    unittest.main()
