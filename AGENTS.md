# AGENTS.md

## Назначение

Короткая карта агента для BytePress Harness.

SOT_MODE: sot_files

`AGENTS.md` — единственное место machine-readable конфигурации устойчивого режима. Условное поле `SOT_GITHUB_REPOSITORY` существует только в `sot_github`; полный контракт режимов и переходов находится в [sops/sot.md](sops/sot.md).

## Основные принципы

```text
Человек управляет, агенты исполняют.
```

```text
Workspace <Slug> делает продукт <Slug>; продукт не управляет Workspace.
```

Подтверждение запуска команды и технический PASS не заменяют решение владельца. Команда «Продолжай» действует только внутри уже разрешённого информационного слоя или фазы.

## Старт агента

1. Прочитать `AGENTS.md` и `SYSTEM.md`.
2. До интервью и изменений обработать текущий `SOT_MODE` по [sops/sot.md](sops/sot.md).
3. Прочитать active PLAN, `plans/backlog.md`, `plans/roadmap.md` и релевантные SOP.
4. Определить фазу, точку контроля, `ALLOWED_SURFACES` и решения владельца, необходимые для ближайшего перехода.
5. Действовать только в границах active PLAN и внешней границы задачи.

`SOT_MODE` читается до любых Git-команд. При `sot_files` Git CLI запрещён до отдельного owner-approved transition; отсутствие `.git` проверяется файловыми средствами.

Подробный порядок старта находится в [sops/start-session.md](sops/start-session.md), интервью — в [sops/interview.md](sops/interview.md), управление плановым контуром — в [sops/project-management.md](sops/project-management.md).

## Карта слоёв

| Слой | Роль |
|---|---|
| `README.md` | вход пользователя, назначение, быстрый старт и навигация |
| `SYSTEM.md` | системный реестр архитектурных границ и постоянных правил |
| `docs/` | объяснения и устойчивый смысл |
| `sops/` | пошаговые нормативные процедуры |
| `templates/` | формы создаваемых записей |
| `plans/` | единственное текущее состояние `ROAD -> BACK -> PLAN` |
| `logs/` | факты и свидетельства |
| `research/` | содержательные результаты исследований Product Unit |
| `tests/` | проверяемые контракты и регрессия |
| `tools/` | механические локальные операции |
| `src/` | код продукта |

## Обязательные границы

1. В `plans/active/` допускается от нуля до одного active `PLAN-*.md`; при наличии PLAN агент обязан следовать ему.
2. Внешняя граница задачи может быть только сужена через `ALLOWED_SURFACES`.
3. `AGENTS.md`, `SYSTEM.md`, `sops/`, `templates/` и `tools/` защищены в `product-work`; точные переходные исключения перечислены в `SYSTEM.md`.
4. Product Unit не хранит текущий маршрут Workspace и не управляет Workspace.
5. Реализация, продуктовая приёмка, выпуск, tag и GitHub write требуют соответствующих отдельных решений владельца.
6. Product Unit tools проверяют только локальный контур, не принимают решения и не выполняют automatic repair.

## Дефект Harness

При дефекте Harness в `product-work` агент выводит:

```text
HARNESS_BLOCKER: <краткое описание>
```

После этого изменения прекращаются. Подробная граница находится в [sops/verify-work.md](sops/verify-work.md) и [sops/system-editing.md](sops/system-editing.md).

## Навигация по процедурам

1. [sops/README.md](sops/README.md) — карта процедур.
2. [sops/sot.md](sops/sot.md) — три режима SoT и переходы.
3. [sops/project-management.md](sops/project-management.md) — `ROAD -> BACK -> PLAN`.
4. [sops/interview.md](sops/interview.md) — интервью и решения владельца.
5. [sops/clean-exit.md](sops/clean-exit.md) — чистое завершение.
