# Discovery

`Docs/Discovery/*` хранит current-truth продукта до перевода в требования и planning contour.

## Current-truth owner
- `Interview.md` — owner текущей аналитической истины generated product repo.

## Bootstrap minimum раннего product-start contour
- `README.md` — карта discovery-layer.
- `Interview.md` — текущее интервью продукта.

## Границы
- этот слой не дублирует `Plans/*` и `Logs/*`;
- history-fact изменений discovery-layer закрывается через planning/log contour;
- `Discussion`, `Research` и `Requirements` не materialize до отдельного pass, который явно открывает расширенный discovery contour.
