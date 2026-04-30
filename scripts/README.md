# scripts

`scripts/*` — переходные shell-оболочки к локальному `Tools/*`.

Основной служебный слой продукта — `Tools/*`. Новые сценарии должны вызывать `Tools/product_check.py` и `Tools/product_bootstrap_smoke.py` напрямую.

Срок переходного удаления: после первого service-layer update pass созданного продукта или при следующем major profile package contract, если продукту не нужны shell aliases.
