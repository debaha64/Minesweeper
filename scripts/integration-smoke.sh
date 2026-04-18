#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ -z "${BYTEPRESS_ROOT:-}" ]]; then
  echo "Set BYTEPRESS_ROOT to the BytePress repository path before running integration-smoke.sh."
  exit 1
fi

SMOKE_SCRIPT="$BYTEPRESS_ROOT/Tools/bp_integration_smoke.py"
REPORT_PATH="$ROOT_DIR/Runtime/Integration_Smoke_Report.json"
if [[ ! -f "$SMOKE_SCRIPT" ]]; then
  echo "BytePress integration smoke script not found at: $SMOKE_SCRIPT"
  exit 1
fi

python3 "$SMOKE_SCRIPT" --repo "$ROOT_DIR" --report "$REPORT_PATH"
echo "Integration smoke report written to: $REPORT_PATH"
