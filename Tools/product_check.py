#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import argparse
import re
import subprocess
import sys

ROOT_MARKERS = ["README.md", "AGENTS.md", "Setup_Guide.md"]
BASE_PATHS = [
    "Docs/Discovery/README.md",
    "Docs/Discovery/Interview.md",
    "Docs/User/README.md",
    "Docs/User/Operating_Mode.md",
    "Docs/User/First_Start.md",
    "Docs/User/Pass_Request.md",
    "Docs/User/Usage_Scenarios.md",
    "Docs/Product/README.md",
    "Docs/Product/Product_Passport.md",
    "Docs/Product/JTBD.md",
    "Docs/Product/PRD.md",
    "Docs/Product/Delivery.md",
    "Docs/Technical/README.md",
    "Docs/Technical/Architecture.md",
    "Docs/Technical/Interfaces.md",
    "Docs/Technical/System_Invariants.md",
    "Docs/Terms/README.md",
    "Docs/Terms/Base_Terms.md",
    "Plans/README.md",
    "Plans/Roadmap.md",
    "Plans/Backlog.md",
    "Logs/README.md",
    "Logs/ChangeLog.md",
    "Logs/ADRlog.md",
    "Logs/QualityLog.md",
    "Logs/ReleaseLog.md",
    "Logs/SupportLog.md",
    "Pipeline/README.md",
    "Pipeline/Phases.md",
    "Pipeline/Workflows.md",
    "Pipeline/Gates.md",
    "Tools/README.md",
    "Tools/product_check.py",
    "Tools/product_bootstrap_smoke.py",
    "Templates/README.md",
    "Templates/Interview.md",
    "Templates/Roadmap.md",
    "Templates/Backlog.md",
    "Templates/Plan.md",
    "Templates/ChangeLog.md",
    "Templates/ADRlog.md",
    "Templates/QualityLog.md",
    "Schemas/README.md",
    "Schemas/roadmap_item.schema.json",
    "Schemas/backlog_item.schema.json",
    "Schemas/plan.schema.json",
    "Schemas/changelog_entry.schema.json",
    "Schemas/adr_entry.schema.json",
]
FORBIDDEN_DIRS = ["Adapters", "Memory", "MCP", "Runtime", "Roles", "Skills", "Standards"]
PIPELINE_GH_ROUTE = re.compile(r"gh pr create|PR.+через `gh`|через gh", re.IGNORECASE)
PIPELINE_CHECK_LEVELS = re.compile(r"Структура|Тесты|GUI-запуск|Ручная проверка", re.IGNORECASE)
PIPELINE_ENGLISH_NAMES = re.compile(r"Discovery confirmation|First product-start|Current truth gate|Execution|Subject pass|Implementation gate")
PIPELINE_RUSSIAN_NAMES = [
    "Подтверждение текущей истины",
    "Первый старт продукта",
    "Гейт текущей истины",
    "Реализация",
    "Предметный проход",
    "Гейт реализации",
]
AGENTS_PIPELINE_ROUTE = re.compile(r"Pipeline/Workflows\.md|Pipeline/\*", re.IGNORECASE)
AGENTS_START_REPORT = [re.compile(pattern, re.IGNORECASE) for pattern in [r"Фаза:", r"Рабочий поток:", r"Гейт:"]]
INTERVIEW_NO_GUESSES = re.compile(r"не равен.*подтвержден|не считается.*подтвержден|догадк|гипотез", re.IGNORECASE)
INTERVIEW_DEPENDENCIES = re.compile(r"стек|зависимост|GUI|tkinter", re.IGNORECASE)
INTERVIEW_UNCONFIRMED_EXPANSION = re.compile(
    r"таймер|timer|сч[её]тчик|counter|рекорд|record|настройк|settings|сохранени|save|установщик|installer",
    re.IGNORECASE,
)
PLAN_FILE = re.compile(r"^[A-Z]{2,3}-000001-product-initialization\.md$")
TASK_BRANCH_NAME = re.compile(r"^(chore|feature|fix|docs)/[0-9]{6}-[a-z0-9]+(?:-[a-z0-9]+)*$")
FIRST_ANALYTIC_BRANCH = re.compile(r"^chore/[0-9]{6}-[a-z0-9]+(?:-[a-z0-9]+)*$")
UNCONFIRMED = re.compile(r"^Статус_текущей_истины:\s+Не_подтверждена$", re.MULTILINE)
CONFIRMED = re.compile(r"^Статус_текущей_истины:\s+Подтверждена$", re.MULTILINE)
PLACEHOLDER = re.compile(r"^Ответ:\s+Не подтверждено пользователем\.$", re.MULTILINE)
STATUS = re.compile(r"^Статус:\s+(\S+)$", re.MULTILINE)
PLAN_ID = re.compile(r"^ID:\s+PLAN-([0-9]{6})$", re.MULTILINE)
SCHEMA_ID = re.compile(r'^\s*"\$id":\s*"SCH-[0-9]{6}"', re.MULTILINE)
TEMPLATE_ID = re.compile(r"^<!-- ID:\s+(TPL-[0-9]{6}) -->$", re.MULTILINE)


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def contains(path: Path, pattern: re.Pattern[str]) -> bool:
    return bool(pattern.search(text(path)))


def initial_plan(root: Path) -> Path | None:
    matches = [path for path in (root / "Plans").glob("*.md") if PLAN_FILE.match(path.name)]
    return matches[0] if matches else None


def status_of(path: Path) -> str | None:
    match = STATUS.search(text(path))
    return match.group(1) if match else None


def is_executable(path: Path) -> bool:
    return path.exists() and bool(path.stat().st_mode & 0o111)


def section_status(path: Path, artifact_id: str) -> str | None:
    lines = text(path).splitlines()
    for index, line in enumerate(lines):
        if line == f"ID: {artifact_id}":
            for candidate in lines[index + 1:index + 12]:
                if candidate.startswith("Статус: "):
                    return candidate.removeprefix("Статус: ")
    return None


def has_later_plan(root: Path) -> bool:
    for path in sorted((root / "Plans").glob("*.md")):
        if path.name in {"README.md", "Roadmap.md", "Backlog.md"}:
            continue
        plan_text = text(path)
        match = PLAN_ID.search(plan_text)
        if not match:
            continue
        if int(match.group(1)) > 1 and status_of(path) in {"В_работе", "Завершено"}:
            return True
    return False


def detect_mode(root: Path) -> str:
    interview = root / "Docs" / "Discovery" / "Interview.md"
    if contains(interview, UNCONFIRMED):
        return "fresh"
    if contains(interview, CONFIRMED):
        return "developed"
    return "unknown"


def git_branch(root: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None
    branch = result.stdout.strip()
    return branch or None


def check(root: Path, mode: str) -> list[str]:
    errors: list[str] = []
    for item in ROOT_MARKERS + BASE_PATHS:
        if not (root / item).exists():
            errors.append(f"missing {item}")
    for item in FORBIDDEN_DIRS:
        if (root / item).exists():
            errors.append(f"forbidden placeholder domain present: {item}")
    for path in sorted((root / "Schemas").glob("*.json")):
        if not contains(path, SCHEMA_ID):
            errors.append(f"{path.relative_to(root)}: missing schema ID")
    template_ids: dict[str, Path] = {}
    for path in sorted((root / "Templates").glob("*.md")):
        if path.name == "README.md":
            continue
        match = TEMPLATE_ID.search(text(path))
        if not match:
            errors.append(f"{path.relative_to(root)}: missing template ID")
            continue
        template_id = match.group(1)
        if template_id in template_ids:
            errors.append(f"{path.relative_to(root)}: duplicate template ID {template_id}")
        else:
            template_ids[template_id] = path
    if "Tools/.reports/" not in text(root / ".gitignore"):
        errors.append(".gitignore: missing Tools/.reports/ ignore")
    agents_text = text(root / "AGENTS.md")
    if not AGENTS_PIPELINE_ROUTE.search(agents_text):
        errors.append("AGENTS.md: missing Pipeline route")
    for pattern in AGENTS_START_REPORT:
        if not pattern.search(agents_text):
            errors.append("AGENTS.md: в стартовом отчёте нет фазы, рабочего потока или гейта")
    workflows = root / "Pipeline" / "Workflows.md"
    if not PIPELINE_GH_ROUTE.search(text(workflows)):
        errors.append("Pipeline/Workflows.md: missing PR route through gh")
    if not PIPELINE_CHECK_LEVELS.search(text(workflows)):
        errors.append("Pipeline/Workflows.md: missing check levels")
    pipeline_text = text(root / "Pipeline" / "Workflows.md") + "\n" + text(root / "Pipeline" / "Phases.md") + "\n" + text(root / "Pipeline" / "Gates.md")
    if PIPELINE_ENGLISH_NAMES.search(pipeline_text):
        errors.append("Pipeline/*: phase, workflow and gate names must use Russian canonical names")
    for marker in PIPELINE_RUSSIAN_NAMES:
        if marker not in pipeline_text:
            errors.append(f"Pipeline/*: missing Russian marker `{marker}`")

    plan = initial_plan(root)
    if plan is None:
        errors.append("missing Plans/<PRODUCT_CODE>-000001-product-initialization.md")
    actual_mode = detect_mode(root) if mode == "auto" else mode
    if actual_mode == "unknown":
        errors.append("Docs/Discovery/Interview.md: cannot detect current-truth lifecycle state")
    interview = root / "Docs" / "Discovery" / "Interview.md"
    if not INTERVIEW_NO_GUESSES.search(text(interview)):
        errors.append("Docs/Discovery/Interview.md: missing ban on guessed current-truth confirmation")
    if not INTERVIEW_DEPENDENCIES.search(text(interview)):
        errors.append("Docs/Discovery/Interview.md: missing stack/dependency source discipline")
    if INTERVIEW_UNCONFIRMED_EXPANSION.search(text(interview)):
        errors.append("Docs/Discovery/Interview.md: must not suggest unconfirmed first-version expansion examples")
    for rel in ["Tools/product_check.py", "Tools/product_bootstrap_smoke.py"]:
        if not is_executable(root / rel):
            errors.append(f"{rel}: служебный файл не исполняемый")
    for path in sorted((root / "scripts").glob("*.sh")):
        if not is_executable(path):
            errors.append(f"{path.relative_to(root)}: переходный скрипт не исполняемый")
    if actual_mode == "fresh":
        if not contains(interview, UNCONFIRMED):
            errors.append("Docs/Discovery/Interview.md: missing unconfirmed current truth")
        if not contains(interview, PLACEHOLDER):
            errors.append("Docs/Discovery/Interview.md: missing placeholder answers")
        if section_status(root / "Plans" / "Roadmap.md", "ROAD-000001") != "В_работе":
            errors.append("Plans/Roadmap.md: ROAD-000001 must be В_работе in fresh state")
        if section_status(root / "Plans" / "Backlog.md", "BACK-000001") != "В_работе":
            errors.append("Plans/Backlog.md: BACK-000001 must be В_работе in fresh state")
        if plan and status_of(plan) != "В_работе":
            errors.append(f"{plan.relative_to(root)}: PLAN-000001 must be В_работе in fresh state")
        current_branch = git_branch(root)
        if current_branch and (current_branch in {"develop", "main"} or not FIRST_ANALYTIC_BRANCH.fullmatch(current_branch)):
            errors.append("git branch: first analytical product-start must use a chore/ working branch")
    elif actual_mode == "developed":
        if contains(interview, UNCONFIRMED) or contains(interview, PLACEHOLDER):
            errors.append("Docs/Discovery/Interview.md: developed state keeps fresh placeholders")
        if section_status(root / "Plans" / "Roadmap.md", "ROAD-000001") != "Завершено":
            errors.append("Plans/Roadmap.md: ROAD-000001 must be Завершено in developed state")
        if section_status(root / "Plans" / "Backlog.md", "BACK-000001") != "Завершено":
            errors.append("Plans/Backlog.md: BACK-000001 must be Завершено in developed state")
        if plan and status_of(plan) != "Завершено":
            errors.append(f"{plan.relative_to(root)}: PLAN-000001 must be Завершено in developed state")
        if not has_later_plan(root):
            errors.append("Plans/*: developed state needs a later active or completed plan")
        if "PLAN-000001" not in text(root / "Logs" / "ChangeLog.md"):
            errors.append("Logs/ChangeLog.md: missing PLAN-000001 closure link")
        if "PLAN-000001" not in text(root / "Logs" / "QualityLog.md"):
            errors.append("Logs/QualityLog.md: missing PLAN-000001 check link")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Проверка локального продуктового каркаса.")
    parser.add_argument("--repo", default=".")
    parser.add_argument("--mode", choices=["auto", "fresh", "developed"], default="auto")
    args = parser.parse_args()
    root = Path(args.repo).resolve()
    errors = check(root, args.mode)
    if errors:
        print("Ошибки продуктового каркаса:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Локальный продуктовый каркас выглядит полным. Режим: {detect_mode(root) if args.mode == 'auto' else args.mode}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
