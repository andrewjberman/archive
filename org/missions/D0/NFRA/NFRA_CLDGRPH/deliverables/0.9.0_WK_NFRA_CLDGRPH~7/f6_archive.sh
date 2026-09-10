#!/usr/bin/env bash
# TO-CG-F-6 step 2 -- ARCHIVE THE THREE FILES + THE ARCHIVE MANIFEST, THEN VERIFY.
#
# FOUR PutObject acts on ONE bucket and nothing else on S3. Each payload is
# uploaded with --checksum-algorithm SHA256 so S3 computes a CONTENT checksum of
# the bytes it received, and head-object --checksum-mode ENABLED reads that back.
# The comparison is therefore
#     S3-computed-over-received-bytes  ==  local-sha256-taken-before-the-upload
# and NOT local-vs-local, which would agree even if nothing had been sent.
#
# NOTHING IS DELETED HERE. Deletion is step 4 and runs only behind a guard that
# re-reads these objects rather than trusting this script's memory.
set -u
cd "$(git rev-parse --show-toplevel)" || exit 3
W=C:/Users/AndrewBerman/Desktop/ajb_workspace/infra/aws/globgrph
BUCKET=opal-313476888478-globgrph
PFX=archive/NFRA_CLDGRPH.CG-s-26
D=org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~7
MAN="$D/f6_ARCHIVE_MANIFEST.json"
AWS=.tools/aws
PY=${PYTHON:-python}

echo "=== f6_archive.sh -- $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "BUCKET=$BUCKET  PREFIX=$PFX"
echo "OBJECTS THIS ORDER MAY WRITE: 4 (three payloads + the archive manifest). No others."
echo

hex2b64() { "$PY" -c "import base64,binascii,sys;print(base64.b64encode(binascii.unhexlify(sys.argv[1])).decode())" "$1"; }
field() { "$PY" -c "import json,sys;d=json.load(sys.stdin);print(d.get(sys.argv[1],''))" "$1"; }

echo "--- 2a. THE ARCHIVE MANIFEST (hashes taken here, before any upload) ---"
"$PY" "$D/f6_archive_manifest.py" "$MAN"
echo "MANIFEST_RC=$?"
echo

OK=0
MATCH=0
N=0
for name in kuzu_stitch_db kuzu_stitch_db._build_manifest.json stitch_graph.json; do
  N=$((N+1))
  SRC="$W/$name"
  KEY="$PFX/$name"
  SZ=$(stat -c '%s' "$SRC")
  HEX=$("$PY" -c "import json,sys;print(json.load(open(sys.argv[1],encoding='utf-8'))['sha256'][sys.argv[2]])" "$MAN" "$name")
  B64=$(hex2b64 "$HEX")
  echo "--- $name ---"
  echo "LOCAL_PRE_UPLOAD size=$SZ sha256_hex=$HEX sha256_b64=$B64  (read OUT of the archive manifest)"
  echo "PUT s3://$BUCKET/$KEY"
  $AWS s3api put-object --bucket "$BUCKET" --key "$KEY" --body "$SRC" \
      --checksum-algorithm SHA256 --region us-east-1 --output json
  echo "PUT_RC=$?"
  HEAD=$($AWS s3api head-object --bucket "$BUCKET" --key "$KEY" \
          --checksum-mode ENABLED --region us-east-1 --output json)
  HEAD_RC=$?
  echo "$HEAD"
  echo "HEAD_RC=$HEAD_RC"
  RSZ=$(printf '%s' "$HEAD" | field ContentLength)
  RCK=$(printf '%s' "$HEAD" | field ChecksumSHA256)
  echo "S3_size=$RSZ  S3_ChecksumSHA256=$RCK"
  if [ "$HEAD_RC" -eq 0 ] && [ "$RSZ" = "$SZ" ]; then
    OK=$((OK+1)); echo "OBJECT_PRESENT_AND_SIZE_EQUAL=true"
  else
    echo "OBJECT_PRESENT_AND_SIZE_EQUAL=false"
  fi
  if [ -n "$RCK" ] && [ "$RCK" = "$B64" ]; then
    MATCH=$((MATCH+1)); echo "SHA256_EQUAL=true (S3-computed == local pre-upload)"
  else
    echo "SHA256_EQUAL=false (S3 returned '$RCK', local pre-upload is '$B64')"
  fi
  echo
done

echo "--- the archive manifest itself (the 4th object) ---"
MSZ=$(stat -c '%s' "$MAN")
MHEX=$(sha256sum "$MAN" | cut -d' ' -f1)
MB64=$(hex2b64 "$MHEX")
echo "LOCAL_PRE_UPLOAD size=$MSZ sha256_hex=$MHEX"
$AWS s3api put-object --bucket "$BUCKET" --key "$PFX/ARCHIVE_MANIFEST.json" --body "$MAN" \
    --checksum-algorithm SHA256 --content-type application/json --region us-east-1 --output json
echo "PUT_RC=$?"
MHEAD=$($AWS s3api head-object --bucket "$BUCKET" --key "$PFX/ARCHIVE_MANIFEST.json" \
        --checksum-mode ENABLED --region us-east-1 --output json)
MHEAD_RC=$?
echo "$MHEAD"
echo "HEAD_RC=$MHEAD_RC"
MRSZ=$(printf '%s' "$MHEAD" | field ContentLength)
MRCK=$(printf '%s' "$MHEAD" | field ChecksumSHA256)
if [ "$MHEAD_RC" -eq 0 ] && [ "$MRSZ" = "$MSZ" ] && [ "$MRCK" = "$MB64" ]; then
  OK=$((OK+1)); echo "OBJECT_PRESENT_AND_SIZE_EQUAL=true SHA256_EQUAL=true"
else
  echo "OBJECT_PRESENT_AND_SIZE_EQUAL=false (rc=$MHEAD_RC size=$MRSZ/$MSZ ck=$MRCK/$MB64)"
fi
echo

echo "--- THE PREFIX AFTER THE UPLOAD (4 keys, and nothing else was written) ---"
$AWS s3api list-objects-v2 --bucket "$BUCKET" --prefix "$PFX/" --region us-east-1 --output json
echo "PREFIX_LIST_RC=$?"
echo

echo "--- STEP 2 VERDICT LINES ---"
echo "ARCHIVE_OBJECTS=$OK of 4"
echo "SHA256_MATCH=$MATCH of 3"
if [ "$OK" -eq 4 ] && [ "$MATCH" -eq 3 ]; then
  echo "ARCHIVE_VERIFIED=true -- the local files MAY now be deleted (step 4, behind its own re-read guard)"
else
  echo "ARCHIVE_VERIFIED=false -- NOTHING IS DELETED; this is a FAIL and a row"
fi
echo "=== f6_archive.sh END ==="
