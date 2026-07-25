# SDLC

## Назначение

SDLC задаёт смысл фаз Product Unit.

## Ключевые фазы

1. `intent` — первичный замысел.
2. `interview` — обязательные ответы владельца.
3. `requirements` — проверяемый контракт продукта.
4. `planning` — открытие PLAN.
5. `implementation` — реализация после owner decision.
6. `verification` — техническая проверка.
7. `owner-review` — передача результата владельцу.
8. `product-acceptance` — отдельное решение владельца.
9. `release-readiness` — отдельная готовность к выпуску.
10. `release` — выпуск после отдельного решения.

## Точка контроля реализации

Implementation требует:

1. `interview_evidence`;
2. `owner_decision` с `DECISION_KIND: implementation`;
3. ссылки в active PLAN;
4. следующий свободный PLAN ID.

Технический PASS не является продуктовой приёмкой.
