# PLAN-000001-product-discovery

Статус: active

Связь:
- ROAD: ROAD-000001
- BACK: BACK-000001

Product Unit: Minesweeper

Фаза SDLC: approval
Операционный режим: product-work
INTERVIEW_EVIDENCE_REF: IE-000001
OWNER_DECISION_REFS: OD-000001,OD-000002,OD-000003
PRODUCT_ACCEPTANCE_REF: none
ALLOWED_SURFACES: .git/**,plans/active/PLAN-000001-product-discovery.md,logs/decisions.md,logs/changes.md,logs/quality.md
Маршрут решений: PRODUCT_INPUT -> verified discovery -> verified sot_files-to-sot_git transition -> verified GATE-GITHUB-BOOTSTRAP -> verified GATE-GITHUB-CONFIG -> verified sot_git-to-sot_github transition -> GATE-IMPLEMENTATION
Граница решения владельца: переход `sot_git -> sot_github` завершён; до отдельного GATE-IMPLEMENTATION product paths, push, GitHub write, Settings и реализация запрещены

Роли: researcher -> architect -> verifier
Gate: owner-decision-required

## Цель

Зафиксировать и проверить контракт CLI-команды `count`, не изменяя существующий продуктовый baseline.

## Разрешено

1. Зафиксировать `PRODUCT_INPUT` как `IE-000001`.
2. Обновить discovery-документы в `docs/product/`.
3. Зафиксировать риски, факты изменений и результаты локальных проверок в разрешённых журналах.
4. Проверить существующий baseline, discovery-контур и локальные ссылки без Git и внешних действий.
5. Зафиксировать завершённый transition checkpoint `sot_git -> sot_github` и результаты его проверки.

## Запрещено

1. Изменять `README.md`, `src/minesweeper.py` или `tests/test_minesweeper.py`.
2. Выполнять push, pull, PR, merge, tag, release, GitHub write или изменение GitHub Settings.
3. Начинать реализацию, создавать implementation decision, выполнять продуктовую приёмку или публикацию.

## DoD

1. Полный `PRODUCT_INPUT` связан с `IE-000001`, все обязательные слои закрыты.
2. Product identity и требования согласованы в `docs/product/`.
3. Существующие product paths и защищённые поверхности не изменены.
4. Существующие unit tests и `--smoke` проходят без записи bytecode в Product Unit.
5. `bp_check.py` проходит с `0 fail, 0 warn`.
6. `sot_github` имеет exact root, единственный `origin`, local `develop` с upstream `origin/develop`, `origin/HEAD -> origin/develop`, clean tree и behind `0`.
7. `OD-000003` применён, `OD-000002` остаётся единственной active route-записью для `BACK-000001`.
8. После transition checkpoint работа останавливается перед отдельным `GATE-IMPLEMENTATION`.

## Transition checkpoint

- BASELINE_COMMIT: `4a649dbe77768f11d194cc71b431162c0a651882`
- SOT_TRANSITION: `sot_files -> sot_git`
- TRANSITION_DECISION: `OD-000001` (`applied`)
- LOCAL_GIT_ROUTE: `OD-000002` (`active`)
- PRODUCT_PATHS: unchanged
- REMOTE_AND_EXTERNAL_ACTIONS: not performed
- NEXT_GATE: `GATE-GITHUB-BOOTSTRAP`

## Transition checkpoint: `sot_git -> sot_github`

- BASELINE_COMMIT: `9cb21987c0160ec20394f4e0533b09fbc7cdad33`
- BASELINE_TREE: `e77824df848356ac7b3c42264e4c07bae98555e2`
- REPOSITORY: `debaha64/Minesweeper`
- REPOSITORY_ID: `1311607972`
- SOT_TRANSITION: `sot_git -> sot_github`
- TRANSITION_DECISION: `OD-000003` (`applied`)
- LOCAL_GIT_ROUTE: `OD-000002` (`active`)
- BRANCH_AND_UPSTREAM: `develop -> origin/develop`
- ORIGIN_HEAD: `origin/develop`
- REMOTE_BASELINE_REFS: `main/develop -> 9cb21987c0160ec20394f4e0533b09fbc7cdad33`
- GITHUB_CONFIGURATION: verified without drift
- GITHUB_WRITE: not performed
- PRODUCT_PATHS: unchanged
- NEXT_GATE: `GATE-IMPLEMENTATION`

## Блокер

1. none

## Разрешение глоссария discovery

Новые термины не требуются; существующего словаря достаточно.
