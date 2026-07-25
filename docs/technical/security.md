# Безопасность

## Смысловые границы

Безопасность Product Unit держится на явных границах: секреты не являются содержанием обвязки, удалённые действия не являются побочным эффектом технического PASS, а входные файлы владельца не становятся Source of Truth автоматически.

## GitHub и удалённые действия

GitHub, удалённые Git-действия, `push`, `PR`, `tag` и GitHub Release относятся к внешнему слою. Скрытое выполнение таких действий разрушает принцип: человек управляет, агенты исполняют.

`bp_check.py` не читает credentials или SSH config, не вызывает сеть и не исправляет remote. Внешний preflight проверяет identity, authentication, repository metadata и permissions без сохранения token/private key в Product Unit. Remote с local path, `file://` или embedded HTTP credentials отклоняется.

## Входные файлы владельца

Входной файл владельца является источником сведений или свидетельством. Внутренним состоянием Product Unit он становится только после решения владельца и переноса принятого смысла в `docs/`, `plans/` или `logs/`.

## Где процедура

Граница SoT, GitHub, `remote`, `tag` и GitHub Release описана в [../../sops/sot.md](../../sops/sot.md). Проверки и передача результата описаны в [../../sops/verify-work.md](../../sops/verify-work.md), [../../sops/clean-exit.md](../../sops/clean-exit.md) и [../../sops/managed-agent-pass.md](../../sops/managed-agent-pass.md).
