# ChangeLog

## Индекс
- 2026-04-28 — Реализована первая playable desktop-версия Сапёра
- 2026-04-28 — Подтверждена текущая истина и открыт pass Python desktop Minesweeper

## 2026-04-28 — Реализована первая playable desktop-версия Сапёра

Связи: ROAD-000002, BACK-000002, PLAN-000002

### Изменения
- Добавлен пакет `minesweeper` с игровой моделью, Tkinter UI и запуском через `python3 -m minesweeper`.
- Добавлены unit-тесты игровой логики в `tests/*`.
- `README.md`, `Setup_Guide.md`, `Docs/User/*`, `Docs/Product/*` и `Docs/Technical/*` синхронизированы с desktop-версией.
- `ROAD-000002`, `BACK-000002` и `PLAN-000002` закрыты как выполненные.

## 2026-04-28 — Подтверждена текущая истина и открыт pass Python desktop Minesweeper

Связи: ROAD-000001, ROAD-000002, BACK-000001, BACK-000002, PLAN-000001, PLAN-000002

### Изменения
- `Docs/Discovery/Interview.md` переведён в подтверждённое состояние на основании запроса пользователя.
- `ROAD-000001`, `BACK-000001` и `PLAN-000001` закрыты как аналитический bootstrap-gate.
- Открыты `ROAD-000002`, `BACK-000002` и `PLAN-000002` для первой настольной версии `Сапёра` на Python.
