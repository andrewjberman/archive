#!/usr/bin/env bash
# MP-a-1 AC2 (A1n LIVE, the refusal arm and its record): the DEPLOYED writer, invoked with no owner header, answers
# {"verdict":"REFUSED","reason":"NO-OWNER-HEADER"}, and the writer's own table mcportal-grant-changes-table then holds at
# least one item carrying that verdict and reason (R-4: one record per outcome, a refusal included).
. "$(dirname "$0")/_root.sh"
AWS="$(pwd)/.tools/aws"
nm=$(python -c "import sys;sys.path.insert(0,'.');import lib.opal_naming as n;print(n.name('mcportal', None, 'grant-writer', 'lambda'))" 2>&1 | tr -d '\r' | tail -1)
tb=$(python -c "import sys;sys.path.insert(0,'.');import lib.opal_naming as n;print(n.name('mcportal', None, 'grant-changes', 'table'))" 2>&1 | tr -d '\r' | tail -1)
T="${TMPDIR:-/tmp}/mp_a1_ac2_$$"; mkdir -p "$T"
p='{"action":"narrow","tid":"00000000-0000-4000-8000-0000000000e5","oid":"00000000-0000-4000-8000-0000000000f6","candidate":{}}'
timeout 60 "$AWS" lambda invoke --function-name "$nm" --cli-binary-format raw-in-base64-out --payload "$p" "$(cygpath -w "$T/r.json")" >/dev/null 2>&1
v=$(python -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));print(d.get('verdict'),d.get('reason'))" "$T/r.json" 2>/dev/null || echo "NONE NONE")
# JSON arguments go through files: an inline JSON argument breaks on its quotes through the aws shim (round 1, t6.AC3).
python -c "import json,sys;json.dump({'#r':'reason'},open(sys.argv[1],'w'));json.dump({':r':{'S':'NO-OWNER-HEADER'}},open(sys.argv[2],'w'))" "$T/n.json" "$T/v.json"
cnt=$(timeout 60 "$AWS" dynamodb scan --table-name "$tb" --select COUNT --filter-expression "#r = :r" \
  --expression-attribute-names "file://$(cygpath -w "$T/n.json")" --expression-attribute-values "file://$(cygpath -w "$T/v.json")" \
  --query Count --output text 2>&1 | tr -d '\r' | tail -1)
rm -rf "$T"
case "$cnt" in ''|*[!0-9]*) cnt_n=0;; *) cnt_n=$cnt;; esac
echo "function $nm: no header -> $v; table $tb items with reason NO-OWNER-HEADER=$cnt"
if [ "$v" = "REFUSED NO-OWNER-HEADER" ] && [ "$cnt_n" -ge 1 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
