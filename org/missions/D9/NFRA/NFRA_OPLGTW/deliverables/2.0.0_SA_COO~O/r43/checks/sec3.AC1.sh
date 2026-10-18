#!/usr/bin/env bash
# OPLGTW OG-sec-3 AC1 (round 43): the SSRF audit of the gateway's outbound HTTP call sites, COMPLETED. OG-sec-1 (round 42) counted 18 sites with a pattern that missed the JWKS fetches (`PyJWKClient(`), which fetch a URL
# (identity.py lines 44 and 115, config-sourced; token_broker.py line 307, a tenant template). The denominator is measured HERE, by one pattern over the SIX modules (the five of OG-sec-1 plus token_broker.py):
# every matching line must appear in the record's sites, the matched count must be at least 20, and the verdict must follow from the rows (any `yes` means STOP).
# Record W/SSRF_AUDIT_R43.json = {"body": {"sites": [{"file", "line", "call", "target_source", "controllable": "yes|no", "reason"}], "controllable_yes": n, "verdict": "CLEAN|STOP"}}
# Override (dry-run controls only): SEC3_REC_OVERRIDE.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
REC="${SEC3_REC_OVERRIDE:-org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~153/SSRF_AUDIT_R43.json}"
[ -f "$REC" ] || { echo "SSRF_AUDIT_R43.json absent"; echo "RESULT: FAIL"; exit 1; }
APP="$GW/app"
PAT='(requests|httpx|urllib\.request|aiohttp|http\.client|session|client|_http|conn)[A-Za-z_.]*\.(get|post|put|delete|patch|request|head|urlopen)\(|urlopen\(|\.request\(|PyJWKClient\('
found=""
for f in identity.py graph.py token_broker.py integrations/ycharts/client.py integrations/globgrph/integration.py integrations/opal_portal/integration.py; do
  [ -f "$APP/$f" ] || { echo "module $f absent"; echo "RESULT: FAIL"; exit 1; }
  found="$found
$(grep -nE "$PAT" "$APP/$f" | cut -d: -f1 | sed "s|^|$f:|")"
done
res=$(FOUND="$found" python -I - "$(native "$REC")" <<'PYEOF'
import json, os, sys
d = json.load(open(sys.argv[1], encoding="utf-8")); b = d.get("body", d)
want = sorted(set(x.strip() for x in os.environ.get("FOUND", "").split("\n") if x.strip()))
sites = b.get("sites") or []
have = set()
bad = 0
for s in sites:
    if not isinstance(s, dict) or not isinstance(s.get("line"), int) or s.get("controllable") not in ("yes", "no") or not s.get("target_source") or not s.get("reason"):
        bad += 1; continue
    f = str(s.get("file", "")).replace(chr(92), "/")
    f = f.split("opal-gateway/app/")[-1]
    have.add("%s:%d" % (f, s["line"]))
missing = [w for w in want if w not in have]
jwks = [w for w in want if w.startswith("identity.py:") or w.startswith("token_broker.py:")]
yes = sum(1 for s in sites if isinstance(s, dict) and s.get("controllable") == "yes")
verdict_ok = b.get("controllable_yes") == yes and b.get("verdict") == ("STOP" if yes else "CLEAN")
ok = len(want) >= 20 and not missing and not bad and verdict_ok
print("call sites matched by the pattern in the six modules: %d (round 42 counted 18 in five; the JWKS fetches add identity.py x2 and token_broker.py x1); listed in the record: %d; matched lines missing from the record: %d (want 0); malformed rows: %d (want 0)" % (len(want), len(have), len(missing), bad))
print("controllable yes: %d; the record says %s and verdict %s: %s" % (yes, b.get("controllable_yes"), b.get("verdict"), "consistent" if verdict_ok else "INCONSISTENT"))
print("OK" if ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r')
printf '%s\n' "$res" | sed '$d'
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
