#!/usr/bin/env bash
# _root.sh (round 2) -- reuse round 1's helpers (cd to the parent worktree root, pytest_named, ledger_closed, sim,
# ssm_run, opal_name, acct, native), then round-2 constants.
_R2_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. "$_R2_DIR/../../round1/checks/_root.sh"
R2="org/missions/D6/NFRA/NFRA_MCPMSP/deliverables"
MAIN="$(cd "$(git rev-parse --git-common-dir)/.." && pwd)"
# private terraform data dir: the main tree's providers + backend pointer, then `terraform get` (local modules only)
tf_private() {
  local pd; pd="$(mktemp -d "${TMPDIR:-/tmp}/ms_r2_tf.XXXXXX")"
  cp -r "$MAIN/$TF_DIR/.terraform/providers" "$pd/" 2>/dev/null && cp "$MAIN/$TF_DIR/.terraform/terraform.tfstate" "$pd/" 2>/dev/null || { echo ""; return 1; }
  local lz="infra/aws/lambda/layers/mcportal-grant-writer-deps/.build/mcportal-grant-writer-deps.zip"
  [ -f "$lz" ] || { mkdir -p "$(dirname "$lz")"; cp "$MAIN/$lz" "$lz" 2>/dev/null; }
  local st="infra/aws/lambda/mcportal/mcportal-grant-writer-lambda/.build/staged"
  [ -d "$st" ] || { [ -d "$MAIN/$st" ] && mkdir -p "$(dirname "$st")" && cp -r "$MAIN/$st" "$st"; }
  (export TF_DATA_DIR="$pd"; cd "$TF_DIR" && timeout 60 terraform get -no-color >/dev/null 2>&1)
  echo "$pd"
}
# naming gate over a whole file graded as an addition; prints "<gate line>|<paths in diff>"
naming_gate_file() {
  local d; d="$(mktemp "${TMPDIR:-/tmp}/ms_r2_ng.XXXXXX")"
  git diff --no-color --no-ext-diff --no-index /dev/null "$1" > "$d" 2>/dev/null
  local go; go=$(python .tools/naming-gate.py --diff "$d" 2>&1 | tr -d '\r'); rm -f "$d"
  printf '%s|%s\n' "$(printf '%s\n' "$go" | grep -m1 'NAMING-GATE:')" "$(printf '%s\n' "$go" | grep -oE 'DENOMINATOR: [0-9]+ path' | grep -oE '[0-9]+')"
}
