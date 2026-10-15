#!/usr/bin/env bash
# OG-ap-18 Phase A v3: the NO-UPLOAD DRY READ of deploy-to-ec2.sh's naming step (issuer msg 34290,
# Z-S132 ruled). Runs the SCRIPT'S OWN BYTES for that step -- extracted by line range from the release
# tree's own copy, never retyped -- so it exercises the two address() command substitutions AND the two
# `case` shape guards that a hand-written python call does not reach. Nothing is uploaded, no SSM
# command is sent, no artifact is built: the extracted span ends before the script's first write.
#
# THREE ARMS, because the first version of this check asserted the WRONG MECHANISM and failed itself.
# The script fails closed two different ways and only one of them is the `case` guard:
#
#   POSITIVE        the release worktree, whose cone now carries infra/logic -> both roots resolve.
#   NEGATIVE-IMPORT a WORKSPACE_ROOT with no lib/ -> python raises, and because the span runs under
#                   `set -euo pipefail` the ASSIGNMENT itself aborts the script. The `case` guard never
#                   runs. So the guard is UNREACHABLE for the registry/import failure its own comment
#                   credits ("fail closed ... if it is empty") -- the fail-closed property holds, but
#                   via set -e, not via the guard. This is the exact shape of the Z-S132 refusal.
#   NEGATIVE-SHAPE  a WORKSPACE_ROOT carrying a stub lib/opal_naming.py whose address() SUCCEEDS and
#                   returns a wrongly-shaped root -> python exits 0, so the script survives to the
#                   `case` and the guard is the thing that refuses. This is the only arm that proves
#                   the guard works at all.
#
# Without the third arm, a reader would credit the guard for a refusal set -e produced.
#
# Usage: bash <this file> <release worktree abs path>
set -uo pipefail

WT="${1:?usage: gt3_naming_dryread.sh <release worktree>}"
SCRIPT="$WT/infra/aws/ec2/opal-gateway/deploy-to-ec2.sh"
[ -f "$SCRIPT" ] || { echo "ERROR: no deploy script at $SCRIPT"; exit 2; }

# The naming step's span, located by its own anchors rather than by hardcoded line numbers: a pinned
# number goes stale the moment the script is edited, and THIS RELEASE edits that very file.
FIRST=$(grep -n 'ADVI_FEE_STATEMENT_S3_ROOT="\$(cd' "$SCRIPT" | head -1 | cut -d: -f1)
LAST=$(awk 'NR>'"$FIRST"' && /^esac$/ {n++; if (n==2) {print NR; exit}}' "$SCRIPT")
[ -n "$FIRST" ] && [ -n "$LAST" ] || { echo "ERROR: could not locate the naming span (first=$FIRST last=$LAST)"; exit 2; }
echo "OK: naming span located at lines $FIRST-$LAST of the release tree's own deploy-to-ec2.sh"
echo "    span sha256: $(sed -n "${FIRST},${LAST}p" "$SCRIPT" | sha256sum | cut -c1-16)"

SPAN=$(mktemp)
EMPTY=$(mktemp -d)
STUB=$(mktemp -d)
trap 'rm -f "$SPAN"; rm -rf "$EMPTY" "$STUB"' EXIT

{ echo 'set -euo pipefail'
  sed -n "${FIRST},${LAST}p" "$SCRIPT"
  echo 'echo "FEE_ROOT=$ADVI_FEE_STATEMENT_S3_ROOT"'
  echo 'echo "MKT_ROOT=$ADVI_MARKET_UPDATE_S3_ROOT"'
} > "$SPAN"

# The shape-arm stub: address() SUCCEEDS so the script reaches the `case`. Lives in a temp dir only.
mkdir -p "$STUB/lib"
cat > "$STUB/lib/opal_naming.py" <<'PY'
def address(*a, **k):
    # Deliberately NOT a /bronze/<table>/ root: the point is to reach the shape guard with a 0 exit.
    return "s3://not-a-real-root/wrong/shape/quarter=X"
PY
: > "$STUB/lib/__init__.py"

run_arm() {   # label, WORKSPACE_ROOT
  local label="$1" root="$2" out rc
  out=$(WORKSPACE_ROOT="$root" bash "$SPAN" 2>&1); rc=$?
  echo "--- arm $label rc=$rc"
  printf '%s\n' "$out" | sed 's/\x1b\[[0-9;]*m//g' | sed 's/^/      /'
  ARM_RC=$rc; ARM_OUT=$out
}

fail=0
ok()  { echo "OK: $1"; }
bad() { echo "ERROR: $1"; fail=1; }

run_arm POSITIVE "$WT"
if [ "$ARM_RC" -eq 0 ] \
   && printf '%s' "$ARM_OUT" | grep -q 'FEE_ROOT=s3://.*/bronze/fee_statement/$' \
   && printf '%s' "$ARM_OUT" | grep -q 'MKT_ROOT=s3://.*/bronze/market_update/$'; then
  ok "POSITIVE -- both roots resolved through the builder and both shape guards passed"
else
  bad "POSITIVE arm did not resolve both roots (rc=$ARM_RC)"
fi

run_arm NEGATIVE-IMPORT "$EMPTY"
if [ "$ARM_RC" -ne 0 ] && ! printf '%s' "$ARM_OUT" | grep -q 'ROOT=s3://'; then
  if printf '%s' "$ARM_OUT" | grep -q 'ModuleNotFoundError\|FileNotFoundError'; then
    ok "NEGATIVE-IMPORT -- refused with exit $ARM_RC and no root escaped; the refusal came from the"
    echo "    failing substitution under set -euo pipefail, NOT from the case guard (which never ran)"
  else
    ok "NEGATIVE-IMPORT -- refused with exit $ARM_RC and no root escaped"
  fi
else
  bad "NEGATIVE-IMPORT did not refuse (rc=$ARM_RC) -- the POSITIVE arm would then prove nothing"
fi

run_arm NEGATIVE-SHAPE "$STUB"
if [ "$ARM_RC" -ne 0 ] \
   && printf '%s' "$ARM_OUT" | grep -q 'ADVI_FEE_STATEMENT_S3_ROOT is empty or does not end in' \
   && ! printf '%s' "$ARM_OUT" | grep -q 'FEE_ROOT=s3://'; then
  ok "NEGATIVE-SHAPE -- address() exited 0 with a wrong-shaped root and the CASE GUARD refused, exit $ARM_RC"
else
  bad "NEGATIVE-SHAPE did not reach the case guard (rc=$ARM_RC) -- the guard is untested"
fi

echo "    registry files visible in the cone: $(ls -A "$WT/infra/logic/registry" 2>/dev/null | wc -l) of 7"
echo "    no upload and no SSM send: the span ends at line $LAST, before the script's first write"
if [ "$fail" -eq 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
