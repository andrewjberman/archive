#!/usr/bin/env bash
# MX-s-19 AC1 (amendment A8, row Z-S101): the SCHEDULED-plane writer census reads 1 writer on ALL 4 BD silver tables.
# Writers counted, per table:
#   - each SSM document opal-bd-{transaction,realized,unrealized,allocation}-download whose $LATEST or DEFAULT content
#     still runs merge-daily-incremental, AND whose trigger Lambda has at least one ENABLED EventBridge rule targeting it.
#     A document with no known trigger Lambda is counted whenever it runs the merge (fail closed). The bound: an ad-hoc
#     `ssm send-command` can still run a document, so this grades the SCHEDULED plane, never reachability;
#   - bd-silver-merge, when an S3 notification on opal-data-bd targets it (it merges all 4 tables);
#   - bd-allocation-processor, when an S3 notification targets it (writes silver/allocations/).
# Round 6's s16.AC1.sh read document CONTENT only, so it could not see a rule disable (A2's whole PHASE B).
# S19_FIXTURE=<dir> reads the same files from <dir> instead of AWS (the planted control for the PASS arm, Z-S100).
. "$(dirname "$0")/_root.sh"
AWS="$(pwd)/.tools/aws"
if [ -n "$S19_FIXTURE" ]; then
  T="$S19_FIXTURE"
else
  T="${TMPDIR:-/tmp}/mx_s19_$$"; mkdir -p "$T"
  for d in transaction realized unrealized allocation; do
    for v in '$LATEST' '$DEFAULT'; do
      timeout 30 "$AWS" ssm get-document --name "opal-bd-$d-download" --document-version "$v" --query Content --output text > "$T/$d.$([ "$v" = '$LATEST' ] && echo latest || echo default).txt" 2>&1
    done
  done
  timeout 30 "$AWS" s3api get-bucket-notification-configuration --bucket opal-data-bd --output json > "$T/notif.json" 2>&1
  for fn in bd-transactions-trigger bd-realized-trigger; do
    arn=$(timeout 30 "$AWS" lambda get-function --function-name "$fn" --query Configuration.FunctionArn --output text 2>&1 | tr -d '\r')
    : > "$T/rules.$fn.txt"
    for r in $(timeout 30 "$AWS" events list-rule-names-by-target --target-arn "$arn" --query 'RuleNames[]' --output text 2>&1 | tr -d '\r'); do
      printf '%s %s\n' "$r" "$(timeout 30 "$AWS" events describe-rule --name "$r" --query State --output text 2>&1 | tr -d '\r')" >> "$T/rules.$fn.txt"
    done
  done
fi
out=$(python - "$(native "$T")" <<'EOF' 2>&1 | tr -d '\r'
import json, os, sys
d = sys.argv[1]
tables = {"transaction": "transactions", "realized": "realized", "unrealized": "unrealized", "allocation": "allocations"}
trigger = {"transaction": "bd-transactions-trigger", "realized": "bd-realized-trigger"}
w = {t: [] for t in tables.values()}
for doc, t in tables.items():
    runs = []
    for v in ("latest", "default"):
        txt = open(os.path.join(d, "%s.%s.txt" % (doc, v)), encoding="utf-8", errors="replace").read()
        if "error" in txt.lower()[:200] and "merge" not in txt:
            print("ERROR: get-document %s %s unreadable: %s" % (doc, v, txt[:120]))
            sys.exit(2)
        runs.append("merge-daily-incremental" in txt)
    if not any(runs):
        continue
    fn = trigger.get(doc)
    if fn is None:
        w[t].append("ssm:opal-bd-%s-download(latest=%s,default=%s,trigger=UNKNOWN)" % (doc, runs[0], runs[1]))
        continue
    lines = [l.split() for l in open(os.path.join(d, "rules.%s.txt" % fn), encoding="utf-8").read().splitlines() if l.strip()]
    if any(len(l) != 2 or l[1] not in ("ENABLED", "DISABLED") for l in lines):
        print("ERROR: rule read for %s unreadable: %s" % (fn, lines))
        sys.exit(2)
    enabled = [l[0] for l in lines if l[1] == "ENABLED"]
    print("trigger %s: %d rule(s) %s, %d ENABLED" % (fn, len(lines), [" ".join(l) for l in lines], len(enabled)))
    if enabled:
        w[t].append("ssm:opal-bd-%s-download(latest=%s,default=%s,rules_enabled=%s)" % (doc, runs[0], runs[1], enabled))
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
[ -n "$S19_FIXTURE" ] || rm -rf "$T"
printf '%s\n' "$out"
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
