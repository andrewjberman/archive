#!/usr/bin/env bash
# OPLGTW OG-db-2 AC2 (round 40): the re-landed PREFLIGHT block runs and refuses, WITHOUT executing the rest of the deploy script.
#  - the block (from "# --- NFRA_OPLGTW OG-db-1" through the line printing PREFLIGHT OK) is extracted from HEAD's deploy-to-ec2.sh into a temp file;
#  - run alone with WORKSPACE_ROOT = this repo and --preflight-only it prints PREFLIGHT OK and exits 0 (the rest of the script is never run: nothing can be deployed);
#  - the control, WORKSPACE_ROOT = an empty folder (no git repo), REFUSES (non-zero exit, REFUSED printed) and prints no PREFLIGHT OK.
# DB2_SCRIPT_OVERRIDE (dry run only) names another file to extract from.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
F="${DB2_SCRIPT_OVERRIDE:-infra/aws/ec2/opal-gateway/deploy-to-ec2.sh}"
root="$(git rev-parse --show-toplevel | tr -d '\r')"
tmp="${TMPDIR:-/tmp}/_db2_block.$$"; mkdir -p "$tmp" "$tmp/empty"
if [ -n "$DB2_SCRIPT_OVERRIDE" ]; then cat "$F" > "$tmp/full.sh"; else git show "HEAD:$F" > "$tmp/full.sh"; fi
s=$(grep -n '^# --- NFRA_OPLGTW OG-db-1' "$tmp/full.sh" | head -1 | cut -d: -f1)
e=$(grep -n 'then echo "PREFLIGHT OK"' "$tmp/full.sh" | head -1 | cut -d: -f1)
if [ -z "$s" ] || [ -z "$e" ] || [ "$e" -lt "$s" ]; then
  echo "preflight block extracted: no (not found in ${F})"; rm -rf "$tmp"; echo "RESULT: FAIL"; exit 1
fi
{ echo 'set -euo pipefail'; sed -n "${s},${e}p" "$tmp/full.sh"; } > "$tmp/block.sh"
out_ok=$(WORKSPACE_ROOT="$root" timeout 60 bash "$tmp/block.sh" --preflight-only 2>&1 | tr -d '\r'); rc_ok=${PIPESTATUS[0]}
out_no=$(WORKSPACE_ROOT="$tmp/empty" timeout 60 bash "$tmp/block.sh" --preflight-only 2>&1 | tr -d '\r'); rc_no=${PIPESTATUS[0]}
okp=no; printf '%s' "$out_ok" | grep -q 'PREFLIGHT OK' && [ "$rc_ok" = 0 ] && okp=yes
refp=no; printf '%s' "$out_no" | grep -q 'REFUSED' && ! printf '%s' "$out_no" | grep -q 'PREFLIGHT OK' && [ "$rc_no" != 0 ] && refp=yes
echo "preflight block extracted: yes ($((e - s + 1)) lines); runs alone on this repo: PREFLIGHT OK rc=${rc_ok}: ${okp}; control (empty root) refuses: ${refp}"
rm -rf "$tmp"
restore_audit
[ "$okp" = yes ] && [ "$refp" = yes ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
