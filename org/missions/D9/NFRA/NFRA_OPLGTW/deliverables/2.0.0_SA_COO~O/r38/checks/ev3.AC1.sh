#!/usr/bin/env bash
# OPLGTW OG-ev-3 AC1 (round 40 W1 measurement): WINDOW_MEASURE.json is complete and self-consistent.
#  - tables transactions and fees: files_read equals partitions (the FULL window was read), runs >= 5, p50 <= p95 <= max of the run walls, every wall > 0, bytes > 0;
#  - the request budget: alb_idle_timeout_seconds 60, inside_threshold_seconds 30; verdict is "inside" if and only if the worst p95 of the two tables <= 30;
#  - concurrency is 16; no content: only ints, floats, booleans and the fixed words; no digit run of 9 or more; no e-mail.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
REC="${EV3_REC_OVERRIDE:-org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/WINDOW_MEASURE.json}"
[ -f "$REC" ] || { echo "WINDOW_MEASURE.json is absent"; echo "RESULT: FAIL"; exit 1; }
res=$(python - "$(native "$REC")" <<'PYEOF'
import json, re, sys
raw = open(sys.argv[1], encoding="utf-8").read()
d = json.loads(raw)
b = d.get("body", d)
tabs = b.get("tables") or {}
lines, ok, p95s = [], True, []
for name in ("transactions", "fees"):
    t = tabs.get(name) or {}
    walls = t.get("wall_seconds") or []
    good = (isinstance(t.get("partitions"), int) and t["partitions"] >= 2 and t.get("files_read") == t.get("partitions")
            and len(walls) >= 5 and all(isinstance(w, (int, float)) and w > 0 for w in walls)
            and isinstance(t.get("p50"), (int, float)) and isinstance(t.get("p95"), (int, float))
            and 0 < t["p50"] <= t["p95"] <= max(walls) + 1e-9 and min(walls) - 1e-9 <= t["p50"]
            and isinstance(t.get("bytes"), int) and t["bytes"] > 0)
    ok = ok and good
    if isinstance(t.get("p95"), (int, float)):
        p95s.append(t["p95"])
    lines.append("%s: partitions %s, files read %s, runs %d, p50 %s s, p95 %s s, bytes %s" % (
        name, t.get("partitions"), t.get("files_read"), len(walls), t.get("p50"), t.get("p95"), t.get("bytes")))
rb = b.get("request_budget") or {}
worst = max(p95s) if p95s else None
want = None if worst is None else ("inside" if worst <= 30 else "outside")
bud = (rb.get("alb_idle_timeout_seconds") == 60 and rb.get("inside_threshold_seconds") == 30 and rb.get("verdict") == want)
conc = b.get("concurrency") == 16
ok = ok and bud and conc
lines.append("budget: ALB idle timeout %s s, threshold %s s, worst p95 %s s, verdict %s (rule says %s); concurrency %s (want 16)" % (
    rb.get("alb_idle_timeout_seconds"), rb.get("inside_threshold_seconds"), worst, rb.get("verdict"), want, b.get("concurrency")))
runs = re.findall(r"(?<![\d.-])\d{9,}(?![\d.-])", raw)
mails = re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", raw)
hyg = not runs and not mails
ok = ok and hyg
lines.append("content hygiene: long digit runs %d (want 0); e-mail addresses %d (want 0)" % (len(runs), len(mails)))
print("\n".join(lines))
print("OK" if ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r')
printf '%s\n' "$res" | sed '$d'
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
