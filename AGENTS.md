# AGENTS

`AGENTS.md` — карта входа агента в replicated product repo `Minesweeper`.

## Что делает агент
- человек направляет, агент исполняет;
- агент работает внутри контрактов product repo;
- каждое изменение проходит через task-ветку, локальные проверки и PR.

## Как читать истину
1. Текущий task-source пользователя.
2. `Docs/Discovery/*` как current-truth route продукта.
3. `Plans/*` как stage/task/pass owner.
4. `Docs/User/*`, `Docs/Product/*`, `Docs/Technical/*`, `Docs/Terms/*` как product knowledge layers.
5. `Logs/*`, `Setup_Guide.md`, `Adapters/*` и `scripts/*` как execution support.

## Startup-handshake первого ответа
Первый содержательный ответ до исследования или правок должен быть коротким стартовым отчётом.

`Приветствие:` короткая рабочая фраза.
`Режим запуска:` какой startup mode используется.
`Scope:` как понят текущий проход.
`Статус ветки:` что обнаружено в Git.
`Действие с веткой:` какой start route используется дальше.
`Состояние планирования:` текущие `ROAD/BACK/PLAN` или отсутствие активного этапа.
`Первые owner-domains:` какие домены читаются первыми.
`Первый конкретный шаг:` какое действие выполняется сразу.

## First product-start gate
- Bootstrap-created repo стартует с `Docs/Discovery/Interview.md` в состоянии `Статус_текущей_истины: Не_подтверждена`.
- Пока пользователь не дал явные ответы и current truth не подтверждена, агент работает только в discovery-only mode.
- До открытия task-ветки любые writable changes запрещены, включая `Docs/Discovery/*`, `Plans/*` и `Logs/*`.
- В этом gate допускаются только `Docs/Discovery/*`, `Plans/*`, `Logs/*` и cleanup route failed pass, но сам writable pass начинается только после branch action в task-ветку.
- В этом gate placeholders bootstrap'а не считаются разрешением на изменения в `Docs/Product/*`, `Docs/Technical/*`, `Runtime/*`, `scripts/*` или предметной реализации.
- Если failed start дал tracked drift вне разрешённого раннего contour, canonical reset route — fresh bootstrap в новый target.

## Start route
- Сначала прочитать `Plans/Roadmap.md`, `Plans/Backlog.md` и current `Plan`.
- Затем прочитать `Docs/Terms/Base_Terms.md` и `Docs/Discovery/Interview.md`.
- Первый writable pass начинать только после открытия task-ветки.
- Для structural check использовать `scripts/dev-test.sh` с `BYTEPRESS_ROOT`.
- Для integration handoff использовать `scripts/integration-smoke.sh`.
- Для failed start использовать `scripts/reset-product-start.sh`.

## Границы
- этот файл не подменяет `Docs/Discovery/*`, `Docs/User/*`, `Docs/Product/*`, `Docs/Technical/*`, `Docs/Terms/*` и `Plans/*`;
- этот файл только направляет агента к owner-documents replicated product repo.
