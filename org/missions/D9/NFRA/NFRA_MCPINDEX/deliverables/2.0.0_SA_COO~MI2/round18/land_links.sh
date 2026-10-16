#!/usr/bin/env bash
# land_links.sh <deployed-tools.json> -- the issuer's release-day step: regenerate the silver rows with the RELEASED tool list and the 34 read links, in the shared tree,
# print what changed, then grade it with c40. Run from anywhere in the repo, after OG-ap-23 reads live. It writes only workflows/atom_decomposition/catalog_entries/.
# Nothing is committed here: review `git status`, then commit the changed rows with safe-commit.
set -uo pipefail
D="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(git -C "$D" rev-parse --show-toplevel)" || exit 9
cd "$ROOT" || exit 9
DEP="${1:?usage: land_links.sh <deployed-tools.json>}"
[ -f "$DEP" ] || { echo "ERROR: $DEP not found"; exit 9; }
R=org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables
PIN=$R/0.9.0_WK_NFRA_MCPINDEX~38
python workflows/atom_decomposition/gen_silver_rows.py --g2 $PIN/G2_pinned.md --g4 $PIN/G4_pinned.md --g5 $PIN/G5_pinned.md --g6 $PIN/G6_pinned.md \
  --g3 $PIN/G3_pinned.md --g2f $PIN/G2f_pinned.md --out workflows/atom_decomposition/catalog_entries --deployed-tools "$DEP" \
  --read-links $R/2.0.0_SA_COO~MI2/round18/read_links.json --firm-map $R/2.0.0_SA_COO~MI/round17/f1_firm_map.json | tail -2 || exit 1
echo "--- changed row files:"; git status --short workflows/atom_decomposition/catalog_entries | tee /dev/stderr | wc -l
C40_DEPLOYED="$DEP" bash $R/2.0.0_SA_COO~MI2/round18/checks/c40.landed.sh
