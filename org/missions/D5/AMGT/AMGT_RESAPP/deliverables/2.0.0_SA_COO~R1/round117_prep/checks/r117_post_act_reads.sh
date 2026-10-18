#!/bin/bash
# AMGT_RESAPP round 117 (AMGT-bx-5): the ISSUER'S reads after SC1's apply, in one run. Read-only (Lambda invokes of GET routes and a config read).
#   bash r117_post_act_reads.sh <evidence_dir_suffix>        e.g. bash r117_post_act_reads.sh issuer-after
# It runs, in order, and prints one verdict line per step:
#   1 config          the function's CodeSha256, LastModified, RevisionId, memory, timeout, environment keys
#   2 capture         the eight live packs to <evidence>/r117-packs-<suffix>
#   3 form            r116_pack_form_check.py <before> <after>     (before = r116-packs-issuer-after, the live packs after the previous round)
#   4 money           r116_pack_money_vs_page.py                   (the live packs against the page's served figures, withheld rule)
#   5 negative arm    HD US and TSM US: their served ai_fill blocks carry no text, so their packs must carry NO `machine-drafted, cleared` line
#   6 timing          the print route for KMB US, RIO LN, GOOGL US, three runs each, against the CTO's 20 s bar
# It grades nothing by itself: the issuer reads the lines.
set -u
cd /c/Dev/ajb_workspace || exit 1
R=org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~R1
EV=C:/dev/ui-walk-evidence
SUF="${1:-issuer-after}"
echo "== 1 config"; python "$R/round114_prep/checks/r114_pack_capture_compare.py" config 2>&1 | grep -v "^warning"
echo "== 2 capture"; python "$R/round114_prep/checks/r114_pack_capture_compare.py" capture "$EV/r117-packs-$SUF" 2>&1 | tail -1
echo "== 3 form"; python "$R/round116_prep/checks/r116_pack_form_check.py" "$EV/r116-packs-issuer-after" "$EV/r117-packs-$SUF" 2>&1 | tee "$EV/r117-form-$SUF.txt" | grep -E "!!|LABELS|PACK FORM"
echo "== 4 money"; python "$R/round116_prep/checks/r116_pack_money_vs_page.py" 2>&1 | grep -v "^warning" | tee "$EV/r117-money-$SUF.txt" | grep -E "WITHHELD|DEDUPED|WRONG|MISSING|MONEY VS PAGE"
echo "== 5 negative arm (HD US, TSM US: no machine-written text served)"
for k in HD_US_Equity TSM_US_Equity; do
  n=$(grep -ci "machine-drafted, cleared" "$EV/r117-packs-$SUF/$k.txt")
  echo "$k machine-drafted lines: $n"
done
echo "== 6 timing"
python - <<'PY'
import boto3, json, time
L = boto3.client("lambda", region_name="us-east-1")
worst = 0.0
for key in ("KMB_US_Equity", "RIO_LN_Equity", "GOOGL_US_Equity"):
    ts = []
    for _ in range(3):
        ev = {"rawPath": "/api/scoped/amgt/security/%s/print" % key, "queryStringParameters": {"format": "pdf"},
              "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"}}
        t = time.time()
        r = json.loads(L.invoke(FunctionName="opal-amgt-scoped-api", Payload=json.dumps(ev).encode())["Payload"].read())
        ts.append((r["statusCode"], round(time.time() - t, 1)))
        worst = max(worst, ts[-1][1])
    print(key, ts)
print("TIMING: worst %.1f s against the 20 s bar (the Lambda timeout is 29 s)" % worst)
PY
