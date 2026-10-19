#!/usr/bin/env bash
# OPLGTW OG-ev-12 AC1 (round 45; row Z-W155-S1, ARMED; round-44 analysis item 1): WHO ANSWERED the organic per-identity 429 of 2026-10-18 about 19:2xZ that left no gw_ratelimit row in the lake? READ-ONLY; no product change.
# Record W/ORGANIC_429.json = {"body": {"code_sha": "<40 hex: the live ref read on the host>",
#   "organic_429_ts_range": {"from": "<iso>", "to": "<iso>"} (the CTO's connection refused at about 19:2xZ; narrow it from the journal or the lake if you can; say so in evidence),
#   "journal": {"source": "<journalctl command>", "first_access_line_ts": "<iso>", "window_end": "<iso>", "post_mcp_429_lines": n, "other_429_lines": n},
#   "lake": {"source": "<where counted>", "window_start": "2026-10-18T19:00:00Z", "window_end": "2026-10-18T20:00:00Z", "gw_ratelimit_rows": n, "suppressed_sum": n, "denominator": n (objects listed), "read_errors": 0},
#   "response_shape": {"guard_middleware_body_seen": true|false|null, "evidence": "<what the 429 answer looked like where it was read: this service answers {\"error\":\"rate_limited\",\"scope\":\"identity\"} with Retry-After; say what you could read of the other layers (the connector, a proxy, the ALB), read-only>"},
#   "throttle_rule": {"refusal_window_s": 10, "first_refusal_writes": true, "source": "app/ratelimit.py:<line>"},
#   "verdict": "THIS_SERVICE_WROTE_NOTHING|OTHER_LAYER|THROTTLED|UNDETERMINED", "evidence": ["<at least 2 strings>"]}}
# THE RULE, fixed before the run, in this order (the check recomputes it):
#   THIS_SERVICE_WROTE_NOTHING  if post_mcp_429_lines >= 1 and gw_ratelimit_rows == 0 (this service answered 429 and no row followed);
#   THROTTLED                   else if post_mcp_429_lines >= 1 and 1 <= gw_ratelimit_rows < post_mcp_429_lines (the per-key fold explains the difference);
#   OTHER_LAYER                 else if post_mcp_429_lines == 0 and the journal COVERS the 429 (first_access_line_ts <= organic_429_ts_range.from and organic_429_ts_range.to <= window_end) (a 429 this service's access log never saw);
#   UNDETERMINED                otherwise (the journal does not cover the time, or the lake leg is unreadable).
# Standing condition 3: `code_sha` is pinned; this check reads _REFUSAL_WINDOW_S in app/ratelimit.py AT that sha (git show) and requires the record's throttle_rule.refusal_window_s to equal it.
# The record carries no email, no principal, no account value and no token. Override (dry-run controls only): EV12_REC_OVERRIDE.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
REC="${EV12_REC_OVERRIDE:-org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/ORGANIC_429.json}"
[ -f "$REC" ] || { echo "ORGANIC_429.json absent"; echo "RESULT: FAIL"; exit 1; }
sha=$(python -I -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));b=d.get('body',d);print(b.get('code_sha',''))" "$(native "$REC")" | tr -d '\r')
git cat-file -e "${sha}^{commit}" 2>/dev/null || { echo "code_sha is not a commit here"; echo "RESULT: FAIL"; exit 1; }
winline=$(git show "$sha:$GW/app/ratelimit.py" | grep -E '^_REFUSAL_WINDOW_S *=' | head -1 | tr -d '\r')
res=$(WINLINE="$winline" SHA="$sha" python -I - "$(native "$REC")" <<'PYEOF'
import json, os, re, sys
raw = open(sys.argv[1], encoding="utf-8").read()
d = json.loads(raw); b = d.get("body", d)
isn = lambda v: isinstance(v, (int, float)) and not isinstance(v, bool) and v >= 0
j = b.get("journal") or {}; lk = b.get("lake") or {}; rs = b.get("response_shape") or {}; tr = b.get("throttle_rule") or {}; rng = b.get("organic_429_ts_range") or {}
m = re.search(r"=\s*([0-9.]+)", os.environ.get("WINLINE", ""))
want_w = float(m.group(1)) if m else None
j_ok = bool(j.get("source")) and bool(j.get("first_access_line_ts")) and bool(j.get("window_end")) and isn(j.get("post_mcp_429_lines")) and isn(j.get("other_429_lines"))
lk_ok = (bool(lk.get("source")) and lk.get("window_start") == "2026-10-18T19:00:00Z" and lk.get("window_end") == "2026-10-18T20:00:00Z" and isn(lk.get("gw_ratelimit_rows")) and isn(lk.get("suppressed_sum"))
         and isn(lk.get("denominator")) and lk["denominator"] > 0 and lk.get("read_errors") == 0)
rs_ok = (rs.get("guard_middleware_body_seen") in (True, False, None)) and bool(rs.get("evidence"))
tr_ok = want_w is not None and tr.get("refusal_window_s") == want_w and tr.get("first_refusal_writes") is True and bool(tr.get("source"))
rng_ok = bool(rng.get("from")) and bool(rng.get("to")) and rng["from"] <= rng["to"]
n429 = j.get("post_mcp_429_lines") or 0; rows = lk.get("gw_ratelimit_rows") or 0
covers = rng_ok and j_ok and j["first_access_line_ts"] <= rng["from"] and rng["to"] <= j["window_end"]
if n429 >= 1 and rows == 0: want = "THIS_SERVICE_WROTE_NOTHING"
elif n429 >= 1 and 1 <= rows < n429: want = "THROTTLED"
elif n429 == 0 and covers: want = "OTHER_LAYER"
else: want = "UNDETERMINED"
ev = b.get("evidence") or []
ev_ok = isinstance(ev, list) and len(ev) >= 2 and all(isinstance(x, str) and len(x) >= 8 for x in ev)
v_ok = b.get("verdict") in ("THIS_SERVICE_WROTE_NOTHING", "OTHER_LAYER", "THROTTLED", "UNDETERMINED") and b.get("verdict") == want
leak = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", raw)
bignums = re.findall(r"(?<![\d.-])\d{9,}(?![\d.-])", re.sub(r'"[0-9a-f]{40,64}"', '""', raw))
ok = j_ok and lk_ok and rs_ok and tr_ok and rng_ok and ev_ok and v_ok and not leak and not bignums
print("journal: 429 lines on POST /mcp %s, on other routes %s, first access line %s, window end %s: %s; lake 19:00Z to 20:00Z: gw_ratelimit rows %s (suppressed %s) over %s objects, read errors %s: %s" % (
      j.get("post_mcp_429_lines"), j.get("other_429_lines"), j.get("first_access_line_ts"), j.get("window_end"), "ok" if j_ok else "NOT OK", lk.get("gw_ratelimit_rows"), lk.get("suppressed_sum"), lk.get("denominator"), lk.get("read_errors"), "ok" if lk_ok else "NOT OK"))
print("throttle rule at the pinned code sha: refusal window %s s (the code at %s reads %s): %s; the journal covers the organic 429's time %s; verdict by the rule fixed before the run: %s, the record says %s: %s" % (
      tr.get("refusal_window_s"), os.environ.get("SHA", "")[:10], want_w, "ok" if tr_ok else "NOT OK", "yes" if covers else "no", want, b.get("verdict"), "consistent" if v_ok else "NOT consistent"))
print("response shape evidence present %s; evidence strings %d (want >= 2); email-shaped strings %d (want 0); digit runs of 9 or more %d (want 0)" % ("yes" if rs_ok else "NO", len(ev), len(leak), len(bignums)))
print("OK" if ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r')
printf '%s\n' "$res" | sed '$d'
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
