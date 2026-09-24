#!/usr/bin/env bash
# AMGT_RESAPP round 39, AMGT-rn-3 AC3 (BOUND) -- prose, docstring and token-reference edits move no styling: the class
# census over the nine source files this cell may touch is byte-identical to the committed baseline. (The one styling
# edit the cell is allowed, PrintExportAction.tsx:136's scrim literal to a token form, changes no counted class -- the
# census counts weight/radius/shadow/size tokens.) usage: bash <this>   (from the repo root; no server)
set -u
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT/portal" || exit 2
BASE="$ROOT/org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round39/checks/baseline.rn-3.census.txt"
node scripts/ui-class-census.mjs src/index.css src/lib/designTokens.ts src/pages/InvestorReporting/export/ExportModal.tsx src/pages/TicketCenter/TicketCenter.tsx src/ui/components/Controls.tsx src/ui/components/graphic/HeroGraphic.tsx src/ui/components/panels/Panel.tsx src/ui/components/states/PanelStates.tsx src/pages/SecurityAnalysis/components/PrintExportAction.tsx > .scratch.rn3.census.txt 2>&1
if cmp -s .scratch.rn3.census.txt "$BASE"; then echo "class census IDENTICAL to the baseline ($(wc -l < "$BASE" | tr -d ' ') lines)"; rm -f .scratch.rn3.census.txt; exit 0; fi
echo "class census DIFFERS from the baseline:"; diff "$BASE" .scratch.rn3.census.txt; rm -f .scratch.rn3.census.txt; exit 1
