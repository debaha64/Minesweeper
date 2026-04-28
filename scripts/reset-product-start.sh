#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPORT_DIR="$ROOT_DIR/Tools/.reports"
if [[ -d "$REPORT_DIR" ]]; then
  rm -rf "$REPORT_DIR"
  echo "Removed local tool reports: $REPORT_DIR"
else
  echo "No local tool reports to remove."
fi

if ! command -v git >/dev/null 2>&1; then
  echo "Git is not available; runtime cleanup completed, but tracked drift was not inspected."
  exit 0
fi

cd "$ROOT_DIR"
if ! git rev-parse --show-toplevel >/dev/null 2>&1; then
  echo "Tool report cleanup completed. Git repository is not initialized yet, so tracked drift was not inspected."
  exit 0
fi

STATUS_OUTPUT="$(git status --short)"
if [[ -z "$STATUS_OUTPUT" ]]; then
  echo "Working tree is clean after runtime cleanup."
  exit 0
fi

echo "Current git status after runtime cleanup:"
printf '%s
' "$STATUS_OUTPUT"

OUT_OF_GATE="$(printf '%s
' "$STATUS_OUTPUT" | awk '{print $2}' | grep -Ev '^(Docs/Discovery/|Plans/|Logs/)' || true)"
if [[ -n "$OUT_OF_GATE" ]]; then
  echo "Tracked or untracked drift exists outside the early analytical contour:"
  printf '%s
' "$OUT_OF_GATE"
  echo "Canonical reset route: discard this repo and materialize a fresh target with BytePress bootstrap."
  exit 1
fi

echo "Remaining drift is limited to Docs/Discovery, Plans, or Logs. Review those edits explicitly before continuing."
