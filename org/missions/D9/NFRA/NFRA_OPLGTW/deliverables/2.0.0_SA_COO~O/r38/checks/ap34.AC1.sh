#!/usr/bin/env bash
# OPLGTW OG-ap-34 AC1 (round 40, the fourth batched gateway release, PHASE A): the re-cut carries exactly the code of OG-en-17 to OG-en-20 and MI's catalog blob, nothing else, and the memory gate passed on the host.
#  - W/ap34_release.json {base_sha, release_sha, trunk_sha[, declared_base_sha]}; the live ref BEFORE this release is EC2_MANIFEST deployed_commit at HEAD (previous_deployed_commit once this release is the deployed one); base_sha is that ref, OR (Amendment A2) the release's parent when declared_base_sha is the live ref and is not fetchable here;
#  - A2: the harvest files app/harvest_{figures,identity,research}.py may be in the diff only byte-equal to trunk_sha's (live from another seat's release, equal to trunk);
#  - base..release differs only in the allowed set (client_adapter_bd49f.py, app/refs/DATA_CATALOG.yaml, the tests, the naming-gate registry files if a prelude is needed);
#  - the MEMORY GATE (W/MEM_GATE.json, the candidate code run on the host in a fresh process, one windowed call at a time): at least 3 pages, the median page-to-page RSS growth at or below 20 MB, the first page's wall at or below 45 s, the release_sha equal to the record's;
#  - the catalog in the release is the blob 2cbe275d03c9a5af85afefabc604e26b71e9be12 (MI's signed emit, md5 bdfee515ec348f0ea2ee716eff5acba5), byte-equal to trunk_sha's;
#  - no Terraform; tools.py and destructive_ops.py untouched; deploy-to-ec2.sh and EC2_MANIFEST.json UNCHANGED; no data copy committed;
#  - every registry file in the diff is byte-equal to its blob at trunk_sha; the ask has the three half headings.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
GW=infra/aws/ec2/opal-gateway
REC="${AP34_REC_OVERRIDE:-org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/ap34_release.json}"
MEM="${AP34_MEM_OVERRIDE:-org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/MEM_GATE.json}"
ASK="${AP34_ASK_OVERRIDE:-org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-ap-34.md}"
[ -f "$REC" ] && [ -f "$ASK" ] && [ -f "$MEM" ] || { echo "ap34_release.json, MEM_GATE.json or the ask absent"; echo "RESULT: FAIL"; exit 1; }
read -r base rel trunk decl <<<"$(python -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));print(d.get('base_sha',''),d.get('release_sha',''),d.get('trunk_sha',''),d.get('declared_base_sha') or d.get('base_sha',''))" "$(native "$REC")" | tr -d '\r')"
git cat-file -e "${rel}^{commit}" && git cat-file -e "${base}^{commit}" && git cat-file -e "${trunk}^{commit}" || { echo "base, release or trunk sha is not a commit here"; echo "RESULT: FAIL"; exit 1; }
read -r dep prev <<<"$(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "import json,sys;s=json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway'];print(s.get('deployed_commit','NONE'),s.get('previous_deployed_commit','NONE'))" | tr -d '\r')"
live=$dep; [ "$dep" = "$rel" ] && live=$prev
ALLOW="^($GW/(app/client_adapter_bd49f\.py|app/harvest_(figures|identity|research)\.py|app/refs/DATA_CATALOG\.yaml|tests/[A-Za-z0-9_./-]+)|infra/logic/registry/[A-Za-z0-9_]+\.json)$"
files=$(git diff --name-only "$base" "$rel" | tr -d '\r'); n=$(printf '%s\n' "$files" | grep -c .)
outside=$(printf '%s\n' "$files" | grep -vE "$ALLOW" | grep -c .)
tf=$(printf '%s\n' "$files" | grep -c '\.tf$')
tools_touched=$(printf '%s\n' "$files" | grep -cE "$GW/app/(tools|destructive_ops)\.py")
deploy_changed=$(printf '%s\n' "$files" | grep -cE "$GW/deploy-to-ec2\.sh|infra/aws/ec2/EC2_MANIFEST\.json")
cm=$(git diff --name-only "$base" "$rel" -- "$GW/app/refs/partner_roster.json" "$GW/app/refs/scopes.json" | grep -c .)
regdiff=0; regbad=0
for p in $(printf '%s\n' "$files" | grep -E '^infra/logic/registry/'); do
  regdiff=$((regdiff+1)); a=$(git rev-parse "$rel:$p" 2>/dev/null | tr -d '\r'); b=$(git rev-parse "$trunk:$p" 2>/dev/null | tr -d '\r')
  [ -n "$a" ] && [ "$a" = "$b" ] || regbad=$((regbad+1))
done
hvdiff=0; hvbad=0
for p in $(printf '%s\n' "$files" | grep -E "^$GW/app/harvest_(figures|identity|research)\.py$"); do
  hvdiff=$((hvdiff+1)); a=$(git rev-parse "$rel:$p" 2>/dev/null | tr -d '\r'); b=$(git rev-parse "$trunk:$p" 2>/dev/null | tr -d '\r')
  [ -n "$a" ] && [ "$a" = "$b" ] || hvbad=$((hvbad+1))
done
catblob=$(git rev-parse "$rel:$GW/app/refs/DATA_CATALOG.yaml" 2>/dev/null | tr -d '\r'); cattrunk=$(git rev-parse "$trunk:$GW/app/refs/DATA_CATALOG.yaml" 2>/dev/null | tr -d '\r')
catok=no; [ "$catblob" = "2cbe275d03c9a5af85afefabc604e26b71e9be12" ] && [ "$catblob" = "$cattrunk" ] && catok=yes
memgate=$(python - "$(native "$MEM")" "$rel" <<'PYEOF'
import json, re, statistics, sys
raw = open(sys.argv[1], encoding="utf-8").read()
d = json.loads(raw)
b = d.get("body", d)
pages = b.get("pages") or []
num = (len(pages) >= 3 and isinstance(b.get("rss_before_mb"), (int, float))
       and all(all(isinstance(p.get(k), (int, float)) for k in ("rss_mb", "host_pct", "wall_s")) for p in pages))
growth = [pages[i]["rss_mb"] - pages[i - 1]["rss_mb"] for i in range(1, len(pages))] if num else []
med = statistics.median(growth) if growth else None
close = med is not None and isinstance(b.get("median_growth_mb"), (int, float)) and abs(b["median_growth_mb"] - med) <= 0.5
same = b.get("release_sha") == sys.argv[2]
wall_ok = num and pages[0]["wall_s"] <= 45
ok = num and close and same and med <= 20 and wall_ok
runs = re.findall(r"(?<![\d.-])\d{9,}(?![\d.-])", re.sub(r'"[0-9a-f]{40}"', '""', raw))
ok = ok and not runs
print("memory gate: pages %d, median growth %s MB per page (limit 20), first-page wall %s s (limit 45), release_sha equal %s: %s" % (
    len(pages), None if med is None else round(med, 1), pages[0]["wall_s"] if pages else None, "yes" if same else "no", "ok" if ok else "NOT OK"))
print("OK" if ok else "NO")
PYEOF
)
memgate=$(printf '%s' "$memgate" | tr -d '\r')
halves=$(python - "$(native "$ASK")" <<'PYEOF'
import re, sys
t = open(sys.argv[1], encoding="utf-8").read()
print("yes" if all(re.search(r"(?mi)^#+ .*%s" % h, t) for h in ("CTO", "COO", "CVO")) else "no")
PYEOF
)
halves=$(printf '%s' "$halves" | tr -d '\r')
echo "base ${decl:0:10} is the live ref before this release: $([ "$decl" = "$live" ] && echo yes || echo no) (manifest ${dep:0:10}/${prev:0:10}); release cut on ${base:0:10}; release ${rel:0:10}; trunk ${trunk:0:10}"
echo "files differing $n; outside the batch set $outside (want 0); terraform files differing $tf (want 0); tools.py or destructive_ops.py touched $tools_touched (want 0)"
echo "catalog blob in the release is ${catblob:0:10} (want 2cbe275d03), equal to trunk's: $catok"
printf '%s\n' "$memgate" | sed '$d'
echo "harvest files in the diff $hvdiff, not byte-equal to trunk's $hvbad (want 0)"
echo "deploy script or manifest changed $deploy_changed (want 0); data copies committed $cm (want 0); registry files in the diff $regdiff, not byte-equal to trunk's $regbad (want 0); ask has the three halves $halves"
[ "$decl" = "$live" ] && [ "$hvbad" = 0 ] && [ "$n" -ge 1 ] && [ "$outside" = 0 ] && [ "$tf" = 0 ] && [ "$tools_touched" = 0 ] && [ "$deploy_changed" = 0 ] && [ "$cm" = 0 ] && [ "$regbad" = 0 ] && [ "$halves" = yes ] && [ "$catok" = yes ] && [ "$(printf '%s\n' "$memgate" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
