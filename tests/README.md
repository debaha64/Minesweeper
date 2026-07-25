# tests

`tests/` хранит поведенческие проверки продукта и узкие локальные regression tests Harness. В starter присутствует только `test_sot_modes.py`, который доказывает конфигурацию, dispatch и network isolation трёх режимов. Тесты продукта создаются после решения владельца или active PLAN фазы `implementation` / `verification`.

Временные проверки создаются через `mktemp -d` вне поставочного дерева. Каталог `fixtures/` в поставочном дереве не создаётся.
