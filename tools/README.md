# Инструменты

Локальные инструменты Product Unit:

- `bp_init.py` показывает текущий `ROAD -> BACK -> PLAN`, фазу и `SOT_MODE`, а при `sot_github` также локально читает и выводит `SOT_GITHUB_REPOSITORY`; он создаёт только отсутствующие обязательные журналы и README product `research/`;
- `bp_check.py` выполняет лёгкую проверку текущего состояния Product Unit;
- `bp_clean.py` удаляет одноразовые Python-файлы; `.agents/` и `.codex/` обрабатываются только с `--local-service`, а используемые долговечные журналы сохраняются.

Инструменты не создают продукт, не управляют Workspace и не выполняют bootstrap Git.

## Граница проверки

`bp_check.py` проверяет:

1. безопасную границу symlink и локальных путей;
2. наличие обязательных текущих файлов;
3. валидность локальных Markdown-ссылок;
4. от нуля до одного active PLAN и его минимальные поля;
5. `ALLOWED_SURFACES` и защиту системных файлов;
6. `SOT_MODE` как единственное объявление одного из трёх режимов и условное поле `SOT_GITHUB_REPOSITORY` только при `sot_github`;
7. отсутствие Git-вызовов при `sot_files`;
8. текущий repository root, `HEAD`, clean tree и remote absent при `sot_git`;
9. при `sot_github` — подготовленные локальные `origin`, URL identity, upstream, remote refs, symbolic `origin/HEAD` и допустимую divergence;
10. отсутствие disposable current paths;
11. product identity, product-first root README и границу `docs/user`;
12. текущие ссылки active PLAN на IE, implementation decision и product acceptance;
13. текущий product state и фазу active PLAN.

Проверка не реконструирует Git-историю, не классифицирует коммиты, не использует сеть и не выполняет automatic repair. GitHub metadata, authentication, fetch и подготовка `origin/HEAD` относятся к внешнему preflight.

## Команды

```bash
python3 -m py_compile tools/bp_init.py tools/bp_check.py tools/bp_clean.py
python3 -m unittest discover -s tests -p 'test_*.py'
python3 tools/bp_init.py --repo .
python3 tools/bp_check.py --repo .
python3 tools/bp_clean.py --repo . --apply
python3 tools/bp_check.py --repo .
```

В `sot_files` инструменты не читают `.git` и не вызывают Git CLI. В `sot_git` проверяется только текущий локальный root; remote и грязное дерево дают `FAIL`. В `sot_github` checker использует только уже существующие локальные Git refs и никогда не вызывает fetch, pull, push, `gh`, `curl` или `wget`.

## Дефект Harness

При дефекте Harness в `product-work` агент выводит:

```text
HARNESS_BLOCKER: <краткое описание>
```

и прекращает изменения. Исправление не проектируется из `product-work`; owner-initiated `system-editing` начинается с уже принятого решения владельца и active PLAN.

Технический PASS не создаёт `PA-*` и не является продуктовой приёмкой.
