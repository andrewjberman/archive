#!/usr/bin/env bash
# E3-AC3 -- NOTHING DELETED, NOTHING REBUILT.
#
# The four dispositioned artifacts are still present in the MAIN WORKSPACE by
# absolute path, and the two STORE files carry the size and mtime the issuer
# censused at the cut. The expected values are CONSTANTS taken from the task
# order (not re-derived from this run), so the check can FAIL: change either
# store's bytes or its mtime and STORE_BYTES_UNCHANGED drops below 2 of 2.
#
# A MANIFEST edit is expected by this order and is NOT a store: the manifests
# are reported separately, outside the 2-of-2 denominator.
set -u
W=/c/Users/AndrewBerman/Desktop/ajb_workspace/infra/aws/globgrph
LOCK=.kuzu_nessie_load.0628067ab4da5610.lock

echo "=== E3-AC3 stores_untouched.sh -- run at $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "MAIN WORKSPACE DIR: $W"
echo

# ---- presence: the four dispositioned artifacts -----------------------------
ARTIFACTS="kuzu_db kuzu_load.py kuzu_ac7.db $LOCK"
present=0
total=0
for a in $ARTIFACTS; do
  total=$((total + 1))
  if [ -e "$W/$a" ]; then
    present=$((present + 1))
    echo "  PRESENT   $W/$a  ($(stat -c '%s bytes, mtime %y' "$W/$a"))"
  else
    echo "  ABSENT    $W/$a"
  fi
done
echo
echo "SUPPLEMENTARY (not in the 4-of-4 denominator -- a manifest and an empty dir,"
echo "carried by their store's disposition, not dispositioned on their own):"
for a in kuzu_db._build_manifest.json kuzu_ac7 kuzu_ac7.db._build_manifest.json; do
  if [ -e "$W/$a" ]; then
    echo "  PRESENT   $W/$a  ($(stat -c '%s bytes, mtime %y' "$W/$a"))"
  else
    echo "  ABSENT    $W/$a"
  fi
done
echo

# ---- bytes + mtime, against the CUT's census --------------------------------
# name|expected_bytes|expected_local_mtime (task order, MEASURED BY THE ISSUER)
EXPECT="kuzu_db|9224192|2026-06-12 09:55
kuzu_ac7.db|4050944|2026-06-12 10:57"

check_one() {
  # $1 abs path, $2 expected bytes, $3 expected 'YYYY-MM-DD HH:MM' local
  _p=$1; _eb=$2; _em=$3
  if [ ! -e "$_p" ]; then echo "  MISSING  $_p"; return 1; fi
  _ab=$(stat -c '%s' "$_p")
  _ae=$(stat -c '%Y' "$_p")
  _am=$(date -d "@$_ae" +'%Y-%m-%d %H:%M')
  if [ "$_ab" = "$_eb" ] && [ "$_am" = "$_em" ]; then
    echo "  UNCHANGED $_p  bytes=$_ab (expected $_eb)  mtime='$_am' (expected '$_em')"
    return 0
  fi
  echo "  CHANGED   $_p  bytes=$_ab (expected $_eb)  mtime='$_am' (expected '$_em')"
  return 1
}

unchanged=0
denom=0
echo "STORE BYTES + MTIME vs the cut's census (2026-09-09 ~15:3xZ):"
while IFS='|' read -r n eb em; do
  [ -z "$n" ] && continue
  denom=$((denom + 1))
  if check_one "$W/$n" "$eb" "$em"; then unchanged=$((unchanged + 1)); fi
done <<EOF
$EXPECT
EOF
echo

# ---- the comparator's negative control --------------------------------------
CTRLDIR=$(git rev-parse --show-toplevel)/.scratch/e3_ac3_control
mkdir -p "$CTRLDIR"
printf 'not a store' > "$CTRLDIR/decoy_store"
if check_one "$CTRLDIR/decoy_store" 9224192 '2026-06-12 09:55' >/dev/null; then
  echo "COMPARATOR_CONTROL=DEAD  (a decoy with the wrong bytes and mtime passed the same comparator)"
else
  echo "COMPARATOR_CONTROL=FIRED (a decoy file with the wrong bytes and mtime was REJECTED by the same comparator)"
fi
rm -f "$CTRLDIR/decoy_store"
echo

echo "--- E3-AC3 VERDICT LINES ---"
echo "STORES_PRESENT=$present of $total"
echo "STORE_BYTES_UNCHANGED=$unchanged of $denom"
