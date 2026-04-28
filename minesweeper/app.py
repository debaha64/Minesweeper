from __future__ import annotations

import tkinter as tk
from tkinter import messagebox

from .game import Cell, Game, GameState


class MinesweeperApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Minesweeper")
        self.game = Game()
        self.buttons: list[list[tk.Button]] = []
        self.status_var = tk.StringVar()
        self._build()
        self._sync_status()

    def _build(self) -> None:
        toolbar = tk.Frame(self.root, padx=10, pady=8)
        toolbar.pack(fill=tk.X)

        tk.Button(toolbar, text="New game", command=self.reset).pack(side=tk.LEFT)
        tk.Label(toolbar, textvariable=self.status_var, padx=12).pack(side=tk.LEFT)

        board = tk.Frame(self.root, padx=10, pady=10)
        board.pack()

        for row in range(self.game.rows):
            button_row: list[tk.Button] = []
            for column in range(self.game.columns):
                button = tk.Button(
                    board,
                    width=3,
                    height=1,
                    font=("TkDefaultFont", 12, "bold"),
                    command=lambda r=row, c=column: self.reveal(r, c),
                )
                button.bind("<Button-3>", lambda event, r=row, c=column: self.toggle_flag(r, c))
                button.bind("<Control-Button-1>", lambda event, r=row, c=column: self.toggle_flag(r, c))
                button.grid(row=row, column=column, sticky="nsew")
                button_row.append(button)
            self.buttons.append(button_row)

    def reset(self) -> None:
        self.game = Game()
        for row in range(self.game.rows):
            for column in range(self.game.columns):
                self._paint_cell(row, column)
        self._sync_status()

    def reveal(self, row: int, column: int) -> None:
        self.game.reveal(row, column)
        self._paint_board()
        self._sync_status()
        self._show_terminal_message()

    def toggle_flag(self, row: int, column: int) -> str:
        self.game.toggle_flag(row, column)
        self._paint_cell(row, column)
        self._sync_status()
        return "break"

    def _paint_board(self) -> None:
        for row in range(self.game.rows):
            for column in range(self.game.columns):
                self._paint_cell(row, column)

    def _paint_cell(self, row: int, column: int) -> None:
        cell = self.game.cell(row, column)
        button = self.buttons[row][column]
        button.configure(
            text=self._cell_text(cell),
            relief=tk.SUNKEN if cell.revealed else tk.RAISED,
            state=tk.DISABLED if cell.revealed or self.game.state in {GameState.WON, GameState.LOST} else tk.NORMAL,
            disabledforeground=self._cell_color(cell),
        )
        if not cell.revealed:
            button.configure(foreground="#111111")

    def _cell_text(self, cell: Cell) -> str:
        if cell.flagged and not cell.revealed:
            return "F"
        if not cell.revealed:
            return ""
        if cell.mine:
            return "*"
        if cell.adjacent_mines:
            return str(cell.adjacent_mines)
        return ""

    def _cell_color(self, cell: Cell) -> str:
        if cell.mine:
            return "#b00020"
        colors = {
            1: "#0b57d0",
            2: "#188038",
            3: "#d93025",
            4: "#6f42c1",
            5: "#a50e0e",
            6: "#007b83",
            7: "#202124",
            8: "#5f6368",
        }
        return colors.get(cell.adjacent_mines, "#202124")

    def _sync_status(self) -> None:
        if self.game.state == GameState.WON:
            text = "Won"
        elif self.game.state == GameState.LOST:
            text = "Lost"
        else:
            text = f"Mines: {self.game.flags_left}"
        self.status_var.set(text)

    def _show_terminal_message(self) -> None:
        if self.game.state == GameState.WON:
            messagebox.showinfo("Minesweeper", "You won")
        elif self.game.state == GameState.LOST:
            messagebox.showinfo("Minesweeper", "You hit a mine")


def main() -> None:
    root = tk.Tk()
    MinesweeperApp(root)
    root.mainloop()
