#!/usr/bin/env bash
S="C:/Users/OPALBL~1/AppData/Local/Temp/claude/C--Users-Opal-Bloomberg-Desktop-ajb-workspace/b0503755-bb6d-429f-ab74-832301c56fa5/scratchpad/sync_branch.py"
cd C:/tmp/wk-oplgtw-103 || exit 1
git checkout HEAD -- org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r37/G2_ADAPTER_PROTOCOL.md 2>&1 | tail -1
python "$S" org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-cl-1.client-core-schwab.md pending 2>&1 | tail -3
git status --short | grep -v portal | head -3
echo SYNC103-DONE
