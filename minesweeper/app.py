from __future__ import annotations

import tkinter as tk
from tkinter import messagebox

from .core import GameState, MinesweeperGame


class MinesweeperApp:
    def __init__(self, width: int = 9, height: int = 9, mines: int = 10) -> None:
        self.game = MinesweeperGame(width=width, height=height, mines=mines)
        self.root = tk.Tk()
        self.root.title("Сапёр")
        self.status = tk.StringVar()
        self.buttons: dict[tuple[int, int], tk.Button] = {}
        self._build_layout()
        self._refresh_all()

    def run(self) -> None:
        self.root.mainloop()

    def _build_layout(self) -> None:
        top = tk.Frame(self.root, padx=8, pady=8)
        top.grid(row=0, column=0, sticky="ew")
        tk.Label(top, textvariable=self.status, width=18, anchor="w").grid(row=0, column=0)
        tk.Button(top, text="Новая игра", command=self._new_game).grid(row=0, column=1, padx=(8, 0))

        board = tk.Frame(self.root, padx=8, pady=(0, 8))
        board.grid(row=1, column=0)
        for y in range(self.game.height):
            for x in range(self.game.width):
                button = tk.Button(board, width=3, height=1, font=("TkDefaultFont", 11, "bold"))
                button.grid(row=y, column=x)
                button.configure(command=lambda cx=x, cy=y: self._reveal(cx, cy))
                button.bind("<Button-3>", lambda event, cx=x, cy=y: self._flag(cx, cy))
                button.bind("<Control-Button-1>", lambda event, cx=x, cy=y: self._flag(cx, cy))
                self.buttons[(x, y)] = button

    def _new_game(self) -> None:
        self.game.reset()
        self._refresh_all()

    def _reveal(self, x: int, y: int) -> None:
        self.game.reveal(x, y)
        self._refresh_all()
        self._show_final_message_if_needed()

    def _flag(self, x: int, y: int) -> str:
        self.game.toggle_flag(x, y)
        self._refresh_all()
        return "break"

    def _refresh_all(self) -> None:
        reveal_mines = self.game.state == GameState.LOST
        for y in range(self.game.height):
            for x in range(self.game.width):
                self._refresh_cell(x, y, reveal_mines=reveal_mines)
        if self.game.state == GameState.PLAYING:
            self.status.set(f"Мин осталось: {self.game.remaining_mines}")
        elif self.game.state == GameState.WON:
            self.status.set("Победа")
        else:
            self.status.set("Поражение")

    def _refresh_cell(self, x: int, y: int, reveal_mines: bool) -> None:
        cell = self.game.cell(x, y)
        button = self.buttons[(x, y)]
        value = self.game.visible_value(x, y, reveal_mines=reveal_mines)
        button.configure(text=value)
        if cell.revealed:
            button.configure(relief=tk.SUNKEN, state=tk.DISABLED, disabledforeground=self._value_color(value))
        elif value == "*":
            button.configure(relief=tk.RAISED, state=tk.DISABLED, disabledforeground="white", bg="#b00020")
        else:
            button.configure(relief=tk.RAISED, state=tk.NORMAL, fg=self._value_color(value), bg="SystemButtonFace")

    def _show_final_message_if_needed(self) -> None:
        if self.game.state == GameState.WON:
            messagebox.showinfo("Сапёр", "Победа! Все безопасные клетки открыты.")
        elif self.game.state == GameState.LOST:
            messagebox.showinfo("Сапёр", "Поражение. Вы открыли мину.")

    def _value_color(self, value: str) -> str:
        return {
            "1": "#1f5fbf",
            "2": "#1f7a1f",
            "3": "#b00020",
            "4": "#4b0082",
            "F": "#b36b00",
            "*": "white",
        }.get(value, "black")


def main() -> None:
    MinesweeperApp().run()
