#!/usr/bin/env bash
# MP-w-1 AC1 (built): .gitmodules maps mcportal (url + branch DEV) beside the existing opal_ai and portal mappings, and
# the gitlink mcportal sits at fa1ff9693b (the remote's DEV = PROD at the cut).
. "$(dirname "$0")/_root.sh"
u=$(git config -f .gitmodules --get submodule.mcportal.url 2>/dev/null || echo NONE)
b=$(git config -f .gitmodules --get submodule.mcportal.branch 2>/dev/null || echo NONE)
o=$(git config -f .gitmodules --get submodule.opal_ai.url 2>/dev/null || echo NONE)
p=$(git config -f .gitmodules --get submodule.portal.url 2>/dev/null || echo NONE)
gl=$(git ls-tree HEAD mcportal | awk '{print $1" "$3}')
echo "mcportal.url=$u mcportal.branch=$b opal_ai.url=$o portal.url=$p gitlink=${gl:-NONE}"
if [ "$u" = "https://github.com/Opal-Capital/mcportal.git" ] && [ "$b" = DEV ] && [ "$o" != NONE ] && [ "$p" != NONE ] \
   && [ "$gl" = "160000 fa1ff9693b0868c29c8ff421d403449db8a1ee39" ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
