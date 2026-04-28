from __future__ import annotations

import tkinter as tk
from tkinter import messagebox

from .engine import CellView, GameBoard, GameState


class MinesweeperApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Minesweeper")
        self.board = GameBoard()
        self.buttons: dict[tuple[int, int], tk.Button] = {}
        self.status = tk.StringVar()
        self._build_ui()
        self._refresh()

    def _build_ui(self) -> None:
        top = tk.Frame(self.root, padx=10, pady=8)
        top.grid(row=0, column=0, sticky="ew")
        top.columnconfigure(0, weight=1)

        tk.Label(top, textvariable=self.status, anchor="w").grid(row=0, column=0, sticky="ew")
        tk.Button(top, text="Restart", command=self.restart).grid(row=0, column=1, padx=(8, 0))

        grid = tk.Frame(self.root, padx=10, pady=(0, 10))
        grid.grid(row=1, column=0)
        for row in range(self.board.rows):
            for col in range(self.board.cols):
                button = tk.Button(
                    grid,
                    width=3,
                    height=1,
                    font=("TkDefaultFont", 11, "bold"),
                    command=lambda r=row, c=col: self.reveal(r, c),
                )
                button.grid(row=row, column=col)
                button.bind("<Button-3>", lambda event, r=row, c=col: self.toggle_flag(r, c))
                button.bind("<Control-Button-1>", lambda event, r=row, c=col: self.toggle_flag(r, c))
                self.buttons[(row, col)] = button

    def restart(self) -> None:
        self.board = GameBoard(rows=self.board.rows, cols=self.board.cols, mines=self.board.mine_count)
        self._refresh()

    def reveal(self, row: int, col: int) -> None:
        previous = self.board.state
        result = self.board.reveal(row, col)
        self._refresh()
        if previous not in {GameState.WON, GameState.LOST} and result.state == GameState.WON:
            messagebox.showinfo("Minesweeper", "You won.")
        elif previous not in {GameState.WON, GameState.LOST} and result.state == GameState.LOST:
            messagebox.showinfo("Minesweeper", "You hit a mine.")

    def toggle_flag(self, row: int, col: int) -> str:
        self.board.toggle_flag(row, col)
        self._refresh()
        return "break"

    def _refresh(self) -> None:
        cells = {(cell.row, cell.col): cell for cell in self.board.view()}
        for key, button in self.buttons.items():
            self._paint(button, cells[key])
            if self.board.state in {GameState.WON, GameState.LOST}:
                button.configure(state=tk.DISABLED)
        status = {
            GameState.READY: "Ready",
            GameState.PLAYING: "Playing",
            GameState.WON: "Won",
            GameState.LOST: "Lost",
        }[self.board.state]
        self.status.set(f"{status} | Mines: {self.board.mine_count} | Flags left: {self.board.flags_left}")

    def _paint(self, button: tk.Button, cell: CellView) -> None:
        button.configure(relief=tk.RAISED, state=tk.NORMAL, text="", bg="SystemButtonFace", fg="black")
        if cell.flagged and not cell.revealed:
            button.configure(text="F", fg="#b00020")
            return
        if not cell.revealed and not cell.mined:
            return
        button.configure(relief=tk.SUNKEN, bg="#e7e7e7")
        if cell.mined:
            button.configure(text="*", bg="#f3b3b3", fg="black")
        elif cell.adjacent_mines:
            button.configure(text=str(cell.adjacent_mines), fg=_NUMBER_COLORS.get(cell.adjacent_mines, "black"))
        button.configure(state=tk.DISABLED)


_NUMBER_COLORS = {
    1: "#1f5fbf",
    2: "#2f7d32",
    3: "#c62828",
    4: "#4527a0",
    5: "#8d3c16",
    6: "#00838f",
    7: "#212121",
    8: "#616161",
}


def main() -> None:
    root = tk.Tk()
    MinesweeperApp(root)
    root.mainloop()
