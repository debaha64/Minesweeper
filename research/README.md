# Исследования

## Назначение

`research/` хранит формальные исследовательские домены Product Unit. Исследование собирает факты, риски, альтернативы и свидетельства, которые могут стать входом для `ROAD -> BACK -> PLAN`, решения владельца, требований или проверки.

Исследование не заменяет active PLAN и не подменяет решение владельца. Владелец принимает смысловые решения отдельно; агент фиксирует исследовательское свидетельство и связывает его с плановым контуром.

## Структура

```text
research/README.md
research/archives/README.md
research/<xxx>-<slug>/000-index.md
research/<xxx>-<slug>/001-<slug>.md
research/<xxx>-<slug>/results.md
```

Дополнительные записи внутри домена продолжают нумерацию:

```text
research/<xxx>-<slug>/002-<slug>.md
research/<xxx>-<slug>/003-<slug>.md
```

## Правила

Правила жизненного цикла, нумерации, evidence, closeout и архивирования находятся в [../sops/research.md](../sops/research.md).

Формы research-записей находятся в [../templates/](../templates/):

1. `research-domain-index.md`;
2. `research-record.md`;
3. `research-results.md`;
4. `owner-decision-package.md`.

## Граница

1. `research/README.md` является индексом домена.
2. `research/archives/README.md` является индексом архивов.
3. `000-index.md` создаётся только внутри конкретного research-домена.
4. Исследование не создаёт второй active PLAN.
5. Исследование не разрешает реализацию, продуктовую приёмку, готовность к выпуску, release/tag или GitHub-действия.
