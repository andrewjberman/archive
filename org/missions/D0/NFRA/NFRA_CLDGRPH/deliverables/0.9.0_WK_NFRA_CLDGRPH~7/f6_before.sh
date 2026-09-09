#!/usr/bin/env bash
# TO-CG-F-6 step 1 -- VERIFY BEFORE ANYTHING MOVES.
#
# Reads (never OPENS with an engine) the local stitch store, its build manifest
# and the local stitch_graph.json scratch in the MAIN workspace by ABSOLUTE
# path, and prints size + mtime + sha256 for each. kuzu.Database CREATES an
# absent store, so no engine is imported anywhere in this order; sha256sum and
# stat are the only readers.
#
# Nothing here writes, moves or deletes. The archive prefix is listed BEFORE
# the upload so "4 objects" later is a delta and not a coincidence.
set -u
W=C:/Users/AndrewBerman/Desktop/ajb_workspace/infra/aws/globgrph
BUCKET=opal-313476888478-globgrph
PFX=archive/NFRA_CLDGRPH.CG-s-26
AWS=.tools/aws

echo "=== f6_before.sh -- $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "SERIAL=0.9.0_WK_NFRA_CLDGRPH~7"
echo "HEAD=$(git rev-parse HEAD)  BRANCH=$(git rev-parse --abbrev-ref HEAD)"
echo "MAIN_WORKSPACE_DIR=$W"
echo "BUCKET=$BUCKET (the ONLY bucket this order writes)"
echo

echo "--- THE THREE LOCAL ARTIFACTS (ls -d by absolute path) ---"
for p in "$W/kuzu_stitch_db" "$W/kuzu_stitch_db._build_manifest.json" "$W/stitch_graph.json"; do
  if ls -d "$p" >/dev/null; then echo "PRESENT $p"; else echo "ABSENT  $p"; fi
done
echo
echo "--- A FOURTH NAME THE .gitignore CARRIES, CHECKED SO ITS ABSENCE IS MEASURED ---"
if ls -d "$W/kuzu_stitch_db.wal" >/dev/null; then
  echo "PRESENT $W/kuzu_stitch_db.wal  -- NOT in this order's three; a ROW, not a deletion"
else
  echo "ABSENT  $W/kuzu_stitch_db.wal  (no write-ahead log beside the store)"
fi
echo

echo "--- SIZE + MTIME + SHA256 ---"
for p in "$W/kuzu_stitch_db" "$W/kuzu_stitch_db._build_manifest.json" "$W/stitch_graph.json"; do
  echo "ARTIFACT $p"
  echo "  size=$(stat -c '%s' "$p")"
  echo "  mtime_local=$(stat -c '%y' "$p")"
  echo "  sha256=$(sha256sum "$p" | cut -d' ' -f1)"
done
echo

echo "--- THE BUILD MANIFEST, QUOTED WHOLE (it is 439 B; it is the whole claim) ---"
cat "$W/kuzu_stitch_db._build_manifest.json"
echo
echo

echo "--- W3-S11: THE BYTES ARE YOUNGER THAN THE MANIFEST THAT CLAIMS THEM ---"
echo "store  mtime: $(stat -c '%y' "$W/kuzu_stitch_db")"
echo "manifest built_at: $(python -c "import json,sys;print(json.load(open(sys.argv[1],encoding='utf-8'))['built_at'])" "$W/kuzu_stitch_db._build_manifest.json")"
echo "-> no manifest describes the bytes on disk; the capable mutator was INFERRED"
echo "   as the deleted kuzu_cost_enrich.py (W3-S11). Recorded as a FIELD of the"
echo "   archive manifest, not as prose only."
echo

echo "--- THE ARCHIVE PREFIX BEFORE THE UPLOAD (expected: no Contents key) ---"
$AWS s3api list-objects-v2 --bucket "$BUCKET" --prefix "$PFX/" --region us-east-1 --output json
echo "PREFIX_LIST_RC=$?"
echo

echo "--- THE BUILDER, STILL AT HEAD (retired in step 3, not here) ---"
git log -1 --format='%H %ad' --date=iso --full-history -- infra/aws/globgrph/kuzu_stitch_load.py
echo "BUILDER_BYTES_AT_HEAD=$(git show HEAD:infra/aws/globgrph/kuzu_stitch_load.py | wc -c)"
echo "BUILDER_BLOB_SHA1=$(git rev-parse HEAD:infra/aws/globgrph/kuzu_stitch_load.py)"
echo

echo "--- NOT TOUCHED BY THIS ORDER, PRINTED SO THE SCOPE IS VISIBLE ---"
ls -la "$W" | grep -i -E 'derive_stitch|extract_portal_stitch|comp_debt|projection_client|kuzu_nessie_load|kuzu_incremental_refresh'
echo
echo "=== f6_before.sh END ==="
