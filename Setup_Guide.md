# Setup_Guide

## Базовая среда
- Linux или WSL
- Git
- Python 3.11+

## Рабочий каталог
- Репозиторий продукта располагается отдельно от BytePress.

## Git start route
```bash
git init -b develop
git add .
git commit -m "Bootstrap baseline"
git checkout -b feat/000001-confirm-current-truth
```

## Проверка
- первый product-start pass остаётся discovery-only, пока пользователь не подтвердил `Docs/Discovery/Interview.md`;
- первый writable action, включая `Docs/Discovery/*`, `Plans/*` и `Logs/*`, допускается только после открытия task-ветки;
- для structural и integration smoke checks replicated repo установить `BYTEPRESS_ROOT` на путь к исходному `BytePress`;
- затем из корня продукта выполнить `BYTEPRESS_ROOT=/path/to/BytePress scripts/dev-test.sh`;
- если ранний product-start сорвался, выполнить `scripts/reset-product-start.sh` и прочитать его drift report;
- при проверке controlled integration contour выполнить `BYTEPRESS_ROOT=/path/to/BytePress scripts/integration-smoke.sh`;
- report artifact integration smoke будет записан в `Runtime/Integration_Smoke_Report.json` как runtime-local файл;
- baseline commit generated repo не должен содержать этот artifact по умолчанию; если текущий pass явно сохраняет smoke evidence в Git, это решение должно быть зафиксировано в current `Plan` и итоговом отчёте.
