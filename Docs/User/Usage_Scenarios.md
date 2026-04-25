# Usage Scenarios

## Сценарий 1. Войти в replicated product repo
- Прочитать `../../README.md` и `First_Start.md`.
- Проверить current truth в `../../Docs/Discovery/Interview.md`.
- Подготовить среду по `../../Setup_Guide.md`.
- Проверить structural contour через `scripts/dev-test.sh`.

## Сценарий 2. Сыграть локальную партию
- Выполнить `python3 -m minesweeper` из корня репозитория.
- Открывать клетки командой `o ROW COL`.
- Ставить или снимать флаги командой `f ROW COL`.
- Завершить игру победой, поражением или командой `q`.

## Сценарий 3. Запустить новый pass с агентом
- Найти current stage/task/pass в `../../Plans/*`.
- Сформулировать pass через `Pass_Request.md`.
- Направить агента на работу через contracts продукта.

## Сценарий 4. Работать с продуктовым knowledge contour
- `Docs/Product/*` — прикладная рамка продукта.
- `Docs/Technical/*` — стартовый technical contour.
- `Logs/*` — факты и quality evidence.
