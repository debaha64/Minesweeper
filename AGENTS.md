# AGENTS

`AGENTS.md` — каноническая entry point карта агента в replicated product repo `Minesweeper`.

## Кто такой агент внутри продукта
- Humans steer. Agents execute.
- Агент работает внутри contracts самого product repo, а не подменяет owner продукта.
- Агент ведёт работу через task-ветку, local checks и PR-flow.

## Source-of-truth hierarchy
1. Текущий task-source пользователя.
2. `Plans/*` как stage/task/pass owner.
3. `Docs/User/*`, `Docs/Product/*`, `Docs/Technical/*` как knowledge/contract layers продукта.
4. `Logs/*` как фактологический слой.
5. `Adapters/*`, `Setup_Guide.md` и `scripts/*` как execution support.

## Как входить в задачу
- Сначала прочитать `Plans/Roadmap.md`, `Plans/Backlog.md` и current `Plan`.
- Для human-facing route использовать `Docs/User/*`.
- Для structural check использовать `scripts/dev-test.sh` с `BYTEPRESS_ROOT`.
- Для minimal integration handoff использовать `scripts/integration-smoke.sh` с `BYTEPRESS_ROOT`.
- Не дублировать repo contracts длинным ручным промптом, если они уже определены продуктом.

## Границы
- этот файл не подменяет `Docs/User/*`, `Docs/Technical/*` и `Plans/*`;
- этот файл направляет агента к owner-documents replicated product repo.
