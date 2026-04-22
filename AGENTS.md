# AGENTS

`AGENTS.md` — каноническая entry point карта агента в replicated product repo `Minesweeper`.

## Кто такой агент внутри продукта
- Humans steer. Agents execute.
- Агент работает внутри contracts самого product repo, а не подменяет owner продукта.
- Агент ведёт работу через task-ветку, local checks и PR-flow.

## Source-of-truth hierarchy
1. Текущий task-source пользователя.
2. `Docs/Discovery/*` как current-truth route продукта.
3. `Plans/*` как stage/task/pass owner.
4. `Docs/User/*`, `Docs/Product/*`, `Docs/Technical/*` как knowledge/contract layers продукта.
5. `Logs/*` как фактологический слой.
6. `Adapters/*`, `Setup_Guide.md` и `scripts/*` как execution support.

## Startup-handshake первого ответа
- Первый содержательный ответ агента до исследования или правок обязан явно показать startup mode продукта.
- В startup-handshake агент коротко фиксирует:
  1. какой startup mode он использует для текущего product-start pass;
  2. как он понял scope текущего pass;
  3. какой branch status он обнаружил;
  4. какой branch action / start route он использует;
  5. какой planning-state обнаружен: текущие `ROAD/BACK/PLAN` или отсутствие активного этапа;
  6. какие owner-domains он читает первыми;
  7. какой первый конкретный шаг выполняет дальше.
- Startup-handshake должен быть коротким, наблюдаемым и проверяемым по generated product repo.

## First product-start gate
- Bootstrap-created repo стартует с `Docs/Discovery/Interview.md` в состоянии `Статус_текущей_истины: Не_подтверждена`.
- Пока пользователь не дал явные ответы и current truth не подтверждена, агент работает только в discovery-only mode.
- До открытия task-ветки любые writable changes запрещены, включая `Docs/Discovery/*`, `Plans/*` и `Logs/*`.
- В этом gate допускаются только `Docs/Discovery/*`, `Plans/*`, `Logs/*` и cleanup route failed pass, но сам writable pass начинается только после branch action в task-ветку.
- В этом gate placeholders bootstrap'а не считаются разрешением на изменения в `Docs/Product/*`, `Docs/Technical/*`, `Runtime/*`, `scripts/*` или предметной реализации.
- Если failed start дал tracked drift вне разрешённого раннего contour, canonical reset route — fresh bootstrap в новый target.

## Как входить в задачу
- Сначала прочитать `Plans/Roadmap.md`, `Plans/Backlog.md` и current `Plan`.
- Для bootstrap-created repo сначала прочитать `Docs/Discovery/Interview.md` и проверить, подтверждена ли current truth ответами пользователя.
- Для human-facing route использовать `Docs/User/*`.
- Для structural check использовать `scripts/dev-test.sh` с `BYTEPRESS_ROOT`.
- Для minimal integration handoff использовать `scripts/integration-smoke.sh` с `BYTEPRESS_ROOT`.
- Для failed early product-start использовать `scripts/reset-product-start.sh`.
- Не дублировать repo contracts длинным ручным промптом, если они уже определены продуктом.

## Границы
- этот файл не подменяет `Docs/User/*`, `Docs/Technical/*` и `Plans/*`;
- этот файл направляет агента к owner-documents replicated product repo.
