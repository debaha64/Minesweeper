# Minesweeper

## Назначение и ценность

Локальная минимальная regression-fixture игрового ядра.

## Пользователь

Пользователь локального приложения.

## Запуск

`python3 src/minesweeper.py --smoke`

## Основные команды

Smoke и unit tests.

## Хранение данных

Постоянное хранение не используется.

## Ограничения

Fixture проверяет только подсчёт соседних мин.

## Проверки

`python3 -m unittest discover -s tests -p 'test_minesweeper.py'`
