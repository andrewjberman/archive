#!/usr/bin/env bash
# STAGED -- DO NOT RUN WITHOUT EXPLICIT DELETE AUTHORIZATION.
#
# ETFS Aug-1 clock: prove the REAL-CONTENT attach set through the DEPLOYED orchestrator,
# in a throwaway month prefix, then remove every object it created.
#
# Author: 0.7.0_AE_CloudOps~A, 2026-07-30. COO instruction 20260730T060255Z: "PREP IT, HOLD IT ...
# Do not seed anything until you have the word." Authorization routed to 1.0.0_SA_CTO~C, who
# sanctioned this same pattern for the predecessor's 9999-qa run.
#
# WHY IT NEEDS AUTHORIZATION AT ALL: step 4 DELETES S3 OBJECTS, which is on the
# human-confirmation list under Agent Autonomy. Seeding without a cleared cleanup would leave
# fixtures in a production bucket -- worse than not running it. Hence one motion, or none.
#
# WHY 9999-07 AND NOT 2026-07: an ad-hoc artifact under platinum/reports/2026-07/ would be
# ENUMERATED AND ATTACHED by the real Aug-1 run as production evidence. 9999-07 can never
# collide with a real month. NOTHING here touches 2026-07.
#
# WHY email_qa IS SEND-FREE: the deployed builder split (_build_report_email build-only;
# _email_report is the single send call site) makes mode=email_qa send-free BY CALL-GRAPH,
# not by a flag anyone can mis-set. Deployed 2026-07-29 @68661972ab, tag etfs-reports-v1.1.0.
#
# PRECONDITION -- regenerate the three REAL July CSVs locally first (writes ZERO S3 objects):
#   python <scratchpad>/exercise_write_month_csvs.py     # -> 3 files, verified 2026-07-30
# Then set SRC to the temp dir it printed.

set -euo pipefail

BUCKET="opal-data-etfs"
PREFIX="platinum/reports/9999-07"
FN="etfs-reports-orchestrator"
SRC="${1:?usage: $0 <dir-holding-the-3-real-july-csvs>}"

echo "=== 0. PRE-STATE: the fixture prefix MUST be empty before we start ==="
aws s3 ls "s3://${BUCKET}/${PREFIX}/" || echo "(empty -- expected)"

echo "=== 1. SEED: the 3 REAL July CSVs + a PDF stand-in, renamed to the 9999-07 month ==="
# The orchestrator verifies a PDF exists before it will build the email, so a stand-in is
# required for the build path to run at all. Renaming 202607 -> 999907 keeps the enumerator's
# {month} contract while guaranteeing no real-month key is written.
for f in "${SRC}"/opaletfs_*_202607.csv; do
  base="$(basename "$f")"
  aws s3 cp "$f" "s3://${BUCKET}/${PREFIX}/${base/202607/999907}" --content-type text/csv
done
aws s3 cp "${SRC}/etf_ownership_stub.pdf" "s3://${BUCKET}/${PREFIX}/etf_ownership.pdf" \
  --content-type application/pdf

echo "=== 2. THE PRODUCED-SET vs RENDER-LIST COMPARISON (COO's actual gate) ==="
echo "--- what is IN S3 (the render's file list) ---"
aws s3 ls "s3://${BUCKET}/${PREFIX}/" | tee /tmp/9999_07_in_s3.txt

echo "--- what the DEPLOYED orchestrator ATTACHES (send-free) ---"
aws lambda invoke --function-name "$FN" \
  --payload "$(printf '{"mode":"email_qa","month":"9999-07"}' | base64 -w0)" \
  --cli-binary-format base64 /tmp/9999_07_qa.json >/tmp/9999_07_invoke.meta 2>&1
cat /tmp/9999_07_invoke.meta
python -c "import json;d=json.load(open('/tmp/9999_07_qa.json'));print('mode:',d.get('mode'));print('month:',d.get('month'));print('ok:',d.get('ok'));print('ATTACHMENTS:');[print('   ',a) for a in d.get('attachments',[])]"

echo ">>> GATE: the attachment list MUST be exactly 1 PDF + 3 CSVs (4 total), and every CSV"
echo ">>> name MUST appear in the S3 listing above. A send rc is NOT the claim."
echo ">>> month MUST read 9999-07 -- if it reads 2026-06, the fixed -5 EST offset in"
echo ">>> _last_month() defaulted (only if 'month' failed to bind). Re-check the payload."

echo "=== 3. NEGATIVE CONTROL: an empty month must attach the PDF ONLY ==="
# Proves the enumerator is actually reading S3 rather than echoing a constructed list --
# without this, a hardcoded 3-CSV list would pass step 2 identically.
aws lambda invoke --function-name "$FN" \
  --payload "$(printf '{"mode":"email_qa","month":"9999-01"}' | base64 -w0)" \
  --cli-binary-format base64 /tmp/9999_01_qa.json >/dev/null 2>&1
python -c "import json;d=json.load(open('/tmp/9999_01_qa.json'));a=d.get('attachments',[]);print('EMPTY-MONTH attachments:',a);print('PASS: zero-CSV branch' if len(a)==1 else 'FAIL: expected PDF only, got %d'%len(a))"

echo "=== 4. CLEANUP -- THE AUTHORIZED DELETE, then PROVE the prefix is empty ==="
aws s3 rm "s3://${BUCKET}/${PREFIX}/" --recursive
echo "--- post-delete listing (MUST be empty; a non-empty listing here is a stranded fixture) ---"
aws s3 ls "s3://${BUCKET}/${PREFIX}/" && echo "*** FAIL: OBJECTS REMAIN -- escalate, do not retry blindly ***" || echo "OK: prefix empty (exit-1 on no-match is the empty proof)"

echo "=== 5. CONFIRM 2026-07 WAS NEVER TOUCHED (the whole point of using 9999-07) ==="
aws s3 ls "s3://${BUCKET}/platinum/reports/2026-07/" || echo "OK: 2026-07 still absent -- untouched, as intended"
