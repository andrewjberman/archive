#!/usr/bin/env bash
# land_links.sh <deployed-tools.json> [out-dir] -- the issuer's release-day step: regenerate the silver rows with the RELEASED tool list, the 34 read links, the ASSETS issuer's 31 (assets_read_links.json, 74e243fe48) and the
# ASSETS issuer's unskip file (2.0.0_SA_COO~MI msg 34772: without it the 12 Schwab dim tables are skipped and never get a read_tool), in the repo, print what changed, then grade it with c40.
# With no out-dir it LANDS in workflows/atom_decomposition/catalog_entries/ (the working tree). A DRY RUN names a temp out-dir: nothing in the repo is written, the change list is the temp
# folder's row count. Nothing is committed here: review `git status`, then commit the changed rows with safe-commit.
set -uo pipefail
D="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(git -C "$D" rev-parse --show-toplevel)" || exit 9
cd "$ROOT" || exit 9
DEP="${1:?usage: land_links.sh <deployed-tools.json> [out-dir]}"
OUT="${2:-}"
[ -f "$DEP" ] || { echo "ERROR: $DEP not found"; exit 9; }
R=org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables
PIN=$R/0.9.0_WK_NFRA_MCPINDEX~38
LAND=0
if [ -z "$OUT" ]; then OUT=workflows/atom_decomposition/catalog_entries; LAND=1; fi
python workflows/atom_decomposition/gen_silver_rows.py --g2 $PIN/G2_pinned.md --g4 $PIN/G4_pinned.md --g5 $PIN/G5_pinned.md --g6 $PIN/G6_pinned.md \
  --g3 $PIN/G3_pinned.md --g2f $PIN/G2f_pinned.md --out "$OUT" --deployed-tools "$DEP" --unskip $R/2.0.0_SA_COO~MI/round18/unskip_schwab_dim.json \
  --read-links $R/2.0.0_SA_COO~MI2/round18/read_links.json --read-links $R/2.0.0_SA_COO~MI/round18/assets_read_links.json --firm-map $R/2.0.0_SA_COO~MI/round17/f1_firm_map.json | tail -2 || exit 1
if [ "$LAND" = 1 ]; then
  echo "--- changed row files:"; git status --short workflows/atom_decomposition/catalog_entries | tee /dev/stderr | wc -l
  C40_DEPLOYED="$DEP" bash $R/2.0.0_SA_COO~MI2/round18/checks/c40.landed.sh
else
  echo "--- DRY RUN: $(ls "$OUT" | wc -l) row files written to $OUT (nothing landed; c40 not run)"
fi
