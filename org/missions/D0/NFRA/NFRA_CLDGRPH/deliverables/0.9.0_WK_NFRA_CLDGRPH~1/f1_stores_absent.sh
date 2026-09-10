#!/usr/bin/env bash
# F1-AC1 -- BOTH STORES ABSENT ON THIS DEVICE.
#
# ls -d by ABSOLUTE path in the main workspace on the two stores, their two
# manifests and the empty kuzu_ac7/ directory, beside a POSITIVE CONTROL: an
# ls -d on projection_client.py IN THE SAME DIRECTORY, which is present. Without
# the control an absent DIRECTORY and an absent FILE read identically, and so
# does a mistyped path.
set -u
W=C:/Users/AndrewBerman/Desktop/ajb_workspace/infra/aws/globgrph

echo "=== f1_stores_absent.sh -- $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "SCOPE=$W (the MAIN workspace; the stores were never tracked in git)"
echo

N=0
echo "--- THE TWO STORES ---"
for p in "$W/kuzu_db" "$W/kuzu_ac7.db"; do
  if ls -d "$p" 2>&1; then N=$((N+1)); echo "  -> PRESENT"; else echo "  -> ABSENT $p"; fi
done
echo
echo "--- THEIR MANIFESTS AND THE EMPTY DIRECTORY (printed, not counted in the 2) ---"
for p in "$W/kuzu_db._build_manifest.json" "$W/kuzu_ac7.db._build_manifest.json" "$W/kuzu_ac7"; do
  if ls -d "$p" 2>&1; then echo "  -> PRESENT $p"; else echo "  -> ABSENT $p"; fi
done
echo
echo "--- POSITIVE CONTROL: a path that IS present in the same directory ---"
if ls -d "$W/projection_client.py"; then
  echo "STORE_PROBE_CONTROL=FIRED  (ls -d resolves this directory and prints a present path, so the two ABSENTs above are readings, not a broken probe)"
else
  echo "STORE_PROBE_CONTROL=DEAD  (ls -d could not print a path known to be present -- the ABSENTs above are worthless)"
fi
echo
echo "--- F1-AC1 VERDICT LINES ---"
echo "STORES_PRESENT=$N of 2"
if ls -d "$W/projection_client.py" >/dev/null 2>&1; then
  echo "STORE_PROBE_CONTROL=FIRED"
else
  echo "STORE_PROBE_CONTROL=DEAD"
fi
echo "=== f1_stores_absent.sh END ==="
