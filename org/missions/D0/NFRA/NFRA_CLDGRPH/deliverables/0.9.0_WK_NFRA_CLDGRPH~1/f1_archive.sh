#!/usr/bin/env bash
# TO-CG-F-1 step 2 -- ARCHIVE kuzu_ac7.db AND ITS CLAIM CARD, THEN VERIFY.
#
# Two PutObject acts and nothing else on S3. The local sha256 is computed
# BEFORE the upload; the object is uploaded with --checksum-algorithm SHA256 so
# S3 stores a CONTENT checksum of its own, and head-object --checksum-mode
# ENABLED reads it back. The comparison is therefore local-bytes vs
# S3-computed-bytes, not local-bytes vs local-bytes.
#
# NOTHING IS DELETED HERE. Deletion is step 4 and runs only after this prints
# ARCHIVE_OBJECTS=2 of 2 sha256_match=2 of 2.
set -u
W=C:/Users/AndrewBerman/Desktop/ajb_workspace/infra/aws/globgrph
BUCKET=opal-313476888478-globgrph
PFX=archive/NFRA_GLOBGRPH.ITEM-3
AWS=.tools/aws
PY=${PYTHON:-python}

echo "=== f1_archive.sh -- $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "BUCKET=$BUCKET (the ONLY bucket this order writes)"
echo

hex2b64() { "$PY" -c "import base64,binascii,sys;print(base64.b64encode(binascii.unhexlify(sys.argv[1])).decode())" "$1"; }

OK=0
MATCH=0
for name in kuzu_ac7.db kuzu_ac7.db._build_manifest.json; do
  SRC="$W/$name"
  KEY="$PFX/$name"
  SZ=$(stat -c '%s' "$SRC")
  HEX=$(sha256sum "$SRC" | cut -d' ' -f1)
  B64=$(hex2b64 "$HEX")
  echo "--- $name ---"
  echo "LOCAL_PRE_UPLOAD size=$SZ sha256_hex=$HEX sha256_b64=$B64"
  echo "PUT s3://$BUCKET/$KEY"
  $AWS s3api put-object --bucket "$BUCKET" --key "$KEY" --body "$SRC" \
      --checksum-algorithm SHA256 --region us-east-1 --output json
  PUT_RC=$?
  echo "PUT_RC=$PUT_RC"
  echo "HEAD s3://$BUCKET/$KEY"
  HEAD=$($AWS s3api head-object --bucket "$BUCKET" --key "$KEY" \
          --checksum-mode ENABLED --region us-east-1 --output json)
  HEAD_RC=$?
  echo "$HEAD"
  echo "HEAD_RC=$HEAD_RC"
  RSZ=$(printf '%s' "$HEAD" | "$PY" -c "import json,sys;print(json.load(sys.stdin).get('ContentLength',''))")
  RCK=$(printf '%s' "$HEAD" | "$PY" -c "import json,sys;print(json.load(sys.stdin).get('ChecksumSHA256',''))")
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

echo "ARCHIVE_OBJECTS=$OK of 2 sha256_match=$MATCH of 2"
if [ "$OK" -eq 2 ] && [ "$MATCH" -eq 2 ]; then
  echo "ARCHIVE_VERIFIED=true -- the local files MAY now be deleted (step 4)"
else
  echo "ARCHIVE_VERIFIED=false -- NOTHING IS DELETED; this is a FAIL and a row"
fi
echo "=== f1_archive.sh END ==="
