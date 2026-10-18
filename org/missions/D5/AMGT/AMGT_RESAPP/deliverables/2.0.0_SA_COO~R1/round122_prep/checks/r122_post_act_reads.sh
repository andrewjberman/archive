#!/bin/bash
# AMGT_RESAPP round 122 (cd-4): the issuer's reads on the LIVE function after SC1's apply. Read-only. Run only AFTER SC1's report (never during its pre-act print and apply).
#
#   bash r122_post_act_reads.sh <suffix>
#
# 1. the round-118 set (config, pack capture, form, money, the live all-names leak scan, the rich exports, timing): `r118_post_act_reads.sh r122<suffix>`
# 2. `r119_cross_surface.py` over the live PDFs and exports it captured
# 3. the 101-name census of the printed CEO line, live, against the live base `r122-ceo-lines-live-base.json` (the CTO's grade: DELTA 0 or a rollback)
# 4. the form check against SC1's same-session before set `r122-packs-before2` (the order's AC1 compares two same-session captures; the older before set reads
#    a market-data move as a defect, as in rounds 119 and 120)
# Prints; grades nothing by itself.
cd /c/Dev/ajb_workspace || exit 1
S="${1:-after}"
C=org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~R1
E=C:/dev/ui-walk-evidence
echo "== 1 the round-118 read set"
bash $C/round118_prep/checks/r118_post_act_reads.sh "r122$S" 2>&1 | grep -v "LABELS:"
echo "== 2 CROSS SURFACE (live PDFs vs live exports)"
python $C/round119_prep/checks/r119_cross_surface.py $E/r118-packs-r122$S $E/r118-rich-r122$S | tail -9
echo "== 3 the 101-name CEO-line census, live after the act, against the live base"
python $C/round122_prep/checks/r122_ceo_line_census.py capture live $E/r122-ceo-lines-live-after.json 2>&1 | grep -v "^warning"
python $C/round122_prep/checks/r122_ceo_line_census.py compare $E/r122-ceo-lines-live-base.json $E/r122-ceo-lines-live-after.json 2>&1 | grep -v "^warning"
echo "== 4 form (SC1's same-session before set vs live after)"
python $C/round116_prep/checks/r116_pack_form_check.py $E/r122-packs-before2 $E/r118-packs-r122$S | tail -1
echo finished
