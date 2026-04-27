# PLAN-000002 — Python Minesweeper first playable

ID: PLAN-000002
Название: Python Minesweeper first playable
Статус: Завершено
Связи: BACK-000002
Источник: Подтверждённая current truth в `Docs/Discovery/Interview.md`
Дата_создания: 2026-04-25
Дата_изменения: 2026-04-25
Основание: Пользователь подтвердил первый предметный результат как запускаемую локальную игру «Сапёр» на Python для одного игрока.
Связанные_требования:
Связанные_backlog: BACK-000002
Связанные_ADR:

## Scope
- Реализовать минимальную локальную игру «Сапёр» без внешних Python-зависимостей.
- Поддержать один фиксированный стартовый режим поля.
- Дать команду запуска из корня репозитория.
- Добавить тестируемое игровое ядро и локальные тесты.

## Out of scope
- Рекорды.
- Настройки сложности.
- Установщик.
- Графические ассеты.
- Онлайн-режим.
- Сохранения.
- Темы оформления.

## Шаги
1. Обновить product/user/technical docs под подтверждённый предметный scope.
   - DoD: документы описывают локальную игру, запуск и границы первой версии.
2. Реализовать Python package `minesweeper` с игровым ядром и entrypoint.
   - DoD: `python3 -m minesweeper` запускает playable loop.
3. Добавить локальные тесты на ключевые правила поля.
   - DoD: `python3 -m unittest` проходит.
4. Провести доступные проверки и записать evidence в `Logs/*`.
   - DoD: quality log содержит факты выполненных проверок и ограничения среды.

## Риски
- В текущей среде отсутствует `tkinter`, поэтому первый pass не должен зависеть от GUI toolkit.
- Поле и сложность должны быть фиксированы, чтобы не расширять scope настройками.

## DoD
Один локальный игрок может запустить игру из репозитория и сыграть партию «Сапёр» на Python; код проходит локальные тесты без внешних зависимостей.

## Итог
Первый playable pass реализован 2026-04-25.

### Evidence
- `python3 -m unittest` — passed, 4 tests.
- `printf 'q\n' | python3 -m minesweeper` — passed, entrypoint starts and exits cleanly.
- `BYTEPRESS_ROOT=/home/dmin/code/BytePress scripts/integration-smoke.sh` — passed.
- `BYTEPRESS_ROOT=/home/dmin/code/BytePress scripts/dev-test.sh` — passed after synchronization with current BytePress; structural check detects `product-developed` mode.
