"""Terminal interface for the first playable Minesweeper pass."""

from __future__ import annotations

from .game import Game, GameStatus


HELP_TEXT = """Commands:
  o ROW COL      open a cell, for example: o 1 1
  f ROW COL      toggle a flag, for example: f 3 4
  q              quit
"""


def main() -> int:
    game = Game()
    print("Minesweeper: 9x9 board, 10 mines.")
    print(HELP_TEXT)

    while game.status is GameStatus.PLAYING:
        print(game.render())
        print(f"Flags left: {game.flags_left}")
        raw_command = input("> ").strip()
        if not raw_command:
            continue
        if raw_command.lower() in {"q", "quit", "exit"}:
            print("Game stopped.")
            return 0
        if raw_command.lower() in {"h", "help", "?"}:
            print(HELP_TEXT)
            continue

        try:
            action, row, column = _parse_command(raw_command)
            if action == "o":
                game.reveal(row, column)
            elif action == "f":
                game.toggle_flag(row, column)
            else:
                raise ValueError("Unknown command.")
        except ValueError as error:
            print(f"Invalid move: {error}")

    print(game.render(reveal_all=True))
    if game.status is GameStatus.WON:
        print("You won.")
    else:
        print("You hit a mine.")
    return 0


def _parse_command(raw_command: str) -> tuple[str, int, int]:
    parts = raw_command.split()
    if len(parts) != 3:
        raise ValueError("Use: o ROW COL or f ROW COL.")

    action = parts[0].lower()
    if action not in {"o", "open", "r", "reveal", "f", "flag"}:
        raise ValueError("Action must be open or flag.")

    try:
        row = int(parts[1]) - 1
        column = int(parts[2]) - 1
    except ValueError as error:
        raise ValueError("Row and column must be numbers.") from error

    canonical_action = "f" if action in {"f", "flag"} else "o"
    return canonical_action, row, column
