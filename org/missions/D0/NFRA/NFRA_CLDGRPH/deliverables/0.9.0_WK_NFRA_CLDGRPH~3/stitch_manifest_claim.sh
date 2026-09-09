#!/usr/bin/env bash
# E4-AC3 -- THE MANIFEST CARRIES ITS CLAIM (S53).
#
# REAL: kuzu_stitch_load.py's manifest-writing function stamps both claim
# keywords, and the MAIN WORKSPACE manifest carries both fields -- with the
# store's bytes and mtime printed beside the task order's census constants
# (9,170,944 @ 2026-08-27 02:32 local), because a manifest edit that moved the
# artifact would not be a manifest edit.
#
# CONTROL: the same instrument against a decoy builder with the claim call
# stripped and a decoy store whose manifest lacks both fields.
set -u
cd "$(git rev-parse --show-toplevel)" || exit 3
D=org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~3
PY=${PYTHON:-python}
STORE='C:\Users\AndrewBerman\Desktop\ajb_workspace\infra\aws\globgrph\kuzu_stitch_db'

echo "=== E4-AC3 stitch_manifest_claim.sh -- run at $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "HEAD=$(git rev-parse --short HEAD)  BRANCH=$(git rev-parse --abbrev-ref HEAD)"
echo

REAL=$("$PY" "$D/_stitch_claim.py" --builder infra/aws/globgrph/kuzu_stitch_load.py \
        --store "$STORE" --expect-bytes 9170944 --expect-mtime '2026-08-27 02:32' --label REAL)
echo "$REAL"
echo

C=$(git rev-parse --show-toplevel)/.scratch/e4_ac3_control
rm -rf "$C"; mkdir -p "$C"
"$PY" - "$C" <<'PYEOF'
import io, re, sys
c = sys.argv[1]
src = io.open("infra/aws/globgrph/kuzu_stitch_load.py", encoding="utf-8").read()
src = re.sub(r"\n *_stamp_claim\(\n(?:.*\n)*? *\)\n", "\n", src, count=1)
io.open(c + "/decoy_builder.py", "w", encoding="utf-8", newline="\n").write(src)
io.open(c + "/kuzu_stitch_db", "w", encoding="utf-8", newline="\n").write("decoy")
io.open(c + "/kuzu_stitch_db._build_manifest.json", "w", encoding="utf-8",
        newline="\n").write('{"edge_count": 5329, "node_count": 3414}\n')
PYEOF
CTRL=$("$PY" "$D/_stitch_claim.py" --builder "$C/decoy_builder.py" \
        --store "$C/kuzu_stitch_db" --expect-bytes 9170944 \
        --expect-mtime '2026-08-27 02:32' --label CONTROL)
echo "$CTRL"
echo

CB=$(printf '%s\n' "$CTRL" | sed -n 's/^BUILDER_STAMPS_CLAIM=//p')
CF=$(printf '%s\n' "$CTRL" | sed -n 's/^MANIFEST_CLAIM_FIELDS=\([0-9]*\) of.*/\1/p')
CU=$(printf '%s\n' "$CTRL" | grep -c 'UNCHANGED=False')
echo "--- CONTROL GRADING ---"
echo "decoy builder -> BUILDER_STAMPS_CLAIM=$CB (must be false)"
echo "decoy manifest -> MANIFEST_CLAIM_FIELDS=$CF of 2 (must be 0)"
echo "decoy store    -> UNCHANGED=False lines=$CU (must be 1: the byte/mtime comparator can fail)"
if [ "$CB" = "false" ] && [ "${CF:-9}" -eq 0 ] && [ "${CU:-0}" -eq 1 ]; then
  echo "CLAIM_PROBE_CONTROL=FIRED"
else
  echo "CLAIM_PROBE_CONTROL=DEAD"
fi
echo

echo "--- E4-AC3 VERDICT LINES ---"
printf '%s\n' "$REAL" | sed -n 's/^BUILDER_STAMPS_CLAIM=/BUILDER_STAMPS_CLAIM=/p'
printf '%s\n' "$REAL" | sed -n 's/^MANIFEST_CLAIM_FIELDS=/MANIFEST_CLAIM_FIELDS=/p'
printf '%s\n' "$REAL" | grep '  STORE bytes='
