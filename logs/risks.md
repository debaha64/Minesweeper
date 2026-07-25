# Риски

Фиксирует риски, блокеры и выбранные меры контроля.

RECORD_ID: RISK-000001
PLAN_ID: PLAN-000001
DATE: 2026-07-25
SUMMARY: CLI validation must preserve exact stdout stderr and exit-code boundaries
SOURCE_REF: codexlog:.codex/codex-20260725-192940.raw.log#lines=97-126

- Дата: 2026-07-25
- Связь ROAD/BACK/PLAN: ROAD-000001 / BACK-000001 / PLAN-000001
- ID риска: RISK-000001
- Описание: ошибки доски или координат могут оставить частичный stdout либо вернуть неверный exit code.
- Причина: новая CLI-граница добавляет разбор аргументов и валидацию поверх существующей функции.
- Влияние: нарушение детерминированного пользовательского контракта.
- Снижение риска: отдельные тесты invalid board и invalid coordinates проверяют exit `2`, пустой stdout и непустой краткий stderr.
- Статус: open до реализации и проверки.
- Связанные требования: `docs/product/prd.md`, `docs/product/dods.md`.
- Свидетельство: `IE-000001`.
- Следующий шаг: отдельный implementation gate после verified discovery.

RECORD_ID: RISK-000002
PLAN_ID: PLAN-000001
DATE: 2026-07-25
SUMMARY: Existing smoke behavior can regress when CLI dispatch is added
SOURCE_REF: codexlog:.codex/codex-20260725-192940.raw.log#lines=97-126

- Дата: 2026-07-25
- Связь ROAD/BACK/PLAN: ROAD-000001 / BACK-000001 / PLAN-000001
- ID риска: RISK-000002
- Описание: новый command dispatcher может изменить существующее поведение `--smoke`.
- Причина: оба режима используют один entrypoint `src/minesweeper.py`.
- Влияние: регрессия принятого baseline-сценария.
- Снижение риска: сохранить существующий smoke и включить его в обязательный DoD.
- Статус: open до реализации и проверки.
- Связанные требования: `docs/product/prd.md`, `docs/product/dods.md`.
- Свидетельство: `IE-000001`.
- Следующий шаг: отдельный implementation gate после verified discovery.
