# Git

## Назначение

Документ описывает смысл локального Git-слоя SoT. Процедура находится в [../../sops/sot.md](../../sops/sot.md).

## Режимы

1. `sot_files` использует только файловый контроль; Git не читается и Git CLI не вызывается.
2. `sot_git` добавляет локальный repository, `HEAD`, рабочее дерево и локальные изменения.
3. `sot_github` связывает подготовленную локальную рабочую копию с ожидаемым GitHub repository через единственный `origin`, upstream и local `origin/HEAD`.

Remote, push, PR, merge, tag, выпуск и GitHub write не разрешаются самим режимом SoT.

## Текущая проверка `sot_git`

`bp_check.py` проверяет:

1. точный Product Unit root;
2. валидный repository и `HEAD`;
3. рабочую ветку и clean working tree;
4. remote absent.

Грязное дерево всегда даёт `FAIL`. История коммитов, reflog и terminal-последовательности не реконструируются.

Объявленный `SOT_MODE: sot_git` разрешает только bootstrap отсутствующего неизменённого repository. Переход, локальная работа и реализация требуют отдельных решений владельца согласно `sops/sot.md` и active PLAN.

## Локальная проверка `sot_github`

`bp_check.py` дополнительно проверяет machine-readable `owner/repository`, ровно один `origin`, поддерживаемый URL, matching identity, upstream, existing local remote refs, symbolic `origin/HEAD` и отсутствие behind/diverged state. Checker не выполняет сеть, fetch или repair; freshness и authentication принадлежат внешнему preflight.

Default/release branch names и merge methods являются repository policy, а не полями core mode. Обратные переходы в `0.5.0` не реализованы.
