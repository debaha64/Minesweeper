# PLAN-000001-product-discovery

Статус: active

Связь:
- ROAD: ROAD-000001
- BACK: BACK-000001

Product Unit: Minesweeper

Фаза SDLC: owner-review
Операционный режим: product-work
INTERVIEW_EVIDENCE_REF: IE-000001
OWNER_DECISION_REFS: OD-000001,OD-000002,OD-000003,OD-000004,OD-000005
PRODUCT_ACCEPTANCE_REF: none
ALLOWED_SURFACES: .git/**,README.md,src/minesweeper.py,tests/test_minesweeper.py,plans/active/PLAN-000001-product-discovery.md,logs/decisions.md,logs/changes.md,logs/quality.md
Маршрут решений: PRODUCT_INPUT -> verified discovery -> verified sot_files-to-sot_git transition -> verified GATE-GITHUB-BOOTSTRAP -> verified GATE-GITHUB-CONFIG -> verified sot_git-to-sot_github transition -> owner-approved GATE-IMPLEMENTATION -> verified implementation -> owner-review -> owner-approved GATE-PR -> feature PR -> owner approval exact head
Граница решения владельца: GATE-PR разрешает только обязательную local identity correction, feature branch через `--track=inherit`, commit exact seven tracked paths, локальные проверки, push feature branch и PR в `develop`; merge, approval, приёмка, tag, release и изменение GitHub Settings запрещены

Роли: verifier -> owner
Gate: ready-for-owner-review

## Цель

Зафиксировать и проверить контракт CLI-команды `count`, не изменяя существующий продуктовый baseline.

## Разрешено

1. Реализовать CLI-команду `count` в `src/minesweeper.py`.
2. Документировать команду и валидный пример в `README.md`.
3. Добавить unit tests в `tests/test_minesweeper.py`.
4. Зафиксировать решение, факт изменения и результаты локальных проверок в разрешённых PLAN/log-поверхностях.

## Запрещено

1. Изменять product paths вне `README.md`, `src/minesweeper.py`, `tests/test_minesweeper.py`.
2. Выполнять merge, owner approval exact head, product acceptance, tag, release или изменение GitHub Settings.
3. Выполнять продуктовую приёмку или публикацию.

## DoD

1. Полный `PRODUCT_INPUT` связан с `IE-000001`, все обязательные слои закрыты.
2. Product identity и требования согласованы в `docs/product/`.
3. Команда `count` использует zero-based координаты и печатает ровно одно целое число для валидного поля.
4. Непустое прямоугольное поле принимает только `*` и `.`; invalid board или coordinates дают exit `2`, пустой stdout и краткий stderr.
5. Unit tests покрывают центр, край, угол, invalid coordinates и invalid board.
6. Существующий `--smoke` и deterministic CLI smoke проходят без записи bytecode в Product Unit.
7. `OD-000004` применён, `OD-000005` разрешает только точный GATE-PR route.
8. Feature branch создан через `--track=inherit`; commit меняет ровно семь tracked paths и имеет исправленную local Git identity.
9. Локальные проверки проходят на exact feature head; feature branch опубликована и PR направлен в `develop`.
10. После read-only проверки PR работа останавливается перед owner approval exact head.

## Implementation checkpoint: CLI `count`

- IMPLEMENTATION_DECISION: `OD-000004` (`applied`)
- PRODUCT_SLICE: `README.md`, `src/minesweeper.py`, `tests/test_minesweeper.py`
- UNIT_TESTS: `26/26 PASS`
- DETERMINISTIC_CLI_SMOKE: `1`
- BASELINE_SMOKE: `Minesweeper smoke: PASS`
- INVALID_INPUT_CONTRACT: verified by unit tests
- COMMIT_BRANCH_PUSH_PR: owner-approved by `OD-000005`
- NEXT_GATE: owner approval exact head

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
