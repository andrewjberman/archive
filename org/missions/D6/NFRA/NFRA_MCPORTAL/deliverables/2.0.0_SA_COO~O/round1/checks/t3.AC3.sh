#!/usr/bin/env bash
# MP-t-3 AC3 (A1n LIVE, the negative arms a worker can raise without a real owner session): the deployed writer, invoked
# (a) with no owner header and (b) with a self-signed forged header, answers {"verdict":"REFUSED"} with reasons
# NO-OWNER-HEADER and HEADER-UNVERIFIED respectively. (The non-owner and stale arms need a genuine ALB-signed header and
# are proven by the unit tests with an injected test key; the close run adds the owner's own write.)
. "$(dirname "$0")/_root.sh"
AWS="$(pwd)/.tools/aws"
nm=$(python -c "import sys;sys.path.insert(0,'.');import lib.opal_naming as n;print(n.name('mcportal', None, 'grant-writer', 'lambda'))" 2>&1 | tr -d '\r' | tail -1)
T="${TMPDIR:-/tmp}/mp_t3_ac3_$$"; mkdir -p "$T"
forged=$(python -c "
import base64, json
b = lambda d: base64.urlsafe_b64encode(json.dumps(d).encode()).rstrip(b'=').decode()
print(b({'alg':'ES256','kid':'00000000-0000-0000-0000-000000000000','typ':'JWT'}) + '.' + b({'email':'andrew@opalinvest.com','exp':9999999999}) + '.AAAA')")
TID='00000000-0000-4000-8000-0000000000e5'; OID='00000000-0000-4000-8000-0000000000f6'
p1="{\"action\":\"narrow\",\"tid\":\"$TID\",\"oid\":\"$OID\",\"candidate\":{}}"
p2="{\"action\":\"narrow\",\"tid\":\"$TID\",\"oid\":\"$OID\",\"candidate\":{},\"owner_header\":\"$forged\"}"
timeout 60 "$AWS" lambda invoke --function-name "$nm" --cli-binary-format raw-in-base64-out --payload "$p1" "$(cygpath -w "$T/r1.json")" >/dev/null 2>&1
timeout 60 "$AWS" lambda invoke --function-name "$nm" --cli-binary-format raw-in-base64-out --payload "$p2" "$(cygpath -w "$T/r2.json")" >/dev/null 2>&1
v() { python -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));print(d.get('verdict'),d.get('reason'))" "$1" 2>/dev/null || echo "NONE NONE"; }
a=$(v "$T/r1.json"); b=$(v "$T/r2.json"); rm -rf "$T"
echo "no header -> $a; forged header -> $b"
if [ "$a" = "REFUSED NO-OWNER-HEADER" ] && [ "$b" = "REFUSED HEADER-UNVERIFIED" ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
