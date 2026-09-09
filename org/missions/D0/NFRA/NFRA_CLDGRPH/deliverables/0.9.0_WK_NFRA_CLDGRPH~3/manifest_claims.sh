#!/usr/bin/env bash
# E3-AC4 -- A STORE THAT STAYS CARRIES ITS CLAIM (S53).
#
# REAL run: the builder infra/aws/globgrph/kuzu_load.py (ast read of the
# keyword arguments at its manifest-writing call site) and the MAIN WORKSPACE
# manifests of every store the disposition record leaves standing.
#
# CONTROL run: the same instrument against a DECOY builder with the claim call
# stripped and a DECOY store root whose manifests lack the fields. Both halves
# must come back false/short, or the REAL true is a constant.
set -u
cd "$(git rev-parse --show-toplevel)" || exit 3
D=org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~3
PY=${PYTHON:-python}
REC="$D/CG-s-19.residual-stores.result.md"
W=/c/Users/AndrewBerman/Desktop/ajb_workspace/infra/aws/globgrph

echo "=== E3-AC4 manifest_claims.sh -- run at $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "HEAD=$(git rev-parse --short HEAD)  BRANCH=$(git rev-parse --abbrev-ref HEAD)"
echo

REAL=$("$PY" "$D/_manifest_claims.py" --builder infra/aws/globgrph/kuzu_load.py \
        --record "$REC" --label REAL)
echo "$REAL"
echo

# ---- the control ------------------------------------------------------------
C=$(git rev-parse --show-toplevel)/.scratch/e3_ac4_control
rm -rf "$C"; mkdir -p "$C"
# decoy builder: the real builder with the _stamp_claim call removed
"$PY" - "$C" <<'PYEOF'
import io, re, sys
c = sys.argv[1]
src = io.open("infra/aws/globgrph/kuzu_load.py", encoding="utf-8").read()
src = re.sub(r"\n *_stamp_claim\(\n(?:.*\n)*? *\)\n", "\n", src, count=1)
io.open(c + "/decoy_builder.py", "w", encoding="utf-8", newline="\n").write(src)
io.open(c + "/kuzu_db._build_manifest.json", "w", encoding="utf-8",
        newline="\n").write('{"edge_count": 2488, "node_count": 1166}\n')
io.open(c + "/kuzu_ac7.db._build_manifest.json", "w", encoding="utf-8",
        newline="\n").write('{"artifact_claim": "historical"}\n')
PYEOF
CTRL=$("$PY" "$D/_manifest_claims.py" --builder "$C/decoy_builder.py" \
        --record "$REC" --store-root "$C" --label CONTROL)
echo "$CTRL"
echo

CB=$(printf '%s\n' "$CTRL" | sed -n 's/^BUILDER_STAMPS_CLAIM=//p')
CS=$(printf '%s\n' "$CTRL" | sed -n 's/^MANIFEST_CLAIM_FIELDS=\([0-9]*\) of.*/\1/p')
echo "--- CONTROL GRADING ---"
echo "decoy builder (claim call stripped) -> BUILDER_STAMPS_CLAIM=$CB (must be false)"
echo "decoy manifests (one lacks both fields, one lacks edge_count_claim) ->"
echo "  MANIFEST_CLAIM_FIELDS=$CS of 2 (must be 0)"
if [ "$CB" = "false" ] && [ "${CS:-9}" -eq 0 ]; then
  echo "MANIFEST_CLAIM_CONTROL=FIRED"
else
  echo "MANIFEST_CLAIM_CONTROL=DEAD"
fi
echo

echo "--- E3-AC4 VERDICT LINES ---"
printf '%s\n' "$REAL" | sed -n 's/^BUILDER_STAMPS_CLAIM=/BUILDER_STAMPS_CLAIM=/p'
printf '%s\n' "$REAL" | sed -n 's/^MANIFEST_CLAIM_FIELDS=/MANIFEST_CLAIM_FIELDS=/p'
echo "NOTE: the denominator is the STAYING stores only. Any store dispositioned"
echo "RETIRE_WITH_TOMBSTONE is printed as EXCLUDED above and is not counted; if"
echo "every store were retired the instrument prints that the 0-of-0 is VACUOUS."
echo "MAIN WORKSPACE store root: $W"
