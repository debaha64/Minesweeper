#!/usr/bin/env python3
import sys


def adjacent_mines(board, row, column):
    total = 0
    for row_index in range(max(0, row - 1), min(len(board), row + 2)):
        for column_index in range(max(0, column - 1), min(len(board[0]), column + 2)):
            if (row_index, column_index) != (row, column):
                total += board[row_index][column_index] == "*"
    return total


if __name__ == "__main__" and sys.argv[1:] == ["--smoke"]:
    assert adjacent_mines(["*.", ".."], 1, 1) == 1
    print("Minesweeper smoke: PASS")
