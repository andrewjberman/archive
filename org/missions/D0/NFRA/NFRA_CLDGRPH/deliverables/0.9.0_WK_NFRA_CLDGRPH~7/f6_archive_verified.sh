#!/usr/bin/env bash
# F6-AC2 -- THE ARCHIVE IS VERIFIED BY HEAD-OBJECT.
#
# Every expectation is read OUT OF THE TOMBSTONE (the tracked artifact a future
# reader holds), never out of the uploading script's memory, and the archive
# manifest is GOT BACK FROM S3 rather than read from the local copy -- the object
# a recoverer downloads is the one that has to carry the fields.
#
# The comparison that can FAIL: S3-computed ChecksumSHA256 over the bytes S3
# received  ==  the sha256 recorded in the tombstone before the upload. A
# negative control on a key that does not exist proves head-object discriminates.
set -u
cd "$(git rev-parse --show-toplevel)" || exit 3
TOMB=infra/aws/globgrph/kuzu_stitch_db.TOMBSTONE.md
D=org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~7
PARSE="$D/f6_tombstone_parse.py"
BUCKET=opal-313476888478-globgrph
PFX=archive/NFRA_CLDGRPH.CG-s-26
AWS=.tools/aws
PY=${PYTHON:-python}
SCRATCH=.scratch/f6
mkdir -p "$SCRATCH"

emit() { "$PY" "$PARSE" "$TOMB" --emit "$1"; }
field() { "$PY" -c "import json,sys;d=json.load(sys.stdin);print(d.get(sys.argv[1],''))" "$1"; }

echo "=== f6_archive_verified.sh -- $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "EXPECTATIONS READ FROM: $TOMB (tracked, at the worktree)"
echo "BUCKET=$BUCKET  PREFIX=$PFX"
echo

OK=0
MATCH=0
for name in kuzu_stitch_db kuzu_stitch_db._build_manifest.json stitch_graph.json ARCHIVE_MANIFEST.json; do
  KEY="$PFX/$name"
  ESZ=$(emit "archive_sha256|$KEY|size_bytes")
  ECK=$(emit "archive_sha256|$KEY|sha256_b64")
  EHX=$(emit "archive_sha256|$KEY|sha256_hex")
  echo "KEY $KEY"
  echo "  tombstone says: size=$ESZ sha256_hex=$EHX sha256_b64=$ECK"
  AH=$($AWS s3api head-object --bucket "$BUCKET" --key "$KEY" --checksum-mode ENABLED --region us-east-1 --output json)
  AH_RC=$?
  ASZ=$(printf '%s' "$AH" | field ContentLength)
  ACK=$(printf '%s' "$AH" | field ChecksumSHA256)
  ALM=$(printf '%s' "$AH" | field LastModified)
  echo "  S3 says:        rc=$AH_RC size=$ASZ ChecksumSHA256=$ACK last_modified=$ALM"
  if [ "$AH_RC" -eq 0 ] && [ -n "$ESZ" ] && [ "$ASZ" = "$ESZ" ]; then
    OK=$((OK+1)); echo "  PRESENT_AND_SIZE_EQUAL=true"
  else
    echo "  PRESENT_AND_SIZE_EQUAL=false"
  fi
  case "$name" in
    ARCHIVE_MANIFEST.json) echo "  (the manifest object itself -- counted in ARCHIVE_OBJECTS, not in SHA256_MATCH's 3 payloads; its own checksum is compared below)" ;;
    *)
      if [ -n "$ACK" ] && [ "$ACK" = "$ECK" ]; then MATCH=$((MATCH+1)); echo "  SHA256_EQUAL=true"; else echo "  SHA256_EQUAL=false"; fi ;;
  esac
  echo
done

echo "--- THE ARCHIVE MANIFEST, FETCHED BACK FROM S3 AND PARSED ---"
$AWS s3api get-object --bucket "$BUCKET" --key "$PFX/ARCHIVE_MANIFEST.json" \
    --region us-east-1 "$SCRATCH/ARCHIVE_MANIFEST.fromS3.json" --output json
echo "GET_RC=$?"
GOT_HEX=$(sha256sum "$SCRATCH/ARCHIVE_MANIFEST.fromS3.json" | cut -d' ' -f1)
EXP_HEX=$(emit "archive_sha256|$PFX/ARCHIVE_MANIFEST.json|sha256_hex")
echo "downloaded sha256=$GOT_HEX  tombstone says=$EXP_HEX"
if [ "$GOT_HEX" = "$EXP_HEX" ]; then echo "MANIFEST_ROUNDTRIP_SHA256_EQUAL=true"; else echo "MANIFEST_ROUNDTRIP_SHA256_EQUAL=false"; fi
HAS=$("$PY" - "$SCRATCH/ARCHIVE_MANIFEST.fromS3.json" <<'PYEOF'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
want = ["bytes_vs_manifest", "builder_last_hash", "sha256"]
have = [k for k in want if d.get(k) not in (None, "", [], {})]
print("ARCHIVE_MANIFEST_HAS=%s" % ",".join(have))
print("ARCHIVE_MANIFEST_MISSING=%s" % (",".join([k for k in want if k not in have]) or "NONE"))
print("  bytes_vs_manifest = %s" % d.get("bytes_vs_manifest"))
print("  builder_last_hash = %s" % d.get("builder_last_hash"))
print("  sha256 keys = %s" % ",".join(sorted((d.get("sha256") or {}).keys())))
PYEOF
)
echo "$HAS"
echo

echo "--- SHA256 AGREEMENT ACROSS THE THREE RECORDS (S3, tombstone, archive manifest) ---"
"$PY" - "$SCRATCH/ARCHIVE_MANIFEST.fromS3.json" <<'PYEOF'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
for k, v in sorted((d.get("sha256") or {}).items()):
    print("  manifest sha256[%s]=%s" % (k, v))
PYEOF
for name in kuzu_stitch_db kuzu_stitch_db._build_manifest.json stitch_graph.json; do
  echo "  tombstone sha256[$name]=$(emit "archive_sha256|$PFX/$name|sha256_hex")"
done
echo

echo "--- NEGATIVE CONTROL: the same verb on a key that does not exist ---"
$AWS s3api head-object --bucket "$BUCKET" --key "$PFX/f6_no_such_object.db" --region us-east-1 --output json
echo "ABSENT_KEY_RC=$? (non-zero = head-object discriminates; a probe returning 0 here proves nothing above)"
echo

echo "--- F6-AC2 VERDICT LINES ---"
echo "ARCHIVE_OBJECTS=$OK of 4"
echo "SHA256_MATCH=$MATCH of 3"
echo "$HAS" | grep '^ARCHIVE_MANIFEST_HAS='
echo "=== f6_archive_verified.sh END ==="
