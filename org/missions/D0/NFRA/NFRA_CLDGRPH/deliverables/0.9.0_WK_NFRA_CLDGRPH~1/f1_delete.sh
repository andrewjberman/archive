#!/usr/bin/env bash
# TO-CG-F-1 step 4 -- DELETE, LAST, AND ONLY BEHIND ITS OWN GUARD.
#
# Every deletion below is guarded IN THIS SCRIPT by a head-object on the object
# the bytes survive in, re-read here and not carried from step 2:
#   kuzu_db + its manifest  -> the tarball they are reproducible from
#   kuzu_ac7.db + its card  -> the two archive objects, size AND sha256
# A guard that does not return the expected size SKIPS that deletion loudly.
# No recursive delete: five named paths, rmdir on an empty directory.
set -u
W=C:/Users/AndrewBerman/Desktop/ajb_workspace/infra/aws/globgrph
BUCKET=opal-313476888478-globgrph
PFX=archive/NFRA_GLOBGRPH.ITEM-3
TARBALL_KEY=snapshots/20260612/graph-20260612.tar.gz
AWS=.tools/aws
PY=${PYTHON:-python}

echo "=== f1_delete.sh -- $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="

field() { "$PY" -c "import json,sys;d=json.load(sys.stdin);print(d.get(sys.argv[1],''))" "$1"; }

echo "--- GUARD A: the tarball kuzu_db is reproducible from ---"
TH=$($AWS s3api head-object --bucket "$BUCKET" --key "$TARBALL_KEY" --region us-east-1 --output json)
TH_RC=$?
echo "$TH"
TSZ=$(printf '%s' "$TH" | field ContentLength)
echo "tarball_head_rc=$TH_RC size=$TSZ (expected 71671)"
GUARD_A=false
[ "$TH_RC" -eq 0 ] && [ "$TSZ" = "71671" ] && GUARD_A=true
echo "GUARD_A=$GUARD_A"
echo

echo "--- GUARD B: the two archive objects for kuzu_ac7.db ---"
GUARD_B=true
for pair in "kuzu_ac7.db 4050944 bN/wStGMStZANcVrVIQY93STFON0Zyhe/Hnkf6EwdM8=" \
            "kuzu_ac7.db._build_manifest.json 908 RNG+YqojvKkJXLSrm+3eB7nkRNdmq4CVbEd+1tBEdUI="; do
  set -- $pair
  n=$1; esz=$2; eck=$3
  AH=$($AWS s3api head-object --bucket "$BUCKET" --key "$PFX/$n" --checksum-mode ENABLED --region us-east-1 --output json)
  AH_RC=$?
  ASZ=$(printf '%s' "$AH" | field ContentLength)
  ACK=$(printf '%s' "$AH" | field ChecksumSHA256)
  echo "$n rc=$AH_RC size=$ASZ (expected $esz) ChecksumSHA256=$ACK (expected $eck)"
  if [ "$AH_RC" -ne 0 ] || [ "$ASZ" != "$esz" ] || [ "$ACK" != "$eck" ]; then GUARD_B=false; fi
done
echo "GUARD_B=$GUARD_B"
echo

echo "--- DELETIONS ---"
if [ "$GUARD_A" = true ]; then
  for p in "$W/kuzu_db" "$W/kuzu_db._build_manifest.json"; do
    rm -f "$p" && echo "DELETED $p" || echo "DELETE_FAILED $p"
  done
else
  echo "SKIPPED kuzu_db and its manifest -- GUARD_A did not hold"
fi
if [ "$GUARD_B" = true ]; then
  for p in "$W/kuzu_ac7.db" "$W/kuzu_ac7.db._build_manifest.json"; do
    rm -f "$p" && echo "DELETED $p" || echo "DELETE_FAILED $p"
  done
  if [ -d "$W/kuzu_ac7" ]; then
    n=$(ls -A "$W/kuzu_ac7" | wc -l)
    if [ "$n" -eq 0 ]; then
      rmdir "$W/kuzu_ac7" && echo "DELETED (rmdir, empty) $W/kuzu_ac7" || echo "RMDIR_FAILED $W/kuzu_ac7"
    else
      echo "SKIPPED $W/kuzu_ac7 -- NOT EMPTY ($n entries); no recursive delete is taken"
    fi
  fi
else
  echo "SKIPPED kuzu_ac7.db, its card and the empty dir -- GUARD_B did not hold"
fi
echo
echo "--- NOT TOUCHED, ON PURPOSE (printed so the scope is visible) ---"
ls -la "$W" | grep -i -E 'kuzu_stitch|nessie_load\.|kuzu_cli|projection_client'
echo "=== f1_delete.sh END ==="
