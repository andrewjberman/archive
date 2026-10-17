#!/usr/bin/env bash
# OPLGTW OG-ev-4 AC1 (round 40, memory retention across paged 49F reads): MEMORY_RETENTION.json is complete and self-consistent.
#  - variants A to F present, each with numeric pages (page, rss_mb, host_pct, wall_s) and a rss_before_mb; at least 3 pages, or at least 2 when stopped_at_host_pct is true;
#  - median_growth_mb equals the median of the page-to-page RSS growth over pages 2..n, within 0.5;
#  - flattening_variant follows the rule: the variant among B to F with the lowest median growth when that median is at or below threshold_mb_per_page (20), else "none";
#  - release_sha is the 40-character sha; host_total_mb is an int; no digit run of 9 or more, no e-mail (numbers and fixed words only).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
REC="${EV4_REC_OVERRIDE:-org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/MEMORY_RETENTION.json}"
[ -f "$REC" ] || { echo "MEMORY_RETENTION.json is absent"; echo "RESULT: FAIL"; exit 1; }
res=$(python - "$(native "$REC")" <<'PYEOF'
import json, re, statistics, sys
raw = open(sys.argv[1], encoding="utf-8").read()
d = json.loads(raw)
b = d.get("body", d)
vs = b.get("variants") or {}
ok, lines, med = True, [], {}
thr = b.get("threshold_mb_per_page")
for name in "ABCDEF":
    v = vs.get(name) or {}
    pages = v.get("pages") or []
    stopped = v.get("stopped_at_host_pct") is True
    need = 2 if stopped else 3
    num = (len(pages) >= need and isinstance(v.get("rss_before_mb"), (int, float))
           and all(isinstance(p.get("page"), int) and all(isinstance(p.get(k), (int, float)) for k in ("rss_mb", "host_pct", "wall_s")) for p in pages))
    growth = [pages[i]["rss_mb"] - pages[i - 1]["rss_mb"] for i in range(1, len(pages))] if num else []
    m = statistics.median(growth) if growth else None
    med[name] = m
    close = m is not None and isinstance(v.get("median_growth_mb"), (int, float)) and abs(v["median_growth_mb"] - m) <= 0.5
    ok = ok and num and close
    lines.append("variant %s: pages %d, median growth %s MB per page, record says %s%s" % (
        name, len(pages), None if m is None else round(m, 1), v.get("median_growth_mb"), " (stopped)" if stopped else ""))
cands = {k: med[k] for k in "BCDEF" if med.get(k) is not None}
best = min(cands, key=cands.get) if cands else None
want = best if (best is not None and cands[best] <= 20) else "none"
flat = thr == 20 and b.get("flattening_variant") == want
ok = ok and flat
lines.append("flattening: threshold %s MB per page, variant %s (rule says %s)" % (thr, b.get("flattening_variant"), want))
meta = bool(re.fullmatch(r"[0-9a-f]{40}", str(b.get("release_sha", "")))) and isinstance(b.get("host_total_mb"), int)
ok = ok and meta
lines.append("release_sha is 40 hex and host_total_mb is an int: %s" % ("yes" if meta else "no"))
runs = re.findall(r"(?<![\d.-])\d{9,}(?![\d.-])", raw)
mails = re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", raw)
ok = ok and not runs and not mails
lines.append("content hygiene: long digit runs %d (want 0); e-mail addresses %d (want 0)" % (len(runs), len(mails)))
print("\n".join(lines))
print("OK" if ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r')
printf '%s\n' "$res" | sed '$d'
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
