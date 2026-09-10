#!/usr/bin/env bash
# TO-CG-F-6 step 4 -- DELETE, LAST, AND ONLY BEHIND A GUARD RE-READ HERE.
#
# The guard is not carried from step 2. Each expected size and sha256 is read OUT
# OF THE TOMBSTONE (the tracked artifact a future reader will actually hold) and
# compared against a FRESH head-object --checksum-mode ENABLED. A payload whose
# object does not verify is SKIPPED loudly and stays on disk.
#
# Three named paths. No recursive delete, no glob, no directory removal.
set -u
cd "$(git rev-parse --show-toplevel)" || exit 3
W=C:/Users/AndrewBerman/Desktop/ajb_workspace/infra/aws/globgrph
BUCKET=opal-313476888478-globgrph
PFX=archive/NFRA_CLDGRPH.CG-s-26
TOMB=infra/aws/globgrph/kuzu_stitch_db.TOMBSTONE.md
D=org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~7
PARSE="$D/f6_tombstone_parse.py"
AWS=.tools/aws
PY=${PYTHON:-python}

echo "=== f6_delete.sh -- $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "GUARD SOURCE: $TOMB (tracked) -- not this run's memory"
echo

emit() { "$PY" "$PARSE" "$TOMB" --emit "$1"; }
field() { "$PY" -c "import json,sys;d=json.load(sys.stdin);print(d.get(sys.argv[1],''))" "$1"; }

echo "--- PRE-CONDITION: THE BUILDER IS ALREADY RETIRED IN THIS WORKTREE ---"
if [ -f infra/aws/globgrph/kuzu_stitch_load.py ]; then
  echo "BUILDER_STILL_IN_WORKTREE=true -- the order's act sequence was not followed; STOP"
  exit 4
fi
echo "BUILDER_STILL_IN_WORKTREE=false (git rm taken before this script)"
echo "TOMBSTONE_PRESENT_BEFORE_DELETE=$([ -f "$TOMB" ] && echo true || echo false)"
echo

DELETED=0
for name in kuzu_stitch_db kuzu_stitch_db._build_manifest.json stitch_graph.json; do
  KEY="$PFX/$name"
  ESZ=$(emit "archive_sha256|$KEY|size_bytes")
  ECK=$(emit "archive_sha256|$KEY|sha256_b64")
  echo "--- GUARD for $name ---"
  echo "tombstone says: key=$KEY size=$ESZ sha256_b64=$ECK"
  AH=$($AWS s3api head-object --bucket "$BUCKET" --key "$KEY" --checksum-mode ENABLED --region us-east-1 --output json)
  AH_RC=$?
  ASZ=$(printf '%s' "$AH" | field ContentLength)
  ACK=$(printf '%s' "$AH" | field ChecksumSHA256)
  echo "S3 says:        rc=$AH_RC size=$ASZ ChecksumSHA256=$ACK"
  if [ "$AH_RC" -eq 0 ] && [ -n "$ESZ" ] && [ "$ASZ" = "$ESZ" ] && [ -n "$ECK" ] && [ "$ACK" = "$ECK" ]; then
    echo "GUARD=held"
    if rm -f "$W/$name"; then DELETED=$((DELETED+1)); echo "DELETED $W/$name"; else echo "DELETE_FAILED $W/$name"; fi
  else
    echo "GUARD=BROKEN -- $W/$name is NOT deleted and stays on disk; this is a FAIL and a row"
  fi
  echo
done

echo "--- AFTER: ls -d ON THE THREE PATHS ---"
for p in "$W/kuzu_stitch_db" "$W/kuzu_stitch_db._build_manifest.json" "$W/stitch_graph.json"; do
  if ls -d "$p" >/dev/null; then echo "STILL PRESENT $p"; else echo "GONE $p"; fi
done
echo
echo "--- NOT TOUCHED, ON PURPOSE (the cloud producer's inputs and the projection's own tooling) ---"
ls -la "$W" | grep -i -E 'derive_stitch|extract_portal_stitch|comp_debt|projection_client|kuzu_nessie_load|kuzu_incremental_refresh|kuzu_cli|TOMBSTONE'
echo
echo "DELETIONS_TAKEN=$DELETED of 3"
echo "=== f6_delete.sh END ==="
