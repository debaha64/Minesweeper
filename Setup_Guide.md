# Setup_Guide

## Базовая среда
- Linux или WSL
- Git
- Python 3.11+

## Рабочий каталог
- Репозиторий продукта располагается отдельно от BytePress.

## Стартовый маршрут Git
```bash
git init -b develop
git add .
git commit -m "Bootstrap baseline"
git checkout -b feature/000001-confirm-current-truth
```

## Проверка
- первый product-start pass остаётся только аналитическим, пока пользователь не подтвердил `Docs/Discovery/Interview.md`;
- первое записываемое действие, включая `Docs/Discovery/*`, `Plans/*` и `Logs/*`, допускается только после открытия task-ветки с типом `chore/`, `feature/`, `fix/` или `docs/`;
- structural check выполняется локально: `python3 Tools/product_check.py --repo . --mode auto`;
- smoke check выполняется локально: `python3 Tools/product_bootstrap_smoke.py`;
- переходные `scripts/*` можно использовать только как оболочки к этим локальным tools;
- report artifacts пишутся в `Tools/.reports/` и не входят в baseline commit.
