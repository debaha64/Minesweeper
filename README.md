# Minesweeper

Minesweeper — локальная игра «Сапёр» на Python внутри replicated product repo.

`README.md` — карта для человека.
`AGENTS.md` — карта для агента.

## Запуск игры
```bash
python3 -m minesweeper
```

Первая playable версия использует текстовый интерфейс без внешних Python-зависимостей: поле 9x9, 10 мин, команды `o ROW COL` для открытия клетки и `f ROW COL` для флага.

## Стартовый маршрут
1. Прочитать `Docs/User/First_Start.md`.
2. Прочитать `Docs/Terms/Base_Terms.md`.
3. Прочитать `Docs/Discovery/Interview.md` и проверить current truth.
4. Подготовить среду по `Setup_Guide.md`.
5. Проверить current stage/task/pass в `Plans/*`.
6. Использовать `scripts/dev-test.sh`, если нужен structural check через `BytePress`.
7. Использовать `scripts/reset-product-start.sh`, если ранний product-start сорвался и нужен cleanup route.
8. Использовать `scripts/integration-smoke.sh`, если нужен minimal integration handoff check.

## Доменная карта
- `Docs/Discovery/*` — current-truth и интервью продукта.
- `Docs/User/*` — human-facing layer продукта.
- `Docs/Product/*` — прикладная рамка продукта.
- `Docs/Technical/*` — стартовый technical contour продукта.
- `Plans/*` — current roadmap, backlog и current plan продукта.
- `Logs/*` — факты, изменения и quality evidence продукта.
- `Adapters/*` — модельный contour продукта.
- `scripts/*` — project entry scripts.
