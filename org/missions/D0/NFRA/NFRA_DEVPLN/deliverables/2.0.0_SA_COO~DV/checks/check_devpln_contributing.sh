#!/usr/bin/env bash
# org/missions/D0/NFRA/NFRA_DEVPLN/deliverables/2.0.0_SA_COO~DV/checks/check_devpln_contributing.sh -- NFRA_DEVPLN cell DP-b-4 acceptance checks (issuer-authored; the worker only runs it).
#   doc    : portal/CONTRIBUTING-BOXES.md carries the one-page convention (C-FEATURE, C-BRANCH, C-APPROVAL, C-CLASS pointers)
#   worker : .claude/agents/worker.md carries a short portal step that points at the doc
# Last line is the verdict: CONTRIBUTING-CHECK <mode> ok=True|False missing=<comma list>
# Git Bash default utilities only. Run from the workspace (or worktree) root.
set -u
MODE="${1:-}"
case "$MODE" in
  doc)
    F="portal/CONTRIBUTING-BOXES.md"
    NEEDLES='cand/<box>/<slug>|worktree add|last PROD release|open-calls.py add --kind approval|portal-merge-forward.sh|client-facing|opal-internal|test-only|on DEV until approved'
    MAXLINES=90
    ;;
  worker)
    F=".claude/agents/worker.md"
    NEEDLES='CONTRIBUTING-BOXES.md|cand/<box>/<slug>'
    MAXLINES=100000
    ;;
  *)
    echo "usage: check_devpln_contributing.sh doc|worker"; echo "CONTRIBUTING-CHECK ${MODE:-none} ok=False missing=mode"; exit 2 ;;
esac
if [ ! -f "$F" ]; then
  echo "CONTRIBUTING-CHECK $MODE ok=False missing=file:$F"; exit 1
fi
missing=""
IFS='|' read -r -a arr <<< "$NEEDLES"
for n in "${arr[@]}"; do
  grep -qF -- "$n" "$F" || missing="${missing:+$missing,}$n"
done
lines=$(wc -l < "$F" | tr -d ' ')
[ "$lines" -le "$MAXLINES" ] || missing="${missing:+$missing,}lines>$MAXLINES"
if [ "$MODE" = "doc" ]; then
  nonascii=$(LC_ALL=C grep -c -P '[^\x00-\x7F]' "$F" 2>/dev/null || true)
  [ "${nonascii:-0}" = "0" ] || missing="${missing:+$missing,}non-ascii"
fi
if [ -z "$missing" ]; then
  echo "CONTRIBUTING-CHECK $MODE ok=True missing=-"; exit 0
fi
echo "CONTRIBUTING-CHECK $MODE ok=False missing=$missing"; exit 1
