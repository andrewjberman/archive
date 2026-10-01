#!/usr/bin/env bash
# MX-s-16 AC1 (row Z-S69; round-5 analysis item 7): the LIVE writer census reads exactly 1 writer per BD silver table.
# Writers counted on the APPLIED plane:
#   - each SSM document opal-bd-{transaction,realized,unrealized,allocation}-download whose $LATEST AND DEFAULT content
#     still runs merge-daily-incremental (a document's merge writes its own table);
#   - bd-silver-merge, when an S3 notification on opal-data-bd targets it (its code merges all 4 tables, run(["all"]));
#   - bd-allocation-processor, when an S3 notification targets it (writes silver/allocations/).
. "$(dirname "$0")/_root.sh"
AWS="$(pwd)/.tools/aws"
T="${TMPDIR:-/tmp}/mx_s16_$$"; mkdir -p "$T"
for d in transaction realized unrealized allocation; do
  for v in '$LATEST' '$DEFAULT'; do
    timeout 30 "$AWS" ssm get-document --name "opal-bd-$d-download" --document-version "$v" --query Content --output text > "$T/$d.$([ "$v" = '$LATEST' ] && echo latest || echo default).txt" 2>&1
  done
done
timeout 30 "$AWS" s3api get-bucket-notification-configuration --bucket opal-data-bd --output json > "$T/notif.json" 2>&1
out=$(python - "$(native "$T")" <<'EOF' 2>&1 | tr -d '\r'
import json, os, sys
d = sys.argv[1]
tables = {"transaction": "transactions", "realized": "realized", "unrealized": "unrealized", "allocation": "allocations"}
w = {t: [] for t in tables.values()}
for doc, t in tables.items():
    runs = []
    for v in ("latest", "default"):
        txt = open(os.path.join(d, "%s.%s.txt" % (doc, v)), encoding="utf-8", errors="replace").read()
        if "error" in txt.lower()[:200] and "merge" not in txt:
            print("ERROR: get-document %s %s unreadable: %s" % (doc, v, txt[:120]))
            sys.exit(2)
        runs.append("merge-daily-incremental" in txt)
    if any(runs):
        w[t].append("ssm:opal-bd-%s-download(latest=%s,default=%s)" % (doc, runs[0], runs[1]))
try:
    n = json.load(open(os.path.join(d, "notif.json"), encoding="utf-8"))
except Exception as e:
    print("ERROR: bucket notification unreadable: %s" % e)
    sys.exit(2)
fns = [c.get("LambdaFunctionArn", "") for c in n.get("LambdaFunctionConfigurations", [])]
print("opal-data-bd Lambda notifications: %d" % len(fns))
if any(f.endswith(":bd-silver-merge") for f in fns):
    for t in w:
        w[t].append("lambda:bd-silver-merge")
if any(f.endswith(":bd-allocation-processor") for f in fns):
    w["allocations"].append("lambda:bd-allocation-processor")
bad = 0
for t, ws in w.items():
    print("%s %s: %d writer(s) %s" % ("OK:" if len(ws) == 1 else "NOT-ONE:", t, len(ws), ws))
    bad += len(ws) != 1
print("WRITER CENSUS: %d of %d BD silver tables have exactly 1 writer" % (len(w) - bad, len(w)))
sys.exit(0 if bad == 0 else 1)
EOF
); rc=$?
rm -rf "$T"
printf '%s\n' "$out"
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
