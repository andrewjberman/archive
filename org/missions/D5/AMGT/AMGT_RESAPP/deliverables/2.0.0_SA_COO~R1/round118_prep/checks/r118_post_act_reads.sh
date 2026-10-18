#!/bin/bash
# AMGT_RESAPP round 118 (AMGT-by-5): the ISSUER'S reads after SC1's apply, in one run. Read-only (Lambda invokes of GET routes and a config read).
#   bash r118_post_act_reads.sh <evidence_dir_suffix>        e.g. bash r118_post_act_reads.sh issuer-after
# Steps, one verdict line each:
#   1 config        CodeSha256, LastModified, RevisionId, memory, timeout, environment keys
#   2 capture       the eight live packs to <evidence>/r118-packs-<suffix>
#   3 form          r116_pack_form_check.py <before> <after> (before = r118-packs-after-cj4, the live packs before this act)
#   4 money         r116_pack_money_vs_page.py (the live packs against the page's served figures, withheld rule)
#   5 leak scan     r118_leak_scan.py live: every covered name's pack, a path / order id / vendor error / raw code anywhere
#   6 rich          the eight live rich exports to <evidence>/r118-rich-<suffix>, a grep for s3:// AMGT- NoSuchKey, and RIO LN's four withheld figures
#   7 timing        the print route (pdf and rich) for KMB US, RIO LN, GOOGL US, three runs each, against the CTO's 20 s bar
# It grades nothing by itself: the issuer reads the lines.
set -u
cd /c/Dev/ajb_workspace || exit 1
R=org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~R1
EV=C:/dev/ui-walk-evidence
SUF="${1:-issuer-after}"
echo "== 1 config"; python "$R/round114_prep/checks/r114_pack_capture_compare.py" config 2>&1 | grep -v "^warning"
echo "== 2 capture"; python "$R/round114_prep/checks/r114_pack_capture_compare.py" capture "$EV/r118-packs-$SUF" 2>&1 | tail -1
echo "== 3 form"; python "$R/round116_prep/checks/r116_pack_form_check.py" "$EV/r118-packs-after-cj4" "$EV/r118-packs-$SUF" 2>&1 | tee "$EV/r118-form-$SUF.txt" | grep -E "!!|LABELS|PACK FORM"
echo "== 4 money"; python "$R/round116_prep/checks/r116_pack_money_vs_page.py" 2>&1 | grep -v "^warning" | tee "$EV/r118-money-$SUF.txt" | grep -E "WITHHELD|DEDUPED|WRONG|MISSING|MONEY VS PAGE"
echo "== 5 leak scan (live, every covered name)"; PYTHONPATH=. python "$R/round118_prep/checks/r118_leak_scan.py" live "$EV/r118-leak-scan-$SUF.json" 2>&1 | grep -v "fitz\|^warning" | tail -6
echo "== 6 rich exports"; python "$R/round114_prep/checks/r114_pack_capture_compare.py" capture-rich "$EV/r118-rich-$SUF" 2>&1 | tail -1
for f in "$EV/r118-rich-$SUF"/*.md; do
  echo "$(basename "$f") s3=$(grep -c 's3://' "$f") amgt=$(grep -c 'AMGT-' "$f") vendor=$(grep -ci 'NoSuchKey\|Traceback\|botocore' "$f")"
done
echo "RIO LN rich, the four figures the page withholds:"; grep -E "^\| (CUR_MKT_CAP|NET_DEBT|CURR_ENTP_VAL|CRNCY_ADJ_MKT_CAP) " "$EV/r118-rich-$SUF/RIO_LN_Equity.md" | cut -c1-200
echo "== 7 timing"
python - <<'PY'
import boto3, json, time
L = boto3.client("lambda", region_name="us-east-1")
worst = 0.0
for fmt in ("pdf", "rich"):
    for key in ("KMB_US_Equity", "RIO_LN_Equity", "GOOGL_US_Equity"):
        ts = []
        for _ in range(3):
            ev = {"rawPath": "/api/scoped/amgt/security/%s/print" % key, "queryStringParameters": {"format": fmt},
                  "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"}}
            t = time.time()
            r = json.loads(L.invoke(FunctionName="opal-amgt-scoped-api", Payload=json.dumps(ev).encode())["Payload"].read())
            ts.append((r["statusCode"], round(time.time() - t, 1)))
            worst = max(worst, ts[-1][1])
        print(fmt, key, ts)
print("TIMING: worst %.1f s against the 20 s bar (the Lambda timeout is 29 s)" % worst)
PY
