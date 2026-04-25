# System_Invariants

## Инварианты
- продукт остаётся отдельным репозиторием вне дерева `BytePress`;
- human/agent entry contour не спорит с planning contour;
- незаполненный discovery bootstrap не считается разрешением на изменение `Docs/Product/*`, `Docs/Technical/*`, `Runtime/*` или предметной реализации;
- product repo не превращается в полную копию `BytePress`.
- первый playable pass игры не требует внешних Python-зависимостей;
- игровая логика отделена от интерактивного CLI-интерфейса.
