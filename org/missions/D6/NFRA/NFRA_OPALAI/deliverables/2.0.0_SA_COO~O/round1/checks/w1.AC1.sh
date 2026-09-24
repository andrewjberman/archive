#!/usr/bin/env bash
# OA-w-1 AC1 (built): .gitmodules maps opal_ai (url + branch DEV) and portal; the gitlink opal_ai sits at 90ca424fc7.
. "$(dirname "$0")/_root.sh"
u=$(git config -f .gitmodules --get submodule.opal_ai.url 2>/dev/null || echo NONE)
b=$(git config -f .gitmodules --get submodule.opal_ai.branch 2>/dev/null || echo NONE)
pu=$(git config -f .gitmodules --get submodule.portal.url 2>/dev/null || echo NONE)
gl=$(git ls-tree HEAD opal_ai | awk '{print $1" "$3}')
echo "opal_ai.url=$u opal_ai.branch=$b portal.url=$pu gitlink=${gl:-NONE}"
if [ "$u" = "https://github.com/Opal-Capital/opal_ai.git" ] && [ "$b" = "DEV" ] \
   && [ "$pu" = "https://github.com/Opal-Capital/portal.git" ] \
   && [ "$gl" = "160000 90ca424fc7551019cc493847637258adf3c1c4b5" ]; then
  echo "RESULT: PASS"; exit 0
fi
echo "RESULT: FAIL"; exit 1
