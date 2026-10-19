#!/usr/bin/env bash
# OPLGTW OG-ev-13 AC1 (round 46; Z-S402; round-45 analysis item 1): the audit lake leg re-read after a FULL DAY of production traffic. READ-ONLY; counts only; no product change.
# Record W/AUDIT_LEG_24H.json = {"body": {"window_start": "2026-10-19T07:44:53Z", "window_end": "<iso, at least 24 hours after window_start>", "code_sha": "<40 hex: the live ref read on the host, expected 6b1a9bd292855841826e194d0bddf9ac79bc8337>", "warn_every_s": 60,
#   "journal": {"source": "<journalctl command>", "first_line_ts": "<iso>", "warn_lines": n, "last_count": n (the last count= those lines print, 0 with none), "classes": ["<exception class name>", ...]},
#   "hours": [{"hour_start": "<iso on the hour>", "lake_objects": n, "post_mcp_lines": n}, ... 24 or 25 consecutive whole hours covering the window (a window that starts at :44 spans 25 buckets; both counts are taken over each WHOLE hour)],
#   "anomaly_hour": {"hour_start": "2026-10-19T02:00:00Z", "objects": n (the lake's count for that hour; about 2896 was listed), "read": n (bodies read), "read_errors": 0, "tools": [{"tool": "<name>", "n": n}], "explanation": "<one line>"},
#   "verdict": "HOLDS|FAILS_SEEN|UNDETERMINED", "evidence": ["<at least 2 strings>"]}}
# THE RULE, fixed before the run, in this order (the check recomputes it):
#   FAILS_SEEN    if journal.warn_lines >= 1 (a failed lake put was reported in the window);
#   HOLDS         else if EVERY hour with post_mcp_lines >= 20 has lake_objects >= 0.5 x post_mcp_lines (the lake keeps pace with the traffic);
#   UNDETERMINED  otherwise (an hour where the lake lags the journal with no WARN line, which is unexplained, or the journal does not reach the window start).
# Standing condition 3: `code_sha` is pinned; this check reads _LAKE_WARN_EVERY_S in app/audit.py AT that sha and requires the record's warn_every_s to equal it.
# The record carries no principal, email, account value or token. Override (dry-run controls only): EV13_REC_OVERRIDE.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
REC="${EV13_REC_OVERRIDE:-org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/AUDIT_LEG_24H.json}"
[ -f "$REC" ] || { echo "AUDIT_LEG_24H.json absent"; echo "RESULT: FAIL"; exit 1; }
sha=$(python -I -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));b=d.get('body',d);print(b.get('code_sha',''))" "$(native "$REC")" | tr -d '\r')
git cat-file -e "${sha}^{commit}" 2>/dev/null || { echo "code_sha is not a commit here"; echo "RESULT: FAIL"; exit 1; }
winline=$(git show "$sha:$GW/app/audit.py" | grep -E '^_LAKE_WARN_EVERY_S *=' | head -1 | tr -d '\r')
res=$(WINLINE="$winline" SHA="$sha" python -I - "$(native "$REC")" <<'PYEOF'
import datetime, json, os, re, sys
raw = open(sys.argv[1], encoding="utf-8").read()
d = json.loads(raw); b = d.get("body", d)
isn = lambda v: isinstance(v, (int, float)) and not isinstance(v, bool) and v >= 0
def ts(s):
    return datetime.datetime.fromisoformat(str(s).replace("Z", "+00:00"))
j = b.get("journal") or {}; hours = b.get("hours") or []; an = b.get("anomaly_hour") or {}
m = re.search(r"=\s*([0-9.]+)", os.environ.get("WINLINE", ""))
want_w = float(m.group(1)) if m else None
try:
    ws, we = ts(b.get("window_start")), ts(b.get("window_end"))
    win_ok = (we - ws).total_seconds() >= 86400 and b.get("window_start") == "2026-10-19T07:44:53Z"
except Exception:
    ws = we = None; win_ok = False
j_ok = bool(j.get("source")) and bool(j.get("first_line_ts")) and isn(j.get("warn_lines")) and isn(j.get("last_count")) and isinstance(j.get("classes"), list)
hours_ok = len(hours) in (24, 25) and all(isinstance(h, dict) and isn(h.get("lake_objects")) and isn(h.get("post_mcp_lines")) and h.get("hour_start") for h in hours)
if hours_ok:
    try:
        starts = [ts(h["hour_start"]) for h in hours]
        hours_ok = all((starts[i + 1] - starts[i]).total_seconds() == 3600 for i in range(len(starts) - 1)) and all(s.minute == 0 and s.second == 0 for s in starts) and ws is not None and starts[0] <= ws and starts[-1] + datetime.timedelta(hours=1) >= we
    except Exception:
        hours_ok = False
an_ok = (an.get("hour_start") == "2026-10-19T02:00:00Z" and isn(an.get("objects")) and an["objects"] >= 2000 and isn(an.get("read")) and an.get("read") == an.get("objects") and an.get("read_errors") == 0
         and isinstance(an.get("tools"), list) and len(an["tools"]) >= 1 and all(isinstance(t, dict) and t.get("tool") and isn(t.get("n")) for t in an["tools"]) and bool(an.get("explanation")))
an_sum_ok = an_ok and sum(t["n"] for t in an["tools"]) >= 0.95 * an["read"]
tr_ok = want_w is not None and b.get("warn_every_s") == want_w
warn = j.get("warn_lines") or 0
busy = [h for h in hours if isinstance(h, dict) and isn(h.get("post_mcp_lines")) and h["post_mcp_lines"] >= 20]
keeps = hours_ok and all(h["lake_objects"] >= 0.5 * h["post_mcp_lines"] for h in busy)
if warn >= 1: want = "FAILS_SEEN"
elif keeps and win_ok and j_ok: want = "HOLDS"
else: want = "UNDETERMINED"
ev = b.get("evidence") or []
ev_ok = isinstance(ev, list) and len(ev) >= 2 and all(isinstance(x, str) and len(x) >= 8 for x in ev)
v_ok = b.get("verdict") in ("HOLDS", "FAILS_SEEN", "UNDETERMINED") and b.get("verdict") == want
leak = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", raw)
bignums = re.findall(r"(?<![\d.-])\d{9,}(?![\d.-])", re.sub(r'"[0-9a-f]{40,64}"', '""', raw))
ok = win_ok and j_ok and hours_ok and an_sum_ok and tr_ok and ev_ok and v_ok and not leak and not bignums
print("window %s to %s (at least 24 hours, from the OG-ap-48 close): %s; journal: audit-lake WARN lines %s (last count %s, classes %s): %s" % (
      b.get("window_start"), b.get("window_end"), "ok" if win_ok else "NOT OK", j.get("warn_lines"), j.get("last_count"), j.get("classes"), "ok" if j_ok else "NOT OK"))
print("24 or 25 consecutive hourly rows %s, busy hours (20 or more POST /mcp lines) %d, the lake keeps pace in every busy hour %s; the throttle constant at the pinned sha reads %s and the record says %s: %s" % (
      "ok" if hours_ok else "NOT OK", len(busy), "yes" if keeps else "no", want_w, b.get("warn_every_s"), "ok" if tr_ok else "NOT OK"))
print("anomaly hour 2026-10-19T02:00Z: %s objects, %s read, errors %s, tool rows %d, histogram covers at least 95 percent of the bodies read: %s; verdict by the rule fixed before the run: %s, the record says %s: %s" % (
      an.get("objects"), an.get("read"), an.get("read_errors"), len(an.get("tools") or []), "ok" if an_sum_ok else "NOT OK", want, b.get("verdict"), "consistent" if v_ok else "NOT consistent"))
print("evidence strings %d (want >= 2); email-shaped strings %d (want 0); digit runs of 9 or more %d (want 0)" % (len(ev), len(leak), len(bignums)))
print("OK" if ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r')
printf '%s\n' "$res" | sed '$d'
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
