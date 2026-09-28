#!/usr/bin/env bash
# OPLGTW OG-m-1 AC1: the recorded per-key PUT counts equal a fresh recount of object VERSIONS under
# s3://opal-data-assets/schwab/08335338/meta/complete/ whose LastModified falls inside the recorded window, key by key.
. "$(dirname "$0")/_ms.sh"
"$(pwd)/.tools/aws" s3api list-object-versions --bucket opal-data-assets --prefix schwab/08335338/meta/complete/ \
  --query 'Versions[].[Key,LastModified]' --output json > "${TMPDIR:-/tmp}/ms1.$$.json" || { echo "list-object-versions failed"; echo "RESULT: FAIL"; exit 1; }
python - "$MS" "$(native "${TMPDIR:-/tmp}/ms1.$$.json")" <<'PY'
import json,sys,collections
from datetime import datetime
rec=json.load(open(sys.argv[1],encoding='utf-8')); live=json.load(open(sys.argv[2],encoding='utf-8')) or []
p=lambda s: datetime.fromisoformat(s.replace('Z','+00:00'))
a,b=p(rec['window']['start']),p(rec['window']['end'])
fresh=collections.Counter(k for k,t in live if a<=p(t)<=b)
mine={k:int(v) for k,v in rec['markers']['per_key'].items()}
diff=sorted(k for k in set(fresh)|set(mine) if fresh.get(k,0)!=mine.get(k,0))
for k in diff[:20]: print(f"  {k}: recorded {mine.get(k,0)} fresh {fresh.get(k,0)}")
print(f"window {a.isoformat()}..{b.isoformat()}; versions listed {len(live)}; keys in window fresh {len(fresh)}, recorded {len(mine)}; keys differing {len(diff)}")
ok=bool(fresh) and not diff
print("RESULT: PASS" if ok else "RESULT: FAIL"); sys.exit(0 if ok else 1)
PY
rc=$?; rm -f "${TMPDIR:-/tmp}/ms1.$$.json"; exit $rc
