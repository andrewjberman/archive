#!/usr/bin/env bash
# F6-AC1 -- THE STORE, ITS MANIFEST AND THE LOCAL SCRATCH ARE ABSENT ON THIS DEVICE.
#
# ls -d by ABSOLUTE path in the MAIN workspace (the three files were gitignored
# and lived there only; a worktree read would be the wrong object), beside a
# POSITIVE CONTROL: an ls -d on a sibling in the SAME directory that is present.
# Without the control an absent file, a mistyped path and an unreadable directory
# all print the same thing.
set -u
W=C:/Users/AndrewBerman/Desktop/ajb_workspace/infra/aws/globgrph

echo "=== f6_store_absent.sh -- $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "SCOPE=$W (the MAIN workspace; these three were never tracked in git)"
echo

N=0
echo "--- THE THREE ---"
for p in "$W/kuzu_stitch_db" "$W/kuzu_stitch_db._build_manifest.json" "$W/stitch_graph.json"; do
  if ls -d "$p"; then N=$((N+1)); echo "  -> PRESENT"; else echo "  -> ABSENT $p"; fi
done
echo
echo "--- THE WAL NAME THE .gitignore ALSO CARRIES (printed, not counted in the 3) ---"
if ls -d "$W/kuzu_stitch_db.wal"; then echo "  -> PRESENT"; else echo "  -> ABSENT $W/kuzu_stitch_db.wal"; fi
echo

echo "--- POSITIVE CONTROLS: paths that ARE present in the same directory ---"
CTRL=0
for p in "$W/projection_client.py" "$W/derive_stitch.py"; do
  if ls -d "$p"; then CTRL=$((CTRL+1)); fi
done
echo "controls_resolved=$CTRL of 2"
echo

echo "--- F6-AC1 VERDICT LINES ---"
echo "STITCH_STORE_PRESENT=$N of 3 files"
if [ "$CTRL" -eq 2 ]; then
  echo "STORE_PROBE_CONTROL=FIRED  (ls -d resolves this directory and prints two present paths, so the ABSENTs above are readings and not a broken probe)"
else
  echo "STORE_PROBE_CONTROL=DEAD  (ls -d could not print paths known to be present -- the ABSENTs above are worthless)"
fi
echo "=== f6_store_absent.sh END ==="
