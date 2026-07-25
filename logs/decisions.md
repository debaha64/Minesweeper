# Решения

Фиксирует типизированные решения владельца после явного ответа владельца.

RECORD_TYPE: owner_decision
RECORD_ID: OD-000001
PLAN_ID: PLAN-000001
SESSION_ID: SESSION-000002
DECISION_KIND: sot_transition
DECISION_VALUE: approved
EVIDENCE_REF: IE-000001
SOT_FROM: sot_files
SOT_TO: sot_git
ROUTE_REF: BACK-000001
ALLOWED_ACTIONS: change AGENTS.md SOT_MODE,create local baseline,create transition checkpoint,verify local repository
PREVIOUS_STATUS: active
STATUS: applied
SOURCE_KIND: owner_response
SOURCE_REF: codexlog:.codex/codex-20260726-011410.raw.log#lines=163-164

RECORD_TYPE: owner_decision
RECORD_ID: OD-000002
PLAN_ID: PLAN-000001
SESSION_ID: SESSION-000002
DECISION_KIND: local_git_route
DECISION_VALUE: approved
EVIDENCE_REF: IE-000001
SOT_FROM: sot_files
SOT_TO: sot_git
ROUTE_REF: BACK-000001
ALLOWED_ACTIONS: initialize local Git,create local commits,verify root HEAD branch clean and remote absent
PREVIOUS_STATUS: none
STATUS: active
SOURCE_KIND: owner_response
SOURCE_REF: codexlog:.codex/codex-20260726-011410.raw.log#lines=163-164
