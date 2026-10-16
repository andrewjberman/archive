#!/usr/bin/env bash
# emit_final.sh (round 20 copy) <out dir> -- the issuer's catalog emit of round 20 (TRIAL until MX-c-27 is on trunk; LANDED only after it) (the round-18 original is kept beside it), run at the workspace root (the emitter needs portal/src/api).
#
# Order of the release day: OG-ap-23 reads live -> 2.0.0_SA_COO~MI2 runs land_links.sh and commits its rows -> THIS script -> a worker places the
# file (place_catalog.py) -> regrade_c23_instance.py -> never-widen pair -> MX-r-15 A1.
# It refuses on a dirty tracked catalog, emits with the six group maps (the sixth is round 19's live_bd_group_map.json) (the emitter reads the served tool list from the tree at the manifest's
# deployed_commit, so no overlay flag), saves the result and its md5 under <out dir>, runs the c21/c23 criteria with the file placed, saves each run
# (stdout then exit=<rc>) as <out dir>/ev/<check>.out, and restores the tracked catalog. Nothing is committed.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)" || exit 9
cd "$ROOT" || exit 9
OUT="${1:?usage: emit_final.sh <out dir>}"
T=infra/aws/ec2/opal-gateway/app/refs/DATA_CATALOG.yaml
D=org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables
C=$D/2.0.0_SA_COO~MI/round18/checks
mkdir -p "$OUT/ev" || exit 9
git diff --quiet -- "$T" || { echo "ERROR: the tracked catalog has uncommitted changes; stop"; exit 9; }
python workflows/atom_decomposition/emit_catalog_v02.py \
  --group-map $D/2.0.0_SA_COO~MI/round18/assets_group_map.json \
  --group-map $D/0.9.0_WK_NFRA_MCPINDEX~52/research_group_map_h1.json \
  --group-map $D/0.9.0_WK_NFRA_MCPINDEX~53/research_group_map_h2.json \
  --group-map $D/0.9.0_WK_NFRA_MCPINDEX~54/research_group_map_h3.json \
  --group-map $D/0.9.0_WK_NFRA_MCPINDEX~55/research_group_map_p1.json \
  --group-map $D/2.0.0_SA_COO~MI/round19/live_bd_group_map.json > "$OUT/emit.log" 2>&1
RC=$?
grep -E "EMIT REFUSED|TOOL INDEX|GROUP-MAP|SILVER DATASET|HARVEST ROWS" "$OUT/emit.log" | cut -c1-240
if [ $RC -ne 0 ]; then echo "ERROR: the emitter exited $RC; see $OUT/emit.log"; git checkout -- "$T"; exit 1; fi
cp "$T" "$OUT/DATA_CATALOG.final.yaml" && md5sum "$OUT/DATA_CATALOG.final.yaml" | tee "$OUT/DATA_CATALOG.final.md5"
FAIL=0
# Round 19: the candidate is graded against the LIVE v3 catalog (r16.AC1, r16.AC2, at the candidate FILE, nothing placed), plus the two round-18 criteria that still
# mean the same (c23.AC4 serves == row-derived pairs, c21.AC2 the tool index N) run with the file placed. c21.AC1 and c23.AC1 to AC3 compare to the round-17 base
# (304 rows) and are history; they are not run.
C20=$D/2.0.0_SA_COO~MI/round20/checks
for a in r20.AC1 r20.AC2; do
  { C20_CATALOG="$OUT/DATA_CATALOG.final.yaml" bash "$C20/$a.sh" 2>&1; echo "exit=$?"; } > "$OUT/ev/$a.out"
  echo "$a: $(grep -E '^RESULT' "$OUT/ev/$a.out" | head -1)"
  grep -q "RESULT: PASS" "$OUT/ev/$a.out" || FAIL=1
done
for a in c23.AC4 c21.AC2; do
  { bash "$C/$a.sh" 2>&1; echo "exit=$?"; } > "$OUT/ev/$a.out"
  echo "$a: $(grep -E '^RESULT' "$OUT/ev/$a.out" | head -1)"
  grep -q "RESULT: PASS" "$OUT/ev/$a.out" || FAIL=1
done
# r13.AC3 (depth and answer-time claims against LIVE AWS, read-only): it graded two shipped catalogs FAIL because a source re-stamped between the
# measure and the apply (2026-10-16: yield-curve 23:01Z, the daily publish before 11:35Z). Run it on the candidate so a stale claim is found before the release.
{ bash "$D/2.0.0_SA_COO~MI/round12/checks/r13.AC3.sh" 2>&1; echo "exit=$?"; } > "$OUT/ev/r13.AC3.out"
echo "r13.AC3: $(grep -E '^RESULT' "$OUT/ev/r13.AC3.out" | tail -1)"
grep -q "RESULT: PASS" "$OUT/ev/r13.AC3.out" || FAIL=1
git checkout -- "$T"
git diff --quiet -- "$T" && echo "tracked catalog restored" || echo "WARN: tracked catalog still differs"
[ $FAIL -eq 0 ] && echo "EMIT-FINAL: r20.AC1, r20.AC2, c23.AC4, c21.AC2 and r13.AC3 PASS" || echo "EMIT-FINAL: a criterion FAILED; read $OUT/ev"
exit $FAIL
