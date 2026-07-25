# Проверки

Техническое свидетельство Product Unit состоит из:

1. product unit tests;
2. product smoke;
3. `bp_check.py`.

BytePress Harness также поставляет локальные unit tests трёх SoT handlers: configuration, Git isolation, repository/remote identity, upstream, `origin/HEAD`, divergence и negative network-command boundary. Fixtures создаются только во временных каталогах и не входят в Product Unit tree.

`bp_check.py` проверяет текущее состояние Product Unit, но не реконструирует историческую последовательность. Technical PASS не является продуктовой приёмкой и не создаёт `PA-*`.

После появления продуктового кода root `README.md` проверяется как пользовательская точка входа: название, назначение и ценность, пользователь, запуск, основные команды, хранение данных, ограничения и проверки.

Готовность к выпуску, выпуск, tag и GitHub-действия относятся к отдельным owner-gated маршрутам. Процедура проверки описана в [../../sops/verify-work.md](../../sops/verify-work.md).
