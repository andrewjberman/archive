#!/usr/bin/env bash
# F1-AC4 -- THE TOMBSTONE CARRIES EVERY FIELD A READER NEEDS.
#
# The tombstone is TRACKED at infra/aws/globgrph/kuzu_db.TOMBSTONE.md; the
# stores it describes never were. Its fenced json block is PARSED (not grepped)
# for eight fields, and the same parser is run against a PLANTED specimen that
# is complete except for archive_sha256. If the planted specimen passes, this
# probe cannot tell a good tombstone from a bad one and the real PASS is a
# constant.
set -u
cd "$(git rev-parse --show-toplevel)" || exit 3
TOMB=infra/aws/globgrph/kuzu_db.TOMBSTONE.md
D=org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~1
PARSE="$D/f1_tombstone_parse.py"
PLANT="$D/f1_plant/planted_tombstone_missing_field.md"
PY=${PYTHON:-python}
FIELDS=tarball_key,tarball_size,tarball_etag,manifest,archive_keys,archive_sha256,builder_last_hash,authority

echo "=== f1_tombstone.sh -- $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "HEAD=$(git rev-parse HEAD)  BRANCH=$(git rev-parse --abbrev-ref HEAD)"
echo

echo "--- IS IT THERE, AND IS IT TRACKED? ---"
if [ -f "$TOMB" ]; then P=true; else P=false; fi
echo "worktree test -f $TOMB -> $P"
git ls-files --error-unmatch "$TOMB" && TRACKED=true || TRACKED=false
echo "git ls-files --error-unmatch -> tracked=$TRACKED"
echo "size_bytes=$(wc -c < "$TOMB")"
echo

echo "--- THE REAL TOMBSTONE, PARSED ---"
REAL=$("$PY" "$PARSE" "$TOMB")
echo "$REAL"
REAL_MISSING=$(printf '%s\n' "$REAL" | sed -n 's/^MISSING_FIELDS=//p')
REAL_N=$(printf '%s\n' "$REAL" | sed -n 's/^FIELDS_PRESENT=\([0-9]*\) of 8/\1/p')
echo

echo "--- THE PLANTED SPECIMEN (complete except archive_sha256) ---"
CTRL=$("$PY" "$PARSE" "$PLANT")
echo "$CTRL"
CTRL_MISSING=$(printf '%s\n' "$CTRL" | sed -n 's/^MISSING_FIELDS=//p')
echo

echo "--- F1-AC4 VERDICT LINES ---"
if [ "$P" = true ] && [ "$TRACKED" = true ]; then
  echo "TOMBSTONE_PRESENT=true"
else
  echo "TOMBSTONE_PRESENT=false (worktree=$P tracked=$TRACKED)"
fi
if [ "$REAL_MISSING" = "NONE" ] && [ "${REAL_N:-0}" -eq 8 ]; then
  echo "TOMBSTONE_NAMES=$FIELDS"
else
  echo "TOMBSTONE_INCOMPLETE missing=$REAL_MISSING present=$REAL_N of 8"
fi
if [ "$CTRL_MISSING" = "archive_sha256" ]; then
  echo "TOMBSTONE_PROBE_CONTROL=FIRED  (the planted specimen was caught, missing exactly archive_sha256)"
else
  echo "TOMBSTONE_PROBE_CONTROL=DEAD  (the planted specimen reported missing='$CTRL_MISSING' -- the checker cannot discriminate)"
fi
echo "=== f1_tombstone.sh END ==="
