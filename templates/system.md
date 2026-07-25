# SYSTEM.md

## Режимы SoT

supported:

- `sot_files`
- `sot_git`
- `sot_github`

`SOT_MODE` хранит устойчивое состояние. Только при `sot_github` `AGENTS.md` содержит условный `SOT_GITHUB_REPOSITORY` в форме `owner/repository`. Переходы и разрешения владельца хранятся в типизированных записях.
