# Architecture

`Minesweeper` — локальная Python-игра внутри replicated product repo с разделением human/user entry, product knowledge, technical contour и planning contour.

## Runtime architecture
- `minesweeper.game` содержит игровое ядро: поле, клетки, генерацию мин, раскрытие областей, флаги, победу и поражение.
- `minesweeper.cli` содержит текстовый интерфейс первого playable pass.
- `minesweeper.__main__` даёт запуск через `python3 -m minesweeper`.
- `tests/*` проверяет ключевые правила без запуска интерактивного интерфейса.

## Constraint
Первый playable pass не зависит от GUI toolkit: в текущей среде отсутствует `tkinter`, а scope требует быстрый проверяемый результат без внешних зависимостей.
