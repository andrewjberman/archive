#!/usr/bin/env bash
# TO-CG-F-1 step 1 -- VERIFY BEFORE ANYTHING MOVES.
#
# Reads (never opens with an engine) the two residual local stores and their
# manifests in the MAIN workspace by ABSOLUTE path, prints size + mtime +
# sha256 for each, and head-objects the tarball kuzu_db is reproducible from.
# Nothing here writes, moves or deletes.
set -u
W=C:/Users/AndrewBerman/Desktop/ajb_workspace/infra/aws/globgrph
BUCKET=opal-313476888478-globgrph
TARBALL_KEY=snapshots/20260612/graph-20260612.tar.gz
AWS=.tools/aws

echo "=== f1_before.sh -- $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "HEAD=$(git rev-parse HEAD)  BRANCH=$(git rev-parse --abbrev-ref HEAD)"
echo "MAIN_WORKSPACE_DIR=$W"
echo

echo "--- LOCAL ARTIFACTS (ls -d by absolute path) ---"
for p in "$W/kuzu_db" "$W/kuzu_db._build_manifest.json" \
         "$W/kuzu_ac7.db" "$W/kuzu_ac7.db._build_manifest.json" \
         "$W/kuzu_ac7"; do
  if ls -d "$p" >/dev/null; then
    echo "PRESENT $p"
  else
    echo "ABSENT  $p"
  fi
done
echo

echo "--- SIZE + MTIME + SHA256 (file artifacts) ---"
for p in "$W/kuzu_db" "$W/kuzu_db._build_manifest.json" \
         "$W/kuzu_ac7.db" "$W/kuzu_ac7.db._build_manifest.json"; do
  sz=$(stat -c '%s' "$p")
  mt=$(stat -c '%y' "$p")
  sh=$(sha256sum "$p" | cut -d' ' -f1)
  echo "ARTIFACT $p"
  echo "  size=$sz"
  echo "  mtime_local=$mt"
  echo "  sha256=$sh"
done
echo "DIR $W/kuzu_ac7 entries=$(ls -A "$W/kuzu_ac7" | wc -l) (0 = empty)"
echo

echo "--- MANIFESTS, QUOTED WHOLE ---"
echo "### kuzu_db._build_manifest.json"
cat "$W/kuzu_db._build_manifest.json"
echo
echo "### kuzu_ac7.db._build_manifest.json"
cat "$W/kuzu_ac7.db._build_manifest.json"
echo
echo

echo "--- THE TARBALL kuzu_db IS REPRODUCIBLE FROM (head-object) ---"
$AWS s3api head-object --bucket "$BUCKET" --key "$TARBALL_KEY" \
  --region us-east-1 --output json
echo "TARBALL_HEAD_RC=$?"
echo

echo "--- THE ARCHIVE PREFIX BEFORE THE UPLOAD (must be empty) ---"
$AWS s3api list-objects-v2 --bucket "$BUCKET" \
  --prefix archive/NFRA_GLOBGRPH.ITEM-3/ --region us-east-1 --output json
echo "PREFIX_LIST_RC=$?"
echo
echo "--- THE BUILDER, STILL AT HEAD ---"
git log -1 --format='%H %ad' --date=iso -- infra/aws/globgrph/kuzu_load.py
echo "BUILDER_BYTES_AT_HEAD=$(git show HEAD:infra/aws/globgrph/kuzu_load.py | wc -c)"
echo
echo "=== f1_before.sh END ==="
