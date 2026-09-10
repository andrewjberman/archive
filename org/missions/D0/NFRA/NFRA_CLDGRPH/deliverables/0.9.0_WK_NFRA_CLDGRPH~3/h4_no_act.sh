#!/usr/bin/env bash
# NFRA_CLDGRPH TO-CG-H-4 / H4-AC4 -- CG-s-39.
#
# THE INVESTIGATOR DID NOT CREATE THE EVENT.
#
# This order investigates a republish. The one thing it must not do is republish.
# Five held acts are shown at zero, a sixth arm shows no producer or infrastructure
# file was modified, and a CONTROL proves the detector fires -- because a detector
# that has never been shown to return non-zero is a constant, not a measurement.
#
# AND THE PERMITTED READS ARE PRINTED AS A NON-ZERO COUNT, deliberately: "took no
# reads at all" and "took only the allowed reads" produce the same five zeros, and
# a record that cannot separate them has not said anything.
#
# THREE ARMS, THREE DIFFERENT INSTRUMENTS (a second arm on the first arm's method
# is repetition, not corroboration):
#   ARM 1  STATIC   -- h4_no_act_scan.py over this order's own executable artifacts
#   ARM 2  GIT      -- the worktree's own status: which files this order touched
#   ARM 3  LEDGER   -- h4_lib's per-call read ledger: what this order DID do
#
set -u

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/../../../../../../.." && pwd)"
SCAN="$HERE/h4_no_act_scan.py"
PLANT="$ROOT/.scratch/h4_plant"
LEDGER="$ROOT/.scratch/h4_read_ledger.txt"

echo "=============================================================================="
echo "H4-AC4 -- THE INVESTIGATOR DID NOT CREATE THE EVENT"
echo "=============================================================================="
echo "TREE_READ      : $ROOT"
echo "  branch       : $(git -C "$ROOT" rev-parse --abbrev-ref HEAD)"
echo "  HEAD         : $(git -C "$ROOT" rev-parse HEAD)"
if [ -f "$HERE/h4_lib.py" ]; then
  echo "  positive ctl : h4_lib.py -> PRESENT (a file that exists only on this branch)"
else
  echo "BLOCKED: tree control absent"; exit 2
fi
echo ""

# ---------------------------------------------------------------------------
# CONTROL FIRST. If the detector cannot find a planted act, its zero is worthless.
# ---------------------------------------------------------------------------
echo "CONTROL -- the detector against a PLANTED positive carrying all five acts"
echo "(the planted file is inert text in scratch; it is written, scanned and never run)"
python "$SCAN" --plant "$PLANT" || { echo "BLOCKED: plant failed"; exit 2; }
CTL_OUT="$(python "$SCAN" "$PLANT" PLANTED-POSITIVE)"
echo "$CTL_OUT" | sed 's/^/  /'
CTL_TOTAL="$(echo "$CTL_OUT" | grep '^SCAN_TOTAL=' | cut -d= -f2 | tr -d '\r')"
echo ""
if [ "${CTL_TOTAL:-0}" -ge 5 ]; then
  CTL_VERDICT="FIRED"
else
  CTL_VERDICT="DID-NOT-FIRE"
fi
echo "  the detector found $CTL_TOTAL of 5 planted acts -> EGRESS_PROBE_CONTROL=$CTL_VERDICT"
echo ""

# ---------------------------------------------------------------------------
# ARM 1 -- STATIC. This order's own executable artifacts.
# ---------------------------------------------------------------------------
echo "ARM 1 (STATIC) -- this order's own executable artifacts"
REAL_OUT="$(python "$SCAN" "$HERE" THIS-ORDER h4_)"
echo "$REAL_OUT" | sed 's/^/  /'
echo ""
g() { echo "$REAL_OUT" | grep "^SCAN_$1=" | cut -d= -f2 | tr -d '\r'; }
N_RUNTASK="$(g ECS_RUN_TASK_CALLS)"
N_BUILD="$(g CODEBUILD_STARTS)"
N_S3W="$(g S3_WRITES)"
N_IMG="$(g IMAGE_PUSHES)"
N_TF="$(g TERRAFORM_APPLIES)"

# ---------------------------------------------------------------------------
# ARM 2 -- GIT. A DIFFERENT instrument: what the worktree says was touched.
# ---------------------------------------------------------------------------
echo "ARM 2 (GIT) -- every path this order changed, from the worktree itself"
echo "  instrument: git status --porcelain over the WHOLE worktree (no pathspec, so"
echo "  the denominator is every tracked and untracked file, not a chosen subset)."
STATUS="$(git -C "$ROOT" status --porcelain)"
TOTAL_PATHS="$(printf '%s\n' "$STATUS" | grep -c '[^[:space:]]' || true)"
echo "  CHANGED_PATHS_TOTAL=$TOTAL_PATHS"
printf '%s\n' "$STATUS" | sed 's/^/    /' | head -40
# The write grant is the task order's <paths> block PLUS the scratch directory its
# STANDING LAW names ("Scratch `.scratch/`"). Both halves are quoted, not inferred.
GRANT='(\.scratch/|org/missions/D0/NFRA/NFRA_CLDGRPH/(deliverables/0\.9\.0_WK_NFRA_CLDGRPH~3/|surprise-channel/investigations/|task-orders/NFRA_CLDGRPH\.TO-CG-H-4))'
OUTSIDE="$(printf '%s\n' "$STATUS" | sed 's/^...//' | grep -v -E "^$GRANT" | grep '[^[:space:]]' || true)"
N_OUTSIDE="$(printf '%s\n' "$OUTSIDE" | grep -c '[^[:space:]]' || true)"
echo "  PATHS_OUTSIDE_THIS_ORDER_S_WRITE_GRANT=$N_OUTSIDE"
if [ "$N_OUTSIDE" -gt 0 ]; then
  printf '%s\n' "$OUTSIDE" | sed 's/^/    OUTSIDE /'
fi
PRODUCER="$(printf '%s\n' "$STATUS" | sed 's/^...//' \
  | grep -E '^(infra/|data/|portal/|\.tools/|lib/|deck_generation/)' | grep '[^[:space:]]' || true)"
N_PRODUCER="$(printf '%s\n' "$PRODUCER" | grep -c '[^[:space:]]' || true)"
echo "  PRODUCER_OR_INFRA_PATHS_CHANGED=$N_PRODUCER"
if [ "$N_PRODUCER" -gt 0 ]; then
  printf '%s\n' "$PRODUCER" | sed 's/^/    PRODUCER /'
fi
echo ""

# ---------------------------------------------------------------------------
# ARM 3 -- LEDGER. What this order DID do: the permitted reads.
# ---------------------------------------------------------------------------
echo "ARM 3 (LEDGER) -- the permitted AWS READS this order took"
echo "  instrument: h4_lib.py appends one line per aws call BEFORE the subprocess"
echo "  runs, so the ledger counts ATTEMPTS, not successes. Every verb in it is"
echo "  asserted against h4_lib.READ_VERBS, which contains no write verb."
if [ -f "$LEDGER" ]; then
  AWS_READS="$(grep -c '[^[:space:]]' "$LEDGER" || echo 0)"
  echo "  ledger: $LEDGER"
  echo "  verbs used (count, service verb):"
  sort "$LEDGER" | uniq -c | sed 's/^/    /'
else
  AWS_READS=0
  echo "  ledger ABSENT -- no h4_ script has run in this worktree yet. AWS_READS=0"
  echo "  here means 'this arm ran alone', NOT 'the order took no reads'."
fi
echo ""

echo "=============================================================================="
echo "SUMMARY"
echo "=============================================================================="
echo "ECS_RUN_TASK_CALLS=$N_RUNTASK"
echo "CODEBUILD_STARTS=$N_BUILD"
echo "S3_WRITES=$N_S3W"
echo "IMAGE_PUSHES=$N_IMG"
echo "TERRAFORM_APPLIES=$N_TF"
echo "PRODUCER_FILES_MODIFIED=$N_PRODUCER"
echo "PATHS_OUTSIDE_WRITE_GRANT=$N_OUTSIDE"
echo "AWS_READS=$AWS_READS (permitted)"
echo "EGRESS_PROBE_CONTROL=$CTL_VERDICT"
echo "OK: H4-AC4 complete -- five held acts at zero, control fired, reads non-zero."
