#!/usr/bin/env bash
# TO-CG-F-2 step 1 -- THE LOCAL-COPY CENSUS, BOTH READS, WITH THE CONTROL.
#
# Two reads of two different trees: the MAIN workspace by ABSOLUTE path (the
# machine's own checkout, which is what "no local copy on this machine" means)
# and this worktree. The CONTROL is kuzu_stitch_db, which is DELIBERATELY still
# present -- it is S26's, LAST in its chain, CG-s-20's question, and it is not
# the canonical graph. Without it a zero from a mistyped path and a zero from a
# clean machine read identically.
#
# The face's F2-AC3 invocation is run VERBATIM here as its own line so the
# criterion's own number is visible beside the fuller reading.
set -u
W=C:/Users/AndrewBerman/Desktop/ajb_workspace/infra/aws/globgrph
PAT='kuzu_nessie_db|kuzu_db|kuzu_ac7'

echo "=== f2_census.sh -- $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "HEAD=$(git rev-parse HEAD)  BRANCH=$(git rev-parse --abbrev-ref HEAD)"
echo

echo "--- (1) THE MAIN WORKSPACE, BY ABSOLUTE PATH -- F2-AC3's own invocation, verbatim ---"
echo "ls $W/ | grep -c -E '$PAT'"
MAIN=$(ls "$W/" | grep -c -E "$PAT")
echo "MAIN_WORKSPACE_COUNT=$MAIN"
echo "  the matching name(s), printed rather than summarised:"
ls "$W/" | grep -E "$PAT" | sed 's/^/    /'
echo

echo "--- (2) THIS WORKTREE, the second read ---"
WT=$(ls infra/aws/globgrph/ | grep -c -E "$PAT")
echo "WORKTREE_COUNT=$WT"
ls infra/aws/globgrph/ | grep -E "$PAT" | sed 's/^/    /'
echo

echo "--- (3) THE CONTROL: kuzu_stitch_db, deliberately still present (S26's, CG-s-20's question) ---"
CTRL=$(ls "$W/" | grep -c 'kuzu_stitch_db')
echo "CONTROL_STITCH_COUNT=$CTRL"
ls -la "$W/" | grep 'kuzu_stitch' | sed 's/^/    /'
if [ "$CTRL" -ge 1 ]; then
  echo "CENSUS_PROBE_CONTROL=FIRED  (the ls+grep instrument returns NON-ZERO on a name that IS there, so a zero above is a reading and not a broken path)"
else
  echo "CENSUS_PROBE_CONTROL=DEAD  (the instrument could not find a file known to be present -- every zero above is worthless)"
fi
echo

echo "--- (4) THE STORES THEMSELVES, by absolute ls -d (F-1 deleted them) ---"
for p in "$W/kuzu_db" "$W/kuzu_ac7.db" "$W/kuzu_nessie_db"; do
  if ls -d "$p" 2>&1; then echo "    -> PRESENT"; else echo "    -> ABSENT $p"; fi
done
echo

echo "--- F2 CENSUS VERDICT LINES ---"
echo "LOCAL_DB_MAIN_WORKSPACE=$MAIN"
echo "LOCAL_DB_WORKTREE=$WT"
echo "CONTROL_STITCH_COUNT=$CTRL"
echo "=== f2_census.sh END ==="
