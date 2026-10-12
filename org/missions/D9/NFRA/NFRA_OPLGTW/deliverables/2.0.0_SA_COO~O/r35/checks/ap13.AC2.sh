#!/usr/bin/env bash
# OPLGTW OG-ap-13 AC2 (OG-tb-1's pair, COO condition A): at HEAD the source census no longer grants gateway/teams/bearer
# (decisions[...].granted is false), and exactly 30 PLATFORM-KEY names stay granted, so the next apply of the root agrees.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
f=infra/aws/terraform/nfra-ctlpln-identity/tests/vendor_secrets_census.json
tmp=$(mktemp); git show "HEAD:$f" >"$tmp" || { echo "census read FAILED"; echo "RESULT: FAIL"; exit 1; }
python - "$(native "$tmp")" <<'PY'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))["decisions"]
b = d.get("gateway/teams/bearer", {})
pk = [n for n, x in d.items() if x.get("granted") is True and x.get("class") == "PLATFORM-KEY" and x.get("kms_default") is True]
print("decisions %d; bearer granted=%s; PLATFORM-KEY granted (kms default) %d (want 30)" % (len(d), b.get("granted"), len(pk)))
raise SystemExit(0 if b and b.get("granted") is False and len(pk) == 30 else 1)
PY
rc=$?; rm -f "$tmp"
[ "$rc" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
