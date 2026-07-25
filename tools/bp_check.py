#!/usr/bin/env python3
"""Лёгкая проверка текущего состояния Product Unit."""

import argparse
import json
import os
import re
import stat
import subprocess
import sys
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit

sys.dont_write_bytecode = True

PLAN_FILE_RE = re.compile(r"^(PLAN-\d{6})(?:-[a-z0-9]+(?:-[a-z0-9]+)*)?\.md$")
ROAD_ID_RE = re.compile(r"^ROAD-\d{6}$")
BACK_ID_RE = re.compile(r"^BACK-\d{6}$")
PLAN_ID_RE = re.compile(r"^PLAN-\d{6}$")
IE_ID_RE = re.compile(r"^IE-\d{6}$")
OD_ID_RE = re.compile(r"^OD-\d{6}$")
PA_ID_RE = re.compile(r"^PA-\d{6}$")
SOT_FIELD_RE = re.compile(r"^\s*SOT_MODE\s*[:=]\s*`?([^`\s]+)`?\s*\.?\s*$")
SOT_REPOSITORY_FIELD_RE = re.compile(r"^\s*SOT_GITHUB_REPOSITORY\s*:\s*`?(.*?)`?\s*$")
CODEXLOG_RE = re.compile(r"^codexlog:(\.codex/[^#]+)#lines=(\d+)-(\d+)$")

SOT_SUPPORTED = {"sot_files", "sot_git", "sot_github"}
PHASES = {
    "intent", "interview", "requirements", "planning", "approval", "discovery",
    "implementation", "verification", "owner-review", "product-acceptance",
    "release-readiness", "release",
}
PHASE_ALIASES = {
    "замысел": "intent",
    "интервью": "interview",
    "требования": "requirements",
    "планирование": "planning",
    "утверждение": "approval",
    "исследование": "discovery",
    "product discovery": "discovery",
    "реализация": "implementation",
    "проверка": "verification",
    "обзор владельцем": "owner-review",
    "продуктовая приёмка": "product-acceptance",
    "готовность к выпуску": "release-readiness",
    "выпуск": "release",
}
PROTECTED_ROOTS = ("AGENTS.md", "SYSTEM.md", "sops/", "templates/", "tools/")
EXACT_EXCEPTIONS = {"AGENTS.md::SOT_MODE", "AGENTS.md::SOT_GITHUB_REPOSITORY"}
LOCAL_SERVICE_DIRS = {".agents", ".codex"}
DISPOSABLE_DIRS = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
DISPOSABLE_SUFFIXES = {".pyc", ".pyo", ".tmp", ".temp", ".orig"}
GIT_TIMEOUT_SECONDS = 30

REQUIRED_FILES = [
    "AGENTS.md", "README.md", "SYSTEM.md", ".gitignore",
    "docs/README.md", "docs/product/README.md", "docs/product/product-brief.md",
    "docs/product/product-passport.md", "docs/product/jtbd.md", "docs/product/prd.md",
    "docs/product/dods.md", "docs/terminology/README.md", "docs/terminology/glossary.md",
    "docs/architecture/README.md", "docs/architecture/architecture.md",
    "docs/architecture/domain-model.md", "docs/architecture/input-output-contract.md",
    "docs/technical/README.md", "docs/technical/testing.md", "docs/user/README.md",
    "docs/user/github-repository-preparation.md",
    "plans/README.md", "plans/roadmap.md", "plans/backlog.md", "plans/active/README.md",
    "plans/completed/README.md", "logs/README.md", "logs/changes.md", "logs/decisions.md",
    "logs/quality.md", "logs/releases.md", "logs/risks.md", "logs/sessions.md",
    "logs/terminology.md", "research/README.md", "research/archives/README.md",
    "sops/README.md", "sops/clean-exit.md", "sops/project-management.md", "sops/research.md",
    "sops/sdlc.md", "sops/terminology.md", "sops/analytics.md", "sops/architecture.md",
    "sops/sot.md", "sops/managed-agent-pass.md", "sops/system-editing.md",
    "sops/change-management.md", "sops/interview.md", "sops/task-intake.md",
    "sops/verify-work.md", "sops/system-diagnostics.md", "sops/start-session.md",
    "sops/record-change.md", "sops/record-decision.md", "sops/record-quality.md",
    "sops/record-risk.md", "sops/record-terminology.md", "sops/roles/README.md",
    "sops/roles/architect.md", "sops/roles/archive-curator.md", "sops/roles/implementer.md",
    "sops/roles/product-acceptance-assistant.md", "sops/roles/release-assistant.md",
    "sops/roles/researcher.md", "sops/roles/verifier.md", "templates/README.md",
    "templates/agent-state-message.md", "templates/interview.md", "templates/agents.md",
    "templates/system.md", "templates/product-readme.md", "templates/domain-readme.md",
    "templates/docs-product-brief.md", "templates/docs-product-passport.md",
    "templates/docs-product-jtbd.md", "templates/docs-product-prd.md",
    "templates/docs-product-dods.md", "templates/docs-terminology-glossary.md",
    "templates/docs-architecture-architecture.md", "templates/docs-architecture-domain-model.md",
    "templates/docs-technical-architecture.md", "templates/docs-technical-testing.md",
    "templates/docs-user-guide.md", "templates/sop.md", "templates/role.md",
    "templates/plan-roadmap.md", "templates/plan-backlog.md", "templates/plan-active.md",
    "templates/plan-completed-readme.md", "templates/log-file.md",
    "templates/session-record.md", "templates/decision-record.md", "templates/risk-record.md",
    "templates/quality-record.md", "templates/change-record.md", "templates/registry-file.md",
    "templates/registry-item.md", "templates/terminology-record.md",
    "templates/research-domain-index.md", "templates/research-record.md",
    "templates/research-results.md", "templates/owner-decision-package.md",
    "tools/README.md", "tools/bp_init.py", "tools/bp_check.py", "tools/bp_clean.py",
    "src/README.md", "tests/README.md", "tests/test_sot_modes.py",
]

ALLOWED_TOP_LEVEL = {
    ".agents", ".codex", ".git", ".gitignore", "AGENTS.md", "README.md", "SYSTEM.md",
    "docs", "logs", "plans", "research", "sops", "src", "templates", "tests", "tools",
}
ALLOWED_TOOLS = {"README.md", "bp_init.py", "bp_check.py", "bp_clean.py"}
FORBIDDEN_CURRENT_PATHS = {
    "state", "checks", "schemas", "roles", "sops/checklists", "docs/technical/agent-roles",
    "Rules", "Pipeline", "Profiles", "docs/git", "docs/sdlc", "docs/operations",
    "docs/references", "docs/evaluation", "comparison", "_sources", "bp_bootstrap.py",
    "tools/bp_ops.py", "tools/bp_core.py", "tools/bp_new_product.py", "release-record.md",
    "examples", "samples", "demo", "playgrounds", "fixtures",
}
HARNESS_TEST_FILES = {"tests/test_sot_modes.py"}


def read(path):
    return path.read_text(encoding="utf-8")


def result(name, status, message=""):
    item = {"check": name, "status": status}
    if message:
        item["message"] = message
    return item


def text_files(repo):
    for base, directories, filenames in os.walk(repo, followlinks=False):
        base_path = Path(base)
        directories[:] = sorted(
            name for name in directories
            if name not in LOCAL_SERVICE_DIRS and name != ".git"
        )
        for filename in sorted(filenames):
            path = base_path / filename
            if path.suffix in {".md", ".py"} or filename in {"AGENTS.md", "SYSTEM.md", "README.md", ".gitignore"}:
                yield path


def safe_tree(repo):
    issues = []
    pending = [repo]
    while pending:
        base = pending.pop()
        try:
            with os.scandir(base) as iterator:
                entries = sorted(iterator, key=lambda entry: entry.name)
        except OSError as error:
            issues.append(f"{base}: {error}")
            continue
        for entry in entries:
            path = base / entry.name
            rel = path.relative_to(repo).as_posix()
            if entry.name in LOCAL_SERVICE_DIRS or rel == ".git":
                continue
            if entry.is_symlink():
                issues.append(f"symlink запрещён: {rel}")
                continue
            if entry.is_dir(follow_symlinks=False):
                pending.append(path)
            elif not entry.is_file(follow_symlinks=False):
                issues.append(f"неподдерживаемый тип пути: {rel}")
    return [result("path-boundary", "fail", issue) for issue in issues] or [result("path-boundary", "pass")]


def check_required(repo):
    missing = [rel for rel in REQUIRED_FILES if not (repo / rel).is_file()]
    items = [result("required-files", "fail", f"отсутствует {rel}") for rel in missing]
    top = {path.name for path in repo.iterdir()}
    for name in sorted(top - ALLOWED_TOP_LEVEL):
        items.append(result("required-files", "fail", f"неразрешённый корневой путь: {name}"))
    tools = repo / "tools"
    if tools.is_dir():
        for path in sorted(tools.iterdir(), key=lambda item: item.name):
            if path.is_file() and path.name not in ALLOWED_TOOLS:
                items.append(result("required-files", "fail", f"неразрешённый tool: tools/{path.name}"))
    return items or [result("required-files", "pass")]


def markdown_targets(text):
    pattern = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
    for match in pattern.finditer(text):
        raw = match.group(1).strip()
        if raw.startswith("<") and ">" in raw:
            raw = raw[1:raw.index(">")]
        elif " " in raw:
            raw = raw.split(" ", 1)[0]
        yield unquote(raw)


def local_target(repo, source, target):
    if not target or target.startswith(("#", "http://", "https://", "mailto:", "codexlog:")):
        return None
    path_part = target.split("#", 1)[0].split("?", 1)[0]
    if not path_part:
        return None
    pure = PurePosixPath(path_part)
    if pure.is_absolute():
        return "абсолютная локальная ссылка запрещена"
    lexical = source.parent.relative_to(repo) / Path(*pure.parts)
    depth = 0
    for part in lexical.parts:
        if part == "..":
            depth -= 1
        elif part not in {"", "."}:
            depth += 1
        if depth < 0:
            return "ссылка выходит за границу Product Unit"
    candidate = source.parent.joinpath(*pure.parts)
    try:
        resolved = candidate.resolve(strict=False)
        resolved.relative_to(repo.resolve())
    except (OSError, ValueError):
        return "ссылка выходит за границу Product Unit"
    if not candidate.exists():
        return "целевой путь отсутствует"
    return None


def check_links(repo):
    items = []
    for path in text_files(repo):
        if path.suffix != ".md":
            continue
        for target in markdown_targets(read(path)):
            issue = local_target(repo, path, target)
            if issue:
                items.append(result("local-links", "fail", f"{path.relative_to(repo)} -> {target}: {issue}"))
    return items or [result("local-links", "pass")]


def field_values(text, label):
    return [value.strip().strip("`") for value in re.findall(rf"^{re.escape(label)}:\s*(.+)$", text, flags=re.MULTILINE)]


def plan_id(path):
    match = PLAN_FILE_RE.match(path.name)
    return match.group(1) if match else None


def heading_id(path):
    match = re.search(r"^#\s+(PLAN-\d{6})(?:\b|-)", read(path), flags=re.MULTILINE)
    return match.group(1) if match else None


def plan_paths(repo):
    active = sorted((repo / "plans" / "active").glob("PLAN-*.md"))
    completed = sorted((repo / "plans" / "completed").glob("PLAN-*.md"))
    return active, completed


def normalized_phase(value):
    value = value.strip().strip("`").lower()
    return PHASE_ALIASES.get(value, value)


def table_ids(path):
    ids = set()
    if not path.is_file():
        return ids
    for line in read(path).splitlines():
        if line.startswith("|"):
            first = line.strip().strip("|").split("|", 1)[0].strip().strip("`")
            ids.add(first)
    return ids


def parse_allowed(value):
    return [token.strip().strip("`") for token in value.split(",") if token.strip()]


def protected_token(token):
    plain = token[:-3] if token.endswith("/**") else token
    plain = plain.rstrip("/")
    return plain in {"AGENTS.md", "SYSTEM.md", "sops", "templates", "tools"}


def check_plans(repo):
    active, completed = plan_paths(repo)
    items = []
    if len(active) > 1:
        items.append(result("planning-contour", "fail", f"active PLAN: {len(active)}, допустимо 0..1"))
    seen = set()
    for path in active + completed:
        pid = plan_id(path)
        if not pid or heading_id(path) != pid:
            items.append(result("planning-contour", "fail", f"PLAN identity: {path.relative_to(repo)}"))
            continue
        if pid in seen:
            items.append(result("planning-contour", "fail", f"PLAN ID повторён: {pid}"))
        seen.add(pid)
        statuses = field_values(read(path), "Статус")
        expected = "active" if path in active else "completed"
        if statuses != [expected]:
            items.append(result("planning-contour", "fail", f"{path.relative_to(repo)}: Статус должен быть {expected}"))
    if len(active) == 1:
        path = active[0]
        text = read(path)
        required = [
            "Product Unit", "Фаза SDLC", "Операционный режим", "INTERVIEW_EVIDENCE_REF",
            "OWNER_DECISION_REFS", "PRODUCT_ACCEPTANCE_REF", "ALLOWED_SURFACES",
        ]
        for label in required:
            if len(field_values(text, label)) != 1:
                items.append(result("active-plan-fields", "fail", f"{label}: требуется ровно одно поле"))
        phases = field_values(text, "Фаза SDLC")
        if phases and normalized_phase(phases[0]) not in PHASES:
            items.append(result("active-plan-fields", "fail", f"неизвестная фаза: {phases[0]}"))
        modes = field_values(text, "Операционный режим")
        if modes and modes[0] not in {"product-work", "system-editing"}:
            items.append(result("active-plan-fields", "fail", f"неизвестный режим: {modes[0]}"))
        road_match = re.findall(r"^- ROAD:\s*(ROAD-\d{6})\s*$", text, flags=re.MULTILINE)
        back_match = re.findall(r"^- BACK:\s*(BACK-\d{6})\s*$", text, flags=re.MULTILINE)
        if len(road_match) != 1 or road_match[0] not in table_ids(repo / "plans" / "roadmap.md"):
            items.append(result("active-plan-fields", "fail", "active PLAN не связан с существующим ROAD"))
        if len(back_match) != 1 or back_match[0] not in table_ids(repo / "plans" / "backlog.md"):
            items.append(result("active-plan-fields", "fail", "active PLAN не связан с существующим BACK"))
        allowed = field_values(text, "ALLOWED_SURFACES")
        if allowed:
            tokens = parse_allowed(allowed[0])
            if not tokens or ("none" in tokens and len(tokens) != 1):
                items.append(result("allowed-surfaces", "fail", "некорректный ALLOWED_SURFACES"))
            for token in tokens:
                if token in EXACT_EXCEPTIONS or token == "none":
                    continue
                if token.startswith("/") or ".." in PurePosixPath(token).parts or "::" in token:
                    items.append(result("allowed-surfaces", "fail", f"некорректный токен: {token}"))
                if modes == ["product-work"] and protected_token(token):
                    items.append(result("protected-surfaces", "fail", f"product-work разрешает системную поверхность: {token}"))
    return items or [result("planning-contour", "pass"), result("active-plan-fields", "pass"), result("allowed-surfaces", "pass"), result("protected-surfaces", "pass")]


def parse_sot_config(repo):
    """Читает machine-readable SoT configuration из AGENTS.md ровно один раз."""
    agents = repo / "AGENTS.md"
    text = read(agents) if agents.is_file() else ""
    mode_values = [match.group(1) for line in text.splitlines() if (match := SOT_FIELD_RE.match(line))]
    repository_values = [
        match.group(1).strip()
        for line in text.splitlines()
        if (match := SOT_REPOSITORY_FIELD_RE.match(line))
    ]
    mode = mode_values[0] if len(mode_values) == 1 and mode_values[0] in SOT_SUPPORTED else None
    repository = repository_values[0] if len(repository_values) == 1 else None
    return {
        "mode": mode,
        "mode_values": mode_values,
        "repository": repository,
        "repository_values": repository_values,
    }


def valid_repository_identity(value):
    match = re.fullmatch(r"[^/\s:@\\?#]+/[^/\s:@\\?#]+", value or "")
    if not match:
        return False
    repository = value.rsplit("/", 1)[1]
    return not repository.casefold().endswith(".git")


def check_sot(repo, config):
    items = []
    mode_values = config["mode_values"]
    repository_values = config["repository_values"]
    mode = config["mode"]
    if len(mode_values) != 1 or mode is None:
        items.append(result("sot-mode", "fail", "AGENTS.md должен содержать один поддерживаемый SOT_MODE"))
    if mode == "sot_github":
        if len(repository_values) != 1 or not valid_repository_identity(config["repository"]):
            items.append(result(
                "sot-config", "fail",
                "sot_github требует ровно один SOT_GITHUB_REPOSITORY в форме owner/repository",
            ))
    elif repository_values:
        items.append(result(
            "sot-config", "fail",
            "SOT_GITHUB_REPOSITORY допустим только при SOT_MODE=sot_github",
        ))
    for path in text_files(repo):
        rel = path.relative_to(repo).as_posix()
        if rel == "AGENTS.md":
            continue
        for line in read(path).splitlines():
            if rel != "templates/agents.md" and SOT_FIELD_RE.match(line):
                items.append(result("sot-config-location", "fail", f"объявление SOT_MODE вне AGENTS.md: {rel}"))
            if SOT_REPOSITORY_FIELD_RE.match(line):
                items.append(result(
                    "sot-config-location", "fail",
                    f"объявление SOT_GITHUB_REPOSITORY вне AGENTS.md: {rel}",
                ))
    return items or [result("sot-mode", "pass"), result("sot-config", "pass")]


def run_git(repo, *args):
    try:
        completed = subprocess.run(
            ["git", "-C", str(repo), *args],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=GIT_TIMEOUT_SECONDS,
            env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"},
        )
    except subprocess.TimeoutExpired:
        return 124, "", "timeout"
    except OSError as error:
        return 127, "", str(error)
    return completed.returncode, completed.stdout.strip(), completed.stderr.strip()


def check_local_git_repository(repo, check_name):
    git_path = repo / ".git"
    if not os.path.lexists(git_path) or git_path.is_symlink():
        return [result(check_name, "fail", "локальный repository отсутствует или невалиден")], None
    items = []
    code, top, error = run_git(repo, "rev-parse", "--show-toplevel")
    if code or not top:
        items.append(result(check_name, "fail", f"repository невалиден: {error}"))
    else:
        try:
            if Path(top).resolve() != repo.resolve():
                items.append(result(check_name, "fail", f"неверный repository root: {top}"))
        except OSError as exc:
            items.append(result(check_name, "fail", str(exc)))
    code, _head, error = run_git(repo, "rev-parse", "--verify", "HEAD^{commit}")
    if code:
        items.append(result(check_name, "fail", f"HEAD невалиден: {error}"))
    code, branch, error = run_git(repo, "symbolic-ref", "--quiet", "--short", "HEAD")
    if code or not branch:
        items.append(result(check_name, "fail", f"рабочая ветка невалидна: {error or 'detached HEAD'}"))
        branch = None
    code, status, error = run_git(repo, "status", "--porcelain=v1", "--untracked-files=all")
    if code:
        items.append(result(check_name, "fail", f"status недоступен: {error}"))
    elif status:
        items.append(result(check_name, "fail", "working tree не чист"))
    return (items or [result(check_name, "pass")]), branch


def repository_path_identity(path):
    value = path.strip("/")
    parts = value.split("/")
    if len(parts) != 2 or not all(parts):
        return None
    owner, repository = parts
    if repository.casefold().endswith(".git"):
        repository = repository[:-4]
    identity = f"{owner}/{repository}"
    return identity if valid_repository_identity(identity) else None


def github_remote_identity(url):
    if re.match(r"^https://", url, flags=re.IGNORECASE):
        try:
            parsed = urlsplit(url)
            port = parsed.port
        except ValueError:
            return None
        if (
            parsed.scheme.casefold() != "https"
            or (parsed.hostname or "").casefold() != "github.com"
            or parsed.username is not None
            or parsed.password is not None
            or port is not None
            or parsed.query
            or parsed.fragment
        ):
            return None
        return repository_path_identity(parsed.path)
    scp_match = re.fullmatch(r"git@([^\s/:]+):([^\s]+)", url)
    if scp_match:
        return repository_path_identity(scp_match.group(2))
    if re.match(r"^ssh://", url, flags=re.IGNORECASE):
        try:
            parsed = urlsplit(url)
            port = parsed.port
        except ValueError:
            return None
        if (
            parsed.scheme.casefold() != "ssh"
            or parsed.username != "git"
            or parsed.password is not None
            or not parsed.hostname
            or port is not None
            or parsed.query
            or parsed.fragment
        ):
            return None
        return repository_path_identity(parsed.path)
    return None


def check_mode_sot_files(_repo, _config):
    return [result("sot-files-git-isolation", "pass")]


def check_mode_sot_git(repo, _config):
    items, _branch = check_local_git_repository(repo, "sot-git-current")
    if any(item["status"] == "fail" for item in items):
        return items
    code, remotes, error = run_git(repo, "remote")
    if code:
        items.append(result("sot-git-remote", "fail", f"remote недоступен: {error}"))
    elif remotes:
        items.append(result("sot-git-remote", "fail", f"remote запрещён: {remotes}"))
    else:
        items.append(result("sot-git-remote", "pass"))
    return items


def check_github_remote(repo, expected):
    code, remotes, error = run_git(repo, "remote")
    names = remotes.splitlines() if not code else []
    if code:
        return [result("sot-github-remote", "fail", f"remote недоступен: {error}")]
    if names != ["origin"]:
        return [result("sot-github-remote", "fail", "требуется ровно один remote origin")]
    items = []
    identities = []
    for label, args in (
        ("fetch", ("remote", "get-url", "origin")),
        ("push", ("remote", "get-url", "--push", "origin")),
    ):
        code, url, error = run_git(repo, *args)
        identity = github_remote_identity(url) if not code else None
        if not identity:
            items.append(result(
                "sot-github-remote", "fail",
                f"{label} URL не является поддерживаемым GitHub remote: {error or url}",
            ))
        else:
            identities.append(identity)
    if identities and any(identity.casefold() != expected.casefold() for identity in identities):
        items.append(result("sot-github-remote", "fail", "repository identity не совпадает с AGENTS.md"))
    if len(identities) == 2 and identities[0].casefold() != identities[1].casefold():
        items.append(result("sot-github-remote", "fail", "fetch и push URL указывают на разные repository"))
    return items or [result("sot-github-remote", "pass")]


def check_github_refs(repo, branch):
    items = []
    code, upstream, error = run_git(repo, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}")
    if code or not upstream.startswith("origin/") or upstream == "origin/HEAD":
        items.append(result("sot-github-upstream", "fail", f"upstream невалиден: {error or upstream}"))
    else:
        code, _value, error = run_git(repo, "show-ref", "--verify", f"refs/remotes/{upstream}")
        if code:
            items.append(result("sot-github-upstream", "fail", f"remote ref отсутствует: {error or upstream}"))
    code, default_ref, error = run_git(repo, "symbolic-ref", "--quiet", "refs/remotes/origin/HEAD")
    if code or not default_ref.startswith("refs/remotes/origin/") or default_ref == "refs/remotes/origin/HEAD":
        items.append(result("sot-github-default-ref", "fail", f"origin/HEAD невалиден: {error or default_ref}"))
    else:
        code, _value, error = run_git(repo, "show-ref", "--verify", default_ref)
        if code:
            items.append(result("sot-github-default-ref", "fail", f"target origin/HEAD отсутствует: {error or default_ref}"))
    if upstream.startswith("origin/"):
        code, counts, error = run_git(repo, "rev-list", "--left-right", "--count", "HEAD...@{upstream}")
        try:
            ahead, behind = (int(value) for value in counts.split())
        except (TypeError, ValueError):
            ahead = behind = -1
        if code or ahead < 0 or behind != 0:
            items.append(result(
                "sot-github-divergence", "fail",
                f"ветка behind или diverged: {error or counts}",
            ))
    if branch is None:
        items.append(result("sot-github-upstream", "fail", "рабочая ветка отсутствует"))
    return items or [
        result("sot-github-upstream", "pass"),
        result("sot-github-default-ref", "pass"),
        result("sot-github-divergence", "pass"),
    ]


def check_mode_sot_github(repo, config):
    items, branch = check_local_git_repository(repo, "sot-github-current")
    if any(item["status"] == "fail" for item in items):
        return items
    items.extend(check_github_remote(repo, config["repository"]))
    if any(item["status"] == "fail" for item in items):
        return items
    items.extend(check_github_refs(repo, branch))
    return items


def check_disposable(repo):
    found = []
    for base, directories, filenames in os.walk(repo, followlinks=False):
        base_path = Path(base)
        rel_base = base_path.relative_to(repo).as_posix()
        if rel_base == ".git" or rel_base.startswith(".git/"):
            directories[:] = []
            continue
        directories[:] = sorted(name for name in directories if name not in LOCAL_SERVICE_DIRS)
        for name in list(directories):
            if name in DISPOSABLE_DIRS:
                found.append((base_path / name).relative_to(repo).as_posix())
        for filename in filenames:
            path = base_path / filename
            if filename.endswith(":Zone.Identifier") or any(filename.endswith(suffix) for suffix in DISPOSABLE_SUFFIXES):
                found.append(path.relative_to(repo).as_posix())
    return [result("disposable-paths", "fail", rel) for rel in sorted(set(found))] or [result("disposable-paths", "pass")]


def check_current_paths(repo):
    items = []
    for rel in sorted(FORBIDDEN_CURRENT_PATHS):
        if (repo / rel).exists():
            items.append(result("current-paths", "fail", f"запрещённый путь: {rel}"))
    research = repo / "research"
    if research.is_dir():
        for path in research.iterdir():
            if path.is_dir() and path.name != "archives" and not re.match(r"^\d{3}-[a-z0-9]+(?:-[a-z0-9]+)*$", path.name):
                items.append(result("current-paths", "fail", f"некорректный research-домен: research/{path.name}"))
    return items or [result("current-paths", "pass")]


def product_files(repo):
    files = []
    for root_name in ("src", "tests"):
        root = repo / root_name
        if not root.is_dir():
            continue
        for path in root.rglob("*"):
            rel = path.relative_to(repo).as_posix()
            if (
                path.is_file()
                and path.name != "README.md"
                and rel not in HARNESS_TEST_FILES
                and not any(part in LOCAL_SERVICE_DIRS | DISPOSABLE_DIRS for part in path.parts)
            ):
                files.append(path)
    return files


def brief_identity(repo):
    path = repo / "docs" / "product" / "product-brief.md"
    if not path.is_file():
        return None
    match = re.search(r"^## Продукт\s*$\n(.*?)(?=^##\s|\Z)", read(path), flags=re.MULTILINE | re.DOTALL)
    if not match:
        return None
    lines = [line.strip().strip("`") for line in match.group(1).splitlines() if line.strip()]
    if not lines or lines[0].lower().rstrip(".") in {"не задан", "none"}:
        return None
    return lines[0]


def active_plan(repo):
    active, _completed = plan_paths(repo)
    return active[0] if len(active) == 1 else None


def check_identity_and_user_docs(repo):
    items = []
    has_product = bool(product_files(repo))
    identity = brief_identity(repo)
    plan = active_plan(repo)
    if has_product:
        if not identity:
            items.append(result("product-identity", "fail", "product identity не задана"))
        readme = repo / "README.md"
        heading = re.search(r"^#\s+(.+)$", read(readme), flags=re.MULTILINE) if readme.is_file() else None
        if identity and (not heading or heading.group(1).strip() != identity):
            items.append(result("product-identity", "fail", "root README не совпадает с product identity"))
        if plan and identity:
            units = field_values(read(plan), "Product Unit")
            if units != [identity]:
                items.append(result("product-identity", "fail", "active PLAN использует другую product identity"))
        required_sections = [
            "## Назначение и ценность", "## Пользователь", "## Запуск", "## Основные команды",
            "## Хранение данных", "## Ограничения", "## Проверки",
        ]
        readme_text = read(readme) if readme.is_file() else ""
        for section in required_sections:
            if section not in readme_text:
                items.append(result("product-readme", "fail", f"отсутствует {section}"))
        user_root = repo / "docs" / "user"
        forbidden = ("ROAD", "BACK", "PLAN", "Harness")
        for path in user_root.rglob("*.md") if user_root.is_dir() else []:
            body = read(path)
            for marker in forbidden:
                if marker in body:
                    items.append(result("user-doc-boundary", "fail", f"{path.relative_to(repo)} содержит {marker}"))
    return items or [result("product-identity", "pass"), result("product-readme", "pass"), result("user-doc-boundary", "pass")]


def parse_records(path):
    if not path.is_file():
        return {}
    records = {}
    current = {}
    for line in read(path).splitlines() + [""]:
        match = re.match(r"^([A-Z][A-Z0-9_]*):\s*(.*)$", line)
        if match:
            key, value = match.groups()
            if key == "RECORD_TYPE" and current:
                rid = current.get("RECORD_ID")
                if rid:
                    records[rid] = current
                current = {}
            current[key] = value.strip()
        elif not line.strip() and current:
            rid = current.get("RECORD_ID")
            if rid:
                records[rid] = current
            current = {}
    return records


def validate_codexlog(repo, value):
    match = CODEXLOG_RE.match(value or "")
    if not match:
        return False
    rel, start_text, end_text = match.groups()
    path = repo / rel
    try:
        path.resolve().relative_to(repo.resolve())
    except (OSError, ValueError):
        return False
    if not path.is_file():
        return False
    start, end = int(start_text), int(end_text)
    if start < 1 or end < start:
        return False
    try:
        line_count = sum(1 for _line in path.open(encoding="utf-8", errors="replace"))
    except OSError:
        return False
    return end <= line_count


def ref_list(value):
    if value == "none":
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def check_active_refs(repo):
    plan = active_plan(repo)
    if not plan:
        return [result("active-plan-links", "pass", "active PLAN absent")]
    text = read(plan)
    phase_values = field_values(text, "Фаза SDLC")
    phase = normalized_phase(phase_values[0]) if len(phase_values) == 1 else "invalid"
    ie_values = field_values(text, "INTERVIEW_EVIDENCE_REF")
    od_values = field_values(text, "OWNER_DECISION_REFS")
    pa_values = field_values(text, "PRODUCT_ACCEPTANCE_REF")
    if not (len(ie_values) == len(od_values) == len(pa_values) == 1):
        return [result("active-plan-links", "fail", "машинные ссылки active PLAN некорректны")]
    sessions = parse_records(repo / "logs" / "sessions.md")
    decisions = parse_records(repo / "logs" / "decisions.md")
    items = []
    ie_ref = ie_values[0]
    ie = None
    if ie_ref != "none":
        ie = sessions.get(ie_ref)
        if not IE_ID_RE.match(ie_ref) or not ie or ie.get("RECORD_TYPE") != "interview_evidence":
            items.append(result("active-plan-links", "fail", f"невалидная IE-ссылка: {ie_ref}"))
        elif not validate_codexlog(repo, ie.get("SOURCE_REF")):
            items.append(result("active-plan-links", "fail", f"IE SOURCE_REF невалиден: {ie_ref}"))
    implementation = None
    for od_ref in ref_list(od_values[0]):
        od = decisions.get(od_ref)
        if not OD_ID_RE.match(od_ref) or not od or od.get("RECORD_TYPE") != "owner_decision":
            items.append(result("active-plan-links", "fail", f"невалидная OD-ссылка: {od_ref}"))
            continue
        if not validate_codexlog(repo, od.get("SOURCE_REF")):
            items.append(result("active-plan-links", "fail", f"OD SOURCE_REF невалиден: {od_ref}"))
        if od.get("DECISION_KIND") == "implementation" and od.get("DECISION_VALUE") == "approved":
            implementation = od
            if od.get("PLAN_ID") != plan_id(plan) or od.get("EVIDENCE_REF") != ie_ref:
                items.append(result("active-plan-links", "fail", f"implementation decision не связан с active PLAN: {od_ref}"))
    if phase in {"implementation", "verification", "owner-review", "product-acceptance"}:
        if ie_ref == "none" or implementation is None:
            items.append(result("active-plan-links", "fail", "фаза требует IE и implementation decision"))
    pa_ref = pa_values[0]
    if pa_ref != "none":
        pa = decisions.get(pa_ref)
        if not PA_ID_RE.match(pa_ref) or not pa or pa.get("RECORD_TYPE") != "product_acceptance":
            items.append(result("active-plan-links", "fail", f"невалидная PA-ссылка: {pa_ref}"))
        else:
            if pa.get("PLAN_ID") != plan_id(plan) or pa.get("DECISION_VALUE") not in {"accepted", "rejected"}:
                items.append(result("active-plan-links", "fail", f"PA не связана с active PLAN: {pa_ref}"))
            if not validate_codexlog(repo, pa.get("SOURCE_REF")):
                items.append(result("active-plan-links", "fail", f"PA SOURCE_REF невалиден: {pa_ref}"))
    if phase == "product-acceptance" and pa_ref == "none":
        items.append(result("active-plan-links", "fail", "product-acceptance требует PA-ссылку"))
    return items or [result("active-plan-links", "pass")]


def check_current_state(repo):
    plan = active_plan(repo)
    has_product = bool(product_files(repo))
    items = []
    if plan:
        phase_values = field_values(read(plan), "Фаза SDLC")
        phase = normalized_phase(phase_values[0]) if len(phase_values) == 1 else "invalid"
        if has_product and phase in {"intent", "interview", "requirements"}:
            items.append(result("product-state", "fail", f"продуктовый код несовместим с фазой {phase}"))
        else:
            items.append(result("product-state", "pass", f"active/{phase}"))
    else:
        accepted = []
        decisions = parse_records(repo / "logs" / "decisions.md")
        for path in plan_paths(repo)[1]:
            refs = field_values(read(path), "PRODUCT_ACCEPTANCE_REF")
            if len(refs) == 1 and refs[0] != "none":
                record = decisions.get(refs[0])
                if record and record.get("DECISION_VALUE") == "accepted":
                    accepted.append(plan_id(path))
        state = "accepted-completed" if accepted else ("idle-product" if has_product else "initial-idle")
        items.append(result("product-state", "pass", state))
    return items


def check_workspace_boundary(repo):
    items = []
    pattern = re.compile(r"\b(?:WROAD|WBACK|WPLAN)-\d{6}\b")
    for path in text_files(repo):
        if pattern.search(read(path)):
            items.append(result("workspace-boundary", "fail", f"текущий Workspace ID в {path.relative_to(repo)}"))
    return items or [result("workspace-boundary", "pass")]


def run(repo):
    checks = safe_tree(repo)
    if any(item["status"] == "fail" for item in checks):
        return checks
    config = parse_sot_config(repo)
    checks.extend(check_required(repo))
    checks.extend(check_links(repo))
    checks.extend(check_plans(repo))
    sot_checks = check_sot(repo, config)
    checks.extend(sot_checks)
    checks.extend(check_disposable(repo))
    checks.extend(check_current_paths(repo))
    checks.extend(check_active_refs(repo))
    checks.extend(check_identity_and_user_docs(repo))
    checks.extend(check_current_state(repo))
    checks.extend(check_workspace_boundary(repo))
    if not any(item["status"] == "fail" for item in sot_checks):
        handler = {
            "sot_files": check_mode_sot_files,
            "sot_git": check_mode_sot_git,
            "sot_github": check_mode_sot_github,
        }[config["mode"]]
        checks.extend(handler(repo, config))
    return checks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=".")
    parser.add_argument("--format", default="text", choices=["text", "json"])
    args = parser.parse_args()
    repo = Path(args.repo).resolve()
    if not repo.is_dir():
        print("FAIL repository-root: Product Unit root отсутствует")
        return 1
    checks = run(repo)
    failures = [item for item in checks if item["status"] == "fail"]
    warnings = [item for item in checks if item["status"] == "warn"]
    if args.format == "json":
        print(json.dumps({"checks": checks, "failures": len(failures), "warnings": len(warnings)}, ensure_ascii=False, indent=2))
    else:
        for item in checks:
            message = f": {item['message']}" if item.get("message") else ""
            print(f"{item['status'].upper()} {item['check']}{message}")
        verdict = "FAIL" if failures else "PASS"
        print(f"{verdict} summary: {len(failures)} fail, {len(warnings)} warn")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
