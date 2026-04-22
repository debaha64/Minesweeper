# Discovery

`Docs/Discovery/*` хранит current-truth продукта до перевода в требования и planning contour.

## Current-truth owner
- `Interview.md` — owner текущей аналитической истины generated product repo.

## Bootstrap minimum раннего product-start contour
- `README.md` — карта discovery-layer.
- `Interview.md` — текущее интервью продукта.

## Gate текущей истины
- bootstrap-created interview стартует в состоянии `Статус_текущей_истины: Не_подтверждена`;
- пока пользователь не ответил явно, generated repo остаётся в discovery-only contour;
- даже в discovery-only contour первый writable action допускается только после открытия task-ветки;
- placeholders bootstrap'а не разрешают переход к `Docs/Product/*`, `Docs/Technical/*`, `Runtime/*` и предметной реализации.

## Формат интервью
- вопросы фиксируются нумерованно;
- если выбор ограничен, использовать буквенные варианты ответа;
- если есть предпочтительный route, помечать рекомендуемый вариант;
- если достаточно узкого delta-интервью, оно всё равно использует тот же numbered / lettered / recommended format.

## Границы
- этот слой не дублирует `Plans/*` и `Logs/*`;
- history-fact изменений discovery-layer закрывается через planning/log contour;
- `Discussion`, `Research` и `Requirements` не materialize до отдельного pass, который явно открывает расширенный discovery contour.
