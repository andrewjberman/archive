#!/usr/bin/env bash
# MX-b-2 AC2 (W1-S3, the issuer's pick): workflows/atom_decomposition/catalog_v02/validation_report.json is NOT tracked at
# HEAD, `git check-ignore` covers it, and running validate_catalog_v02.py leaves `git status --porcelain` clean for it.
. "$(dirname "$0")/_root.sh"
R="workflows/atom_decomposition/catalog_v02/validation_report.json"
tracked=yes; git cat-file -e "HEAD:$R" 2>/dev/null || tracked=no
ign=no; git check-ignore -q "$R" && ign=yes
timeout 110 python workflows/atom_decomposition/validate_catalog_v02.py >/dev/null 2>&1; vrc=$?
st=$(git status --porcelain -- "$R" | grep -c .)
# While the report is still tracked (the FAIL arm), the run just rewrote it: put the tracked bytes back so a dry run
# never leaves the shared tree dirty (row NFRA_MCPINDEX-W1-S3's trap).
[ "$tracked" = yes ] && git restore -- "$R"
echo "tracked at HEAD=$tracked; ignored=$ign; validator rc=$vrc; status lines for the report after a run=$st"
if [ "$tracked" = no ] && [ "$ign" = yes ] && [ "$st" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
