# scripts

`scripts/*` — переходные shell-оболочки к локальному `Tools/*`.

Основной служебный слой продукта — `Tools/*`. Новые сценарии должны вызывать `Tools/product_check.py` и `Tools/product_bootstrap_smoke.py` напрямую.
