#!/usr/bin/env bash
# =============================================================================================
# *** SUPERSEDED 20260731T1355Z -- DO NOT RUN. THIS SCRIPT WOULD NOW REPORT A FALSE FAILURE. ***
# =============================================================================================
# Superseded by CVO 20260731T135324Z, ~25 min after I authored it. CTO found that IAM CANNOT
# EVALUATE "TODAY"; CVO then ruled (a)-deliberate + storage-layer integrity for BOTH principals,
# superseding CVO's OWN daily-apply ruling.
#
# THE SPECIFIC WAY THIS FILE IS NOW WRONG -- and it is wrong in the dangerous direction:
#   Invocation (2) below asserts DENY on {past-day}/text-input/ and treats an ALLOW as a floor
#   violation. Under the new ruling a **past-day ALLOW is EXPECTED AND DELIBERATE** -- the date
#   dimension is no longer the fence at all. So this script, run against a CORRECTLY applied
#   policy, prints "floor NOT satisfied" and reports a healthy boundary as broken.
#   **A FALSE FAILURE ON A CVO GATE IS NOT A SAFE ERROR** -- it manufactures pressure to "fix" a
#   policy that is right, which is how a correct fence gets widened.
#
# THE NEW BATTERY (CVO 135324Z) fences on PRINCIPAL and SUBFOLDER, not on date:
#   - per-principal ALLOWs, subfolder-scoped, ALL DATES (past-day ALLOW expected)
#   - CROSS-PRINCIPAL DENYs: runner DENIED on text-input/ and signed-review/; the writer role
#     denied on everything but text-input/  <- the discriminator lives here now
#   - STORAGE EXERCISES: (i) versioning enabled, verified LIVE; (ii) OVERWRITE MUTANT -- PutObject
#     twice on one key, version count must go 1->2 with the original intact; (iii) FALLBACK MUTANT
#     -- break the assume-role path, the write must FAIL LOUD (a success means ambient-credential
#     fallback, i.e. the role is decoration); (iv) manifest-hash detection against a deliberately
#     altered copy.
#
# WHY I AM NOT WRITING THE REPLACEMENT YET, deliberately: the floor has moved TWICE in ~20 minutes
# and step 3 now waits on **Andrew's step-0 yes/no** (writer-role creation, held by CTO as a
# distinct act). Authoring a third battery against an unsettled contract would just be re-derived
# again -- and a staged script frozen at authoring time firing a stale verdict is precisely the
# failure the 49F watch script already committed once. The replacement gets written when the
# principals exist and the contract stops moving.
#
# WHAT SURVIVES AND WAS RATIFIED: the DISCRIMINATOR PRINCIPLE in section (1) below -- if the
# expected-ALLOW case also denies, the battery is VOID AND UNRUNNABLE, never "all boundaries held."
# CVO ratified that permanently into the battery spec for every seat: at least one expected-ALLOW
# and one expected-DENY on the same principal, or the run proves nothing about either.
#
exit 99   # hard stop: refuses to run rather than emit a superseded verdict
# =============================================================================================
#
# ---- ORIGINAL CONTENT BELOW, PRESERVED UNEDITED FOR THE RECORD (do not resurrect piecemeal) ----
#
# STAGED -- DO NOT EXECUTE YET. Fires only AFTER hold (a) v2 step 3 (safe-apply) has LANDED.
#
# CVO hold (a) v2, STEP 4 of 6: the APPLIED IAM battery for the estate-report day-first storage contract.
# Executor: 0.7.0_AE_CloudOps~A -- assigned by 3.0.0_SA_CVO 20260731T133832Z as the INDEPENDENT executor.
# Author of the policy: 0.7.0_AE_CloudOps~B (steps 1-2, draft battery via simulate-custom-policy).
#
# WHY THE SPLIT: the author of a boundary must not be the one who exercises it for the lift. ~B authors
# and proves the DRAFT; I exercise the APPLIED object. CVO reads MY output and lifts their own hold.
# I do not lift the hold and I do not open the write path.
#
# ================== THE TRAP THIS SCRIPT EXISTS TO NOT FALL INTO ==================
# ~B found (and I independently re-derived, 20260731T134xZ) that the mid-key boundaries DID NOT EXIST:
#   APPLIED policy granted PutObject on daily/* manifest/* logs/* -- leading-prefix, RULING-8-superseded.
#   Bucket held exactly code/ daily/ logs/ manifest/. Key census: text-input=0, signed-review=0, daily=2
#   (the daily=2 is the POSITIVE CONTROL that makes the two zeros evidence rather than an empty query).
# Running simulate against THAT policy returns implicitDeny for every mid-key case -- TRUE BUT MEANINGLESS.
# It denies because NO GRANT OF ANY SHAPE EXISTS, not because a boundary held. Reported as a passing DENY
# it is A FALSE PASS ON A BOUNDARY THAT WAS NEVER BUILT. Section 0 below refuses to run in that state.

set -uo pipefail

ROLE_ARN="arn:aws:iam::313476888478:role/estate-report-runner-role"
ROLE_NAME="estate-report-runner-role"
POLICY_NAME="estate-report-runner"
BUCKET="opal-estate-report"
TODAY="${TODAY_OVERRIDE:-$(date -u +%Y-%m-%d)}"
PASTDAY="${PASTDAY_OVERRIDE:-$(date -u -d 'yesterday' +%Y-%m-%d)}"

echo "=== 0. PRECONDITION: the day-first contract must actually BE APPLIED. Verify, never assume. ==="
APPLIED="$(aws iam get-role-policy --role-name "$ROLE_NAME" --policy-name "$POLICY_NAME" \
             --query 'PolicyDocument' --output json 2>&1)"
echo "$APPLIED" | grep -q 'text-input' || {
  echo "*** STOP: the APPLIED policy contains no 'text-input' pattern."
  echo "*** Step 3 has NOT landed. Running the battery now would exercise the STALE object and every"
  echo "*** mid-key case would deny by GRANT-ABSENCE -- indistinguishable from a boundary holding."
  echo "*** This is the exact false-pass ~B caught. Do not proceed. Tell CVO."
  exit 1
}
echo "  day-first contract present in the APPLIED policy: OK"
echo "  APPLIED policy fingerprint (pin this beside any quoted verdict):"
echo "$APPLIED" | md5sum | awk '{print "    md5 " $1}'

echo "=== 0b. ACTION-NAME VALIDITY -- and NOT via simulate ==="
# simulate-principal-policy returns implicitDeny for a NONEXISTENT action, byte-identically to a real
# deny (exercised 2026-07-25: s3:ZzzNoSuchActionName9999 -> implicitDeny). So a typo in an action string
# is indistinguishable from a missing grant and sends you hunting a policy gap that does not exist.
# accessanalyzer validate-policy is the discriminating oracle.
cat > /tmp/_actchk.json <<'EOF'
{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Action":["s3:PutObject"],"Resource":"*"}]}
EOF
aws accessanalyzer validate-policy --policy-document file:///tmp/_actchk.json --policy-type IDENTITY_POLICY \
  --query "length(findings[?findingType=='ERROR'])" --output text
echo "  ^^ MUST be 0. Non-zero = my action string is bogus and every verdict below is meaningless."

echo
echo "=== THE FOUR-INVOCATION FLOOR (CVO-enumerated, 20260731T133832Z) ==="
echo "  ONE --resource-arns per invocation. 2+ ARNs in one call flips the HELD ones to implicitDeny,"
echo "  which would silently disarm the very control this hold rests on."
echo "  Each call is SEPARATE -- a control batched with its target is corrupted by its own presence."

sim () {  # $1 = label, $2 = exact resource ARN
  echo "--- $1"
  echo "    resource: $2"
  aws iam simulate-principal-policy \
    --policy-source-arn "$ROLE_ARN" \
    --action-names s3:PutObject \
    --resource-arns "$2" \
    --query 'EvaluationResults[0].EvalDecision' --output text
}

echo
echo "### (1) THE DISCRIMINATOR -- must be 'allowed'. Run FIRST and in ISOLATION."
D1=$(sim "ALLOW today/text-input" "arn:aws:s3:::${BUCKET}/${TODAY}/text-input/probe.jsonl")
echo "    -> $D1"

if [ "$D1" != "allowed" ]; then
  echo
  echo "*** BATTERY VOID -- NOT 'ALL BOUNDARIES HELD'. ***"
  echo "*** The ALLOW case did not return allowed. A typo'd role ARN, a malformed resource ARN, an"
  echo "*** unsatisfied Condition and a nonexistent action ALL return implicitDeny byte-identically."
  echo "*** With (1) failing I cannot distinguish 'the boundary holds' from 'my instrument is broken and"
  echo "*** failing closed' -- and the all-deny result would look CLEANER, not worse. That anti-correlation"
  echo "*** is the whole reason (1) is the discriminator and not merely the first case."
  echo "*** Report VOID to CVO. Do NOT report the denies below as a pass."
  exit 2
fi
echo "    INSTRUMENT DISCRIMINATES: it can return 'allowed' for this principal. Denies below are meaningful."

echo
echo "### (2) DENY past-day/text-input -- producer cannot rewrite history"
D2=$(sim "DENY pastday/text-input" "arn:aws:s3:::${BUCKET}/${PASTDAY}/text-input/probe.jsonl"); echo "    -> $D2"
echo "### (3) DENY today/signed-review -- the mid-key wildcard hazard proper"
D3=$(sim "DENY today/signed-review" "arn:aws:s3:::${BUCKET}/${TODAY}/signed-review/probe.json"); echo "    -> $D3"
echo "### (4) DENY past-day/manifest.json -- history rewrites through the INDEX even when objects are denied"
D4=$(sim "DENY pastday/manifest" "arn:aws:s3:::${BUCKET}/${PASTDAY}/manifest.json"); echo "    -> $D4"

echo
echo "=== REPORT FOR CVO -- raw verdicts + denominator, never a bare PASS ==="
echo "  DENOMINATOR: 4 of 4 floor cells exercised (all four run even where a deny holds trivially"
echo "               by grant-absence, per CVO's instruction)."
echo "  role      : $ROLE_ARN"
echo "  today     : $TODAY      past-day: $PASTDAY"
echo "  (1) ALLOW  {today}/text-input     -> $D1   [discriminator]"
echo "  (2) DENY   {past}/text-input      -> $D2"
echo "  (3) DENY   {today}/signed-review  -> $D3"
echo "  (4) DENY   {past}/manifest.json   -> $D4"
FAIL=0
[ "$D1" = "allowed" ] || FAIL=1
for d in "$D2" "$D3" "$D4"; do case "$d" in allowed) FAIL=1;; esac; done
if [ "$FAIL" -eq 0 ]; then
  echo "  VERDICT: floor SATISFIED on the APPLIED object. This is EVIDENCE FOR CVO, NOT A LIFT."
  echo "           CVO's read of this output lifts hold (a) v2. I do not lift it and I do not open the write path."
else
  echo "  VERDICT: floor NOT satisfied -- at least one cell returned the wrong decision. STOP, report to CVO."
fi
rm -f /tmp/_actchk.json
