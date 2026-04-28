# Tools

`Tools/*` хранит локальные служебные команды продукта.

## Команды
- `product_check.py` — структурная проверка fresh/developed product state.
- `product_bootstrap_smoke.py` — локальный smoke route с отчётом в `Tools/.reports/`.

## Граница
Продукт не зависит от `BYTEPRESS_ROOT` для обычной проверки после bootstrap.
