#!/bin/bash
# =============================================================================
# OPAL_ASSETS.V2-5 -- the 22a IAM sweep over every monolith producer role.
# READ-ONLY: simulate-principal-policy evaluates policy; it writes nothing.
#
# 22a discipline, mechanically enforced by this script's shape:
#   * ONE --resource-arns per invocation (2+ ARNs flips HELD resources to
#     implicitDeny -- false-deny mode 1).
#   * Positive controls are SEPARATE invocations (a positive control run in the
#     same call as the target is disarmed by mode 1).
#   * --context-entries s3:prefix passed for every conditioned ListBucket
#     statement (an unevaluated Condition returns implicitDeny byte-identical
#     to a real deny -- false-deny mode 2). One deliberate no-context row per
#     conditioned statement is included, LABELED instrument-control, to show
#     the two modes apart in the record.
#
# Evidence: raw simulate JSON per block -> OPAL_ASSETS_V2-5_IAM_SWEEP_RAW_20260714/
# Re-runnable, idempotent, changes nothing.
# =============================================================================
set -u
WS="/c/Users/AndrewBerman/Desktop/ajb_workspace"
OUT="$WS/org/tier2_senior/0.7.0_AE_CloudOps/deliverables/OPAL_ASSETS_V2-5_IAM_SWEEP_RAW_20260714"
mkdir -p "$OUT"
ROLEPFX="arn:aws:iam::313476888478:role"
PASS=0; FAIL=0; TOTAL=0

run() {
  local id="$1" role="$2" action="$3" resource="$4" ctx="$5" ctype="$6" expect="$7" note="$8"
  TOTAL=$((TOTAL+1))
  if [ -n "$ctx" ]; then
    aws iam simulate-principal-policy \
      --policy-source-arn "$ROLEPFX/$role" \
      --action-names "$action" \
      --resource-arns "$resource" \
      --context-entries "ContextKeyName=s3:prefix,ContextKeyValues=$ctx,ContextKeyType=string" \
      --output json > "$OUT/$id.json" 2> "$OUT/$id.stderr"
  else
    aws iam simulate-principal-policy \
      --policy-source-arn "$ROLEPFX/$role" \
      --action-names "$action" \
      --resource-arns "$resource" \
      --output json > "$OUT/$id.json" 2> "$OUT/$id.stderr"
  fi
  local rc=$?
  local decision
  decision=$(python - "$OUT/$id.json" <<'PYEOF'
import json, sys
try:
    d = json.load(open(sys.argv[1]))
    rs = d.get("EvaluationResults", [])
    print(rs[0]["EvalDecision"] if rs else "NO-RESULT")
except Exception as e:
    print("PARSE-ERROR")
PYEOF
)
  local mark
  if [ "$rc" -ne 0 ]; then
    mark="CALL-ERROR"; FAIL=$((FAIL+1))
  elif [ "$decision" = "$expect" ]; then
    mark="MATCH"; PASS=$((PASS+1))
  else
    mark="MISMATCH"; FAIL=$((FAIL+1))
  fi
  printf '%-8s %-34s %-22s %-9s expect=%-12s got=%-12s %-9s [%s] %s\n' \
    "$id" "$role" "$action" "$ctype" "$expect" "$decision" "$mark" "${ctx:--}" "$note"
}

echo "=== V2-5 22a IAM SWEEP $(date -u +%Y-%m-%dT%H:%M:%SZ) -- one resource per call ==="
echo ""
echo "--- ROLE 1/5: opal-assets-ingest-router-role (channels: orion/inflection, eclipse/inflection, blackdiamond/cottonwood) ---"
R=opal-assets-ingest-router-role
run R01 $R s3:PutObject "arn:aws:s3:::opal-data-assets/orion/inflection/bronze/holdings/2026-07-14/sweep-probe.jsonl.gz" "" target allowed "own-tree write"
run R02 $R s3:PutObject "arn:aws:s3:::opal-data-assets/eclipse/inflection/bronze/accounts/2026-07-14/sweep-probe.jsonl.gz" "" target allowed "own-tree write"
run R03 $R s3:PutObject "arn:aws:s3:::opal-data-assets/blackdiamond/cottonwood/bronze/holdings/2026-07-14/sweep-probe.json" "" target allowed "own-tree write"
run R04 $R s3:GetObject "arn:aws:s3:::opal-data-assets/orion/inflection/bronze/holdings/2026-07-14/sweep-probe.jsonl.gz" "" positive allowed "read-back-verify grant, separate invocation"
run R05 $R s3:GetObject "arn:aws:s3:::opal-data-inf/bronze/2026-07-14/sweep-probe.json" "" target allowed "source bronze read"
run R06 $R s3:ListBucket "arn:aws:s3:::opal-data-inf" "bronze/2026-07-14/" conditioned allowed "conditioned list WITH context"
run R07 $R s3:ListBucket "arn:aws:s3:::opal-data-inf" "" instrument implicitDeny "SAME statement WITHOUT context -- false-deny mode 2 demonstrated, NOT a policy verdict"
run R08 $R s3:PutObject "arn:aws:s3:::opal-data-bd/bronze/sweep-negative-probe" "" negative explicitDeny "firm bucket -- fence belt 2"
run R09 $R s3:PutObject "arn:aws:s3:::opal-data-inf/gold/meta/pipeline-complete.json" "" negative explicitDeny "DOOR 6 key -- fence belt 3 (simulation only; nothing writes)"
run R10 $R s3:PutObject "arn:aws:s3:::opal-data-assets/schwab/08242234/bronze/sweep-negative-probe" "" negative implicitDeny "out-of-scope monolith prefix (no grant; fence excludes monolith)"
run R11 $R s3:DeleteObject "arn:aws:s3:::opal-data-assets/orion/inflection/bronze/sweep-negative-probe" "" negative implicitDeny "no delete grant on own tree (additive-only)"

echo ""
echo "--- ROLE 2/5: quartz-si2-spike-role (channels: schwab/08242234 + schwab/08335338 -- the box, write-only) ---"
Q=quartz-si2-spike-role
run Q01 $Q s3:PutObject "arn:aws:s3:::opal-data-assets/schwab/08242234/bronze/ACC/20260714/sweep-probe.zip" "" target allowed "0824 bronze write"
run Q02 $Q s3:PutObject "arn:aws:s3:::opal-data-assets/schwab/08335338/bronze/ACC/20260714/sweep-probe.zip" "" target allowed "0833 bronze write"
run Q03 $Q s3:PutObject "arn:aws:s3:::opal-data-assets/schwab/08242234/_ops/daily_pull/sweep-probe.json" "" target allowed "run-manifest write"
run Q04 $Q s3:ListBucket "arn:aws:s3:::opal-data-assets" "schwab/08242234/bronze/" conditioned allowed "skip-index list WITH context, separate invocation"
run Q05 $Q s3:ListBucket "arn:aws:s3:::opal-data-assets" "" instrument implicitDeny "SAME statement WITHOUT context -- false-deny mode 2, labeled"
run Q06 $Q s3:GetObject "arn:aws:s3:::opal-data-assets/schwab/08242234/bronze/sweep-probe.zip" "" negative implicitDeny "WRITE-ONLY invariant: box cannot read monolith data back"
run Q07 $Q s3:PutObject "arn:aws:s3:::opal-data-bd/bronze/sweep-negative-probe" "" negative explicitDeny "firm bucket -- DenyBdPlane"
run Q08 $Q s3:PutObject "arn:aws:s3:::opal-data-inf/gold/meta/pipeline-complete.json" "" negative explicitDeny "DOOR 6 -- covered by DenyInfPlane"
run Q09 $Q s3:PutObject "arn:aws:s3:::opal-data-assets/orion/inflection/bronze/sweep-negative-probe" "" negative implicitDeny "out-of-scope monolith prefix"
run Q10 $Q s3:PutObject "arn:aws:s3:::opal-data-assets/schwab/99999999/bronze/sweep-negative-probe" "" negative implicitDeny "INVENTED master -- masters-enumerated property (never-commingle)"

echo ""
echo "--- ROLE 3/5: opal-schwab-monolith-remap-role (schwab aux: one-time remap + pre-floor Glacier leg) ---"
M=opal-schwab-monolith-remap-role
run M01 $M s3:GetObject "arn:aws:s3:::opal-data-schwab/08242234/bronze/sweep-probe.zip" "" target allowed "staging source read"
run M02 $M s3:PutObject "arn:aws:s3:::opal-data-assets/schwab/08335338/bronze/sweep-probe.zip" "" target allowed "monolith target write"
run M03 $M s3:RestoreObject "arn:aws:s3:::opal-data-schwab/01_raw/CRS20230117.RLD" "" target allowed "pre-floor thaw (CTO-ruled; grant REMOVED at migration close)"
run M04 $M s3:GetObject "arn:aws:s3:::opal-data-schwab/01_raw/CRS20230117.RLD" "" target allowed "pre-floor read (H1 header master observation + tier-3 MD5)"
run M05 $M s3:ListBucket "arn:aws:s3:::opal-data-schwab" "08242234/bronze/" conditioned allowed "staging list WITH context, separate invocation"
run M06 $M s3:GetObject "arn:aws:s3:::opal-data-assets/schwab/08242234/bronze/sweep-probe.zip" "" negative implicitDeny "CANNOT read the monolith (verify-by-listing design)"
run M07 $M s3:DeleteObject "arn:aws:s3:::opal-data-schwab/01_raw/CRS20230117.RLD" "" negative implicitDeny "structurally incapable of deleting a byte"
run M08 $M s3:PutObject "arn:aws:s3:::opal-data-bd/bronze/sweep-negative-probe" "" negative explicitDeny "firm bucket -- DenyBdPlane"
run M09 $M s3:PutObject "arn:aws:s3:::opal-data-inf/gold/meta/pipeline-complete.json" "" negative explicitDeny "DOOR 6 -- covered by DenyInfPlane"
run M10 $M s3:GetObject "arn:aws:s3:::opal-data-schwab/backfill/sweep-negative-probe" "" negative implicitDeny "staging read scoped to master bronze + 01_raw only"

echo ""
echo "--- ROLE 4/5: etfs-netassets-daily-role (channels: trueshares [+pathfinder+msn scopes held]) ---"
E=etfs-netassets-daily-role
run E01 $E s3:PutObject "arn:aws:s3:::opal-data-assets/trueshares/DIVZ/bronze/netassets/2026-07-14/sweep-probe.json" "" target allowed "C4 first landing tonight 22:00Z -- pre-flight"
run E02 $E s3:PutObject "arn:aws:s3:::opal-data-assets/trueshares/IDVZ/bronze/netassets/2026-07-14/sweep-probe.json" "" target allowed "second fund scope"
run E03 $E s3:GetObject "arn:aws:s3:::opal-data-assets/trueshares/DIVZ/bronze/netassets/2026-07-14/sweep-probe.json" "" positive allowed "read-back-verify, separate invocation"
run E04 $E s3:ListBucket "arn:aws:s3:::opal-data-assets" "trueshares/DIVZ/bronze/" conditioned allowed "monolith list WITH context"
run E05 $E s3:PutObject "arn:aws:s3:::opal-data-etfs/bronze/netassets/2026-07-14/sweep-probe.json" "" target allowed "legacy-grammar bronze write (until cutover)"
run E06 $E s3:PutObject "arn:aws:s3:::opal-data-bd/bronze/sweep-negative-probe" "" negative implicitDeny "firm bucket -- NO fence on this role: no-grant only, recorded honestly"
run E07 $E s3:PutObject "arn:aws:s3:::opal-data-inf/gold/meta/pipeline-complete.json" "" negative implicitDeny "DOOR 6 -- NO explicit deny on this role: no-grant only, recorded honestly"
run E08 $E s3:PutObject "arn:aws:s3:::opal-data-assets/schwab/08242234/bronze/sweep-negative-probe" "" negative implicitDeny "out-of-scope monolith prefix"

echo ""
echo "--- ROLE 5/5: smartx-assets-pull-role (channel: smartx/* -- C5 pull engine) ---"
S=smartx-assets-pull-role
run S01 $S s3:PutObject "arn:aws:s3:::opal-data-assets/smartx/model/bronze/holdings/20260714/sweep-probe.json" "" target allowed "own-tree write"
run S02 $S s3:GetObject "arn:aws:s3:::opal-data-assets/smartx/model/bronze/holdings/20260714/sweep-probe.json" "" positive allowed "AC10 re-derive read, separate invocation"
run S03 $S s3:ListBucket "arn:aws:s3:::opal-data-assets" "smartx/model/bronze/" conditioned allowed "distinct-landing guard list WITH context"
run S04 $S s3:PutObject "arn:aws:s3:::opal-data-bd/bronze/sweep-negative-probe" "" negative implicitDeny "firm bucket -- NO fence on this role: no-grant only, recorded honestly"
run S05 $S s3:PutObject "arn:aws:s3:::opal-data-inf/gold/meta/pipeline-complete.json" "" negative implicitDeny "DOOR 6 -- NO explicit deny on this role: no-grant only, recorded honestly"
run S06 $S s3:PutObject "arn:aws:s3:::opal-data-assets/trueshares/DIVZ/bronze/sweep-negative-probe" "" negative implicitDeny "out-of-scope monolith prefix"
run S07 $S s3:PutObject "arn:aws:s3:::opal-data-smartx-v2/sweep-negative-probe" "" negative implicitDeny "old pipeline bucket -- no grant in this role"

echo ""
echo "=== SWEEP COMPLETE: $PASS/$TOTAL expectation-MATCH, $FAIL mismatch/error ==="
echo "raw evidence: $OUT/"
