#!/usr/bin/env python3
"""Локальная regression-матрица трёх режимов SoT."""

import ast
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SOURCE_ROOT = Path(__file__).resolve().parents[1]
REAL_GIT = shutil.which("git")
MODE_PREFIX = "SOT_" + "MODE:"
REPOSITORY_PREFIX = "SOT_GITHUB_" + "REPOSITORY:"


class SotModeTests(unittest.TestCase):
    maxDiff = None

    def copy_unit(self):
        temporary = tempfile.TemporaryDirectory(prefix="bytepress-sot-test-")
        self.addCleanup(temporary.cleanup)
        repo = Path(temporary.name) / "ProductUnit"
        shutil.copytree(
            SOURCE_ROOT,
            repo,
            ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc", "*.pyo"),
        )
        self.set_config(repo, "sot_files")
        return repo

    def set_config(self, repo, mode, repositories=()):
        path = repo / "AGENTS.md"
        lines = [
            line for line in path.read_text(encoding="utf-8").splitlines()
            if not line.strip().startswith(REPOSITORY_PREFIX)
        ]
        indexes = [index for index, line in enumerate(lines) if line.strip().startswith(MODE_PREFIX)]
        self.assertEqual(len(indexes), 1)
        index = indexes[0]
        lines[index] = f"{MODE_PREFIX} {mode}"
        for offset, repository in enumerate(repositories, start=1):
            lines.insert(index + offset, f"{REPOSITORY_PREFIX} {repository}")
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    def command(self, args, *, env=None, input_text=None, check=True):
        completed = subprocess.run(
            args,
            text=True,
            input=input_text,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            env=env,
        )
        if check and completed.returncode:
            self.fail(
                f"command failed ({completed.returncode}): {shlex.join(map(str, args))}\n"
                f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
            )
        return completed

    def git(self, repo, *args, input_text=None, check=True):
        self.assertIsNotNone(REAL_GIT, "Git CLI нужен для локальной Git-матрицы")
        env = {
            **os.environ,
            "GIT_AUTHOR_NAME": "BytePress Test",
            "GIT_AUTHOR_EMAIL": "test@example.invalid",
            "GIT_COMMITTER_NAME": "BytePress Test",
            "GIT_COMMITTER_EMAIL": "test@example.invalid",
            "GIT_OPTIONAL_LOCKS": "0",
        }
        return self.command(
            [REAL_GIT, "-C", str(repo), *args], env=env, input_text=input_text, check=check
        )

    def run_checker(self, repo, *, env=None):
        completed = self.command(
            [sys.executable, str(repo / "tools" / "bp_check.py"), "--repo", str(repo), "--format", "json"],
            env=env,
            check=False,
        )
        try:
            payload = json.loads(completed.stdout)
        except json.JSONDecodeError:
            self.fail(f"checker did not return JSON:\n{completed.stdout}\n{completed.stderr}")
        return completed, payload

    def run_init(self, repo, *, env=None):
        return self.command(
            [sys.executable, str(repo / "tools" / "bp_init.py"), "--repo", str(repo)],
            env=env,
            check=False,
        )

    def assert_pass(self, result):
        completed, payload = result
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertEqual(payload["failures"], 0, completed.stdout)

    @staticmethod
    def check_names(payload):
        return {item["check"] for item in payload["checks"]}

    @staticmethod
    def failure_names(payload):
        return {item["check"] for item in payload["checks"] if item["status"] == "fail"}

    def make_git(self, mode="sot_git", repositories=()):
        repo = self.copy_unit()
        self.set_config(repo, mode, repositories)
        self.git(repo, "init", "-b", "work")
        self.git(repo, "config", "user.name", "BytePress Test")
        self.git(repo, "config", "user.email", "test@example.invalid")
        self.git(repo, "add", "-A")
        self.git(repo, "commit", "-m", "fixture baseline")
        return repo

    def make_github(self, url="https://github.com/Example/Widget.git", repository="Example/Widget"):
        repo = self.make_git("sot_github", [repository])
        self.git(repo, "remote", "add", "origin", url)
        self.git(repo, "update-ref", "refs/remotes/origin/work", "HEAD")
        self.git(repo, "symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/work")
        self.git(repo, "branch", "--set-upstream-to=origin/work", "work")
        return repo

    def make_product_fixture(self):
        repo = self.copy_unit()
        (repo / "plans" / "active" / "PLAN-000001-product-discovery.md").unlink(
            missing_ok=True
        )
        (repo / "docs" / "product" / "product-brief.md").write_text(
            "# Краткое описание продукта\n\n## Продукт\n\nMinesweeper\n",
            encoding="utf-8",
        )
        (repo / "README.md").write_text(
            """# Minesweeper

## Назначение и ценность

Локальная минимальная regression-fixture игрового ядра.

## Пользователь

Пользователь локального приложения.

## Запуск

`python3 src/minesweeper.py --smoke`

## Основные команды

Smoke и unit tests.

## Хранение данных

Постоянное хранение не используется.

## Ограничения

Fixture проверяет только подсчёт соседних мин.

## Проверки

`python3 -m unittest discover -s tests -p 'test_minesweeper.py'`
""",
            encoding="utf-8",
        )
        for path in (repo / "docs" / "user").glob("*.md"):
            path.write_text(
                f"# {path.stem.replace('-', ' ').title()}\n\nЛокальная пользовательская документация Minesweeper.\n",
                encoding="utf-8",
            )
        (repo / "src" / "minesweeper.py").write_text(
            """#!/usr/bin/env python3
import sys


def adjacent_mines(board, row, column):
    total = 0
    for row_index in range(max(0, row - 1), min(len(board), row + 2)):
        for column_index in range(max(0, column - 1), min(len(board[0]), column + 2)):
            if (row_index, column_index) != (row, column):
                total += board[row_index][column_index] == "*"
    return total


if __name__ == "__main__" and sys.argv[1:] == ["--smoke"]:
    assert adjacent_mines(["*.", ".."], 1, 1) == 1
    print("Minesweeper smoke: PASS")
""",
            encoding="utf-8",
        )
        (repo / "tests" / "test_minesweeper.py").write_text(
            """import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from minesweeper import adjacent_mines


class MinesweeperTests(unittest.TestCase):
    def test_adjacent_mines(self):
        self.assertEqual(adjacent_mines(["*.", ".."], 1, 1), 1)


if __name__ == "__main__":
    unittest.main()
""",
            encoding="utf-8",
        )
        return repo

    def test_sot_files_passes_with_failing_git_stub_and_no_invocation(self):
        repo = self.copy_unit()
        marker = repo.parent / "git-called"
        bindir = repo.parent / "bin"
        bindir.mkdir()
        stub = bindir / "git"
        stub.write_text(
            "#!/bin/sh\nprintf '%s\\n' called >> \"$BP_GIT_LOG\"\nexit 97\n",
            encoding="utf-8",
        )
        stub.chmod(0o755)
        env = {**os.environ, "PATH": str(bindir), "BP_GIT_LOG": str(marker)}
        self.assert_pass(self.run_checker(repo, env=env))
        self.assertFalse(marker.exists())

    def test_existing_product_discovery_allows_preexisting_product_outside_surfaces(self):
        repo = self.make_product_fixture()
        plan = repo / "plans" / "active" / "PLAN-000001-existing-product-discovery.md"
        plan.write_text(
            """# PLAN-000001-existing-product-discovery

Статус: active

Связь:
- ROAD: ROAD-000001
- BACK: BACK-000001

Product Unit: Minesweeper
Фаза SDLC: discovery
Операционный режим: product-work
INTERVIEW_EVIDENCE_REF: none
OWNER_DECISION_REFS: none
ALLOWED_SURFACES: docs/product/, plans/, logs/
PRODUCT_ACCEPTANCE_REF: none
""",
            encoding="utf-8",
        )
        self.assertNotIn("src/", re.search(
            r"^ALLOWED_SURFACES:\s*(.+)$", plan.read_text(encoding="utf-8"), re.MULTILINE
        ).group(1))
        self.assertNotIn("tests/", re.search(
            r"^ALLOWED_SURFACES:\s*(.+)$", plan.read_text(encoding="utf-8"), re.MULTILINE
        ).group(1))
        self.assert_pass(self.run_checker(repo))

    def test_sot_git_clean_passes_and_dispatch_is_isolated(self):
        completed, payload = self.run_checker(self.make_git())
        self.assertEqual(completed.returncode, 0, completed.stdout)
        names = self.check_names(payload)
        self.assertIn("sot-git-current", names)
        self.assertIn("sot-git-remote", names)
        self.assertNotIn("sot-files-git-isolation", names)
        github_handler_checks = {
            "sot-github-current", "sot-github-remote", "sot-github-upstream",
            "sot-github-default-ref", "sot-github-divergence",
        }
        self.assertTrue(names.isdisjoint(github_handler_checks))

    def test_sot_git_remote_present_fails(self):
        repo = self.make_git()
        self.git(repo, "remote", "add", "origin", "https://github.com/Example/Widget.git")
        completed, payload = self.run_checker(repo)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("sot-git-remote", self.failure_names(payload))

    def test_github_configuration_contract(self):
        cases = [
            ("sot_github", [], "missing"),
            ("sot_github", ["Example/Widget", "Example/Other"], "duplicate"),
            ("sot_files", ["Example/Widget"], "field-in-files"),
            ("sot_git", ["Example/Widget"], "field-in-git"),
            ("sot_github", ["https://github.com/Example/Widget"], "url-value"),
            ("sot_github", ["Example/Widget.git"], "git-suffix"),
            ("sot_github", ["Example /Widget"], "whitespace"),
            ("sot_github", [""], "empty"),
        ]
        for mode, repositories, label in cases:
            with self.subTest(label=label):
                repo = self.copy_unit()
                self.set_config(repo, mode, repositories)
                completed, payload = self.run_checker(repo)
                self.assertNotEqual(completed.returncode, 0)
                self.assertIn("sot-config", self.failure_names(payload))

    def test_valid_github_configuration_continues_to_mode_handler(self):
        repo = self.copy_unit()
        self.set_config(repo, "sot_github", ["Example/Widget"])
        completed, payload = self.run_checker(repo)
        self.assertNotEqual(completed.returncode, 0)
        self.assertNotIn("sot-config", self.failure_names(payload))
        self.assertIn("sot-github-current", self.failure_names(payload))

    def test_github_configuration_allows_github_io_repository_name(self):
        repo = self.copy_unit()
        self.set_config(repo, "sot_github", ["Example/example.github.io"])
        _completed, payload = self.run_checker(repo)
        self.assertNotIn("sot-config", self.failure_names(payload))
        self.assertIn("sot-github-current", self.failure_names(payload))

    def test_github_configuration_allows_internal_git_name_segment(self):
        repo = self.copy_unit()
        self.set_config(repo, "sot_github", ["Example/tool.git.adapter"])
        _completed, payload = self.run_checker(repo)
        self.assertNotIn("sot-config", self.failure_names(payload))
        self.assertIn("sot-github-current", self.failure_names(payload))

    def test_github_supported_remote_urls_pass(self):
        urls = [
            "https://github.com/example/widget.git",
            "https://github.com/Example/Widget",
            "git@github.com:Example/Widget.git",
            "git@work-gh:Example/Widget.git",
            "ssh://git@github.com/Example/Widget.git",
        ]
        for url in urls:
            with self.subTest(url=url):
                self.assert_pass(self.run_checker(self.make_github(url)))

    def test_github_rejects_invalid_remote_identity(self):
        cases = [
            ("https://github.com/Example/Other.git", "mismatch"),
            ("https://example.com/Example/Widget.git", "unexpected-host"),
            ("/tmp/local-bare.git", "local-path"),
            ("file:///tmp/local-bare.git", "file-url"),
            ("https://user:secret@github.com/Example/Widget.git", "credentials"),
        ]
        for url, label in cases:
            with self.subTest(label=label):
                completed, payload = self.run_checker(self.make_github(url))
                self.assertNotEqual(completed.returncode, 0)
                self.assertIn("sot-github-remote", self.failure_names(payload))

    def test_github_requires_only_origin(self):
        repo = self.make_github()
        self.git(repo, "remote", "add", "mirror", "https://github.com/Example/Widget.git")
        completed, payload = self.run_checker(repo)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("sot-github-remote", self.failure_names(payload))

        repo = self.make_github()
        self.git(repo, "remote", "rename", "origin", "source")
        completed, payload = self.run_checker(repo)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("sot-github-remote", self.failure_names(payload))

        repo = self.make_git("sot_github", ["Example/Widget"])
        completed, payload = self.run_checker(repo)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("sot-github-remote", self.failure_names(payload))

    def test_github_default_branch_snapshot_contract(self):
        repo = self.make_github()
        self.git(repo, "symbolic-ref", "--delete", "refs/remotes/origin/HEAD")
        completed, payload = self.run_checker(repo)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("sot-github-default-ref", self.failure_names(payload))

        repo = self.make_github()
        self.git(repo, "symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/missing")
        completed, payload = self.run_checker(repo)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("sot-github-default-ref", self.failure_names(payload))

        repo = self.make_github()
        self.git(repo, "update-ref", "refs/remotes/else/work", "HEAD")
        self.git(repo, "symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/else/work")
        completed, payload = self.run_checker(repo)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("sot-github-default-ref", self.failure_names(payload))

    def test_github_rejects_missing_upstream(self):
        repo = self.make_github()
        self.git(repo, "config", "--unset", "branch.work.remote")
        self.git(repo, "config", "--unset", "branch.work.merge")
        completed, payload = self.run_checker(repo)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("sot-github-upstream", self.failure_names(payload))

    def test_github_rejects_absent_git_detached_head_and_dirty_tree(self):
        repo = self.copy_unit()
        self.set_config(repo, "sot_github", ["Example/Widget"])
        completed, payload = self.run_checker(repo)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("sot-github-current", self.failure_names(payload))

        repo = self.make_github()
        self.git(repo, "checkout", "--detach")
        completed, payload = self.run_checker(repo)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("sot-github-current", self.failure_names(payload))

        repo = self.make_github()
        with (repo / "README.md").open("a", encoding="utf-8") as stream:
            stream.write("\nlocal dirty fixture\n")
        completed, payload = self.run_checker(repo)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("sot-github-current", self.failure_names(payload))

    def test_github_allows_ahead_and_rejects_behind(self):
        repo = self.make_github()
        base = self.git(repo, "rev-parse", "HEAD").stdout.strip()
        tree = self.git(repo, "rev-parse", "HEAD^{tree}").stdout.strip()
        child = self.git(repo, "commit-tree", tree, "-p", base, input_text="next\n").stdout.strip()
        self.git(repo, "update-ref", "refs/heads/work", child, base)
        self.assert_pass(self.run_checker(repo))

        repo = self.make_github()
        base = self.git(repo, "rev-parse", "HEAD").stdout.strip()
        tree = self.git(repo, "rev-parse", "HEAD^{tree}").stdout.strip()
        child = self.git(repo, "commit-tree", tree, "-p", base, input_text="remote next\n").stdout.strip()
        self.git(repo, "update-ref", "refs/remotes/origin/work", child, base)
        completed, payload = self.run_checker(repo)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("sot-github-divergence", self.failure_names(payload))

    def test_dispatch_and_mode_parsing_are_explicit(self):
        source = (SOURCE_ROOT / "tools" / "bp_check.py").read_text(encoding="utf-8")
        tree = ast.parse(source)
        run_node = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "run")
        parse_calls = [
            node for node in ast.walk(run_node)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "parse_sot_config"
        ]
        self.assertEqual(len(parse_calls), 1)
        handlers = {
            node.name for node in tree.body
            if isinstance(node, ast.FunctionDef) and node.name.startswith("check_mode_sot_")
        }
        self.assertEqual(handlers, {"check_mode_sot_files", "check_mode_sot_git", "check_mode_sot_github"})

        repo = self.copy_unit()
        completed, payload = self.run_checker(repo)
        self.assertEqual(completed.returncode, 0, completed.stdout)
        names = self.check_names(payload)
        self.assertIn("sot-files-git-isolation", names)
        self.assertNotIn("sot-git-current", names)
        self.assertFalse(any(name.startswith("sot-github-") for name in names))

        completed, payload = self.run_checker(self.make_github())
        self.assertEqual(completed.returncode, 0, completed.stdout)
        names = self.check_names(payload)
        self.assertIn("sot-github-current", names)
        self.assertNotIn("sot-files-git-isolation", names)
        self.assertNotIn("sot-git-current", names)

    def test_github_checker_uses_only_local_git_commands(self):
        repo = self.make_github()
        bindir = repo.parent / "network-guard"
        bindir.mkdir()
        git_log = repo.parent / "git.log"
        external_log = repo.parent / "external.log"
        git_stub = bindir / "git"
        git_stub.write_text(
            "#!/bin/sh\nprintf '%s\\n' \"$*\" >> \"$BP_GIT_LOG\"\nexec \"$BP_REAL_GIT\" \"$@\"\n",
            encoding="utf-8",
        )
        git_stub.chmod(0o755)
        for name in ("gh", "curl", "wget"):
            stub = bindir / name
            stub.write_text(
                f"#!/bin/sh\nprintf '%s\\n' '{name}' >> \"$BP_EXTERNAL_LOG\"\nexit 99\n",
                encoding="utf-8",
            )
            stub.chmod(0o755)
        env = {
            **os.environ,
            "PATH": str(bindir) + os.pathsep + os.environ.get("PATH", ""),
            "BP_REAL_GIT": REAL_GIT,
            "BP_GIT_LOG": str(git_log),
            "BP_EXTERNAL_LOG": str(external_log),
        }
        self.assert_pass(self.run_checker(repo, env=env))
        forbidden = {"fetch", "pull", "push"}
        for line in git_log.read_text(encoding="utf-8").splitlines():
            argv = shlex.split(line)
            self.assertGreaterEqual(len(argv), 3)
            self.assertNotIn(argv[2], forbidden, line)
        self.assertFalse(external_log.exists())

    def test_bp_init_prints_github_identity_without_git_or_network(self):
        repo = self.copy_unit()
        self.set_config(repo, "sot_github", ["Example/Widget"])
        bindir = repo.parent / "guard"
        bindir.mkdir()
        marker = repo.parent / "external-called"
        for name in ("git", "gh", "curl", "wget"):
            stub = bindir / name
            stub.write_text(
                "#!/bin/sh\nprintf '%s\\n' called >> \"$BP_EXEC_LOG\"\nexit 99\n",
                encoding="utf-8",
            )
            stub.chmod(0o755)
        env = {**os.environ, "PATH": str(bindir), "BP_EXEC_LOG": str(marker)}
        completed = self.run_init(repo, env=env)
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn("SOT_GITHUB_REPOSITORY: Example/Widget", completed.stdout)
        self.assertFalse(marker.exists())

    def test_product_bearing_minesweeper_regression_in_files_and_git_modes(self):
        repo = self.make_product_fixture()
        product_tests = self.command(
            [
                sys.executable, "-m", "unittest", "discover", "-s", str(repo / "tests"),
                "-p", "test_minesweeper.py",
            ],
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        self.assertIn("OK", product_tests.stderr)
        smoke = self.command(
            [sys.executable, str(repo / "src" / "minesweeper.py"), "--smoke"],
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        self.assertEqual(smoke.stdout.strip(), "Minesweeper smoke: PASS")

        completed, payload = self.run_checker(repo)
        self.assertEqual(completed.returncode, 0, completed.stdout)
        self.assertIn("protected-surfaces", self.check_names(payload))
        self.assertIn("sot-files-git-isolation", self.check_names(payload))

        self.set_config(repo, "sot_git")
        self.git(repo, "init", "-b", "work")
        self.git(repo, "config", "user.name", "BytePress Test")
        self.git(repo, "config", "user.email", "test@example.invalid")
        self.git(repo, "add", "-A")
        self.git(repo, "commit", "-m", "Minesweeper fixture baseline")
        completed, payload = self.run_checker(repo)
        self.assertEqual(completed.returncode, 0, completed.stdout)
        self.assertIn("protected-surfaces", self.check_names(payload))
        self.assertIn("sot-git-current", self.check_names(payload))


if __name__ == "__main__":
    unittest.main()
