#!/usr/bin/env bash
# OPLGTW OG-ap-36 AC1 (round 41, the fifth batched gateway release, PHASE A): the re-cut carries exactly the code of OG-en-21, OG-en-22, OG-db-2 and OG-db-3, and the host measurements passed.
#  - W/ap36_release.json {base_sha, release_sha, trunk_sha}; the live ref BEFORE this release is EC2_MANIFEST deployed_commit at HEAD (previous_deployed_commit once this release is the deployed one);
#  - base..release differs only in the take list: app/tools.py, app/client_core.py, app/client_adapter_bd49f.py, deploy-to-ec2.sh, tests/test_og_en21.py, test_og_en22.py, test_og_en23.py, test_og_db3.py, and (only if the naming gate needs it) infra/logic/registry/*.json;
#  - every file in the diff is byte-equal to its blob at trunk_sha, and all four code files ARE in the diff (the take is complete);
#  - NOT in the diff: destructive_ops.py, the harvest files, the catalog, EC2_MANIFEST.json, Terraform, the data copies;
#  - W/MEM_GATE_OG-ap-36.json (the candidate code on the host, fresh processes, one windowed call at a time): the four-page chain (median growth <= 20 MB, first page <= 45 s, host peak < 75), the plateau test (two chains in one process,
#    net growth of the second <= 50 MB, host < 80, no page > 55 s), page wall candidate < live, pages equal live row for row, health under 1 s during a page.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
GW=infra/aws/ec2/opal-gateway
W=org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1
REC="${AP36_REC_OVERRIDE:-$W/ap36_release.json}"
MEM="${AP36_MEM_OVERRIDE:-$W/MEM_GATE_OG-ap-36.json}"
ASK="${AP36_ASK_OVERRIDE:-$W/NEVER_WIDEN_ASK_OG-ap-36.md}"
CT1="${AP36_CT1_OVERRIDE:-$W/CT1_CONCURRENT_OG-ap-36.json}"
[ -f "$REC" ] && [ -f "$ASK" ] && [ -f "$MEM" ] && [ -f "$CT1" ] || { echo "ap36_release.json, MEM_GATE_OG-ap-36.json, CT1_CONCURRENT_OG-ap-36.json or the ask absent"; echo "RESULT: FAIL"; exit 1; }
read -r base rel trunk meas mbase <<<"$(python -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));print(d.get('base_sha',''),d.get('release_sha',''),d.get('trunk_sha',''),d.get('measured_release_sha',''),d.get('measured_base_sha',''))" "$(native "$REC")" | tr -d '\r')"
[ -n "$meas" ] || meas=$rel
# OG-ap-36 amendment A4: when another seat's release landed on the live ref between the measured release and this one (the CTO's host-order swap, msg 35508),
# the record names measured_base_sha (the live ref the measured release was cut on); the files that base moved are not this release's delta
[ -n "$mbase" ] || mbase=$base
git cat-file -e "${mbase}^{commit}" || { echo "measured_base_sha is not a commit here"; echo "RESULT: FAIL"; exit 1; }
git cat-file -e "${meas}^{commit}" || { echo "measured_release_sha is not a commit here"; echo "RESULT: FAIL"; exit 1; }
git cat-file -e "${rel}^{commit}" && git cat-file -e "${base}^{commit}" && git cat-file -e "${trunk}^{commit}" || { echo "base, release or trunk sha is not a commit here"; echo "RESULT: FAIL"; exit 1; }
read -r dep prev <<<"$(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "import json,sys;s=json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway'];print(s.get('deployed_commit','NONE'),s.get('previous_deployed_commit','NONE'))" | tr -d '\r')"
live=$dep; [ "$dep" = "$rel" ] && live=$prev
[ -n "$AP36_LIVE_OVERRIDE" ] && live=$AP36_LIVE_OVERRIDE
ALLOW="^($GW/(app/(tools|client_core|client_adapter_bd49f)\.py|deploy-to-ec2\.sh|tests/test_og_(en21|en22|en23|en24|db3)\.py)|infra/logic/registry/[A-Za-z0-9_]+\.json)$"
files=$(git diff --name-only "$base" "$rel" | tr -d '\r'); n=$(printf '%s\n' "$files" | grep -c .)
outside=$(printf '%s\n' "$files" | grep -vE "$ALLOW" | grep -c .)
tf=$(printf '%s\n' "$files" | grep -c '\.tf$')
barred=$(printf '%s\n' "$files" | grep -cE "$GW/app/(destructive_ops|harvest_[a-z]+|refs/DATA_CATALOG)\.(py|yaml)|infra/aws/ec2/EC2_MANIFEST\.json|$GW/app/refs/(partner_roster|scopes)\.json")
missing=0
for p in app/tools.py app/client_core.py app/client_adapter_bd49f.py deploy-to-ec2.sh; do
  printf '%s\n' "$files" | grep -qx "$GW/$p" || missing=$((missing+1))
done
neq=0
for p in $files; do
  a=$(git rev-parse "$rel:$p" 2>/dev/null | tr -d '\r'); b=$(git rev-parse "$trunk:$p" 2>/dev/null | tr -d '\r')
  [ -n "$a" ] && [ "$a" = "$b" ] || neq=$((neq+1))
done
# the memory/plateau/wall/equality/health record may have been measured on an EARLIER release (OG-ap-36 amendment A3: a later release adds one line of
# client_core._answer and one test, nothing on the read path); then that release must differ from this one only in those two files and by at most 4 changed lines
mdelta="memory record measured on this release: yes"; mok=1
if [ "$meas" != "$rel" ]; then
  mfiles=$(git diff --name-only "$meas" "$rel" | tr -d '\r')
  if [ "$mbase" != "$base" ]; then mmoved=$(git diff --name-only "$mbase" "$base" | tr -d '\r'); else mmoved=""; fi
  mout=$(printf '%s\n' "$mfiles" | grep -vE "^$GW/(app/client_core\.py|tests/test_og_en24\.py)$" | grep -vxF -f <(printf '%s\n' "$mmoved" | grep .; echo __none__) | grep -c .)
  mhunks=$(git diff -U0 "$meas" "$rel" -- "$GW/app/client_core.py" | grep -c '^@@'); mlines=$(git diff -U0 "$meas" "$rel" -- "$GW/app/client_core.py" | grep -cE '^[+-][^+-]')
  mdelta="memory record measured on release ${meas:0:10}; this release differs from it in files outside client_core.py and test_og_en24.py: $mout (want 0); client_core.py hunks $mhunks (want 1), changed lines $mlines (want 4 or fewer)"
  [ "$mout" = 0 ] && [ "$mhunks" = 1 ] && [ "$mlines" -le 4 ] || mok=0
  mdelta="$mdelta: $([ "$mok" = 1 ] && echo ok || echo NOT OK)"
fi
rec=$(python - "$(native "$MEM")" "$meas" <<'PYEOF'
import json, re, statistics, sys
raw = open(sys.argv[1], encoding="utf-8").read()
d = json.loads(raw)
b = d.get("body", d)
isn = lambda v: isinstance(v, (int, float)) and not isinstance(v, bool)
pages = b.get("pages") or []
num = (len(pages) >= 3 and isn(b.get("rss_before_mb"))
       and all(all(isn(p.get(k)) for k in ("rss_mb", "host_pct", "wall_s")) for p in pages))
growth = [pages[i]["rss_mb"] - pages[i - 1]["rss_mb"] for i in range(1, len(pages))] if num else []
med = statistics.median(growth) if growth else None
close = med is not None and isn(b.get("median_growth_mb")) and abs(b["median_growth_mb"] - med) <= 0.5
same = b.get("release_sha") == sys.argv[2]
peak = max([p["host_pct"] for p in pages] + [b.get("peak_host_pct") or 0]) if num else None
chain_ok = num and close and same and med <= 20 and pages[0]["wall_s"] <= 45 and peak < 75
pl = b.get("plateau") or {}
plat_ok = (all(isn(pl.get(k)) for k in ("net_growth_mb", "peak_host_pct", "max_page_wall_s"))
           and pl["net_growth_mb"] <= 50 and pl["peak_host_pct"] < 80 and pl["max_page_wall_s"] <= 55)
wl = b.get("wall") or {}
wall_ok = isn(wl.get("live_first_page_s")) and isn(wl.get("candidate_first_page_s")) and wl["candidate_first_page_s"] < wl["live_first_page_s"]
eq = b.get("equality") or {}
eq_ok = isn(eq.get("pages_compared")) and eq["pages_compared"] >= 3 and eq.get("pages_equal") == eq["pages_compared"]
hl = b.get("health") or {}
hl_ok = isn(hl.get("probes")) and hl["probes"] >= 3 and isn(hl.get("max_probe_s")) and hl["max_probe_s"] < 1.0
runs = re.findall(r"(?<![\d.-])\d{9,}(?![\d.-])", re.sub(r'"[0-9a-f]{40}"', '""', raw))
ok = chain_ok and plat_ok and wall_ok and eq_ok and hl_ok and not runs
print("memory gate: pages %d, median growth %s MB per page (limit 20), first-page wall %s s (limit 45), host peak %s (limit 75), release_sha equal %s: %s" % (
    len(pages), None if med is None else round(med, 1), pages[0]["wall_s"] if pages else None, peak, "yes" if same else "no", "ok" if chain_ok else "NOT OK"))
print("plateau: net growth %s MB (limit 50), host peak %s (limit 80), longest page %s s (limit 55): %s" % (pl.get("net_growth_mb"), pl.get("peak_host_pct"), pl.get("max_page_wall_s"), "ok" if plat_ok else "NOT OK"))
print("first page wall: live %s s, candidate %s s (want candidate < live): %s; pages equal live row for row %s of %s: %s; health during a page: %s probes, longest %s s (limit 1): %s" % (
    wl.get("live_first_page_s"), wl.get("candidate_first_page_s"), "ok" if wall_ok else "NOT OK", eq.get("pages_equal"), eq.get("pages_compared"), "ok" if eq_ok else "NOT OK", hl.get("probes"), hl.get("max_probe_s"), "ok" if hl_ok else "NOT OK"))
print("OK" if ok else "NO")
PYEOF
)
rec=$(printf '%s' "$rec" | tr -d '\r')
ct1=$(python - "$(native "$CT1")" "$rel" <<'CTEOF'
import json, re, sys
raw = open(sys.argv[1], encoding="utf-8").read()
d = json.loads(raw)
b = d.get("body", d)
isn = lambda v: isinstance(v, (int, float)) and not isinstance(v, bool)
same = b.get("release_sha") == sys.argv[2]
first = b.get("first_equals_solo") is True
real = b.get("second_real_gate")
short = b.get("second_short_gate")
real_ok = real in ("waited_then_equal_solo", "window_read_busy")
short_ok = short == "window_read_busy"
hl = b.get("health") or {}
hl_ok = isn(hl.get("probes")) and hl["probes"] >= 3 and isn(hl.get("max_probe_s")) and hl["max_probe_s"] < 1.0
cn = b.get("counts") or {}
cn_ok = isn(cn.get("pages_compared")) and cn["pages_compared"] >= 6 and cn.get("pages_equal") == cn["pages_compared"]
runs = re.findall(r"(?<![\d.-])\d{9,}(?![\d.-])", re.sub(r'"[0-9a-f]{40}"', '""', raw))
ok = same and first and real_ok and short_ok and hl_ok and cn_ok and not runs
print("CT1 two concurrent windowed calls: release_sha equal %s; first equals its solo rows %s; second under the real gate wait: %s; second under a 0.5 s gate wait: %s; health during the pair: %s probes, longest %s s (limit 1): %s" % (
    "yes" if same else "no", "yes" if first else "no", real, short, hl.get("probes"), hl.get("max_probe_s"), "ok" if (same and first and real_ok and short_ok and hl_ok) else "NOT OK"))
print("partition_rows and fence_excluded per page, candidate against the live code: %s of %s pages equal (want all of 6 or more): %s" % (
    cn.get("pages_equal"), cn.get("pages_compared"), "ok" if cn_ok else "NOT OK"))
print("OK" if ok else "NO")
CTEOF
)
ct1=$(printf '%s' "$ct1" | tr -d '\r')
halves=$(python - "$(native "$ASK")" <<'PYEOF'
import re, sys
t = open(sys.argv[1], encoding="utf-8").read()
print("yes" if all(re.search(r"(?mi)^#+ .*%s" % h, t) for h in ("CTO", "COO", "CVO")) else "no")
PYEOF
)
halves=$(printf '%s' "$halves" | tr -d '\r')
echo "base ${base:0:10} is the live ref before this release: $([ "$base" = "$live" ] && echo yes || echo no) (manifest ${dep:0:10}/${prev:0:10}); release ${rel:0:10}; trunk ${trunk:0:10}"
echo "files differing $n; outside the take list $outside (want 0); take-list code files missing $missing (want 0); not byte-equal to trunk's $neq (want 0)"
echo "terraform files differing $tf (want 0); destructive_ops, harvest, catalog or manifest files in the diff $barred (want 0)"
echo "$mdelta"
printf '%s\n' "$rec" | sed '$d'
printf '%s\n' "$ct1" | sed '$d'
echo "ask has the three halves $halves"
[ "$base" = "$live" ] && [ "$n" -ge 4 ] && [ "$outside" = 0 ] && [ "$missing" = 0 ] && [ "$neq" = 0 ] && [ "$tf" = 0 ] && [ "$barred" = 0 ] && [ "$mok" = 1 ] && [ "$halves" = yes ] && [ "$(printf '%s\n' "$ct1" | tail -1)" = OK ] && [ "$(printf '%s\n' "$rec" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
