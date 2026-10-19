#!/bin/bash
# AMGT_RESAPP round 124 (cf-4): the issuer's reads on the LIVE function after SC1's apply. Read-only. Run only AFTER SC1's report (never during its pre-act print and apply).
#
#   bash r124_post_act_reads.sh <suffix>
#
# 1. the round-118 read set (config, pack capture, form, money, the live all-names leak scan, the rich exports, timing): `r118_post_act_reads.sh r124<suffix>`
# 2. `r119_cross_surface.py` over the live PDFs and exports it captured
# 3. the full-text census of the LIVE function after the act (every covered name, PDF and rich) against the local candidate
#    `r124-full-local-candidate.json` captured before the act: the rich lines must be equal on the 100 comparable names, the PDF identical on all
# 4. the word-swap check of SC1's same-session before sets (`r124-packs-before`, `r124-rich-before`) against this capture
# Prints; grades nothing by itself.
cd /c/Dev/ajb_workspace || exit 1
S="${1:-a}"
C=org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~R1
E=C:/dev/ui-walk-evidence
echo "== 1 the round-118 read set"
bash $C/round118_prep/checks/r118_post_act_reads.sh "r124$S" 2>&1 | grep -v "LABELS:"
echo "== 2 CROSS SURFACE (live PDFs vs live exports)"
python $C/round119_prep/checks/r119_cross_surface.py $E/r118-packs-r124$S $E/r118-rich-r124$S | tail -9
echo "== 3 the full-text census, live after cf-4, against the local candidate"
python $C/round124_prep/checks/r124_full_text_census.py capture live $E/r124-full-live-after.json 2>&1 | grep -v "^warning"
python $C/round124_prep/checks/r124_full_text_census.py compare $E/r124-full-local-candidate.json $E/r124-full-live-after.json 2>&1 | grep -v "^warning" | grep -v "line(s)$"
echo "== 4 word swap (SC1's same-session before sets vs this capture)"
python $C/round124_prep/checks/r124_pack_word_swap_check.py $E/r124-packs-before $E/r118-packs-r124$S | tail -1
python $C/round124_prep/checks/r124_pack_word_swap_check.py $E/r124-rich-before $E/r118-rich-r124$S --ext md | tail -1
echo finished
