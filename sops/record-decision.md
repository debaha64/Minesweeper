# Запись

Целевой артефакт: `logs/decisions.md`.
Шаблон или формат: `templates/decision-record.md`.
Способ записи: дозапись.

Канонический runtime `SOURCE_REF` новых типизированных решений использует точный конечный диапазон долговечного `codexlog:.codex/<actual-raw-file>.raw.log#lines=<start>-<end>`. Clean `.log` является presentation evidence и не обещает совпадение строк. Существующие ordinary accepted IE/OD/PA сохраняют валидность корректного locator существующего clean `.log` без миграции или нового поля. Локальная схема `owner_decision` или `product_acceptance` и `SOURCE_KIND: owner_response` задаёт ожидаемый класс источника.

`local_git_route` и `sot_transition` перехода принятого продукта обязаны ссылаться через `EVIDENCE_REF` на IE текущей задачи класса `transition`, иметь тот же `SESSION_ID` и один raw source выбора `B`; `PRODUCT_INPUT_REF` этого IE расположен раньше выбора. Исторический IE принятого продукта из предыдущей сессии не подходит.

Любой последующий `owner_decision`, чей `EVIDENCE_REF` указывает transition IE, также обязан использовать существующий конечный raw locator. Позднее implementation permission может находиться в другом raw-файле. Если product acceptance относится к PLAN с `INTERVIEW_EVIDENCE_REF` на transition IE, `PA.SOURCE_REF` обязан использовать долговечный raw-файл, который также может отличаться от raw перехода.

`owner_decision.SOURCE_REF` указывает фактическую реплику решения владельца, а `product_acceptance.SOURCE_REF` — фактическую реплику продуктовой приёмки. Итоговая техническая проверка фиксируется отдельно и не подменяет приёмку.
