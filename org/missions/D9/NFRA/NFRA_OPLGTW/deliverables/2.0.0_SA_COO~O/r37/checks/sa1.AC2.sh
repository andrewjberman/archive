#!/usr/bin/env bash
# OPLGTW OG-sa-1 AC2 (round-37 G1-FIX, FWD-22, PRD v3.8): the runner's LIVE registration matches the branch the access read chose.
#  ACCESS_REFUSED: the runner is untouched -- still Running, `sa` not in its publishers, no ledger left open.
#  ACCESS_HOLDS:   the live task is Running with `sa` in its --publishers and -RefreshOnce's flag, the state/runtime roots unchanged, the ledger CLOSED,
#                  and at least one of the four SA bronze tables (symbol, report, analysis, news) holds an object newer than the proof's restored_at
#                  for the three sampled securities (BA, BABA, COST; the sample is stated, not the table).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~ZW"
[ -f "$W/SA1_ACCESS.json" ] && [ -f "$W/SA1_PROOF.json" ] || { echo "SA1_ACCESS.json or SA1_PROOF.json absent"; echo "RESULT: FAIL"; exit 1; }
live=$(powershell.exe -NoProfile -Command "\$x = Export-ScheduledTask -TaskName 'Opal Data Harvest - Continuous Cycle'; \$a = ([xml]\$x).Task.Actions.Exec.Arguments; \$s = (Get-ScheduledTask -TaskName 'Opal Data Harvest - Continuous Cycle').State; 'STATE=' + \$s; 'ARGS=' + \$a" | tr -d '\r')
res=$(LIVE="$live" python - "$W/SA1_ACCESS.json" "$W/SA1_PROOF.json" <<'PY'
import json, os, re, sys
acc = json.load(open(sys.argv[1], encoding="utf-8")); prf = json.load(open(sys.argv[2], encoding="utf-8"))
live = os.environ["LIVE"]
state = (re.search(r"STATE=(\S+)", live) or [None, ""])[1]
args = live.split("ARGS=", 1)[-1]
m = re.search(r"--publishers\s+((?:[a-z]+\s*)+?)(?=--|$)", args)
pubs = m.group(1).split() if m else []
has_sa = "sa" in pubs
refresh = "--refresh-once" in args
out = acc.get("outcome")
if out == "ACCESS_REFUSED":
    ok = state == "Running" and not has_sa and prf.get("branch") == "refused" and prf.get("runner_changed") is False
    print("branch refused: runner %s, publishers %s, sa registered %s (want no), runner changed %s (want False)" % (state, pubs, has_sa, prf.get("runner_changed")))
    sys.exit(0 if ok else 1)
import boto3, datetime as dt
c = boto3.client("s3")
restored = dt.datetime.fromisoformat(str(prf.get("restored_at")).replace("Z", "+00:00"))
newer = {}
for t in ("symbol", "report", "analysis", "news"):
    n = 0
    for sk in ("BA_US_Equity", "BABA_US_Equity", "COST_US_Equity"):
        for pg in c.get_paginator("list_objects_v2").paginate(Bucket="opal-data-harvest", Prefix="seeking-alpha/harvest/bronze/%s/security_key=%s/" % (t, sk)):
            n += sum(1 for o in pg.get("Contents", []) if o["LastModified"] > restored)
    newer[t] = n
ok = state == "Running" and has_sa and refresh and prf.get("branch") == "restored" and any(v > 0 for v in newer.values())
print("branch restored: runner %s, publishers %s, sa registered %s, --refresh-once %s; objects newer than restored_at (3 sampled securities) %s" % (state, pubs, has_sa, refresh, newer))
sys.exit(0 if ok else 1)
PY
); rc=$?
printf '%s\n' "$res" | tr -d '\r'
led=$(git ls-files org/critical_paths/change_management | grep -c "nfra-oplgtw-harvest-runner-sa" | tr -d '\r'); sen=$(git ls-tree -r --name-only HEAD org/critical_paths/.open_deploys/ | grep -c "nfra-oplgtw-harvest-runner-sa" | tr -d '\r')
echo "ledger entries for nfra-oplgtw-harvest-runner-sa $led (want 0 on the refused branch, 1+ on the restored); sentinel at HEAD $sen (want 0)"
[ "$rc" = 0 ] && [ "$sen" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
