# Управление проектом

Product Unit ведёт локальный контур `ROAD -> BACK -> PLAN`.

## ID плана

1. PLAN ID уникален и не переиспользуется.
2. Имя файла и заголовок содержат один ID.
3. Перенос в `plans/completed/` не меняет ID.
4. Префикс `COMPLETED-` запрещён.
5. Новый active PLAN получает следующий свободный ID по active и completed PLAN.

## Активный PLAN

В `plans/active/` допускается от нуля до одного `PLAN-*.md` со значением:

```text
Статус: active
```

Минимальные машинные поля:

```text
INTERVIEW_EVIDENCE_REF: none | IE-000001
OWNER_DECISION_REFS: none | OD-000001,OD-000002
PRODUCT_ACCEPTANCE_REF: none | PA-000001
ALLOWED_SURFACES: <relative paths, trees, exact field exceptions | none>
```

PLAN также содержит один `Product Unit`, `Фаза SDLC`, `Операционный режим` и связь с существующими ROAD/BACK.

`ALLOWED_SURFACES` принимает:

1. точный относительный путь;
2. дерево вида `src/**`;
3. точные исключения `AGENTS.md::SOT_MODE` и `AGENTS.md::SOT_GITHUB_REPOSITORY`;
4. `none` как единственное значение.

Внешняя граница может быть только сужена.

## Точка контроля реализации

Implementation разрешён, если:

1. обязательное интервью завершено или допустимо отложено;
2. active PLAN ссылается на валидное `interview_evidence`;
3. active PLAN ссылается на отдельное решение владельца `DECISION_KIND: implementation`;
4. решение имеет `DECISION_VALUE: approved` и относится к тому же PLAN и IE;
5. product identity согласована между brief и PLAN;
6. `ALLOWED_SURFACES` задаёт разрешённый product slice.

Полный `PRODUCT_INPUT`, начальный запрос и команда «Продолжай» не разрешают реализацию.

## Фаза активного PLAN

Фаза отражает текущее состояние. После технической проверки допустимы `verification`, `owner-review` или закрытие PLAN. Состояние продукта выводится из текущего active PLAN, наличия продукта и существующей принятой completed basis без реконструкции истории.

## Продуктовая приёмка

Приёмка фиксируется отдельной записью `RECORD_TYPE: product_acceptance` с ID `PA-*`.

При `accepted`:

1. PLAN ссылается на `PA-*` того же PLAN;
2. получает фазу `product-acceptance` и `Статус: completed`;
3. переносится в `plans/completed/` без смены ID;
4. active PLAN отсутствует до нового решения владельца.

При `rejected` PLAN остаётся active в фазе `owner-review`, ссылается на `PA-*` и фиксирует блокер следующего решения владельца.

Technical PASS не создаёт `PA-*`.

## Защищённые поверхности

Канонический реестр находится в `SYSTEM.md`. В `product-work` защищённые поверхности запрещены, кроме точных исключений `AGENTS.md::SOT_MODE` и `AGENTS.md::SOT_GITHUB_REPOSITORY`, уже разрешённых владельцем и PLAN для одного transition checkpoint.

При запрещённом изменении или дефекте Harness агент выводит:

```text
HARNESS_BLOCKER: <краткое описание>
```

и прекращает изменения. Агент не проектирует исправление, не запрашивает `system-editing PLAN`, не предлагает повторное исполнение, не создаёт Harness research и не управляет Workspace.

## SoT и локальная Git-работа

`SOT_MODE: sot_git` сам по себе разрешает только bootstrap отсутствующего неизменённого repository. Переход режима и `local_git_route` являются разными решениями владельца. Для одного BACK существует не более одного `local_git_route`; PLAN сужает его через `ALLOWED_SURFACES`.

Текущая Git-проверка выбирается по mode: `sot_git` требует exact root, valid `HEAD`, branch, clean tree и remote absent; `sot_github` дополнительно требует подготовленные `origin`, identity, upstream, remote refs и `origin/HEAD`. Подробный контракт находится в `sops/sot.md`.
