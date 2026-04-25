# Interfaces

## Стартовые интерфейсы
- human entry: `README.md`, `Docs/User/*`, `Setup_Guide.md`;
- agent entry: `AGENTS.md`;
- planning entry: `Plans/*`;
- structural check route: `scripts/dev-test.sh` с `BYTEPRESS_ROOT`;
- integration smoke route: `scripts/integration-smoke.sh` с `BYTEPRESS_ROOT`.

## Игровые интерфейсы
- запуск игры: `python3 -m minesweeper`;
- открытие клетки: `o ROW COL`;
- установка или снятие флага: `f ROW COL`;
- выход из партии: `q`;
- локальные тесты: `python3 -m unittest`.
