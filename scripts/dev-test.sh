#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ -z "${BYTEPRESS_ROOT:-}" ]]; then
  echo "Set BYTEPRESS_ROOT to the BytePress repository path before running dev-test.sh."
  exit 1
fi

LINT_SCRIPT="$BYTEPRESS_ROOT/Tools/bp_lint.py"
if [[ ! -f "$LINT_SCRIPT" ]]; then
  echo "BytePress lint script not found at: $LINT_SCRIPT"
  exit 1
fi

python3 "$LINT_SCRIPT" --repo "$ROOT_DIR" --mode auto
