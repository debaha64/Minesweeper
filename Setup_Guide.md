# Setup_Guide

## Базовая среда
- Linux или WSL
- Git
- Python 3.11+
- Tkinter для запуска desktop-окна

## Рабочий каталог
- Репозиторий продукта располагается отдельно от BytePress.

## Git start route
```bash
git init -b develop
git add .
git commit -m "Bootstrap baseline"
git checkout -b feature/000001-confirm-current-truth
```

## Запуск игры
```bash
python3 -m minesweeper
```

## Проверка
- текущая истина подтверждена в `Docs/Discovery/Interview.md`;
- каждый записываемый pass начинается после открытия task-ветки;
- логика проверяется командой `python3 -m unittest discover`;
- structural check выполняется локально: `python3 Tools/product_check.py --repo . --mode auto`;
- smoke check выполняется локально: `python3 Tools/product_bootstrap_smoke.py`;
- переходные `scripts/*` можно использовать только как оболочки к этим локальным tools;
- report artifacts пишутся в `Tools/.reports/` и не входят в baseline commit.
