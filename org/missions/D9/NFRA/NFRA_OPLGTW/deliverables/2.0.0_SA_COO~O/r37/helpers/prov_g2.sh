#!/usr/bin/env bash
cd "C:/Users/Opal Bloomberg/Desktop/ajb_workspace" || exit 1
T=org/missions/D9/NFRA/NFRA_OPLGTW/task-orders
declare -A O=(
 [103]=NFRA_OPLGTW.TO-OG-cl-1.client-core-schwab.md
 [104]=NFRA_OPLGTW.TO-OG-cl-2.client-bd49f.md
 [105]=NFRA_OPLGTW.TO-OG-cl-3.client-orion-eclipse.md
 [106]=NFRA_OPLGTW.TO-OG-cl-4.client-bd-cottonwood.md
 [107]=NFRA_OPLGTW.TO-OG-cl-5.client-smartx.md
 [108]=NFRA_OPLGTW.TO-OG-cl-6.client-commonwealth.md
 [109]=NFRA_OPLGTW.TO-OG-gp-1.gp-remainder.md
 [110]=NFRA_OPLGTW.TO-OG-gf-1.gf-wave-b-remainder.md
)
for n in 103 104 105 106 107 108 109 110; do
  ( bash .tools/wk-provision.sh provision NFRA_OPLGTW $n --path "C:/tmp/wk-oplgtw-$n" --node-modules none --order "$T/${O[$n]}" > "C:/tmp/prov$n.out" 2>&1; echo "PROV$n-DONE rc=$?" >> "C:/tmp/prov$n.out" ) &
done
wait
echo ALL-PROVISIONED
