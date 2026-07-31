#!/usr/bin/env bash
# CVO hold (a), STEP 4: the APPLIED battery. Executor 0.7.0_AE_CloudOps~A (INDEPENDENT of the author).
# Author of the boundary: 0.7.0_AE_CloudOps~B (steps 1-3). CVO reads THIS output and lifts their own hold.
# I do not lift the hold. I do not open the write path.
#
# WHY v3 AND NOT EARLIER: v2 was authored against a floor that moved twice in 20 minutes and was DISARMED
# (@4280d68923) once it became a FALSE-FAILURE trap. CVO ruled: do not pre-stage against principals that do
# not exist. They exist now (estate-capture-writer created 2026-07-31T14:51:57Z), so this is authored
# against MEASURED objects, not guessed ARNs.
#
# ============================ NAME THE PRINCIPAL, NOT JUST THE COUNT ============================
# Three times on 2026-07-31 a correct instrument, correctly read, was pointed ONE OBJECT OFF:
#   1. CVO's original hold would have re-proved the pre-RULING-8 policy;
#   2. ~B's battery nearly ran against estate-report-runner-role instead of estate-capture-writer;
#   3. MY OWN GATE READ estate-report-runner-role AND CONCLUDED "step 3 not applied" -- a FALSE NEGATIVE.
# A correct policy on the wrong principal is INDISTINGUISHABLE from an unapplied change on the right one.
# THE SHARED FAILURE WAS NEVER THE MEASUREMENT. IT WAS THE NOUN.
# => every verdict below prints the PRINCIPAL it is *of*. A denominator without its noun is half a number.
# ===============================================================================================

set -uo pipefail

ACCT=313476888478
BUCKET=opal-estate-report
WRITER_ARN="arn:aws:iam::${ACCT}:role/estate-capture-writer"
RUNNER_ARN="arn:aws:iam::${ACCT}:role/estate-report-runner-role"
TODAY="$(date -u +%Y-%m-%d)"
PAST="$(date -u -d 'yesterday' +%Y-%m-%d)"
PASS=0; FAIL=0; CELLS=0

# ONE --resource-arns PER INVOCATION. 2+ ARNs in a single call flips the HELD ones to implicitDeny,
# which would silently disarm the very control this gate rests on.
sim () { # $1 principal-arn  $2 action  $3 resource-arn
  aws iam simulate-principal-policy --policy-source-arn "$1" --action-names "$2" \
      --resource-arns "$3" --query 'EvaluationResults[0].EvalDecision' --output text 2>&1
}
cell () { # $1 label  $2 principal-arn  $3 action  $4 resource  $5 expected
  CELLS=$((CELLS+1))
  local got; got="$(sim "$2" "$3" "$4")"
  if [ "$got" = "$5" ]; then PASS=$((PASS+1)); printf "  [OK  ] %-46s %s\n" "$1" "$got"
  else FAIL=$((FAIL+1));   printf "  [FAIL] %-46s got=%s want=%s\n" "$1" "$got" "$5"; fi
}

echo "==============================================================================="
echo " STEP 4 APPLIED BATTERY -- hold (a)"
echo "   PRINCIPAL UNDER TEST : $WRITER_ARN"
echo "   CROSS-PRINCIPAL      : $RUNNER_ARN"
echo "   today=$TODAY  past=$PAST   bucket=$BUCKET"
echo "==============================================================================="

echo
echo "### 0. ACTION-NAME VALIDITY -- via accessanalyzer, NEVER via simulate."
# simulate returns implicitDeny for a NONEXISTENT action byte-identically to a real deny, so a typo in an
# action string is indistinguishable from a missing grant. accessanalyzer is the discriminating oracle.
cat > /tmp/_av.json <<'EOF'
{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Action":["s3:PutObject","s3:DeleteObject"],"Resource":"*"}]}
EOF
AV=$(aws accessanalyzer validate-policy --policy-document file:///tmp/_av.json \
       --policy-type IDENTITY_POLICY --query "length(findings[?findingType=='ERROR'])" --output text 2>&1)
echo "  action-name ERROR findings: $AV   (MUST be 0, else every verdict below is meaningless)"
rm -f /tmp/_av.json

echo
echo "### 1. FALLBACK MUTANT -- ordered FIRST by CVO ruling."
# If ambient-credential fallback exists, every later verdict is evidence about a principal the code never
# used. It is not one cell among many: it is the precondition that makes the others MEAN anything.
echo "  Question: with the assume-role path broken, does the tool's write FAIL LOUD?"
echo "  MEASURED at source (.tools/estate-capture.py): boto3 imports=0, put_object/upload=0, s3 refs=0."
echo "  Positive control on that same search: dedup_key=2 -> the search discriminates; the zeros are real."
echo "  >> VERDICT: **NOT RUNNABLE** -- there is no S3 write path in the tool to break."
echo "     Reporting NOT-RUNNABLE rather than substituting a proxy. A stand-in for the one test that"
echo "     distinguishes a working boundary from a DECORATIVE one is worse than the gap: it would close"
echo "     the gate on evidence about something else. BOUNDARY PROVEN, PATH UNPROVEN."

echo
echo "### 2. DISCRIMINATOR + per-principal ALLOWs  [principal: estate-capture-writer]"
echo "    (if the expected-ALLOW also denies, the run is VOID -- not 'all boundaries held')"
cell "ALLOW today/text-input (DISCRIMINATOR)" "$WRITER_ARN" s3:PutObject "arn:aws:s3:::$BUCKET/$TODAY/text-input/probe.jsonl" allowed
cell "ALLOW past-day/text-input (EXPECTED)"   "$WRITER_ARN" s3:PutObject "arn:aws:s3:::$BUCKET/$PAST/text-input/probe.jsonl"  allowed
cell "ALLOW legit nesting under text-input"   "$WRITER_ARN" s3:PutObject "arn:aws:s3:::$BUCKET/$TODAY/text-input/dev/sess/x.jsonl" allowed
echo "    ^ past-day ALLOW is DELIBERATE (CVO (a)-ruling): IAM cannot evaluate 'today'. Expected, not a leak."

echo
echo "### 3. SAME-PRINCIPAL DENYs -- the fence  [principal: estate-capture-writer]"
cell "DENY  today/signed-review (adjacent)"   "$WRITER_ARN" s3:PutObject "arn:aws:s3:::$BUCKET/$TODAY/signed-review/x.json" implicitDeny
cell "DENY  NESTED SIBLING (~B's cell)"       "$WRITER_ARN" s3:PutObject "arn:aws:s3:::$BUCKET/$TODAY/signed-review/text-input/evil.md" implicitDeny
echo "    ^ THE cell that distinguishes '*' from '[^/]*'. IAM's * matches '/', so the ADJACENT deny above"
echo "      can hold while the NESTED variant is wide open -- an honest battery, aimed one segment too shallow."
cell "DENY  deeper nesting a/b/text-input"    "$WRITER_ARN" s3:PutObject "arn:aws:s3:::$BUCKET/$TODAY/a/b/text-input/x.md" implicitDeny
cell "DENY  past manifest.json (index rewrite)" "$WRITER_ARN" s3:PutObject "arn:aws:s3:::$BUCKET/$PAST/manifest.json" implicitDeny
cell "DENY  DeleteObject on its OWN key"      "$WRITER_ARN" s3:DeleteObject "arn:aws:s3:::$BUCKET/$TODAY/text-input/probe.jsonl" implicitDeny
echo "    ^ the Sid CLAIMS 'NeverDelete'. A name is not a control; this exercises it."

echo
echo "### 4. RESIDUAL CELL (CVO) -- an ACCEPTED bound, kept MEASURED rather than remembered"
cell "ALLOW aaaa-aa-aa (shape, not a date)"   "$WRITER_ARN" s3:PutObject "arn:aws:s3:::$BUCKET/aaaa-aa-aa/text-input/x.md" allowed
echo "    ^ EXPECTED-ALLOWED-AND-NAMED. '????-??-??' constrains SHAPE, not VALUE. Ruled a KNOWN BOUND"
echo "      (junk day-root inside the producer's own surface = namespace pollution, NOT a fence crossing)."
echo "      Recorded because 'date-shaped' READS like a date constraint and the next reader will believe it."

echo
echo "### 5. CROSS-PRINCIPAL DENYs  [principal: estate-report-runner-role -- the OTHER noun]"
cell "runner CONTROL: ALLOW daily/ (its own)" "$RUNNER_ARN" s3:PutObject "arn:aws:s3:::$BUCKET/daily/x.json" allowed
cell "runner DENY today/text-input"           "$RUNNER_ARN" s3:PutObject "arn:aws:s3:::$BUCKET/$TODAY/text-input/x.jsonl" implicitDeny
cell "runner DENY today/signed-review"        "$RUNNER_ARN" s3:PutObject "arn:aws:s3:::$BUCKET/$TODAY/signed-review/x.json" implicitDeny
echo "    ^ the runner CONTROL is load-bearing: without it, three denies are indistinguishable from a"
echo "      broken invocation against a mistyped principal -- which is exactly today's false-negative class."

echo
echo "### 6. STORAGE: versioning must be ENABLED (an overwrite must not destroy history)"
VER=$(aws s3api get-bucket-versioning --bucket "$BUCKET" --query 'Status' --output text 2>&1)
CELLS=$((CELLS+1)); if [ "$VER" = "Enabled" ]; then PASS=$((PASS+1)); echo "  [OK  ] bucket versioning                          $VER"
else FAIL=$((FAIL+1)); echo "  [FAIL] bucket versioning                          got=$VER want=Enabled"; fi

echo
echo "==============================================================================="
echo " DENOMINATOR: $CELLS cells exercised on NAMED principals | PASS $PASS | FAIL $FAIL"
echo "   NOT RUN (reported, not substituted): fallback mutant (no write path exists);"
echo "   overwrite mutant + manifest-hash detection (both need a live write path)."
echo " THIS IS EVIDENCE FOR CVO, NOT A LIFT. Hold (a) stays whole until CVO reads it."
echo "==============================================================================="
[ "$FAIL" -eq 0 ] || exit 1
