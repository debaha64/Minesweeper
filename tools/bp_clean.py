#!/usr/bin/env python3
import argparse
import os
import stat
import sys
from pathlib import Path

sys.dont_write_bytecode = True

import re


DISPOSABLE_DIR_NAMES = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
DISPOSABLE_SUFFIXES = {".pyc", ".pyo", ".tmp", ".temp", ".orig"}
ZONE_IDENTIFIER_PATTERNS = (
    re.compile(r".*:Zone\.Identifier$"),
    re.compile(r".*\.Identifier$"),
)
LOCAL_SERVICE_DIR_NAMES = {".agents", ".codex"}
DURABLE_RAW_LOG_RE = re.compile(r"^.+\.raw\.log$")
CODEXLOG_REF_RE = re.compile(
    r"^[A-Z][A-Z0-9_]*:\s*codexlog:(?P<path>\.codex/[^#\r\n]+)#"
    r"(?:(?:lines=(?P<start>\d+)-(?P<end>\d+))|(?:event=(?P<event>[A-Za-z0-9._:-]+)))\s*$",
    flags=re.MULTILINE,
)


def is_zone_identifier(path):
    return any(pattern.match(path.name) for pattern in ZONE_IDENTIFIER_PATTERNS)


def scan_directory(directory, *, skip_local_service=True):
    directories = []
    filenames = []
    symlinks = []
    with os.scandir(directory) as iterator:
        entries = sorted(iterator, key=lambda entry: entry.name)
    for entry in entries:
        name = entry.name
        if name == ".git" or (skip_local_service and name in LOCAL_SERVICE_DIR_NAMES):
            continue
        if entry.is_symlink():
            symlinks.append(name)
        elif entry.is_dir(follow_symlinks=False):
            directories.append(name)
        elif entry.is_file(follow_symlinks=False):
            filenames.append(name)
    return directories, filenames, symlinks


def disposable_paths(repo):
    found = []
    pending = [Path(repo)]
    while pending:
        base = pending.pop()
        directories, filenames, _symlinks = scan_directory(base)
        for name in directories:
            path = base / name
            if name in DISPOSABLE_DIR_NAMES:
                found.append(path)
            else:
                pending.append(path)
        for name in filenames:
            path = base / name
            if path.suffix in DISPOSABLE_SUFFIXES or is_zone_identifier(path):
                found.append(path)
    return sorted(found, key=lambda p: str(p.relative_to(repo)))


def local_service_paths(repo):
    with os.scandir(repo) as iterator:
        entries = sorted(iterator, key=lambda entry: entry.name)
    found = []
    for entry in entries:
        name = entry.name
        if name == ".git" or name not in LOCAL_SERVICE_DIR_NAMES:
            continue
        if entry.is_symlink():
            found.append(repo / name)
        elif entry.is_dir(follow_symlinks=False) or entry.is_file(follow_symlinks=False):
            found.append(repo / name)
    return sorted(found, key=lambda p: str(p.relative_to(repo)))


def local_regular_file_no_symlink(repo, relative):
    if relative.is_absolute() or ".." in relative.parts or relative.parts[:1] != (".codex",):
        return None
    current = repo
    for index, part in enumerate(relative.parts):
        current = current / part
        try:
            mode = os.lstat(current).st_mode
        except OSError:
            return None
        if stat.S_ISLNK(mode):
            return None
        if index < len(relative.parts) - 1 and not stat.S_ISDIR(mode):
            return None
    return current if stat.S_ISREG(mode) else None


def referenced_codex_paths(repo):
    """Собирает существующие `.codex`-файлы из корректных ссылок постоянных Markdown records."""
    retained = set()
    records = Path(repo) / "logs"
    _directories, filenames, _symlinks = scan_directory(records)
    for name in filenames:
        if not name.endswith(".md"):
            continue
        text = (records / name).read_text(encoding="utf-8")
        for match in CODEXLOG_REF_RE.finditer(text):
            relative = Path(match.group("path"))
            target = local_regular_file_no_symlink(repo, relative)
            if target is None:
                continue
            if match.group("start"):
                start, end = int(match.group("start")), int(match.group("end"))
                count = len(target.read_text(encoding="utf-8", errors="replace").splitlines())
                if not 1 <= start <= end <= count:
                    continue
            retained.add(target)
    return retained


def remove_path_no_follow(path, retained_codex_paths=frozenset(), inside_codex=False):
    """Удаляет путь без следования symlink и возвращает число удалённых payload-путей."""
    try:
        mode = os.lstat(path).st_mode
    except FileNotFoundError:
        return 0
    if stat.S_ISLNK(mode) or not stat.S_ISDIR(mode):
        if path in retained_codex_paths and stat.S_ISREG(mode):
            return 0
        path.unlink()
        return 1
    removed = 0
    current_inside_codex = inside_codex or path.name == ".codex"
    with os.scandir(path) as iterator:
        entries = sorted(iterator, key=lambda entry: entry.name)
    for entry in entries:
        name = entry.name
        if name == ".git":
            continue
        child = path / name
        if entry.is_symlink():
            child.unlink()
            removed += 1
        elif entry.is_dir(follow_symlinks=False):
            removed += remove_path_no_follow(
                child, retained_codex_paths, inside_codex=current_inside_codex,
            )
        else:
            if not entry.is_file(follow_symlinks=False):
                continue
            if current_inside_codex and (
                DURABLE_RAW_LOG_RE.fullmatch(name) or child in retained_codex_paths
            ):
                continue
            child.unlink()
            removed += 1
    try:
        path.rmdir()
    except OSError:
        return removed
    return removed


def apply_paths(paths, retained_codex_paths=frozenset()):
    removed = 0
    for path in paths:
        removed += remove_path_no_follow(path, retained_codex_paths)
    return removed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=".")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--local-service", action="store_true")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    try:
        found = disposable_paths(repo)
        service = local_service_paths(repo)
        retained_codex = referenced_codex_paths(repo) if args.local_service else set()
    except OSError as error:
        print(f"FAIL clean-boundary: невозможно безопасно прочитать Product Unit: {error}")
        return 1
    if args.local_service:
        found.extend(service)
    mode = "apply" if args.apply else "dry-run"
    if args.apply and args.local_service:
        mode += " with local-service"
    print(f"bp_clean: режим {mode}")
    if service and not args.local_service:
        print("Локальные служебные пути игнорируются и не удаляются:")
        for path in service:
            print(str(path.relative_to(repo)))
    if not found:
        print("Одноразовые пути не найдены.")
        return 0

    for path in found:
        print(str(path.relative_to(repo)))

    if args.apply:
        removed = apply_paths(found, retained_codex)
        print(f"Удалено: {removed}")
    else:
        print("Ничего не удалено. Для удаления перечисленных путей повторите команду с --apply.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
