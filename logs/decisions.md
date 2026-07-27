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

RECORD_TYPE: owner_decision
RECORD_ID: OD-000003
PLAN_ID: PLAN-000001
SESSION_ID: SESSION-000003
DECISION_KIND: sot_transition
DECISION_VALUE: approved
EVIDENCE_REF: IE-000001
SOT_FROM: sot_git
SOT_TO: sot_github
ROUTE_REF: BACK-000001
ALLOWED_ACTIONS: add origin,fetch main and develop,set origin HEAD,create local develop with upstream,change AGENTS.md SOT fields,create transition commit,verify local repository
PREVIOUS_STATUS: active
STATUS: applied
SOURCE_KIND: owner_response
SOURCE_REF: codexlog:.codex/codex-20260726-220340.raw.log#lines=404-442

RECORD_TYPE: owner_decision
RECORD_ID: OD-000004
PLAN_ID: PLAN-000001
SESSION_ID: SESSION-000004
DECISION_KIND: implementation
DECISION_VALUE: approved
EVIDENCE_REF: IE-000001
SOT_FROM: none
SOT_TO: none
ROUTE_REF: BACK-000001
ALLOWED_ACTIONS: write README.md,write src/minesweeper.py,write tests/test_minesweeper.py,run local tests,run deterministic smoke
PREVIOUS_STATUS: active
STATUS: applied
SOURCE_KIND: owner_response
SOURCE_REF: codexlog:.codex/codex-20260727-041316.raw.log#lines=556-562

RECORD_TYPE: owner_decision
RECORD_ID: OD-000005
PLAN_ID: PLAN-000001
SESSION_ID: SESSION-000005
DECISION_KIND: github_pr
DECISION_VALUE: approved
EVIDENCE_REF: IE-000001
SOT_FROM: none
SOT_TO: none
ROUTE_REF: BACK-000001
ALLOWED_ACTIONS: correct local Git identity,create feature branch via --track=inherit,commit exact seven tracked paths,run local checks,push feature branch,create PR targeting develop,verify exact PR head
PREVIOUS_STATUS: none
STATUS: active
SOURCE_KIND: owner_response
SOURCE_REF: codexlog:.codex/codex-20260727-055446.raw.log#lines=638-638
