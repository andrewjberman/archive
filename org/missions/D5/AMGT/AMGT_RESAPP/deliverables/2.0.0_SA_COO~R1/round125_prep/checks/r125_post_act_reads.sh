#!/bin/bash
# AMGT_RESAPP round 125 (cg-4): the issuer's reads on the LIVE function after SC1's apply. Read-only. Run only AFTER SC1's report (never during its pre-act print and apply).
#
#   bash r125_post_act_reads.sh <suffix>
#
# 1. the round-118 read set (config, pack capture, form, money, the live all-names leak scan, the rich exports, timing): `r118_post_act_reads.sh r125<suffix>`
# 2. `r119_cross_surface.py` over the live PDFs and exports it captured
# 3. the full-text census of the LIVE function after the act (every covered name, PDF and rich) against the local candidate `r125-full-local-candidate.json` captured before
#    the act: both hold the new words, so the kind comparator must read 0 moved lines and 0 other; the PDF identical
# 4. the live-after against the live-BEFORE capture (`r125-full-live-before.json`, taken before the act): the kinds moved, nothing else (the act's own outcome)
# 5. SC1's same-session rich before set against this capture (`r125_rich_kind_check.py`)
# Prints; grades nothing by itself.
cd /c/Dev/ajb_workspace || exit 1
S="${1:-a}"
C=org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~R1
E=C:/dev/ui-walk-evidence
echo "== 1 the round-118 read set"
bash $C/round118_prep/checks/r118_post_act_reads.sh "r125$S" 2>&1 | grep -v "LABELS:"
echo "== 2 CROSS SURFACE (live PDFs vs live exports)"
python $C/round119_prep/checks/r119_cross_surface.py $E/r118-packs-r125$S $E/r118-rich-r125$S | tail -9
echo "== 3 the full-text census, live after cg-4"
python $C/round124_prep/checks/r124_full_text_census.py capture live $E/r125-full-live-after.json 2>&1 | grep -v "^warning"
echo "-- 3a live after vs the local candidate (both new words: expect 0 moved, 0 other)"
python $C/round125_prep/checks/r125_kind_census.py compare $E/r125-full-local-candidate.json $E/r125-full-live-after.json 2>&1 | grep -v "^warning"
echo "-- 3b live before vs live after (the act's own outcome: the kinds moved, nothing else)"
python $C/round125_prep/checks/r125_kind_census.py compare $E/r125-full-live-before.json $E/r125-full-live-after.json 2>&1 | grep -v "^warning"
echo "== 4 rich kind check (SC1's same-session before set vs this capture)"
python $C/round125_prep/checks/r125_rich_kind_check.py $E/r125-rich-before $E/r118-rich-r125$S | tail -1
echo finished
