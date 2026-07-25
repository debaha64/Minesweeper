# Интервью

## Назначение

Интервью превращает начальный запрос владельца в проверяемый контекст. Императивный запрос фиксирует замысел, но не открывает реализацию.

## Обязательные слои

1. `product-frame` — рамка продукта.
2. `user-scenario` — пользовательский сценарий и CLI.
3. `data-storage` — данные и хранение.
4. `technical-frame` — техническая рамка.
5. `verification-dod` — проверки и DoD.
6. `next-transition` — следующий переход.

Каждый слой должен быть `complete` или `deferred` с причиной. `open` даёт `FAIL`. Отложенный слой записывается в виде `<layer>=<причина>`; имя слоя без причины невалидно.

`SOT_MODE` не является слоем или вопросом продуктового интервью. Устойчивый режим читается из `AGENTS.md`; bootstrap отсутствующего репозитория завершается до интервью. Transition и изменяющая локальная Git-работа требуют отдельных типизированных решений по `sops/sot.md`.

Начальный пакет интервью не содержит вопроса или запроса разрешения `local_git_route`. Сначала владелец передаёт фактический `PRODUCT_INPUT`. Для уже объявленного `sot_git` только после этого агент отдельной репликой запрашивает route. Ответ внутри начального интервью, предварительное упоминание route или команда «Продолжай» маршрут не открывают.

Полный `PRODUCT_INPUT` закрывает пять продуктовых слоёв интервью без дополнительного подтверждения `Да`. Агент сразу переходит к слою `next-transition`: при первоначальном создании продукта в `sot_files` это обычный discovery без выбора маршрута; для принятого продукта действует раздел ниже; в уже объявленном `sot_git` это отдельный запрос `local_git_route`. Неполный `PRODUCT_INPUT` по-прежнему требует уточнений по незакрытым слоям.

Карточка implementation gate готовится только после зафиксированного и проверенного discovery checkpoint. Единственный owner gate реализации — новая отдельная однозначная реплика `Разрешаю реализацию <Product Unit>.`, полученная после этой проверки.

## Выбор маршрута принятого продукта

Выбор маршрута в слое `next-transition` обязателен только при одновременном выполнении условий:

1. состояние продукта — `accepted-completed`;
2. задача является новой;
3. полный `PRODUCT_INPUT` получен;
4. текущий режим — `sot_files`;
5. поддерживаемый следующий режим — `sot_git`.

После закрытия пяти продуктовых слоёв агент не делает постоянных изменений, останавливается и один раз предлагает:

```text
A. Продолжить задачу в текущем sot_files.
B. Перейти из sot_files в sot_git.
C. Отложить задачу.
D. Другой вариант.
```

Семантика ответа:

1. `A` — текущий режим остаётся `sot_files`; Git не создаётся; агент выполняет обычный discovery, проверяет discovery/evidence checkpoint и только затем готовит отдельный implementation gate.
2. `B` — одна реплика владельца одновременно выбирает `sot_git`, разрешает переход и предоставляет `local_git_route`. Агент не задаёт повторных вопросов о переходе, локальном Git или подтверждении выбора.
3. `C` — постоянные изменения не выполняются; отложенное состояние фиксируется только там, где это разрешено текущим режимом и плановым контуром.
4. `D` — агент уточняет другой вариант владельца и не считает переход разрешённым до однозначного решения.

Первоначальное создание продукта не получает выбор маршрута. Выбор также не выполняется для незавершённой текущей задачи, до полного `PRODUCT_INPUT` или при отсутствии поддерживаемого следующего режима. Выбор маршрута не является разрешением реализации: после перехода и проверенного discovery/evidence checkpoint требуется новая отдельная implementation permission.

## Свидетельство интервью

Свидетельство хранится в `logs/sessions.md` как `RECORD_TYPE: interview_evidence`. Для обычного discovery оно является discovery evidence. Для перехода принятого продукта то же `RECORD_TYPE` получает `EVIDENCE_CLASS: transition` и входит в transition commit; новый тип evidence не создаётся.

Минимальные поля:

```text
RECORD_TYPE: interview_evidence
RECORD_ID: IE-000001
PLAN_ID: PLAN-000001
SESSION_ID: SESSION-000001
LAYERS_COMPLETE: product-frame,user-scenario,data-storage,technical-frame,verification-dod,next-transition
LAYERS_DEFERRED: none | data-storage=отложено владельцем до следующего slice
STATUS: complete
SOURCE_KIND: owner_response
SOURCE_REF: codexlog:.codex/<actual-raw-file>.raw.log#lines=<product-input-start>-<product-input-end>
```

Для обычного IE без `EVIDENCE_CLASS: transition` поле `PLAN_ID` указывает capture PLAN, active в момент фактического получения ответов интервью. Будущий implementation PLAN не записывается в IE и ссылается на него через `INTERVIEW_EVIDENCE_REF`. `SOURCE_REF` указывает существующий конечный диапазон фактического ответа внутри долговечного `.codex/*.raw.log`; ожидаемый класс — `owner_answer` или `owner_confirmation`. `SOURCE_KIND: agent_inference` запрещён.

Существующие ordinary accepted records могут сохранять корректный locator существующего clean `.log`; такая историческая совместимость не требует миграции или нового поля записи.

Transition IE дополнительно содержит:

```text
EVIDENCE_CLASS: transition
PRODUCT_INPUT_REF: codexlog:.codex/<actual-raw-file>.raw.log#lines=<start>-<end>
ROUTE_CHOICE_REF: codexlog:.codex/<actual-raw-file>.raw.log#lines=<choice>-<choice>
```

Оба диапазона принадлежат тому же raw-файлу и текущему `SESSION_ID`; полный `PRODUCT_INPUT` расположен раньше выбора `B`. Узкое исключение действует только для принятого продукта, новой задачи и перехода `sot_files -> sot_git`: `PLAN_ID` transition IE указывает transition PLAN, созданный из того же выбора `B` и впервые зафиксированный вместе с IE и обеими OD в одном transition commit. Не утверждается, что этот PLAN существовал или был active при получении `PRODUCT_INPUT` либо `B`; время и порядок owner input доказывают `PRODUCT_INPUT_REF`, `ROUTE_CHOICE_REF`, `SOURCE_REF` и `SESSION_ID`. Transition IE закрывает пять продуктовых слоёв и `next-transition`, но не открывает реализацию. Следующий feature/discovery PLAN ссылается на этот IE без создания второй записи и без смены `EVIDENCE_CLASS`.

## Решение реализации

Реализация требует отдельного `owner_decision` в `logs/decisions.md`:

```text
RECORD_TYPE: owner_decision
RECORD_ID: OD-000001
PLAN_ID: PLAN-000002
SESSION_ID: SESSION-000001
DECISION_KIND: implementation
DECISION_VALUE: approved
EVIDENCE_REF: IE-000001
SOT_FROM: none
SOT_TO: none
ALLOWED_ACTIONS: write product slice
ROUTE_REF: none
PREVIOUS_STATUS: none
STATUS: active
SOURCE_KIND: owner_response
SOURCE_REF: codexlog:.codex/<actual-raw-file>.raw.log#lines=<start>-<end>
```

PLAN хранит только ссылки:

```text
INTERVIEW_EVIDENCE_REF: IE-000001
OWNER_DECISION_REFS: OD-000001
```

Для валидного gate обычный `IE.PLAN_ID` остаётся capture PLAN; у переиспользуемого transition IE он остаётся transition PLAN того checkpoint. `OD.PLAN_ID` реализации совпадает с active implementation PLAN. `EVIDENCE_REF` решения и `INTERVIEW_EVIDENCE_REF` implementation PLAN ссылаются на один валидный `IE-*`. Дополнительные поля `BASIS_PLAN_ID` и `CAPTURE_PLAN_ID` не используются.

Если связанный `IE-*` имеет `EVIDENCE_CLASS: transition`, `SOURCE_REF` implementation OD обязан указывать существующий конечный диапазон долговечного `*.raw.log`. Более позднее разрешение реализации может находиться в другом локальном raw-файле.

Временная граница решения:

1. discovery/evidence checkpoint уже зафиксирован;
2. собственная проверка этого checkpoint завершилась PASS;
3. только после этого агент запрашивает решение реализации;
4. только новый последующий ответ владельца создаёт implementation `OD-*`;
5. `OD-*` и ссылка active implementation PLAN фиксируются вместе с отдельным `implementation-open` checkpoint.

Если реплика `Разрешаю реализацию <Product Unit>.` пришла до завершения и проверки discovery checkpoint, агент:

1. не создаёт implementation `OD-*`;
2. не считает реплику active или applied решением;
3. сообщает, что ответ преждевременный;
4. после PASS discovery повторно запрашивает решение владельца.

До discovery checkpoint каноническая identity фиксируется одновременно:

1. в `docs/product/product-brief.md` под точным заголовком `## Продукт`;
2. в поле `Product Unit` discovery PLAN;
3. в IE и route текущего BACK;
4. в закрытии discovery или подготовленной следующей точке решения.

Переименование `## Продукт` в `## Название` не задаёт identity. Последующие product-work PLAN и product-first README используют то же точное имя.

## Точка контроля реализации

Реализация разрешена только при одновременном выполнении всех условий:

1. каждый обязательный слой имеет `complete` или `deferred` с непустой причиной;
2. `IE-*` валиден, имеет `SOURCE_KIND: owner_response` и указывает PLAN фактического получения;
3. активный `OD-*` имеет `DECISION_KIND: implementation`, `DECISION_VALUE: approved`, относится к implementation PLAN и ссылается на этот `IE-*`;
4. active implementation PLAN ссылается на эти `IE-*` и `OD-*`;
5. начальный запрос зафиксирован как замысел, но не засчитан как ответ на интервью или решение о реализации;
6. implementation `OD-*` впервые появился в отдельном `implementation-open` checkpoint после проверенного discovery;
7. для `initial-idle` до gate в `src/` и `tests/` отсутствуют продуктовый код и поведенческие тесты; для `idle-product` и `accepted-completed` существующий baseline допустим, но до gate product paths не изменяются и не включаются в `ALLOWED_SURFACES` discovery PLAN.

Нарушение любого условия даёт `FAIL`; продуктовая реализация не начинается.

После выполнения одноразового решения реализации его статус меняется `active -> applied`. При закрытии PLAN действующего одноразового решения быть не должно.

## Команда «Продолжай»

Команда «Продолжай» разрешает продолжить текущий информационный слой, уточнение или подготовку следующего пакета вопросов. Она не является решением о смене фазы SDLC, открытии нового маршрута, начале реализации, продуктовой приёмке, готовности к выпуску, выпуске, tag или GitHub-действиях.

Переход фазы или маршрута требует явного выбора владельца.

## Связанные формы

1. `templates/interview.md`.
2. `templates/session-record.md`.
3. `templates/decision-record.md`.
