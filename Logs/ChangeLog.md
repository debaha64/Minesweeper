# ChangeLog

## Индекс
- 2026-04-25 — Подтверждена discovery current truth первого product-start pass.
- 2026-04-25 — Реализован первый playable pass игры «Сапёр» на Python.

## 2026-04-25 — Подтверждена discovery current truth первого product-start pass
Ветка: `feature/000001-confirm-current-truth`
Связи: ROAD-000001, BACK-000001, PLAN-000001

### Изменения
- `Docs/Discovery/Interview.md` переведён из `Не_подтверждена` в `Подтверждена` на основании явных ответов пользователя.
- `Plans/Roadmap.md`, `Plans/Backlog.md`, `Plans/MSW-000001-product-initialization.md` синхронизированы с закрытием discovery-only gate.

## 2026-04-25 — Реализован первый playable pass игры «Сапёр» на Python
Ветка: `feature/000001-confirm-current-truth`
Связи: ROAD-000002, BACK-000002, PLAN-000002

### Изменения
- Добавлен package `minesweeper` с игровым ядром, CLI и entrypoint `python3 -m minesweeper`.
- Добавлены локальные тесты игровой логики.
- Product, user и technical docs обновлены под первый playable scope.
- `Plans/*` обновлены под предметный pass `PLAN-000002`.
