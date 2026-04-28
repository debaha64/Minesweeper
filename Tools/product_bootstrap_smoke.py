#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import subprocess
import sys


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    report_dir = root / "Tools" / ".reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        [sys.executable, str(root / "Tools" / "product_check.py"), "--repo", str(root), "--mode", "auto"],
        text=True,
        capture_output=True,
    )
    report = {
        "check": "product_bootstrap_smoke",
        "returncode": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }
    (report_dir / "product_bootstrap_smoke.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Product bootstrap smoke report written to: {report_dir / 'product_bootstrap_smoke.json'}")
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
