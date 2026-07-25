# Шаблоны

`templates/` хранит формы целевых артефактов и журнальных записей. Шаблон не является SOP, скрытой реализацией, проверкой, решением владельца или источником продуктового смысла.

Правила применения шаблонов находятся в `sops/`. Если для формы нужен порядок действий, запрет или точка контроля, он фиксируется в SOP, а не внутри шаблона как процедура.

## Модель записи

Минимальная карта шаблона:

```text
Шаблон -> целевой артефакт -> владелец смысла -> режим записи -> обязательность -> проверка
```

Владельцы смысла:

1. `owner:human` - решения владельца, продуктовая приёмка, выпуск, архив.
2. `owner:agent` - исполнение в границах PLAN и подготовка свидетельств.
3. `owner:tools` - технические проверки без продуктового решения.
4. `owner:harness-engineering` - системный контракт и обвязка Product Unit.

Режимы записи:

1. `replace` - целевой файл создаётся или переписывается как текущая форма.
2. `append` - запись добавляется в конец журнала или results-файла.
3. `move+append` - артефакт переносится и получает итоговую append-секцию.
4. `reference` - шаблон описывает форму внешнего пакета или отчёта.

Обязательность:

1. `required` - нужен для текущего контракта.
2. `conditional` - нужен при указанной фазе, точке контроля или типе изменения.
3. `optional` - вспомогательная форма без обязательного потребителя.

## Системные входы

- `agents.md` -> `AGENTS.md` -> `owner:harness-engineering` -> `replace` -> `required` -> `bp_check.py`.
- `system.md` -> `SYSTEM.md` -> `owner:harness-engineering` -> `replace` -> `required` -> `system contract`.
- `product-readme.md` -> `README.md` -> `owner:harness-engineering` -> `replace` -> `required` -> product-first readme coverage после появления продуктового кода.
- `domain-readme.md` -> `*/README.md` домена -> `owner:agent` -> `replace` -> `conditional` -> `readme coverage`.
- `agent-state-message.md` -> сообщение `Состояние агента` -> `owner:agent` -> `reference` -> `conditional` -> ручная сверка SOP.
- `owner-decision-package.md` -> пакет вопросов владельцу -> `owner:human` -> `reference` -> `conditional` -> ручная сверка `sops/project-management.md`.

## Продукт и документы

- `docs-product-brief.md` -> `docs/product/product-brief.md` -> `owner:human` -> `replace` -> `required` -> `phase profile`.
- `docs-product-passport.md` -> `docs/product/product-passport.md` -> `owner:human` -> `replace` -> `required` -> `phase profile`.
- `docs-product-jtbd.md` -> `docs/product/jtbd.md` -> `owner:human` -> `replace` -> `required` -> `phase profile`.
- `docs-product-prd.md` -> `docs/product/prd.md` -> `owner:human` -> `replace` -> `conditional` -> русская форма требований к продукту и точка контроля `implementation`.
- `docs-product-dods.md` -> `docs/product/dods.md` -> `owner:human` -> `replace` -> `required` -> русская форма критериев готовности и точка контроля `implementation`.
- `docs-terminology-glossary.md` -> `docs/terminology/glossary.md` -> `owner:harness-engineering` -> `replace` -> `required` -> `terminology review`.
- `docs-architecture-architecture.md` -> `docs/architecture/architecture.md` -> `owner:agent` -> `replace` -> `conditional` -> `phase profile`.
- `docs-architecture-domain-model.md` -> `docs/architecture/domain-model.md` -> `owner:agent` -> `replace` -> `conditional` -> `phase profile`.
- `docs-technical-architecture.md` -> краткая справочная форма технической архитектуры -> `owner:agent` -> `reference` -> `optional` -> ручная сверка.
- `docs-technical-testing.md` -> `docs/technical/testing.md` -> `owner:agent` -> `replace` -> `conditional` -> русские разделы модульных тестов и сквозной проверки, `phase profile`.
- `docs-user-guide.md` -> `docs/user/*` -> `owner:human` -> `replace` -> `conditional` -> `docs phase gates`.

## SOP, роли и плановый контур

- `sop.md` -> `sops/*.md` -> `owner:harness-engineering` -> `replace` -> `required` -> `required files`.
- `role.md` -> `sops/roles/*.md` -> `owner:harness-engineering` -> `replace` -> `conditional` -> `roles check`.
- `plan-roadmap.md` -> `plans/roadmap.md` -> `owner:human` -> `replace` -> `required` -> плановый контур.
- `plan-backlog.md` -> `plans/backlog.md` -> `owner:agent` -> `replace` -> `required` -> плановый контур.
- `plan-active.md` -> `plans/active/PLAN-*.md` -> `owner:agent` -> `replace` -> `required` -> PLAN ID, `ALLOWED_SURFACES`, `PRODUCT_ACCEPTANCE_REF` и плановый контур.
- `plan-completed-readme.md` -> `plans/completed/README.md` -> `owner:harness-engineering` -> `replace` -> `required` -> плановый контур.
- `execution-plan.md` -> внешний PLAN фазы `implementation` или проход миграции -> `owner:agent` -> `reference` -> `optional` -> ручная сверка.

## Исследования и Codex

- `research-domain-index.md` -> `research/<xxx>-<slug>/000-index.md` -> `owner:agent` -> `replace` -> `conditional` -> `sops/research.md`.
- `research-record.md` -> `research/<xxx>-<slug>/<nnn>-<slug>.md` -> `owner:agent` -> `replace` или `append` -> `conditional` -> `sops/research.md`.
- `research-results.md` -> `research/<xxx>-<slug>/results.md` -> `owner:agent` -> `replace` -> `conditional` -> `sops/research.md`.
- `codex-task.md` -> задание Codex -> `owner:human` -> `reference` -> `conditional` -> входная точка контроля и чистое завершение (`clean-exit`).
- `codex-report.md` -> итоговый отчёт Codex -> `owner:agent` -> `reference` -> `conditional` -> сверка с PLAN и logs.
- `interview.md` -> слоевое пакетное интервью -> `owner:human` -> `reference` -> `conditional` -> решение владельца.

## Журналы

- `log-file.md` -> файл журнала `logs/*.md` -> `owner:harness-engineering` -> `replace` -> `required` -> контур Управления проектом.
- `change-record.md` -> запись `logs/changes.md` -> `owner:agent` -> `append` -> `required` для изменений -> контур Управления проектом.
- `decision-record.md` -> запись `owner_decision` (`OD-*`) или `product_acceptance` (`PA-*`) в `logs/decisions.md` -> `owner:human` -> `append` -> `required` для решений -> локальный конечный `#lines=` locator.
- `quality-record.md` -> запись `logs/quality.md` -> `owner:tools` -> `append` -> `required` для проверок -> локальный конечный `#lines=` locator.
- `risk-record.md` -> запись `logs/risks.md` -> `owner:agent` -> `append` -> `conditional` -> проверка `high-risk`.
- `session-record.md` -> запись `logs/sessions.md` -> `owner:agent` -> `append` -> `required` для чистого завершения (`clean-exit`) -> capture PLAN и локальный конечный `#lines=` locator ответа владельца.
- `terminology-record.md` -> запись `logs/terminology.md` -> `owner:harness-engineering` -> `append` -> `conditional` -> `terminology review`.
- `log-release-record.md` -> запись `logs/releases.md` -> `owner:human` -> `append` -> `conditional` -> только точка контроля выпуска.

## Формы границы выпуска

- `release-readiness-record.md` -> запись готовности к точке выпуска -> `owner:human` -> `append` -> `conditional` -> ручная сверка точки контроля выпуска.
- `release-tag-decision-record.md` -> запись решения о tag/release -> `owner:human` -> `append` -> `conditional` -> ручная сверка границы выпуска и тега.
- `archive-decision-record.md` -> запись решения об архиве -> `owner:human` -> `append` -> `conditional` -> ручная сверка границы архива.

Эти шаблоны являются только формами записей. Они не разрешают release, tag, архив выпуска, заметки выпуска, GitHub Release или `gh release create`.

## Реестры

- `registry-file.md` -> реестровый markdown-файл -> `owner:harness-engineering` -> `replace` -> `conditional` -> `system contract`.
- `registry-item.md` -> строка реестра -> `owner:harness-engineering` -> `append` или `replace` -> `conditional` -> `system contract`.

## Правила слоя

- Для нового целевого артефакта сначала выбрать существующий шаблон или добавить новый.
- Для нового журнала нужны шаблон файла и шаблон записи.
- При изменении шаблона проверить `SYSTEM.md`, эту карту, связанные SOP и журналы.
- Не создавать демонстрационные каталоги, fixtures или скрытые реализации внутри `templates/`.
- Шаблоны интервью, Codex-заданий и записей границы выпуска не являются продуктовой приёмкой и не разрешают выпуск, тег или архив.

## Быстрая привязка форм

1. Codex-задание: `templates/codex-task.md`.
2. Codex-отчёт: `templates/codex-report.md`.
3. Состояние агента: `templates/agent-state-message.md`.
4. Запись качества: `templates/quality-record.md`.
5. Чистое завершение (`clean-exit`): `templates/session-record.md`.
6. Research:
   - `templates/research-domain-index.md`
   - `templates/research-record.md`
   - `templates/research-results.md`
   - `templates/owner-decision-package.md`
7. Формы границы выпуска:
   - `templates/release-readiness-record.md`
   - `templates/release-tag-decision-record.md`
   - `templates/archive-decision-record.md`
   - `templates/log-release-record.md`
