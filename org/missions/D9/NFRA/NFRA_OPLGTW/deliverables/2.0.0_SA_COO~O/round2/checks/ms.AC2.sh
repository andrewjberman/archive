#!/usr/bin/env bash
# OPLGTW OG-m-1 AC2: the dispatch tally partitions a FRESH recount of the dispatcher's "Event:" lines over the
# recorded window, both by trigger source and by outcome (each class sum equals the recount).
. "$(dirname "$0")/_ms.sh"
read s e < <(python -c "
import json,sys
from datetime import datetime
r=json.load(open(sys.argv[1],encoding='utf-8'))['window']
p=lambda x:int(datetime.fromisoformat(x.replace('Z','+00:00')).timestamp()*1000)
print(p(r['start']),p(r['end']))" "$MS" | tr -d '\r')
MSYS_NO_PATHCONV=1 "$(pwd)/.tools/aws" logs filter-log-events --region us-east-1 --log-group-name /aws/lambda/advi-49f-gold-dispatch \
  --start-time "$s" --end-time "$e" --filter-pattern '"Event:"' --query 'events[].timestamp' --output json > "${TMPDIR:-/tmp}/ms2.$$.json" \
  || { echo "filter-log-events failed"; echo "RESULT: FAIL"; exit 1; }
python - "$MS" "$(native "${TMPDIR:-/tmp}/ms2.$$.json")" <<'PY'
import json,sys
rec=json.load(open(sys.argv[1],encoding='utf-8'))['dispatch']; fresh=len(json.load(open(sys.argv[2],encoding='utf-8')) or [])
n=int(rec['invocations']); src=sum(int(v) for v in rec['by_source'].values()); out=sum(int(v) for v in rec['by_outcome'].values())
print(f"fresh recount {fresh}; recorded invocations {n}; by_source sum {src}; by_outcome sum {out}")
ok= fresh>0 and n==fresh==src==out
print("RESULT: PASS" if ok else "RESULT: FAIL"); sys.exit(0 if ok else 1)
PY
rc=$?; rm -f "${TMPDIR:-/tmp}/ms2.$$.json"; exit $rc
