#!/usr/bin/env bash
# MP-pc-4 AC1 (FWD-22 U1, the READ; decomposition PC.1): the findings file exists and its one ```json block parses to
# {"sources": [...]}, where every source carries source, exposes, how_read, box_measured, claim and reason; claim is one of
# measured / inferred / absent; and the three things FWD-22 needs are each covered by at least one source (exposes holds
# "account", "limit_5h", "limit_weekly"). No credential value is in the file: 0 hits for an Anthropic key prefix, a JWT
# prefix, or a token-named field carrying a value.
. "$(dirname "$0")/_root.sh"
F="${MP_PC4_FILE:-org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/0.9.0_WK_NFRA_MCPORTAL~23/U1_CLAUDE_ACCOUNT_AND_LIMITS_SOURCES.md}"
[ -f "$F" ] || { echo "$F absent"; echo "RESULT: FAIL"; exit 1; }
v=$(python - "$F" <<'PY'
import json, re, sys
t = open(sys.argv[1], encoding="utf-8").read()
m = re.findall(r"```json\s*(\{.*?\})\s*```", t, re.S)
if len(m) != 1:
    print("json_blocks=%d covered=none bad_rows=n/a" % len(m)); sys.exit()
try:
    d = json.loads(m[0])
except Exception as e:
    print("json_blocks=1 parse=%s covered=none bad_rows=n/a" % type(e).__name__); sys.exit()
src = d.get("sources") or []
need = ("source", "exposes", "how_read", "box_measured", "claim", "reason")
bad = sum(1 for s in src if not isinstance(s, dict) or any(k not in s for k in need) or s.get("claim") not in ("measured", "inferred", "absent"))
cov = set()
for s in src:
    if isinstance(s, dict):
        e = s.get("exposes")
        cov.update(e if isinstance(e, list) else [e])
ok = [k for k in ("account", "limit_5h", "limit_weekly") if k in cov]
print("json_blocks=1 sources=%d bad_rows=%d covered=%s" % (len(src), bad, ",".join(ok) or "none"))
PY
)
sec=$(grep -cE 'sk-ant-[A-Za-z0-9]|eyJ[A-Za-z0-9_-]{20,}|"?(access|refresh)_?[Tt]oken"?\s*[:=]\s*"?[A-Za-z0-9_.-]{12,}' "$F")
echo "$v; credential-shaped hits=$sec"
if printf '%s' "$v" | grep -q 'json_blocks=1 sources=' && printf '%s' "$v" | grep -q 'bad_rows=0' \
   && printf '%s' "$v" | grep -q 'covered=account,limit_5h,limit_weekly' && [ "$sec" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
