# Изменения

Фиксирует факты изменения артефактов после реальной работы в этой Product Unit.

RECORD_ID: CHANGE-000001
PLAN_ID: PLAN-000001
DATE: 2026-07-25
SUMMARY: Discovery contract and evidence recorded without product-path changes
SOURCE_REF: codexlog:.codex/codex-20260725-230039.raw.log#lines=198-198

- Дата: 2026-07-25
- Связь ROAD/BACK/PLAN: ROAD-000001 / BACK-000001 / PLAN-000001
- Содержание: открыт discovery PLAN, `PRODUCT_INPUT` связан с `IE-000001`, продуктовый смысл и риски высушены в канонические документы.
- Изменённые файлы: `plans/active/PLAN-000001-product-discovery.md`, `logs/sessions.md`, `logs/risks.md`, `docs/product/product-brief.md`, `docs/product/product-passport.md`, `docs/product/jtbd.md`, `docs/product/prd.md`, `docs/product/dods.md`.
- Проверка связанных артефактов: ссылки PLAN, IE и product identity проверены `bp_check.py`.
- Свидетельство: `IE-000001`; runtime edit summary в `SOURCE_REF`.
- Что не выполнялось: `README.md`, `src/`, `tests/`, защищённые поверхности, Git, переход режима, сеть, внешние действия и реализация не изменялись.
- Следующий шаг: verified discovery и отдельный owner gate.

RECORD_ID: CHANGE-000002
PLAN_ID: PLAN-000001
DATE: 2026-07-26
SUMMARY: Owner-approved local sot_files to sot_git transition checkpoint recorded and candidate-verified
SOURCE_REF: codexlog:.codex/codex-20260726-023743.raw.log#lines=441-488

- Дата: 2026-07-26
- Связь ROAD/BACK/PLAN: ROAD-000001 / BACK-000001 / PLAN-000001
- Содержание: применён единый локальный transition checkpoint `sot_files -> sot_git`; `OD-000001` переведён в `applied`, `OD-000002` сохранён как единственный active `local_git_route`, PLAN остановлен перед `GATE-GITHUB-BOOTSTRAP`.
- Изменённые файлы: `AGENTS.md`, `docs/product/product-passport.md`, `plans/active/PLAN-000001-product-discovery.md`, `logs/decisions.md`, `logs/changes.md`, `logs/quality.md`.
- Проверка связанных артефактов: clean candidate commit `e0c8525107e040ff25f8601424159b613d5707e2` проверен полным локальным набором для `sot_git`.
- Свидетельство: pre-transition baseline `4a649dbe77768f11d194cc71b431162c0a651882`; candidate commit, проверки и product hashes находятся в `SOURCE_REF`.
- Что не выполнялось: product paths не изменялись; реализация, remote, fetch, pull, push, сеть, GitHub write, приёмка и публикация не выполнялись.
- Следующий шаг: остановиться перед отдельным `GATE-GITHUB-BOOTSTRAP`.
