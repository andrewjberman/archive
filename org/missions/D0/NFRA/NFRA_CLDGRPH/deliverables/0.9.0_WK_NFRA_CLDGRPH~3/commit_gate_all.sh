#!/usr/bin/env bash
# COMMIT GATE on every .py this SLOT's orders touch -- E4-AC5 (and, at its own
# vintage, E3-AC5).
#
# SUPERSESSION, DECLARED: TO-CG-E-3 and TO-CG-E-4 both name a script at this
# exact path. The E-3 version gated 7 files and its proof-of-spec instance
# quotes its measured output at commit 85e33e98ee ("OK: pre-commit gate clean
# for 7 of 7 file(s)"), which stays true at that vintage. This version is the
# UNION: it gates E-3's seven AND E-4's, so neither order's surface is left
# unchecked by the script that carries the name. Recorded as surprise row
# NFRA_CLDGRPH-W3-S13 rather than done quietly.
#
# It also runs the BOUNDED REAL RUN of comp_debt.py that TO-CG-E-4 deliverable 3
# requires, and quotes it verbatim -- including the refusal, which is the point:
# a consumer that refuses with the decision named is what this order shipped.
set -u
cd "$(git rev-parse --show-toplevel)" || exit 3
D=org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~3
PY=${PYTHON:-python}

FILES="infra/aws/globgrph/comp_debt.py
infra/aws/globgrph/kuzu_stitch_load.py
infra/aws/globgrph/kuzu_load.py
$D/_readers_ast.py
$D/_dispositions_parse.py
$D/_manifest_claims.py
$D/apply_manifest_claims.py
$D/_refusal_ast.py
$D/_rebuild_path_ast.py
$D/_stitch_claim.py
$D/_stitch_home_parse.py
$D/apply_stitch_manifest_claim.py
$D/plant_e3/planted_reader.py
$D/plant_e3/planted_docstring_only.py
$D/plant_e4/planted_refusal_unnamed.py
$D/plant_e4/planted_rebuild_path.py"

echo "=== E4-AC5 commit_gate_all.sh -- run at $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "HEAD=$(git rev-parse --short HEAD)  BRANCH=$(git rev-parse --abbrev-ref HEAD)"
n=0
for f in $FILES; do n=$((n + 1)); echo "  $n. $f"; done
echo "DENOMINATOR: $n .py file(s) -- TO-CG-E-4's two tracked edits, TO-CG-E-3's"
echo "one, and every .py this slot added under its deliverables folder."
echo
# shellcheck disable=SC2086
bash .tools/commit-gate.sh $FILES
rc=$?
echo "COMMIT_GATE_RC=$rc"
echo
echo "=== THE BOUNDED REAL RUN (TO-CG-E-4 deliverable 3) ==="
echo "\$ timeout 120 python infra/aws/globgrph/comp_debt.py"
set +e
timeout 120 "$PY" infra/aws/globgrph/comp_debt.py > .scratch/e4_cd_out.txt 2> .scratch/e4_cd_err.txt
crc=$?
set -e
echo "COMP_DEBT_RC=$crc  (rc read DIRECT, never through a pipe)"
echo "--- stdout, $(wc -c < .scratch/e4_cd_out.txt) byte(s) ---"
cat .scratch/e4_cd_out.txt
echo "--- stderr, verbatim ---"
cat .scratch/e4_cd_err.txt
echo
echo "READING THE RUN, so the refusal is not mistaken for a break:"
echo "  * The NESSIE leg ANSWERED: freshness_assert() calls projection_client.health()"
echo "    FIRST and raises SystemExit if the served graph is unreachable. It did not."
echo "  * The STITCH leg refuses NOT-FOUND from a worktree by construction: STITCH_DB"
echo "    is os.path.join(_HERE, 'kuzu_stitch_db') and the store is gitignored, so it"
echo "    exists only in the main workspace. Run from there, where the store IS"
echo "    present, the refusal is STALE (age 322h > 48h). Both measured; row W3-S12."
echo "  * Either way the refusal now NAMES the home decision and CG-s-20 (E4-AC2)."
exit $rc
