#!/usr/bin/env python3
import argparse
import sys


def adjacent_mines(board, row, column):
    total = 0
    for row_index in range(max(0, row - 1), min(len(board), row + 2)):
        for column_index in range(max(0, column - 1), min(len(board[0]), column + 2)):
            if (row_index, column_index) != (row, column):
                total += board[row_index][column_index] == "*"
    return total


def validate_count_input(board, row, column):
    if not board or not board[0]:
        raise ValueError("board must be non-empty")

    width = len(board[0])
    if any(len(board_row) != width for board_row in board):
        raise ValueError("board must be rectangular")
    if any(cell not in "*." for board_row in board for cell in board_row):
        raise ValueError("board may contain only '*' and '.'")
    if row < 0 or row >= len(board) or column < 0 or column >= width:
        raise ValueError("coordinates are outside the board")


def build_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    count_parser = subparsers.add_parser("count")
    count_parser.add_argument("--row", type=int, required=True)
    count_parser.add_argument("--column", type=int, required=True)
    count_parser.add_argument("board", nargs="+", metavar="board-row")
    return parser


def main(argv=None):
    arguments = sys.argv[1:] if argv is None else argv
    if arguments == ["--smoke"]:
        assert adjacent_mines(["*.", ".."], 1, 1) == 1
        print("Minesweeper smoke: PASS")
        return 0

    args = build_parser().parse_args(arguments)
    try:
        validate_count_input(args.board, args.row, args.column)
    except ValueError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    print(adjacent_mines(args.board, args.row, args.column))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
