#!/usr/bin/env bash
# F1-AC2 -- THE ARCHIVE OBJECTS ARE VERIFIED BY HEAD-OBJECT.
#
# Every expected value in this probe is read OUT OF THE TOMBSTONE, not out of
# the uploading script's memory: the keys, the sizes, the pre-upload sha256.
# That is deliberate -- the tombstone is what a future reader will hold, so it
# is the tombstone that has to be right. The comparison is
#   S3-computed ChecksumSHA256  ==  the sha256 the tombstone recorded
# and it CAN fail: change one byte of either side and sha256_match drops.
set -u
cd "$(git rev-parse --show-toplevel)" || exit 3
TOMB=infra/aws/globgrph/kuzu_db.TOMBSTONE.md
D=org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~1
PARSE="$D/f1_tombstone_parse.py"
AWS=.tools/aws
PY=${PYTHON:-python}

emit() { "$PY" "$PARSE" "$TOMB" --emit "$1"; }
field() { "$PY" -c "import json,sys;d=json.load(sys.stdin);print(d.get(sys.argv[1],''))" "$1"; }

echo "=== f1_archives_verified.sh -- $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "EXPECTATIONS READ FROM: $TOMB (at the worktree, tracked)"
echo

TB_BUCKET=$(emit tarball_bucket)
TB_KEY=$(emit tarball_key)
TB_SIZE=$(emit tarball_size)
TB_ETAG=$(emit tarball_etag)
echo "--- THE TARBALL kuzu_db IS REPRODUCIBLE FROM ---"
echo "tombstone says: bucket=$TB_BUCKET key=$TB_KEY size=$TB_SIZE etag=$TB_ETAG"
TH=$($AWS s3api head-object --bucket "$TB_BUCKET" --key "$TB_KEY" --region us-east-1 --output json)
TH_RC=$?
echo "$TH"
TSZ=$(printf '%s' "$TH" | field ContentLength)
TET=$(printf '%s' "$TH" | field ETag | tr -d '"')
echo "head-object rc=$TH_RC size=$TSZ etag=$TET"
if [ "$TH_RC" -eq 0 ] && [ "$TSZ" = "$TB_SIZE" ] && [ "$TET" = "$TB_ETAG" ]; then
  echo "TARBALL_PRESENT=true size=$TSZ etag_match=true"
else
  echo "TARBALL_PRESENT=false size=$TSZ etag_match=false"
fi
echo

AR_BUCKET=$(emit archive_bucket)
KEYS=$(emit archive_keys | tr -d '[]"' | tr ',' '\n' | sed 's/^ *//;s/ *$//' | grep -v '^$')
NKEYS=$(printf '%s\n' "$KEYS" | grep -c .)
echo "--- THE ARCHIVE OBJECTS (bucket=$AR_BUCKET, $NKEYS key(s) named by the tombstone) ---"
OK=0
MATCH=0
for k in $KEYS; do
  ESZ=$(emit "archive_sha256|$k|size_bytes")
  ECK=$(emit "archive_sha256|$k|sha256_b64")
  EHX=$(emit "archive_sha256|$k|sha256_hex")
  echo "KEY $k"
  echo "  tombstone says: size=$ESZ sha256_hex=$EHX sha256_b64=$ECK"
  AH=$($AWS s3api head-object --bucket "$AR_BUCKET" --key "$k" --checksum-mode ENABLED --region us-east-1 --output json)
  AH_RC=$?
  ASZ=$(printf '%s' "$AH" | field ContentLength)
  ACK=$(printf '%s' "$AH" | field ChecksumSHA256)
  ALM=$(printf '%s' "$AH" | field LastModified)
  echo "  S3 says:        rc=$AH_RC size=$ASZ ChecksumSHA256=$ACK last_modified=$ALM"
  if [ "$AH_RC" -eq 0 ] && [ "$ASZ" = "$ESZ" ]; then OK=$((OK+1)); echo "  PRESENT_AND_SIZE_EQUAL=true"; else echo "  PRESENT_AND_SIZE_EQUAL=false"; fi
  if [ -n "$ACK" ] && [ "$ACK" = "$ECK" ]; then MATCH=$((MATCH+1)); echo "  SHA256_EQUAL=true"; else echo "  SHA256_EQUAL=false"; fi
done
echo

echo "--- NEGATIVE CONTROL: the same verb on a key that does not exist ---"
$AWS s3api head-object --bucket "$AR_BUCKET" --key "archive/NFRA_GLOBGRPH.ITEM-3/f1_no_such_object.db" --region us-east-1 --output json
echo "ABSENT_KEY_RC=$? (non-zero = head-object discriminates; a probe that returns 0 here proves nothing above)"
echo

echo "--- F1-AC2 VERDICT LINES ---"
if [ "$TH_RC" -eq 0 ] && [ "$TSZ" = "$TB_SIZE" ] && [ "$TET" = "$TB_ETAG" ]; then
  echo "TARBALL_PRESENT=true size=$TSZ"
else
  echo "TARBALL_PRESENT=false size=$TSZ"
fi
echo "ARCHIVE_OBJECTS=$OK of 2 sha256_match=$MATCH of 2"
if [ "$OK" -eq 2 ] && [ "$MATCH" -eq 2 ]; then
  echo "NOTE: both archive objects verified, so the local deletions in f1_after.txt were taken behind a satisfied guard."
else
  echo "NOTE: a mismatch here means the local files would NOT have been deleted -- see f1_after.txt, whose guards SKIP a deletion whose object does not verify."
fi
echo "=== f1_archives_verified.sh END ==="
