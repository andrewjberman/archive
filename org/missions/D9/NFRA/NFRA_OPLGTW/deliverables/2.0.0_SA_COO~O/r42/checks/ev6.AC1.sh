#!/usr/bin/env bash
# OPLGTW OG-ev-6 AC1 (round 42): the measured sweep of the window page size (PAGE_PARTITIONS) on the host, under the hard guard, graded by a rule FIXED BY THE ORDER BEFORE ANY RUN.
# Record W/PAGE_SWEEP.json = {"body": {"trunk_sha": "<40 hex>", "guard": "<named guard>", "rule_stated_before_runs": true,
#   "sizes": {"30": {"runs": [3 x {"max_page_wall_s", "first_page_wall_s", "median_growth_mb", "vmhwm_mb", "host_peak_pct", "pages": n, "rows_hash_120": "<64 hex>"}]}, "60": {...}, "120": {...}},
#   "chosen_partitions": n}}
# The rule (recomputed here from the runs, never read from a flag): a size PASSES only if, in all 3 fresh-process runs, the longest page took under 15 s, the host peak was under 75 percent and the combined rows of the newest 120 partitions
# hash equal to size 30's; and the median of the 3 run medians of RSS growth per page is 20 MB or less with no run median above 30 MB. chosen_partitions = the largest size that passes AND whose every smaller size also passed (30 when 60 fails: a gap is not stepped over).
# Override (dry-run controls only): EV6_REC_OVERRIDE.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
REC="${EV6_REC_OVERRIDE:-org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/PAGE_SWEEP.json}"
[ -f "$REC" ] || { echo "PAGE_SWEEP.json absent"; echo "RESULT: FAIL"; exit 1; }
res=$(python -I - "$(native "$REC")" <<'PYEOF'
import json, re, statistics, sys
raw = open(sys.argv[1], encoding="utf-8").read()
d = json.loads(raw); b = d.get("body", d)
isn = lambda v: isinstance(v, (int, float)) and not isinstance(v, bool)
GUARDS = ("oom_score_adj_1000_rlimit_as_1400mb", "oom_score_adj_1000_cgroup_memmax_1400mb")
sz = b.get("sizes") or {}
need = ("30", "60", "120")
shape = all(k in sz and len((sz[k].get("runs") or [])) == 3 for k in need)
run_ok = lambda r: all(isn(r.get(k)) for k in ("max_page_wall_s", "first_page_wall_s", "median_growth_mb", "vmhwm_mb", "host_peak_pct", "pages")) and isinstance(r.get("rows_hash_120"), str) and len(r["rows_hash_120"]) == 64
fields = shape and all(run_ok(r) for k in need for r in sz[k]["runs"])
passed = {}
if fields:
    base_hashes = {r["rows_hash_120"] for r in sz["30"]["runs"]}
    one_base = len(base_hashes) == 1
    for k in need:
        runs = sz[k]["runs"]
        meds = [r["median_growth_mb"] for r in runs]
        passed[k] = (all(r["max_page_wall_s"] < 15 and r["host_peak_pct"] < 75 for r in runs) and one_base
                     and all(r["rows_hash_120"] in base_hashes for r in runs)
                     and statistics.median(meds) <= 20 and max(meds) <= 30)
    chosen = 30
    for k in need:
        if passed[k]:
            chosen = int(k)
        else:
            break
else:
    one_base = False; chosen = None
chosen_ok = fields and b.get("chosen_partitions") == chosen
sha_ok = bool(re.fullmatch(r"[0-9a-f]{40}", str(b.get("trunk_sha", ""))))
guard_ok = b.get("guard") in GUARDS and b.get("rule_stated_before_runs") is True
stripped = re.sub(r'"[0-9a-f]{40,64}"', '""', raw)
bignums = re.findall(r"(?<![\d.-])\d{9,}(?![\d.-])", stripped)
ok = shape and fields and one_base and chosen_ok and sha_ok and guard_ok and not bignums
print("sweep record: 3 sizes x 3 fresh runs %s; every run carries its fields %s; the newest-120-partition row hash is one value across all runs and sizes %s" % ("yes" if shape else "NO", "yes" if fields else "NO", "yes" if one_base else "NO"))
print("rule recomputed from the runs: pass by size %s; chosen %s; the record says %s: %s; guard named and rule stated before the runs: %s; trunk sha is 40 hex: %s; digit runs of 9 or more: %d (want 0)" % (
      passed, chosen, b.get("chosen_partitions"), "agree" if chosen_ok else "DISAGREE", "yes" if guard_ok else "NO", "yes" if sha_ok else "NO", len(bignums)))
print("OK" if ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r')
printf '%s\n' "$res" | sed '$d'
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
