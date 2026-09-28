#!/usr/bin/env bash
# OPLGTW OG-m-1 AC3: every tracked non-test code file under data/ or infra/ that names the meta/complete/ prefix is in
# the record's writer census with a role, and every file classed "writer" carries a measured deployed-bytes state.
. "$(dirname "$0")/_ms.sh"
git grep -lE 'meta/complete' -- 'data/*.py' 'infra/*.py' 'infra/*.tf' 'infra/*.sh' 'data/*.sh' | grep -vE '/tests?/' > "${TMPDIR:-/tmp}/ms3.$$.txt"
python - "$MS" "$(native "${TMPDIR:-/tmp}/ms3.$$.txt")" <<'PY'
import json,sys
w={x['file']:x for x in json.load(open(sys.argv[1],encoding='utf-8'))['writers']}
files=[l.strip() for l in open(sys.argv[2],encoding='utf-8') if l.strip()]
miss=[f for f in files if f not in w]
norole=[f for f in files if f in w and w[f].get('role') not in ('writer','reader','config')]
unmeas=[f for f,x in w.items() if x.get('role')=='writer' and x.get('deployed_bytes') not in ('match','differs')]
for f in miss: print("  missing:",f)
for f in norole: print("  no role:",f)
for f in unmeas: print("  writer without measured deployed bytes:",f)
nw=sum(1 for x in w.values() if x.get('role')=='writer')
print(f"code files naming the prefix {len(files)}; in census {len(files)-len(miss)}; writers {nw}; missing {len(miss)}; no role {len(norole)}; writers unmeasured {len(unmeas)}")
ok= files and not miss and not norole and not unmeas and nw>=1
print("RESULT: PASS" if ok else "RESULT: FAIL"); sys.exit(0 if ok else 1)
PY
rc=$?; rm -f "${TMPDIR:-/tmp}/ms3.$$.txt"; exit $rc
