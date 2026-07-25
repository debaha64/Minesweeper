# Старт сессии

Прочитать `AGENTS.md`, `SYSTEM.md`, активный PLAN, `plans/backlog.md`, `plans/roadmap.md` и релевантные SOP.

В стартовой обвязке Product Unit управляющий активный PLAN находится в `plans/active/`.

## Первый старт

Для первого старта существующего контура:

1. Прочитать `README.md`, `AGENTS.md` и `SYSTEM.md`.
2. До любых Git-команд прочитать объявленный режим SoT в `AGENTS.md`.
3. При `sot_git` до интервью обработать existing/missing repository вход по `sops/sot.md`.
4. Для missing repository после первого запроса автоматически создать baseline неизменённой Product Unit; отдельное разрешение владельца не спрашивать.
5. При `sot_github` выполнить внешний preflight identity/metadata/fetch/`origin/HEAD`, затем локальную диагностику без сети.
6. Только после успешного bootstrap, preflight или проверки existing repository запустить `python3 tools/bp_init.py --repo .`.
7. Найти активную `ROAD`, активную `BACK` и единственный активный `PLAN` в управляющем контуре текущей работы.
8. Определить фазу SDLC, gate, `Маршрут решений`, роль, разрешённые файлы и запреты.
9. Проверить, требуется ли решение владельца для ближайшего перехода.
10. Продолжать работу только в границах active PLAN.
11. Если есть внешний домен-свидетельство, указать его в `Состоянии агента`.

`bp_init.py` восстанавливает отсутствующие обязательные журналы и README, но не очищает существующие файлы. Операционные записи работающей Product Unit сохраняются; требование пустоты относится только к исходной поставке и минимальному сценарию восстановления.

При `sot_files` Git CLI запрещён до отдельного owner-approved transition. Отсутствие `.git` проверяется файловыми средствами.

При `sot_git` без `.git/` Product Unit tools не создают repository. До baseline их не запускают, потому что `bp_init.py` может восстанавливать отсутствующие scaffold-файлы.

Для первого старта Product Unit:

1. Использовать его собственный `ROAD -> BACK -> PLAN`.
2. Считать первый продуктовый запрос discovery-входом до решения владельца.
3. Не переходить к коду, пока точка контроля после `discovery` не выполнена по `sops/managed-agent-pass.md`.

## Порядок восстановления

Порядок восстановления:

1. `AGENTS.md`;
2. `SYSTEM.md`;
3. `plans/active/`;
4. `plans/backlog.md`;
5. `plans/roadmap.md`;
6. `plans/completed/`;
7. `logs/sessions.md`;
8. `logs/quality.md`;
9. `logs/risks.md`;
10. документы-владельцы смысла.

Сессия не требует отдельного `state/session-handoff.md`, если плановый контур, журналы и чистое завершение (`clean-exit`) актуальны.

Стартовое `Состояние агента` показывает:

1. цель;
2. статус;
3. ROAD/BACK/PLAN;
4. фазу и точку контроля;
5. режим SoT; для `sot_files` — подтверждение полного игнорирования `.git`, для `sot_git` — состояние local repository, для `sot_github` — repository identity, `origin`, upstream, `origin/HEAD` и external-preflight boundary;
6. gate и `Маршрут решений`, если они есть в active PLAN;
7. запреты;
8. внешний домен как свидетельство, если применимо;
9. следующий шаг.
