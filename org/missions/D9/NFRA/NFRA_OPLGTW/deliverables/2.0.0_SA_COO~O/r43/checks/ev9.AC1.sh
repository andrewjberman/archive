#!/usr/bin/env bash
# OPLGTW OG-ev-9 AC1 (round 43): the read-only trace of the gateway's per-identity limiter (Z-S177: this session's own opalgateway MCP connection failed with 429 rate_limited scope identity).
# The facts the record states are checked HERE against the code: app/config.py's RL_MCP_IDENTITY_LIMIT and RL_MCP_IDENTITY_WINDOW defaults, the key and the Retry-After header in app/server.py and app/ratelimit.py.
# Record W/LIMITER_TRACE.json = {"body": {"limiter": {"limit": n, "window_s": n, "key": "<what the bucket is keyed on>", "retry_after_header": true|false, "fail_mode": "open|closed", "source": ["<file>:<line>", ...]},
#   "identities_24h": {"source": "<where counted>"|null, "absent_reason": "<why not read>"|null, "denominator": n, "rows": [{"principal_hash": "<8 hex>", "refused": n, "client_keys": n}]},
#   "reconnect_path": {"retry_after_seconds_max": n, "client_retry_inside_window_rehits": "yes|no|unknown", "evidence": "<one line>"},
#   "recommendation": "<one paragraph; no change is made>"}}
# The record carries no email, no principal and no account value; principal_hash is at most 8 hex characters.
# Override (dry-run controls only): EV9_REC_OVERRIDE.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
REC="${EV9_REC_OVERRIDE:-org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~155/LIMITER_TRACE.json}"
[ -f "$REC" ] || { echo "LIMITER_TRACE.json absent"; echo "RESULT: FAIL"; exit 1; }
cfgline=$(grep -nE 'RL_MCP_IDENTITY_(LIMIT|WINDOW)' "$GW/app/config.py" | tr -d '\r')
res=$(CFG="$cfgline" python -I - "$(native "$REC")" <<'PYEOF'
import json, os, re, sys
d = json.load(open(sys.argv[1], encoding="utf-8")); b = d.get("body", d)
cfg = os.environ.get("CFG", "")
def default(name):
    m = re.search(name + r"[^\n]*?(?:,|\()\s*['\"]?(\d+(?:\.\d+)?)['\"]?\s*\)", cfg)
    return float(m.group(1)) if m else None
lim = b.get("limiter") or {}
want_limit, want_window = default("RL_MCP_IDENTITY_LIMIT"), default("RL_MCP_IDENTITY_WINDOW")
isn = lambda v: isinstance(v, (int, float)) and not isinstance(v, bool)
lim_ok = (isn(lim.get("limit")) and isn(lim.get("window_s")) and bool(lim.get("key")) and lim.get("retry_after_header") is True and lim.get("fail_mode") == "open"
          and isinstance(lim.get("source"), list) and len(lim["source"]) >= 2
          and (want_limit is None or float(lim["limit"]) == want_limit) and (want_window is None or float(lim["window_s"]) == want_window))
ids = b.get("identities_24h") or {}
rows = ids.get("rows") or []
rows_ok = all(isinstance(r, dict) and re.fullmatch(r"[0-9a-f]{1,8}", str(r.get("principal_hash", ""))) and isn(r.get("refused")) and r["refused"] >= 0 for r in rows)
ids_ok = rows_ok and ((ids.get("source") and isn(ids.get("denominator"))) or ids.get("absent_reason"))
rc = b.get("reconnect_path") or {}
rc_ok = isn(rc.get("retry_after_seconds_max")) and rc.get("client_retry_inside_window_rehits") in ("yes", "no", "unknown") and bool(rc.get("evidence"))
raw = open(sys.argv[1], encoding="utf-8").read()
leak = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", raw)
rec_ok = isinstance(b.get("recommendation"), str) and len(b["recommendation"]) >= 40
ok = lim_ok and ids_ok and rc_ok and rec_ok and not leak
print("limiter: limit %s per %s s (config defaults read here: %s per %s s), key %s, Retry-After header %s, fail mode %s, sources %s: %s" % (
      lim.get("limit"), lim.get("window_s"), want_limit, want_window, lim.get("key"), lim.get("retry_after_header"), lim.get("fail_mode"), len(lim.get("source") or []), "ok" if lim_ok else "NOT OK"))
print("identities in the last 24 hours: %s (denominator %s, rows %d, hashes of 8 hex or fewer: %s); reconnect path: max Retry-After %s s, a client retry inside the window re-hits %s: %s; email-shaped strings in the record %d (want 0)" % (
      ("counted from " + str(ids.get("source"))) if ids.get("source") else ("ABSENT: " + str(ids.get("absent_reason"))), ids.get("denominator"), len(rows), "yes" if rows_ok else "NO", rc.get("retry_after_seconds_max"), rc.get("client_retry_inside_window_rehits"), "ok" if rc_ok else "NOT OK", len(leak)))
print("OK" if ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r')
printf '%s\n' "$res" | sed '$d'
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
