#!/usr/bin/env bash
# AMGT_RESAPP round 40, AMGT-ro-1 AC4 (JUDGMENT, graded at L9 by 3.0.0_SA_CVO~Z) -- writes the rich export beside the
# page's own six renders so a person can read "nothing in the export that is not on the page" as a reader would.
set -u
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT" || exit 2
OUT="${1:?out dir}"; mkdir -p "$OUT"
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
cp org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~143/handler_rich_to_file.py "$T/h.py"
PYTHONPATH="$ROOT" python "$T/h.py" > /dev/null 2>&1; cp "$T/served/BA_US_Equity.md" "$OUT/BA_US_Equity.rich.md" && wc -c "$OUT/BA_US_Equity.rich.md"
echo "READ BESIDE: org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round40/real-run/{thesis,exec,peers,model,posture}.png (the issuer writes them at the round close)"
