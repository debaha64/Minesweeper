# Записи решений

## Решение владельца `OD-*`

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
ROUTE_REF: none | BACK-000001
ALLOWED_ACTIONS: write src,write tests
PREVIOUS_STATUS: none
STATUS: active
SOURCE_KIND: owner_response
SOURCE_REF: codexlog:.codex/<actual-raw-file>.raw.log#lines=<start>-<end>
```

Для implementation-решения `PLAN_ID` указывает implementation PLAN, а `EVIDENCE_REF` — обычный capture IE или переиспользуемый transition IE. Для `local_git_route` и `sot_transition` перехода `EVIDENCE_REF` указывает transition IE той же сессии; обе OD и IE используют `PLAN_ID` transition PLAN и впервые фиксируются вместе с ним в одном transition commit. Runtime использует локальный конечный диапазон raw.

Если `EVIDENCE_REF` указывает transition IE, downstream implementation OD также использует существующий конечный raw locator. Ordinary historical OD с корректной ссылкой на существующий clean `.log` сохраняется без миграции.

`implementation` и `sot_transition`: `active -> applied | revoked`.

`local_git_route`: `active -> suspended -> active`, `active -> closed | revoked`, `suspended -> closed | revoked`.

Для одного `ROUTE_REF` создаётся одна запись `local_git_route`. В обычном маршруте её `PLAN_ID` фиксирует PLAN, при котором получено решение. В transition checkpoint принятого продукта это transition PLAN, управляющий применением выбора `B`, а не ранее существовавший PLAN получения реплики. В обоих случаях `PLAN_ID` не ограничивает разрешение одним PLAN: последовательные PLAN того же BACK используют маршрут до terminal closeout и не обязаны повторять route OD в `OWNER_DECISION_REFS`. Вторая запись для того же BACK недопустима; `closed` остаётся историческим свидетельством и не разрешает новые коммиты.

## Продуктовая приёмка `PA-*`

```text
RECORD_TYPE: product_acceptance
RECORD_ID: PA-000001
PLAN_ID: PLAN-000002
DECISION_VALUE: accepted | rejected
SOURCE_KIND: owner_response
SOURCE_REF: codexlog:.codex/<actual-raw-file>.raw.log#lines=<start>-<end>
```

Локальная ссылка `PA-*` разрешается в конечный диапазон фактического ответа владельца. Итоговая техническая проверка фиксируется отдельной записью качества.

Если PLAN ссылается через `INTERVIEW_EVIDENCE_REF` на transition IE, `PA.SOURCE_REF` обязан указывать существующий долговечный `*.raw.log`; acceptance raw может отличаться от transition raw. Ordinary historical PA с существующим clean evidence остаётся валидной.
