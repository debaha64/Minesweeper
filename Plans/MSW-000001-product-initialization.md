# PLAN-000001 — Product initialization

ID: PLAN-000001
Название: Product initialization
Статус: В_работе
Связи: BACK-000001
Источник: First current pass replicated product repo
Дата_создания: 2026-04-22
Дата_изменения: 2026-04-22
Основание: Bootstrap materialize first-usable replicated product repo; первый pass должен подтвердить discovery current truth ответами пользователя и не трактовать placeholders как разрешение на implementation.
Связанные_требования:
Связанные_backlog: BACK-000001
Связанные_ADR:

## Шаги
1. Подтвердить current truth в `Docs/Discovery/Interview.md` явными ответами пользователя.
   - DoD: статус current truth больше не остаётся bootstrap-placeholder.
2. Синхронизировать discovery-only contour с `Plans/*` и `Logs/*`.
   - DoD: planning/log route отражает подтверждённую current truth без выхода в product docs или implementation.
3. Открыть следующий предметный pass только после подтверждённой current truth.
   - DoD: следующий scope сформулирован отдельно и не смешан с bootstrap placeholders.

## Риски
- bootstrap placeholders могут быть ошибочно приняты за утверждённый scope;
- отсутствие явных ответов пользователя заблокирует предметный pass.

## Артефакты
- AGENTS.md
- Docs/*
- Plans/*
- Logs/*
- Profiles/Product.md
- Adapters/*
- scripts/*

## DoD
Bootstrap-created current truth подтверждена, discovery-only gate снят явным решением, а следующий предметный pass открыт отдельно.
