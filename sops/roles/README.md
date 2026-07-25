# Роли

Роли помогают агенту исполнять задачу в границах PLAN.

Карта фаз и ролей:

- Фаза `discovery` -> researcher -> architect -> verifier
- Фаза `implementation` -> implementer -> verifier только после решения владельца и точки контроля `implementation`
- Подготовка продуктовой приёмки -> product-acceptance-assistant
- Release -> release-assistant только после решения владельца
- Архивирование -> archive-curator только после решения владельца

Продуктовая приёмка, выпуск, тег и архив не выполняются verifier, чистым завершением (`clean-exit`) или техническим PASS. Эти переходы требуют отдельного решения владельца и отдельного PLAN.
