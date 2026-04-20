# Setup_Guide

## Базовая среда
- Linux или WSL
- Git
- Python 3.11+

## Рабочий каталог
- Репозиторий продукта располагается отдельно от BytePress.

## Проверка
- для structural и integration smoke checks replicated repo установить `BYTEPRESS_ROOT` на путь к исходному `BytePress`;
- затем из корня продукта выполнить `BYTEPRESS_ROOT=/path/to/BytePress scripts/dev-test.sh`;
- при проверке controlled integration contour выполнить `BYTEPRESS_ROOT=/path/to/BytePress scripts/integration-smoke.sh`;
- report artifact integration smoke будет записан в `Runtime/Integration_Smoke_Report.json` как runtime-local файл;
- baseline commit generated repo не должен содержать этот artifact по умолчанию; если текущий pass явно сохраняет smoke evidence в Git, это решение должно быть зафиксировано в current `Plan` и итоговом отчёте.
