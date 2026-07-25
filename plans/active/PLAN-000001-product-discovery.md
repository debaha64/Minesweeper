# PLAN-000001-product-discovery

Статус: active

Связь:
- ROAD: ROAD-000001
- BACK: BACK-000001

Product Unit: Minesweeper

Фаза SDLC: planning
Операционный режим: product-work
INTERVIEW_EVIDENCE_REF: IE-000001
OWNER_DECISION_REFS: OD-000001,OD-000002
PRODUCT_ACCEPTANCE_REF: none
ALLOWED_SURFACES: AGENTS.md::SOT_MODE,.git/**,docs/product/**,plans/active/PLAN-000001-product-discovery.md,logs/sessions.md,logs/decisions.md,logs/changes.md,logs/risks.md,logs/quality.md
Маршрут решений: PRODUCT_INPUT -> verified discovery -> owner-approved sot_files-to-sot_git transition -> отдельное решение владельца о реализации
Граница решения владельца: разрешены только локальный переход SoT и один local_git_route; product paths, реализация и внешние действия запрещены

Роли: researcher -> architect -> verifier
Gate: owner-approved-transition

## Цель

Зафиксировать и проверить контракт CLI-команды `count`, не изменяя существующий продуктовый baseline.

## Разрешено

1. Зафиксировать `PRODUCT_INPUT` как `IE-000001`.
2. Обновить discovery-документы в `docs/product/`.
3. Зафиксировать риски, факты изменений и результаты локальных проверок в разрешённых журналах.
4. Проверить существующий baseline, discovery-контур и локальные ссылки без Git и внешних действий.
5. Создать или квалифицировать локальный repository без remote, зафиксировать локальный baseline и единый transition checkpoint.
6. Изменить только `AGENTS.md::SOT_MODE` с `sot_files` на `sot_git` после разрешения `OD-000001`.

## Запрещено

1. Изменять `README.md`, `src/minesweeper.py` или `tests/test_minesweeper.py`.
2. Создавать remote, выполнять fetch, pull, push, PR, merge, tag, release или любые сетевые и внешние действия.
3. Начинать реализацию, создавать implementation decision, выполнять продуктовую приёмку или публикацию.

## DoD

1. Полный `PRODUCT_INPUT` связан с `IE-000001`, все обязательные слои закрыты.
2. Product identity и требования согласованы в `docs/product/`.
3. Существующие product paths и защищённые поверхности не изменены.
4. Существующие unit tests и `--smoke` проходят без записи bytecode в Product Unit.
5. `bp_check.py` проходит с `0 fail, 0 warn`.
6. `sot_git` имеет exact root, valid `HEAD`, ветку `main`, clean tree и remote absent.
7. `OD-000001` применён, `OD-000002` остаётся единственной active route-записью для `BACK-000001`.
8. После transition checkpoint работа останавливается на отдельном owner gate реализации.

## Блокер

1. none

## Разрешение глоссария discovery

Новые термины не требуются; существующего словаря достаточно.
