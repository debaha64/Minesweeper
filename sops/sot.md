# Режим источника истины

`AGENTS.md` — единственное место machine-readable конфигурации устойчивого режима Product Unit.

Поддерживаются ровно:

- `sot_files`;
- `sot_git`;
- `sot_github`.

Обязательное поле `SOT_MODE` существует ровно один раз. Только при `sot_github` рядом существует ровно одно условное поле `SOT_GITHUB_REPOSITORY` со значением `owner/repository`. В двух других режимах это поле отсутствует.

Repository identity:

1. содержит две непустые части через один `/`;
2. не является URL;
3. repository component не оканчивается суффиксом `.git`; whitespace, `:`, `@`, `\`, `?`, `#`, scheme, host и credentials запрещены;
4. сравнивается с identity remote без учёта регистра.

Поэтому `owner/example.github.io` и `owner/tool.git.adapter` допустимы, а `owner/widget.git` запрещён. Полные GitHub naming rules здесь не проверяются.

Remote name фиксирован как `origin` и не параметризуется. URL, default branch, release branch, account и token в Product Unit configuration не хранятся.

## Общая dispatch-модель

`bp_check.py` один раз разбирает SoT configuration, выполняет общие файловые проверки и запускает ровно один handler текущего режима. Общие проверки не вызывают Git.

Checker никогда не выполняет network, `fetch`, `pull`, `push`, `gh`, GitHub API, Settings или PR operations. Он не реконструирует историю и ничего не исправляет автоматически.

## `sot_files`

Источником текущего состояния являются файлы Product Unit. Handler:

1. не читает и не классифицирует `.git`;
2. не требует Git executable;
3. не вызывает Git CLI;
4. не проверяет remote или GitHub.

## `sot_git`

Локальный repository является частью текущего состояния. Handler проверяет:

1. точный Product Unit root;
2. валидные `HEAD` и рабочую ветку;
3. clean working tree;
4. отсутствие remote.

Git-история, reflog и смысловая классификация коммитов не реконструируются. Режим не разрешает remote, push, PR, tag, выпуск или GitHub write.

## `sot_github`

Внешний accepted baseline принадлежит ожидаемому GitHub repository; локальный Git остаётся рабочей копией. После внешнего preflight handler проверяет только локальное состояние:

1. valid repository, exact root, `HEAD`, рабочую ветку и clean tree;
2. ровно один remote с именем `origin`;
3. fetch и push URL в поддерживаемой GitHub-образной форме;
4. совпадение извлечённого `owner/repository` с `SOT_GITHUB_REPOSITORY`;
5. upstream текущей ветки под `origin` и существующий local remote ref;
6. symbolic `refs/remotes/origin/HEAD`, указывающий на существующий `refs/remotes/origin/<branch>`;
7. отсутствие behind/diverged state; равное состояние и локальный ahead-only work допустимы.

Поддерживаются HTTPS `github.com`, стандартная SSH scp-form, SSH alias scp-form и `ssh://git@<host>/owner/repository.git`. Для alias checker подтверждает только синтаксис и repository path: `~/.ssh/config`, реальный host, authentication и permissions проверяет внешний preflight.

Local path, `file://`, embedded HTTP credentials, неполный repository path, второй remote, имя remote не `origin` и identity mismatch дают `FAIL` без repair.

Default branch name не является полем режима. Его обязательный локальный snapshot — `refs/remotes/origin/HEAD`. Release/hotfix branches, tag и GitHub Release являются repository policy и отдельными owner-gated маршрутами, а не core mode invariant.

## Внешний preflight `sot_github`

До transition checkpoint внешний read-only/preparation step:

1. квалифицирует operating identity, authentication и ожидаемый `owner/repository` без раскрытия secrets;
2. получает default branch из GitHub repository metadata;
3. добавляет или квалифицирует единственный `origin` только в owner-approved transition route;
4. выполняет отдельно разрешённый fetch;
5. устанавливает или обновляет local `origin/HEAD` по полученной metadata;
6. фиксирует exact refs и передаёт подготовленное состояние локальному checker.

`bp_check.py` не выполняет ни один из этих внешних шагов и не утверждает freshness metadata.

## Bootstrap отсутствующего repository

Если `sot_git` уже объявлен, а `.git/` отсутствует, агент до интервью может создать неизменённый локальный baseline:

1. подтвердить exact root и отсутствие `.git/` без запуска Product Unit tools;
2. подтвердить отсутствие продуктовых изменений;
3. выполнить локальный `git init` с начальной веткой, принятой текущим route;
4. задать только локальную техническую identity;
5. создать baseline commit неизменённых файлов;
6. проверить `HEAD`, clean tree и remote absent.

Любая ошибка останавливает работу до интервью. Bootstrap не создаёт `local_git_route` и не разрешает продуктовые изменения.

## Переход `sot_files -> sot_git`

Переход выполняется только после отдельного решения владельца. Для новой задачи принятого продукта после полного `PRODUCT_INPUT` агент один раз предлагает варианты продолжить текущий режим, перейти в `sot_git`, отложить задачу или указать другой вариант.

Выбор перехода означает разрешение `sot_transition` и один `local_git_route` для текущего BACK, но не разрешает implementation. Единый transition checkpoint изменяет `AGENTS.md::SOT_MODE` и сохраняет связанные IE/OD, BACK/PLAN и transition evidence.

## Переход `sot_git -> sot_github`

Переход выполняется только из устойчивого `sot_git` и отдельного owner-approved route:

1. зафиксировать PASS локального `sot_git` без remote;
2. выполнить внешний preflight, добавить канонический `origin`, получить refs и подготовить `origin/HEAD`;
3. квалифицировать repository identity, текущую ветку и upstream;
4. единым transition checkpoint изменить `AGENTS.md::SOT_MODE` и добавить `AGENTS.md::SOT_GITHUB_REPOSITORY`;
5. выполнить локальный `bp_check.py` без сети.

Checker не создаёт remote, не делает fetch и не меняет `origin/HEAD`.

## Составной и обратные переходы

Атомарного `sot_files -> sot_github` нет. Пользовательский маршрут состоит из двух отдельных checkpoints:

```text
sot_files -> sot_git -> sot_github
```

Переходы `sot_github -> sot_git` и `sot_github -> sot_files` в `0.5.0` не реализованы и требуют отдельного решения владельца. Если обратный переход будет разрешён в будущем, поле repository удаляется в его checkpoint.

## Роли и merge contract

Core различает автора изменения, утверждающего, исполнителя слияния и публикатора выпуска. Один account может совмещать роли; BytePress не управляет users, permissions или rulesets и не проверяет login.

Раздельные accounts рекомендованы, но не обязательны. При одном account независимое GitHub approval может отсутствовать, а решение владельца по exact head фиксируется в plan/evidence текущего route.

Approval относится к exact current head SHA. Новый push требует новой approval. После действующей approval merge может выполнить любой permitted executor; merger не обязан совпадать с approver. Method определяется branch policy. Tag и GitHub Release остаются отдельными owner-gated действиями. Bypass actors не рекомендуются и не являются частью core.

## Защищённые поля

Точные исключения `AGENTS.md::SOT_MODE` и `AGENTS.md::SOT_GITHUB_REPOSITORY` не являются постоянным разрешением `product-work`. Они допустимы только вместе с owner-approved transition либо отдельной owner-approved migration procedure и с разрешением active PLAN.

## Маршрутное разрешение

Для одного BACK используется не более одной записи `DECISION_KIND: local_git_route`. Только статус `active` разрешает локальную работу; `suspended`, `closed` и `revoked` не разрешают новые изменения. `ALLOWED_SURFACES` active PLAN остаётся более узкой границей.

## Failure и clean-exit

Invalid configuration, repository, remote, URL, identity, branch, upstream, remote ref, `origin/HEAD`, dirty, behind или diverged state останавливает работу. Automatic init, remote repair, fetch, merge, rebase, reset и history attachment запрещены.

При дефекте Harness в `product-work` агент выводит `HARNESS_BLOCKER: <краткое описание>` и прекращает изменения.

Clean-exit фиксирует режим, repository identity для `sot_github`, результаты текущего handler, отсутствие hidden network/repair, состояние разрешения и чистоту root. Technical PASS не является продуктовой приёмкой или GitHub write authority.
