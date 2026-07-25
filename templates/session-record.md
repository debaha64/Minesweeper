# Запись сессии

```text
RECORD_TYPE: interview_evidence
RECORD_ID: IE-000001
PLAN_ID: PLAN-000001
SESSION_ID: SESSION-000001
LAYERS_COMPLETE: product-frame,user-scenario,data-storage,technical-frame,verification-dod,next-transition
LAYERS_DEFERRED: none
STATUS: complete
SOURCE_KIND: owner_response
SOURCE_REF: codexlog:.codex/<actual-raw-file>.raw.log#lines=<start>-<end>
```

Для обычной записи без `EVIDENCE_CLASS: transition` поле `PLAN_ID` — capture PLAN, active в момент фактического получения интервью. Implementation PLAN хранит ссылку `INTERVIEW_EVIDENCE_REF: IE-...`; поля `BASIS_PLAN_ID` и `CAPTURE_PLAN_ID` не добавляются. Runtime использует локальный конечный диапазон raw.

Для transition checkpoint к той же записи добавляются поля `EVIDENCE_CLASS: transition`, `PRODUCT_INPUT_REF` и `ROUTE_CHOICE_REF`. Её `PLAN_ID` — transition PLAN, созданный из того же выбора `B` и впервые зафиксированный вместе с IE и обеими OD в одном transition commit и `SESSION_ID`. Оба locator указывают один `*.raw.log` и доказывают `PRODUCT_INPUT -> B`; они не доказывают существование PLAN до checkpoint. Следующий discovery PLAN переиспользует IE без копии.
