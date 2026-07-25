# SYSTEM.md

## Назначение

Системный реестр архитектурных границ и постоянных правил BytePress Harness. Процедуры находятся в `sops/`, текущая работа — только в `plans/`.

## Домены и границы слоёв

| ID | Путь | Каноническая роль |
|---|---|---|
| `domain:agent-map` | `AGENTS.md` | короткая карта агента и machine-readable SoT |
| `domain:human-entry` | `README.md` | вход пользователя, быстрый старт и навигация |
| `domain:system-registry` | `SYSTEM.md` | архитектурные границы и постоянные правила |
| `domain:docs` | `docs/` | объяснения и устойчивый смысл |
| `domain:sops` | `sops/` | нормативные процедуры |
| `domain:templates` | `templates/` | формы создаваемых записей |
| `domain:plans` | `plans/` | единственное текущее состояние `ROAD -> BACK -> PLAN` |
| `domain:logs` | `logs/` | факты и свидетельства |
| `domain:research` | `research/` | исследования Product Unit |
| `domain:tests` | `tests/` | проверяемые контракты и регрессия |
| `domain:tools` | `tools/` | механические локальные операции |
| `domain:src` | `src/` | код продукта; в starter пуст по замыслу |

Полное правило хранится в каноническом слое. Другие слои дают только необходимое краткое пояснение и ссылку.

## Инварианты

| ID | Формулировка |
|---|---|
| `invariant:human-control` | Человек управляет, агенты исполняют. |
| `invariant:workspace-product` | Workspace `<Slug>` делает продукт `<Slug>`; продукт не управляет Workspace. |
| `invariant:local-plan` | В `plans/active/` допускается от нуля до одного active `PLAN-*.md`. |
| `invariant:no-current-workspace-route` | Product Unit не хранит текущий маршрут Workspace. |
| `invariant:technical-check-boundary` | Технический PASS не является продуктовой приёмкой. |
| `invariant:sot-single-source` | Текущий `SOT_MODE` объявляется только в `AGENTS.md`. |
| `invariant:sot-files-isolation` | `sot_files` не читает `.git` и не вызывает Git CLI. |
| `invariant:sot-git-current` | `sot_git` требует валидные `HEAD` и ветвь, чистое дерево и отсутствие remote. |
| `invariant:sot-github-current` | `sot_github` проверяет только подготовленный локальный repository, один `origin`, совпадающую identity, upstream и `origin/HEAD`. |
| `invariant:canonical-product-identity` | Product identity согласована между brief, active PLAN и product-first README. |
| `invariant:typed-acceptance` | Продуктовая приёмка фиксируется только записью `product_acceptance` с ID `PA-*`. |
| `invariant:protected-surfaces` | Системные поверхности не меняются в `product-work` вне точного разрешённого исключения. |
| `invariant:harness-blocker` | При дефекте Harness агент выводит `HARNESS_BLOCKER: <краткое описание>` и прекращает изменения. |

## Фазы SDLC (`registry:sdlc-phases`)

| ID | Назначение | Граница |
|---|---|---|
| `intent` | замысел | не открывает реализацию |
| `interview` | интервью | требует ответа владельца |
| `requirements` | требования | draft не разрешает код |
| `planning` | планирование | требует управляемой границы |
| `approval` | утверждение | silence approval запрещён |
| `implementation` | реализация | требует implementation decision |
| `verification` | техническая проверка | PASS не равен приёмке |
| `owner-review` | обзор владельцем | не является приёмкой |
| `product-acceptance` | продуктовая приёмка | только отдельное решение |
| `release-readiness` | готовность к выпуску | не создаёт tag или release |
| `release` | выпуск | только отдельный маршрут |

Стартовый discovery-проход использует `discovery`. Порядок фаз и переходов описан в `sops/sdlc.md` и `sops/project-management.md`.

## Операционные режимы (`registry:operational-modes`)

| ID | Назначение | Граница |
|---|---|---|
| `product-work` | обычная продуктовая работа | следует active PLAN и фазе SDLC |
| `system-editing` | изменение системных файлов | только owner-initiated active PLAN |

Product-work агент сам не открывает `system-editing`.

## Режимы SoT (`registry:sot-modes`)

Поддерживаются ровно три режима:

| ID | Локальный контракт |
|---|---|
| `sot_files` | файловая поверхность; Git полностью вне проверки |
| `sot_git` | валидный локальный repository без remote |
| `sot_github` | подготовленные локальные `origin`, identity, upstream, remote refs и `origin/HEAD`; сеть вне checker |

При `sot_github` в `AGENTS.md` существует ровно одно поле `SOT_GITHUB_REPOSITORY` со значением `owner/repository`; в других режимах поле отсутствует. Кроме технического bootstrap отсутствующей неизменённой Product Unit в уже объявленном `sot_git`, режим не разрешает transition, изменяющую Git-работу, fetch, push, PR, merge, tag, выпуск или GitHub write. Нормативный контракт находится в `sops/sot.md`.

## Типизированные записи

| Запись | Хранилище | Назначение |
|---|---|---|
| `interview_evidence`, `IE-*` | `logs/sessions.md` | фактический ответ интервью |
| `owner_decision`, `OD-*` | `logs/decisions.md` | отдельное решение владельца |
| `product_acceptance`, `PA-*` | `logs/decisions.md` | отдельная продуктовая приёмка |

Active PLAN хранит ссылки `INTERVIEW_EVIDENCE_REF`, `OWNER_DECISION_REFS` и `PRODUCT_ACCEPTANCE_REF`, но не копирует содержимое записей. Канонический локальный источник использует конечный диапазон `codexlog:.codex/<actual-log-file>#lines=<start>-<end>`.

## Состояние продукта

| Условие | Состояние |
|---|---|
| существует active PLAN | его текущая фаза |
| active PLAN отсутствует, есть принятая completed basis | `accepted-completed` |
| есть продуктовые файлы без active PLAN и принятой basis | `idle-product` |
| starter пуст и active PLAN отсутствует | `initial-idle` |

Состояние определяется по текущим артефактам без реконструкции истории.

`idle-product` и `accepted-completed` могут входить в `discovery` с существующим product baseline. Наличие baseline-кода само по себе не является свидетельством преждевременной реализации; границу изменений по-прежнему задают active PLAN и `ALLOWED_SURFACES`.

## Защищённые поверхности (`registry:protected-surfaces`)

| ID | Путь |
|---|---|
| `protected:agent-map` | `AGENTS.md` |
| `protected:system-registry` | `SYSTEM.md` |
| `protected:sops` | `sops/` |
| `protected:templates` | `templates/` |
| `protected:tools` | `tools/` |

`ALLOWED_SURFACES` принимает точный относительный путь, дерево `path/**`, `none` либо точные исключения `AGENTS.md::SOT_MODE` и `AGENTS.md::SOT_GITHUB_REPOSITORY`. Исключения допустимы только в owner-approved transition; внешняя граница всегда имеет приоритет.

## Гейты (`registry:gates`)

| ID | Назначение |
|---|---|
| `owner-decision-required` | требуется решение владельца |
| `interview-complete` | обязательное интервью закрыто |
| `implementation-approved` | владелец открыл реализацию |
| `verification-pass` | техническая проверка прошла |
| `ready-for-owner-review` | результат можно передать владельцу |
| `product-acceptance` | отдельная продуктовая приёмка |
| `release-readiness` | отдельная готовность к выпуску |
| `release/tag` | отдельное решение о выпуске и tag |

## Системные связи

| Смысл | Канонический владелец | Процедура или проверка |
|---|---|---|
| решения и плановый контур | `plans/`, `logs/` | `sops/project-management.md` |
| режим источника истины | `AGENTS.md`, этот реестр | `sops/sot.md`, `tools/bp_check.py` |
| защищённые поверхности | этот реестр | `sops/project-management.md`, `sops/verify-work.md` |
| продуктовая приёмка | `logs/decisions.md` | `sops/verify-work.md` |
| терминология | `docs/terminology/glossary.md` | `sops/terminology.md` |
| механические проверки | `tools/`, `tests/` | `tools/README.md`, `tests/README.md` |

После появления продуктового кода root `README.md` становится product-first по `templates/product-readme.md`. Пользовательские документы не хранят внутренние `ROAD`, `BACK`, `PLAN`, решения владельца или динамический статус Harness; публичная SoT configuration остаётся допустимым пользовательским контрактом.
