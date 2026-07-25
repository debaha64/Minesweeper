# PLAN-000001-product-discovery

Статус: active

Связь:
- ROAD: ROAD-000001
- BACK: BACK-000001

Product Unit: Minesweeper

Фаза SDLC: approval
Операционный режим: product-work
INTERVIEW_EVIDENCE_REF: IE-000001
OWNER_DECISION_REFS: OD-000001,OD-000002
PRODUCT_ACCEPTANCE_REF: none
ALLOWED_SURFACES: .git/**,plans/active/PLAN-000001-product-discovery.md,logs/decisions.md,logs/changes.md,logs/quality.md
Маршрут решений: PRODUCT_INPUT -> verified discovery -> verified sot_files-to-sot_git transition -> GATE-GITHUB-BOOTSTRAP
Граница решения владельца: локальный переход завершён; до отдельного GATE-GITHUB-BOOTSTRAP product paths, реализация, remote и внешние действия запрещены

Роли: researcher -> architect -> verifier
Gate: owner-decision-required

## Цель

Зафиксировать и проверить контракт CLI-команды `count`, не изменяя существующий продуктовый baseline.

## Разрешено

1. Зафиксировать `PRODUCT_INPUT` как `IE-000001`.
2. Обновить discovery-документы в `docs/product/`.
3. Зафиксировать риски, факты изменений и результаты локальных проверок в разрешённых журналах.
4. Проверить существующий baseline, discovery-контур и локальные ссылки без Git и внешних действий.
5. Зафиксировать завершённый локальный transition checkpoint и результаты его проверки.

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
8. После transition checkpoint работа останавливается перед отдельным `GATE-GITHUB-BOOTSTRAP`.

## Transition checkpoint

- BASELINE_COMMIT: `4a649dbe77768f11d194cc71b431162c0a651882`
- SOT_TRANSITION: `sot_files -> sot_git`
- TRANSITION_DECISION: `OD-000001` (`applied`)
- LOCAL_GIT_ROUTE: `OD-000002` (`active`)
- PRODUCT_PATHS: unchanged
- REMOTE_AND_EXTERNAL_ACTIONS: not performed
- NEXT_GATE: `GATE-GITHUB-BOOTSTRAP`

## Блокер

1. none

## Разрешение глоссария discovery

Новые термины не требуются; существующего словаря достаточно.
