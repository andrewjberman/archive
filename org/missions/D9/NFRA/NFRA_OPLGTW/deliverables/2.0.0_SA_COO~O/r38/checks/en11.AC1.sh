#!/usr/bin/env bash
# OPLGTW OG-en-11 AC1 (round 38, CTO msg 35014): the SERVED read of the 49F Black Diamond adapter names, per client tool, WHICH BUCKET it read.
# The record W/BD49F_SERVED.json = {"read_at": "<iso>", "live_commit": "<sha>", "method": "<one line>", "role_assumed": "<the role name the adapter's session carried>",
#  "tools": [{"tool": "client_get_holdings", "bucket": "<bucket of the first source key>", "bucket_class": "opal-data-bd|opal-data-assets|other|none",
#             "source_prefix": "<key prefix up to the table, no object date>", "partition_date": "<YYYY-MM-DD or null>", "rows": n, "note": "<one line>"}, ...], "finding": "<one line>"}
# At least the four tools holdings, transactions, allocation, fees; every tool has a bucket_class from the enum; no digit run of 8 or more, no e-mail address, no person key.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z"
[ -f "$W/BD49F_SERVED.json" ] || { echo "BD49F_SERVED.json absent"; echo "RESULT: FAIL"; exit 1; }
res=$(python - "$(native "$W/BD49F_SERVED.json")" <<'PYEOF'
import json, re, sys
raw = open(sys.argv[1], encoding="utf-8").read(); d = json.loads(raw)
tools = d.get("tools") or []
names = {t.get("tool") for t in tools if isinstance(t, dict)}
need = {"client_get_holdings", "client_get_transactions", "client_get_allocation", "client_get_fees"}
enum = {"opal-data-bd", "opal-data-assets", "other", "none"}
classes = [t.get("bucket_class") for t in tools if isinstance(t, dict)]
bad_class = sum(1 for c in classes if c not in enum)
bd = sum(1 for c in classes if c == "opal-data-bd"); assets = sum(1 for c in classes if c == "opal-data-assets")
runs = len(re.findall(r"(?<![\w*])\d{8,}(?![\w])", raw)); mails = len(re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", raw))
has = all(d.get(x) for x in ("read_at", "live_commit", "method", "role_assumed", "finding"))
print("49f bd served: tools %d of the 4 required present %s; bucket classes: opal-data-bd %d, opal-data-assets %d, bad class %d (want 0); fields present %s; digit runs of 8 or more %d (want 0); e-mail addresses %d (want 0)" % (len(tools), need <= names, bd, assets, bad_class, has, runs, mails))
print("OK" if need <= names and bad_class == 0 and has and runs == 0 and mails == 0 else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
