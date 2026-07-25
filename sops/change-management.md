# Управление изменениями

Целевой артефакт: связанные системные и продуктовые артефакты.
Шаблоны: `templates/change-record.md`, `templates/quality-record.md`.
Способ записи: проверка связей, правка и дозапись.

## Назначение

Процедура предотвращает рассинхронизацию между терминами, SOP, шаблонами, инструментами, фазой, SoT и пользовательскими документами.

## Когда применять

Применять в owner-initiated `system-editing`, а также при изменении:

1. термина или SOP;
2. шаблона или инструмента;
3. фазы, gate или SoT;
4. README или пользовательской документации.

## Карта связей

- термин -> glossary, `SYSTEM.md`, `AGENTS.md`, связанные SOP/templates, `logs/terminology.md`;
- SOP -> `SYSTEM.md`, `AGENTS.md`, связанные SOP/templates/tools, `logs/changes.md`;
- template -> `SYSTEM.md`, `templates/README.md`, применяющая SOP, журналы;
- tool -> `tools/README.md`, `SYSTEM.md`, `tests/README.md`, `logs/quality.md`;
- phase/gate -> `sops/sdlc.md`, `sops/project-management.md`, `templates/plan-active.md`, `bp_check.py`;
- SoT -> `sops/sot.md`, `bp_init.py`, `bp_check.py`, glossary, `SYSTEM.md`, active PLAN и решения владельца;
- README -> `templates/product-readme.md`, `docs/user/`, product identity и текущая фаза;
- docs/SOP boundary -> README соответствующих слоёв, связанная SOP, `logs/changes.md`, `logs/quality.md`.

## Процедура

1. Подтвердить active PLAN и разрешённые поверхности.
2. Определить затронутые связи по карте.
3. Изменить только ставшие ложными или неполными артефакты.
4. Если меняется шаблон, проверить `templates/README.md` и применяющую SOP.
5. Если меняется docs, оставить в docs смысл и ссылки, а порядок действий — в SOP.
6. Если меняется tool, обновить `tools/README.md`, `SYSTEM.md` и релевантные проверки.
7. Если меняется SoT, подтвердить три изолированных handler: отсутствие Git-вызовов в `sot_files`; root/branch/clean/remote absent в `sot_git`; local identity/`origin`/upstream/`origin/HEAD`/divergence и no-network в `sot_github`.
8. Записать факт в `logs/changes.md`, проверки — в `logs/quality.md`, изменившийся риск — в `logs/risks.md`.

## Проверки

```bash
python3 -m py_compile tools/bp_init.py tools/bp_check.py tools/bp_clean.py
python3 tools/bp_check.py --repo .
```

При наличии продуктового кода добавляются product unit tests и product smoke.

## Запреты

1. Не менять связный артефакт без проверки его связей.
2. Не переписывать исторические журналы ради косметической синхронизации.
3. Не выводить продуктовую приёмку, выпуск, tag или GitHub-действия из технического PASS.
4. Не предлагать `system-editing` из `product-work`: при дефекте Harness вывести `HARNESS_BLOCKER: <краткое описание>` и остановиться.
