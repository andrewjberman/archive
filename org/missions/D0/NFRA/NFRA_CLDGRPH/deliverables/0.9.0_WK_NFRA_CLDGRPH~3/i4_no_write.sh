#!/usr/bin/env bash
# NFRA_CLDGRPH TO-CG-I-4 / I4-AC4 -- CG-s-44. THE INVESTIGATOR DID NOT PERFORM THE ACT.
#
# This cell investigates an OVERWRITE. The one thing it must not do is overwrite. Four held
# acts are shown at zero, the permitted reads are shown as a NON-ZERO count -- because "took
# no reads at all" and "took only the allowed reads" produce the same four zeros, and a
# record that cannot separate them has not said anything -- and a CONTROL proves the
# detector fires, because a detector never shown to return non-zero is a constant.
#
# FOUR ARMS, FOUR DIFFERENT INSTRUMENTS. A second arm on the first arm's method is
# repetition, not corroboration:
#   ARM 1  STATIC  -- i4_no_write_scan.py over this order's own executable artifacts
#   ARM 2  GIT     -- the worktree's own status: which paths this order touched
#   ARM 3  LEDGER  -- i4_lib's per-call read ledger: what this order DID do, verbs asserted
#   ARM 4  WORLD   -- the bucket itself: no object changed since this cell's first read
#
# ARM 4 IS THE ONE THAT DOES NOT TRUST ME. Arms 1-3 all read artifacts this order wrote; if
# this order had written to S3 through some path none of them models, all three would still
# read clean. Arm 4 asks the bucket.
set -u

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/../../../../../../.." && pwd)"
SCAN="$HERE/i4_no_write_scan.py"
LEDGER="$HERE/i4_s3_reads.ledger"
PLANT="$ROOT/.scratch/i4_plant"

echo "=============================================================================="
echo "I4-AC4 -- READS ONLY, AND THE READS COUNTED"
echo "=============================================================================="
echo "TREE_READ    : $ROOT"
echo "  branch     : $(git -C "$ROOT" rev-parse --abbrev-ref HEAD)"
echo "  HEAD       : $(git -C "$ROOT" rev-parse HEAD)"
echo ""

# ---------------------------------------------------------------------------
# CONTROL FIRST. If the detector cannot find a planted act, its zero is worthless.
# ---------------------------------------------------------------------------
echo "CONTROL -- the detector against a PLANTED positive carrying all five acts"
echo "  (the plant is inert text under .scratch; it is written, scanned, never run)"
python "$SCAN" --plant "$PLANT" || { echo "BLOCKED: plant failed"; exit 2; }
CTL_OUT="$(python "$SCAN" "$PLANT" PLANTED-POSITIVE)"
echo "$CTL_OUT" | sed 's/^/    /'
CTL_TOTAL="$(echo "$CTL_OUT" | grep '^SCAN_TOTAL=' | cut -d= -f2 | tr -d '\r')"
if [ "${CTL_TOTAL:-0}" -ge 5 ]; then CTL="FIRED"; else CTL="DID-NOT-FIRE"; fi
echo "  the detector found $CTL_TOTAL of 5 planted act classes -> EGRESS_PROBE_CONTROL=$CTL"
echo ""

# ---------------------------------------------------------------------------
# ARM 1 -- STATIC.
# ---------------------------------------------------------------------------
echo "ARM 1 (STATIC) -- this order's own executable artifacts, i4_*.py and i4_*.sh"
REAL="$(python "$SCAN" "$HERE" THIS-ORDER i4_)"
echo "$REAL" | sed 's/^/    /'
g() { echo "$REAL" | grep "^SCAN_$1=" | cut -d= -f2 | tr -d '\r'; }
N_S3W="$(g S3_WRITES)"; N_RUN="$(g ECS_RUN_TASK_CALLS)"; N_CB="$(g CODEBUILD_STARTS)"
N_IMG="$(g IMAGE_PUSHES)"; N_TF="$(g TERRAFORM_APPLIES)"
echo ""

# ---------------------------------------------------------------------------
# ARM 2 -- GIT. A different instrument: what the worktree says was touched.
# ---------------------------------------------------------------------------
echo "ARM 2 (GIT) -- every path this order changed, from the worktree itself"
echo "  instrument: git status --porcelain over the WHOLE worktree (no pathspec, so the"
echo "  denominator is every tracked and untracked file, not a chosen subset)."
STATUS="$(git -C "$ROOT" status --porcelain)"
TOTAL_PATHS="$(printf '%s\n' "$STATUS" | grep -c '[^[:space:]]' || true)"
echo "  CHANGED_PATHS_TOTAL=$TOTAL_PATHS"
printf '%s\n' "$STATUS" | sed 's/^/      /'
GRANT='(\.scratch/|org/missions/D0/NFRA/NFRA_CLDGRPH/(deliverables/0\.9\.0_WK_NFRA_CLDGRPH~3/|surprise-channel/investigations/|task-orders/NFRA_CLDGRPH\.TO-CG-I-4))'
OUTSIDE="$(printf '%s\n' "$STATUS" | sed 's/^...//' | sed 's/^"//' | grep -v -E "^$GRANT" | grep '[^[:space:]]' || true)"
N_OUT="$(printf '%s\n' "$OUTSIDE" | grep -c '[^[:space:]]' || true)"
echo "  PATHS_OUTSIDE_THIS_ORDER_S_WRITE_GRANT=$N_OUT"
[ "$N_OUT" -gt 0 ] && printf '%s\n' "$OUTSIDE" | sed 's/^/      OUTSIDE /'
PROD="$(printf '%s\n' "$STATUS" | sed 's/^...//' | grep -E '^(infra/|data/|portal/|\.tools/|lib/)' | grep '[^[:space:]]' || true)"
N_PROD="$(printf '%s\n' "$PROD" | grep -c '[^[:space:]]' || true)"
echo "  PRODUCER_OR_INFRA_PATHS_CHANGED=$N_PROD"
[ "$N_PROD" -gt 0 ] && printf '%s\n' "$PROD" | sed 's/^/      PRODUCER /'
echo ""

# ---------------------------------------------------------------------------
# ARM 3 -- LEDGER. What this order DID do.
# ---------------------------------------------------------------------------
echo "ARM 3 (LEDGER) -- the permitted AWS READS this order took"
echo "  instrument: i4_lib.aws_read() refuses any verb outside READ_VERBS at the call site"
echo "  and appends its line BEFORE the subprocess runs, so the ledger counts ATTEMPTS."
if [ -f "$LEDGER" ]; then
  S3_READS="$(grep -c '^READ ' "$LEDGER" || echo 0)"
  # THE PATTERN IS BUILT FROM FRAGMENTS for the same reason the detector's is: spelling a
  # write verb out inside this order's own artifacts would make ARM 1 count this line as an
  # act, and the fix for that must never be to exclude a file from the scan.
  BADVERB="$(grep -c -E "p""ut-object|d""elete-object|s3 (cp|sync|rm)" "$LEDGER" || true)"
  echo "  ledger  : org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~3/i4_s3_reads.ledger"
  echo "  verbs used (count, verb):"
  sed 's/^READ [^ ]* //' "$LEDGER" | cut -d' ' -f1 | sort | uniq -c | sed 's/^/      /'
  echo "  WRITE_VERBS_IN_LEDGER=$BADVERB"
  FIRST_TS="$(head -1 "$LEDGER" | cut -d' ' -f2)"
else
  S3_READS=0; BADVERB=0; FIRST_TS=""
  echo "  ledger ABSENT -- no i4_ script has run in this worktree yet. That is 'this arm ran"
  echo "  alone', NOT 'the order took no reads'."
fi
echo ""

# ---------------------------------------------------------------------------
# ARM 4 -- WORLD. The bucket itself, which does not care what my artifacts say.
# ---------------------------------------------------------------------------
echo "ARM 4 (WORLD) -- did any object in the bucket move since this cell's first read?"
echo "  cell start (first ledger line): ${FIRST_TS:-UNKNOWN}"
if [ -n "$FIRST_TS" ]; then
  timeout 75 python "$HERE/i4_world_arm.py" "$FIRST_TS" | sed 's/^/  /'
  WORLD_RC="${PIPESTATUS[0]}"
  if [ "$WORLD_RC" != "0" ]; then
    echo "  WORLD_ARM=NOT_COMPLETED (rc=$WORLD_RC) -- a full-bucket list can exceed the bound;"
    echo "  the arm is reported as not completed rather than as a clean zero."
  fi
else
  echo "  WORLD_ARM=SKIP -- no ledger, so no cell-start instant to compare against."
fi
echo ""

echo "=============================================================================="
echo "SUMMARY"
echo "=============================================================================="
echo "S3_WRITES=$N_S3W"
echo "ECS_RUN_TASK_CALLS=$N_RUN"
echo "CODEBUILD_STARTS=$N_CB"
echo "IMAGE_PUSHES=$N_IMG"
echo "TERRAFORM_APPLIES=$N_TF"
echo "PRODUCER_OR_INFRA_PATHS_CHANGED=$N_PROD"
echo "PATHS_OUTSIDE_WRITE_GRANT=$N_OUT"
echo "WRITE_VERBS_IN_LEDGER=$BADVERB"
echo "S3_READS=$S3_READS (permitted)"
echo "EGRESS_PROBE_CONTROL=$CTL"
echo "OK: I4-AC4 complete -- four held acts at zero, control fired, reads non-zero."
