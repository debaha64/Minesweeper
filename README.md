# Minesweeper

## Назначение и ценность

Локальная минимальная regression-fixture игрового ядра.

## Пользователь

Пользователь локального приложения.

## Запуск

`python3 src/minesweeper.py --smoke`

## Основные команды

Подсчёт мин в соседних клетках:

```bash
python3 src/minesweeper.py count --row <row> --column <column> <board-row> [<board-row> ...]
```

Координаты отсчитываются от нуля. Поле должно быть непустым и прямоугольным
и может содержать только `*` и `.`.

Пример:

```bash
python3 src/minesweeper.py count --row 1 --column 1 '*.' '..'
```

Вывод:

```text
1
```

Smoke:

```bash
python3 src/minesweeper.py --smoke
```

## Хранение данных

Постоянное хранение не используется.

## Ограничения

Команда `count` только подсчитывает соседние мины; состояние не сохраняется.

## Проверки

`python3 -m unittest discover -s tests -p 'test_minesweeper.py'`
