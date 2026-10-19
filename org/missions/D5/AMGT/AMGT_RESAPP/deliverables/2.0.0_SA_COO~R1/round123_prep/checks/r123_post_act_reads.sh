#!/bin/bash
# AMGT_RESAPP round 123 (ce-4): the issuer's reads on the LIVE function after SC1's apply. Read-only. Run only AFTER SC1's report.
#
#   bash r123_post_act_reads.sh <suffix>
#
# Same shape as r122_post_act_reads.sh, round-123 names: base = r122-ceo-lines-live-after.json (the live state before ce-4), before packs = SC1's r123-packs-before.
cd /c/Dev/ajb_workspace || exit 1
S="${1:-a}"
C=org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~R1
E=C:/dev/ui-walk-evidence
echo "== 1 the round-118 read set"
bash $C/round118_prep/checks/r118_post_act_reads.sh "r123$S" 2>&1 | grep -v "LABELS:"
echo "== 2 CROSS SURFACE (live PDFs vs live exports)"
python $C/round119_prep/checks/r119_cross_surface.py $E/r118-packs-r123$S $E/r118-rich-r123$S | tail -9
echo "== 3 the 101-name CEO-line census, live after ce-4, against the live base (r122 after)"
python $C/round122_prep/checks/r122_ceo_line_census.py capture live $E/r123-ceo-lines-live-after.json 2>&1 | grep -v "^warning"
python $C/round122_prep/checks/r122_ceo_line_census.py compare $E/r122-ceo-lines-live-after.json $E/r123-ceo-lines-live-after.json 2>&1 | grep -v "^warning"
echo "== 4 form (SC1's same-session before set vs live after)"
python $C/round116_prep/checks/r116_pack_form_check.py $E/r123-packs-before $E/r118-packs-r123$S | tail -1
echo finished
