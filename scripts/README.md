# scripts

`scripts/*` — project entry scripts replicated product repo.

- `dev-up.sh` — placeholder старта локального product contour.
- `dev-down.sh` — placeholder остановки локального contour.
- `dev-test.sh` — structural check route через `BYTEPRESS_ROOT` с автоопределением режима fresh/developed product repo.
- `integration-smoke.sh` — controlled integration handoff route через `BYTEPRESS_ROOT` с runtime-local report artifact в `Runtime/Integration_Smoke_Report.json`.
- `reset-product-start.sh` — cleanup route failed early product-start с drift report.
- report artifact по умолчанию остаётся вне baseline commit и force-add допускается только при явном evidence-preservation решении текущего pass.
