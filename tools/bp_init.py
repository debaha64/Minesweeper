#!/usr/bin/env python3
import argparse
import os
import re
import stat
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True

from bp_check import parse_sot_config, valid_repository_identity

CHECK_COMMANDS = [
    "python3 -m py_compile tools/bp_init.py tools/bp_check.py tools/bp_clean.py",
    "python3 -m unittest discover -s tests -p 'test_*.py'",
    "python3 tools/bp_check.py --repo .",
]
OWNER_DOCS = [
    "AGENTS.md", "SYSTEM.md", "README.md", "docs/README.md", "docs/product/dods.md",
    "docs/product/jtbd.md", "docs/product/prd.md", "plans/roadmap.md", "plans/backlog.md",
    "plans/active/README.md", "logs/sessions.md", "logs/decisions.md", "logs/risks.md",
    "logs/quality.md", "sops/interview.md", "sops/project-management.md", "sops/sot.md",
    "tools/README.md",
]
FORBIDDEN_ACTIONS = [
    "не писать код продукта до обязательного интервью и решения владельца о реализации",
    "не создавать synthetic owner decision или фиктивное свидетельство интервью",
    "не выполнять выпуск, tag или GitHub write-действия без отдельного решения владельца",
    "не считать технические проверки продуктовой приёмкой",
]
LOCAL_SERVICE_DIR_NAMES = {".agents", ".codex"}
GIT_COMMAND_TIMEOUT_SECONDS = 30

LOG_PURPOSES = {
    "changes.md": "Фиксирует факты изменения артефактов после реальной работы в этой Product Unit.",
    "decisions.md": "Фиксирует типизированные owner_decision и отдельные product_acceptance после явного ответа владельца.",
    "quality.md": "Фиксирует команды проверки, результаты и непроверенные области.",
    "releases.md": "Фиксирует факты выпуска только после отдельного owner-approved release route.",
    "risks.md": "Фиксирует риски, блокеры и выбранные меры контроля.",
    "sessions.md": "Фиксирует реальные сессии, включая interview_evidence после ответа владельца.",
    "terminology.md": "Фиксирует изменения терминов и статусов терминов.",
}
LOG_README = """# Журналы

`logs/` хранит операционные факты этой Product Unit.

## Индекс

1. `changes.md` — изменения артефактов.
2. `decisions.md` — решения владельца.
3. `quality.md` — проверки и результаты.
4. `releases.md` — факты выпуска после отдельного решения.
5. `risks.md` — риски и блокеры.
6. `sessions.md` — сессии и свидетельства интервью.
7. `terminology.md` — изменения терминов.

Первая реальная работа создаёт первую операционную запись. Стартовая поставка не содержит синтетических решений владельца или фиктивных свидетельств интервью.
"""
RESEARCH_README_TEXT = """# Исследования

`research/` хранит формальные research-домены Product Unit.

Правила находятся в `sops/research.md`. Формы находятся в `templates/`.
"""
RESEARCH_ARCHIVES_README_TEXT = """# Архивы исследований

`research/archives/` хранит архивы завершённых research-доменов.

Архивы не перезаписываются.
"""
SOPS_RESEARCH_TEXT = """# Исследования

Research-домены Product Unit ведутся в формате `research/<xxx>-<slug>/`.

Минимальная структура домена:

```text
research/<xxx>-<slug>/000-index.md
research/<xxx>-<slug>/001-<slug>.md
research/<xxx>-<slug>/results.md
```

Research не заменяет active PLAN, решение владельца, продуктовую приёмку или release.
"""


def read(path):
    return path.read_text(encoding="utf-8")


def split_table_row(line):
    return [cell.strip().strip("`") for cell in line.strip().strip("|").split("|")]


def table_rows(path):
    rows = []
    if not path.exists():
        return rows
    for line in read(path).splitlines():
        if line.strip().startswith("|") and "---" not in line:
            cells = split_table_row(line)
            if cells and cells[0] != "ID":
                rows.append(cells)
    return rows


def first_by_status(rows, status, status_index):
    for cells in rows:
        if len(cells) > status_index and cells[status_index] == status:
            return cells
    return None


def scan_tree_symlinks(repo):
    """Preflight без следования symlink и без классификации exact `.git`."""
    found = []
    pending = [Path(repo)]
    while pending:
        base = pending.pop()
        with os.scandir(base) as iterator:
            entries = sorted(iterator, key=lambda entry: entry.name)
        directories = []
        for entry in entries:
            name = entry.name
            if name == ".git" or name in LOCAL_SERVICE_DIR_NAMES:
                continue
            if entry.is_symlink():
                found.append(base / name)
            elif entry.is_dir(follow_symlinks=False):
                directories.append(name)
            else:
                entry.is_file(follow_symlinks=False)
        pending.extend(base / name for name in reversed(directories))
    return found


def active_plan_paths(repo):
    directory = repo / "plans" / "active"
    current = Path(repo)
    for part in ("plans", "active"):
        current = current / part
        try:
            mode = os.lstat(current).st_mode
        except OSError:
            return []
        if stat.S_ISLNK(mode) or not stat.S_ISDIR(mode):
            return []
    with os.scandir(directory) as iterator:
        entries = sorted(iterator, key=lambda entry: entry.name)
    plans = []
    for entry in entries:
        name = entry.name
        if name == ".git" or name in LOCAL_SERVICE_DIR_NAMES:
            continue
        if entry.is_symlink():
            continue
        if entry.is_file(follow_symlinks=False) and name.startswith("PLAN-") and name.endswith(".md"):
            plans.append(directory / name)
    return plans


def active_plan(repo):
    plans = active_plan_paths(repo)
    return plans[0].relative_to(repo) if len(plans) == 1 else None


def active_plan_text(repo):
    plan = active_plan(repo)
    return read(repo / plan) if plan else ""


def active_phase(repo):
    text = active_plan_text(repo)
    if not text:
        return "idle"
    matches = re.findall(r"^Фаза SDLC:\s*(.+)$", text, flags=re.MULTILINE)
    if len(matches) != 1:
        return "invalid"
    value = matches[0].strip().strip("`").lower()
    aliases = {
        "замысел": "intent",
        "интервью": "interview",
        "требования": "requirements",
        "планирование": "planning",
        "утверждение": "approval",
        "реализация": "implementation",
        "проверка": "verification",
        "обзор владельцем": "owner-review",
        "продуктовая приёмка": "product-acceptance",
        "готовность к выпуску": "release-readiness",
        "выпуск": "release",
        "исследование": "discovery",
        "product discovery": "discovery",
    }
    supported = {
        "intent", "interview", "requirements", "planning", "approval",
        "implementation", "verification", "owner-review", "product-acceptance",
        "release-readiness", "release", "discovery",
    }
    return aliases.get(value, value if value in supported else "invalid")


def field_from_active_plan(repo, label):
    text = active_plan_text(repo)
    match = re.search(rf"^{re.escape(label)}:\s*(.+)$", text, flags=re.MULTILINE)
    return match.group(1).strip() if match else "не указано"


def active_operational_mode(repo):
    if not active_plan(repo):
        return "idle"
    text = active_plan_text(repo)
    matches = re.findall(r"^Операционный режим:\s*(.+)$", text, flags=re.MULTILINE)
    if len(matches) != 1:
        return "invalid"
    value = matches[0].strip().strip("`").lower()
    return value if value in {"product-work", "system-editing"} else "invalid"


def linked_id_from_active_plan(repo, label):
    text = active_plan_text(repo)
    match = re.search(rf"^- {re.escape(label)}:\s*(.+)$", text, flags=re.MULTILINE)
    return match.group(1).strip() if match else "не найдено"


def active_road_row(repo):
    return first_by_status(table_rows(repo / "plans" / "roadmap.md"), "active", 1)


def active_back_row(repo):
    return first_by_status(table_rows(repo / "plans" / "backlog.md"), "active", 2)


def next_action(repo):
    if active_plan(repo):
        return "следовать active PLAN без вывода новых разрешений из текста backlog"
    return "Состояние Product Unit: idle; открыть PLAN только после решения владельца"


def first_heading(path):
    if not path.is_file():
        return None
    match = re.search(r"^#\s+(.+)$", read(path), flags=re.MULTILINE)
    return match.group(1).strip() if match else None


def explicit_project_name(path):
    if not path.is_file():
        return None
    match = re.search(r"^Проект:\s*(.+)$", read(path), flags=re.MULTILINE)
    return match.group(1).strip() if match else None


def project_name(repo):
    brief = repo / "docs" / "product" / "product-brief.md"
    for candidate in [explicit_project_name(brief), first_heading(repo / "README.md"), first_heading(brief)]:
        if candidate and candidate != "Описание продукта":
            return candidate
    return repo.name


def allowed_surfaces(repo):
    if not active_plan(repo):
        return []
    values = re.findall(r"^ALLOWED_SURFACES:\s*(.+)$", active_plan_text(repo), flags=re.MULTILINE)
    if len(values) != 1:
        return []
    return [item.strip().strip("`") for item in values[0].split(",") if item.strip()]


def surface_allows(repo, relative_path):
    protected = (
        relative_path in {"AGENTS.md", "SYSTEM.md"}
        or relative_path.startswith(("sops/", "templates/", "tools/"))
    )
    if protected and active_operational_mode(repo) != "system-editing":
        return False
    for value in allowed_surfaces(repo):
        if "::" in value:
            continue
        if value.endswith("/**") and (relative_path == value[:-3] or relative_path.startswith(value[:-2])):
            return True
        if value.endswith("/") and relative_path.startswith(value):
            return True
        if value == relative_path:
            return True
    return False


def ensure_research_scaffold(repo):
    restored = []
    blocked = []
    directories = [repo / "research", repo / "research" / "archives"]
    for directory in directories:
        if not directory.is_dir():
            rel = str(directory.relative_to(repo))
            if surface_allows(repo, rel) or surface_allows(repo, rel + "/README.md"):
                directory.mkdir(parents=True, exist_ok=True)
                restored.append(rel + "/")
            else:
                blocked.append(rel + "/")
    files = [
        (repo / "research" / "README.md", RESEARCH_README_TEXT),
        (repo / "research" / "archives" / "README.md", RESEARCH_ARCHIVES_README_TEXT),
        (repo / "sops" / "research.md", SOPS_RESEARCH_TEXT),
    ]
    for path, text in files:
        if not path.is_file() or not read(path).strip():
            rel = str(path.relative_to(repo))
            if surface_allows(repo, rel):
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text, encoding="utf-8")
                restored.append(rel)
            else:
                blocked.append(rel)
    return restored, blocked


def ensure_log_scaffold(repo):
    restored = []
    blocked = []
    logs = repo / "logs"
    if not logs.is_dir() and surface_allows(repo, "logs/**"):
        logs.mkdir(parents=True, exist_ok=True)
        restored.append("logs/")
    if not logs.is_dir():
        return restored, ["logs/"]
    readme = logs / "README.md"
    if not readme.is_file() or not read(readme).strip():
        if surface_allows(repo, "logs/README.md"):
            readme.write_text(LOG_README, encoding="utf-8")
            restored.append("logs/README.md")
        else:
            blocked.append("logs/README.md")
    for filename, purpose in LOG_PURPOSES.items():
        path = logs / filename
        if not path.is_file() or not read(path).strip():
            title = {
                "changes.md": "Изменения",
                "decisions.md": "Решения",
                "quality.md": "Качество",
                "releases.md": "Выпуски",
                "risks.md": "Риски",
                "sessions.md": "Сессии",
                "terminology.md": "Терминология",
            }[filename]
            rel = f"logs/{filename}"
            if surface_allows(repo, rel):
                path.write_text(f"# {title}\n\n{purpose}\n", encoding="utf-8")
                restored.append(rel)
            else:
                blocked.append(rel)
    return restored, blocked


def run_git(repo, *args):
    try:
        completed = subprocess.run(
            ["git", "-C", str(repo), *args],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=GIT_COMMAND_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        return 124, "", f"git timeout after {GIT_COMMAND_TIMEOUT_SECONDS}s"
    except OSError as error:
        return 127, "", str(error)
    return completed.returncode, completed.stdout.strip(), completed.stderr.strip()


def bootstrap_candidate_state(repo):
    """Проверяет pre-bootstrap starter только чтением файлов."""
    plan = active_plan(repo)
    if (
        plan is None
        or re.match(r"^PLAN-000001(?:-[a-z0-9]+)*\.md$", plan.name) is None
        or active_phase(repo) not in {"discovery", "intent", "interview", "requirements", "planning", "approval"}
        or active_operational_mode(repo) != "product-work"
        or field_from_active_plan(repo, "INTERVIEW_EVIDENCE_REF") != "none"
        or field_from_active_plan(repo, "OWNER_DECISION_REFS") != "none"
        or field_from_active_plan(repo, "PRODUCT_ACCEPTANCE_REF") != "none"
        or list((repo / "plans" / "completed").glob("PLAN-*.md"))
    ):
        return False
    for directory in (repo / "src", repo / "tests"):
        for path in directory.rglob("*") if directory.is_dir() else []:
            if path.is_file() and path.name not in {"README.md", "test_sot_modes.py"}:
                return False
    for filename in ("changes.md", "quality.md", "risks.md", "sessions.md", "decisions.md"):
        path = repo / "logs" / filename
        if path.is_file() and re.search(r"^(?:RECORD_TYPE|RECORD_ID):\s*\S+", read(path), flags=re.MULTILINE):
            return False
    product_brief = repo / "docs" / "product" / "product-brief.md"
    if product_brief.is_file():
        section = re.search(r"^## Продукт\s*$\n(.*?)(?=^##\s|\Z)", read(product_brief), flags=re.MULTILINE | re.DOTALL)
        values = [line.strip() for line in section.group(1).splitlines() if line.strip()] if section else []
        if values and values[0].lower() not in {"не задан.", "не задан", "none"}:
            return False
    return True


def git_state(repo, mode):
    if mode == "sot_files":
        return "ignored-by-sot_files"
    if mode != "sot_git":
        return "not-checked"
    if not os.path.lexists(repo.joinpath("." + "git")):
        return "bootstrap-required" if bootstrap_candidate_state(repo) else "bootstrap-product-unit-changed"
    code, top, _error = run_git(repo, "rev-parse", "--show-toplevel")
    if code or not top:
        return "invalid-repository"
    try:
        if Path(top).resolve() != repo.resolve():
            return "wrong-repository-root"
    except OSError:
        return "invalid-repository-root"
    code, _head, _error = run_git(repo, "rev-parse", "--verify", "HEAD^{commit}")
    if code:
        return "missing-baseline-commit"
    code, remotes, _error = run_git(repo, "remote")
    if code:
        return "remote-check-failed"
    if remotes:
        return "remote-present"
    code, status, _error = run_git(repo, "status", "--porcelain=v1", "--untracked-files=all")
    if code:
        return "status-check-failed"
    return "valid-clean" if not status else "valid-dirty"


def sot_message(repo, mode, repository):
    if mode == "sot_files":
        return "SoT: SOT_MODE=sot_files; Git и служебный путь полностью игнорируются; см. sops/sot.md"
    if mode == "sot_git":
        state = git_state(repo, mode)
        if state == "bootstrap-required":
            return "SoT: SOT_MODE=sot_git; repository absent; после первого запроса агент выполняет baseline bootstrap до интервью; см. sops/sot.md"
        if state == "valid-clean":
            return "SoT: SOT_MODE=sot_git; базовый коммит есть, remote отсутствует, дерево чисто; см. sops/sot.md"
        if state == "valid-dirty":
            return "SoT: SOT_MODE=sot_git; дерево содержит изменения; bp_check.py остановит работу; см. sops/sot.md"
        return f"SoT: SOT_MODE=sot_git; локальный репозиторий невалиден ({state}); см. sops/sot.md"
    if mode == "sot_github":
        return (
            f"SoT: SOT_MODE=sot_github; repository={repository}; "
            "bp_check.py проверяет только подготовленное локальное состояние; см. sops/sot.md"
        )
    return f"SoT: SOT_MODE некорректен ({mode}); см. sops/sot.md"


def print_back(label, row):
    if row:
        print(f"{label}: {row[0]} - {row[3] if len(row) > 3 else ''} ({row[2] if len(row) > 2 else ''})")
    else:
        print(f"{label}: не найдено")


def print_road(label, row):
    if row:
        print(f"{label}: {row[0]} - {row[2]} ({row[1]})")
    else:
        print(f"{label}: не найдено")


def print_init(repo):
    try:
        symlinks = scan_tree_symlinks(repo)
    except OSError as error:
        print(f"FAIL bootstrap-boundary: невозможно безопасно прочитать Product Unit: {error}")
        return 1
    if symlinks:
        print("FAIL bootstrap-boundary: symlink запрещены и не читаются:")
        for path in symlinks:
            print(f"- {path.relative_to(repo)}")
        return 1
    restored = []
    blocked = []
    sot_config = parse_sot_config(repo)
    mode = sot_config["mode"] or (
        "missing" if not sot_config["mode_values"] else "duplicate-or-unsupported"
    )
    repository = sot_config["repository"]
    sot_config_valid = (
        len(sot_config["mode_values"]) == 1
        and mode in {"sot_files", "sot_git", "sot_github"}
        and (
            (mode == "sot_github" and len(sot_config["repository_values"]) == 1 and valid_repository_identity(repository))
            or (mode != "sot_github" and not sot_config["repository_values"])
        )
    )
    initial_git_state = git_state(repo, mode)
    research_restored, research_blocked = ensure_research_scaffold(repo)
    log_restored, log_blocked = ensure_log_scaffold(repo)
    restored.extend(research_restored)
    restored.extend(log_restored)
    blocked.extend(research_blocked)
    blocked.extend(log_blocked)
    roadmap_rows = table_rows(repo / "plans" / "roadmap.md")
    backlog_rows = table_rows(repo / "plans" / "backlog.md")
    plan = active_plan(repo)
    road_row = active_road_row(repo)
    back_row = active_back_row(repo)
    road_id = linked_id_from_active_plan(repo, "ROAD")
    back_id = linked_id_from_active_plan(repo, "BACK")
    plan_text = str(plan) if plan else "не найден"
    plan_count = len(active_plan_paths(repo))
    state = "active" if plan else ("idle" if plan_count == 0 else "invalid")
    print("Диагностика старта Product Unit")
    print(f"Корень: {repo}")
    print(f"Состояние Product Unit: {state}")
    print(f"Проект: {project_name(repo)}")
    print(f"Product Unit: {field_from_active_plan(repo, 'Product Unit') if plan else 'N/A'}")
    print(f"Фаза SDLC: {active_phase(repo)}")
    print(f"Операционный режим: {active_operational_mode(repo)}")
    print(f"Управление проектом: ROAD {road_id} / BACK {back_id} / PLAN {plan_text}")
    print(f"Активный ROAD: {road_row[0] if road_row else 'не найден'}")
    print(f"Активный BACK: {back_row[0] if back_row else 'не найден'}")
    print(f"Активный PLAN: {plan_text}")
    print(f"Роль по старту: {field_from_active_plan(repo, 'Роли') if plan else 'idle'}")
    print(f"Текущая точка контроля: {field_from_active_plan(repo, 'Gate') if plan else 'idle'}")
    print(f"Следующее действие: {next_action(repo)}")
    print(f"INTERVIEW_EVIDENCE_REF: {field_from_active_plan(repo, 'INTERVIEW_EVIDENCE_REF') if plan else 'N/A'}")
    print(f"OWNER_DECISION_REFS: {field_from_active_plan(repo, 'OWNER_DECISION_REFS') if plan else 'N/A'}")
    print(f"ALLOWED_SURFACES: {field_from_active_plan(repo, 'ALLOWED_SURFACES') if plan else 'N/A'}")
    print(f"PRODUCT_ACCEPTANCE_REF: {field_from_active_plan(repo, 'PRODUCT_ACCEPTANCE_REF') if plan else 'N/A'}")
    print(f"SOT_MODE: {mode}")
    if mode == "sot_github":
        print(f"SOT_GITHUB_REPOSITORY: {repository}")
    print(f"Состояние Git: {initial_git_state}")
    print("Scaffold: ready" if not restored else "Scaffold: restored " + ", ".join(restored))
    if blocked:
        print("Scaffold blocker: нет разрешения на восстановление " + ", ".join(blocked))
    print(sot_message(repo, mode, repository))
    print_road("Активный ROAD", first_by_status(roadmap_rows, "active", 1))
    print_back("Активная BACK", first_by_status(backlog_rows, "active", 2))
    print_back("Следующая запланированная BACK", first_by_status(backlog_rows, "planned", 2))
    print()
    phase = active_phase(repo)
    if plan:
        print(f"Product Unit имеет active PLAN в фазе {phase}.")
        if phase in {"discovery", "intent", "interview", "requirements", "planning", "approval"}:
            print("Следующий шаг: завершить обязательные информационные слои; начальный запрос не открывает реализацию.")
        elif phase in {"implementation", "verification"}:
            print("Следующий шаг: работать только после проверки связанных IE-* и OD-* и в ALLOWED_SURFACES.")
        elif phase == "owner-review":
            print("Следующий шаг: ожидать отдельное решение владельца; технический PASS не создаёт PA-*.")
        else:
            print("Следующий шаг: исправить некорректную фазу active PLAN.")
    else:
        print("Состояние Product Unit: idle")
        print("Следующий шаг: открыть локальный PLAN только после решения владельца.")
    print()
    print("Документы для чтения:")
    for rel in OWNER_DOCS:
        print(f"- {rel}")
    print()
    print("Команды проверки:")
    for command in CHECK_COMMANDS:
        print(f"- {command}")
    print()
    print("Запрещённые действия:")
    for action in FORBIDDEN_ACTIONS:
        print(f"- {action}")
    invalid = (
        plan_count > 1
        or phase == "invalid"
        or active_operational_mode(repo) == "invalid"
        or not sot_config_valid
        or (mode == "sot_git" and initial_git_state not in {"bootstrap-required", "valid-clean", "valid-dirty"})
        or bool(blocked)
    )
    return 1 if invalid else 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=".")
    parser.add_argument("--format", default="text", choices=["text"])
    args = parser.parse_args()
    return print_init(Path(args.repo).resolve())


if __name__ == "__main__":
    raise SystemExit(main())
