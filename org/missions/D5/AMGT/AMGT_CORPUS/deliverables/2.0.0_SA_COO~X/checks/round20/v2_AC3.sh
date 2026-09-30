#!/usr/bin/env bash
# AMGT_CORPUS round 20 -- check as a file: v2_AC3 -- the walker account is back at rest (disabled, no SSM parameter). Run from the repo root.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH="$(pwd)"
python .claude/skills/ui-walk/ui_walker_account.py status 2>&1 | grep -E '^STATUS' | tail -1
