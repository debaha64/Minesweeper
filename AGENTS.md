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
  3. какой branch/start route он использует;
  4. какой planning-state обнаружен: текущие `ROAD/BACK/PLAN` или отсутствие активного этапа;
  5. какие owner-domains он читает первыми;
  6. какой первый конкретный шаг выполняет дальше.
- Startup-handshake должен быть коротким, наблюдаемым и проверяемым по generated product repo.

## Как входить в задачу
- Сначала прочитать `Plans/Roadmap.md`, `Plans/Backlog.md` и current `Plan`.
- Если scope касается текущей истины продукта, сначала прочитать `Docs/Discovery/Interview.md`.
- Для human-facing route использовать `Docs/User/*`.
- Для structural check использовать `scripts/dev-test.sh` с `BYTEPRESS_ROOT`.
- Для minimal integration handoff использовать `scripts/integration-smoke.sh` с `BYTEPRESS_ROOT`.
- Не дублировать repo contracts длинным ручным промптом, если они уже определены продуктом.

## Границы
- этот файл не подменяет `Docs/User/*`, `Docs/Technical/*` и `Plans/*`;
- этот файл направляет агента к owner-documents replicated product repo.
