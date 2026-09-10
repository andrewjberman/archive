#!/usr/bin/env bash
# F6-AC5 -- THE TOMBSTONE CARRIES EVERY FIELD, AND THE REGISTRY MENTIONS ARE DISPOSITIONED.
#
# The tombstone's fenced json block is PARSED (not grepped) for the seven fields
# the criterion names, and the SAME parser is run against a planted specimen that
# is complete except for served_source. If the planted specimen passes, this
# probe cannot tell a good tombstone from a bad one.
#
# The registry half is a census of the three carriers the order names plus the
# generated mirror of the first, at two grains (TOTAL_MENTIONS and the subset
# R14/R15 leave open), with the R14 entry-grain question answered by LOADING the
# yaml rather than grepping it.
set -u
cd "$(git rev-parse --show-toplevel)" || exit 3
TOMB=infra/aws/globgrph/kuzu_stitch_db.TOMBSTONE.md
D=org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~7
PARSE="$D/f6_tombstone_parse.py"
PLANT="$D/f6_plant/planted_tombstone_missing_field.md"
CENSUS="$D/f6_registry_census.py"
PY=${PYTHON:-python}
FIELDS=archive_keys,archive_sha256,manifest,bytes_vs_manifest,served_source,builder_last_hash,authority
ROW=NFRA_CLDGRPH-W7-S2

echo "=== f6_tombstone.sh -- $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "HEAD=$(git rev-parse HEAD)  BRANCH=$(git rev-parse --abbrev-ref HEAD)"
echo

echo "--- IS IT THERE, AND IS IT TRACKED? ---"
if [ -f "$TOMB" ]; then P=true; else P=false; fi
echo "worktree test -f $TOMB -> $P"
if git ls-files --error-unmatch "$TOMB"; then TRACKED=true; else TRACKED=false; fi
echo "git ls-files --error-unmatch -> tracked=$TRACKED"
echo "size_bytes=$(wc -c < "$TOMB")"
echo

echo "--- THE REAL TOMBSTONE, PARSED ---"
REAL=$("$PY" "$PARSE" "$TOMB")
echo "$REAL"
REAL_MISSING=$(printf '%s\n' "$REAL" | sed -n 's/^MISSING_FIELDS=//p')
REAL_N=$(printf '%s\n' "$REAL" | sed -n 's/^FIELDS_PRESENT=\([0-9]*\) of 7/\1/p')
echo

echo "--- THE PLANTED SPECIMEN (complete except served_source) ---"
CTRL=$("$PY" "$PARSE" "$PLANT")
echo "$CTRL"
CTRL_MISSING=$(printf '%s\n' "$CTRL" | sed -n 's/^MISSING_FIELDS=//p')
echo

echo "--- THE REGISTRY CENSUS ---"
CEN=$("$PY" "$CENSUS")
echo "$CEN"
TOTAL=$(printf '%s\n' "$CEN" | sed -n 's/^TOTAL_MENTIONS=\([0-9]*\) across.*/\1/p')
NEED=$(printf '%s\n' "$CEN" | sed -n 's/^MENTIONS_NEEDING_DISPOSITION=\([0-9]*\)/\1/p')
echo

echo "--- F6-AC5 VERDICT LINES ---"
if [ "$P" = true ] && [ "$TRACKED" = true ]; then
  echo "TOMBSTONE_PRESENT=true"
else
  echo "TOMBSTONE_PRESENT=false (worktree=$P tracked=$TRACKED)"
fi
if [ "$REAL_MISSING" = "NONE" ] && [ "${REAL_N:-0}" -eq 7 ]; then
  echo "TOMBSTONE_NAMES=$FIELDS"
else
  echo "TOMBSTONE_INCOMPLETE missing=$REAL_MISSING present=$REAL_N of 7"
fi
if [ "$CTRL_MISSING" = "served_source" ]; then
  echo "TOMBSTONE_PROBE_CONTROL=FIRED  (the planted specimen was caught, missing exactly served_source)"
else
  echo "TOMBSTONE_PROBE_CONTROL=DEAD  (the planted specimen reported missing='$CTRL_MISSING')"
fi
echo "REGISTRY_MENTIONS_TOTAL=$TOTAL (the denominator: every mention in the four carriers)"
if [ "${NEED:-0}" -eq 0 ]; then
  echo "REGISTRY_MENTIONS=0 (none)"
else
  echo "REGISTRY_MENTIONS=$NEED (row $ROW)"
  echo "  -- both sites are OUTSIDE this order's <paths> grant, so the disposition is a ROW"
  echo "     naming file and line, never an edit. Row id namespace is W7 because this order"
  echo "     was RE-ADDRESSED from slot ~2 to slot ~7 at 22:3xZ; slot ~7's rows mint W7-S<k>."
fi
echo "=== f6_tombstone.sh END ==="
