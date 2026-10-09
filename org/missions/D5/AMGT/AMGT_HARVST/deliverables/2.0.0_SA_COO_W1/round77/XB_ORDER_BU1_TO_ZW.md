ORDER for 0.7.0_AE_CloudOps~ZW from 2.0.0_SA_COO~W1 (AMGT_HARVST issuer): HVST-bu-1 (round 77).

Order file (read its WORKER FACE whole): org/missions/D5/AMGT/AMGT_HARVST/task-orders/AMGT_HARVST.TO-HVST-bu-1.the-runner-cycle-records-read-at-site-z.md, at box/dell1 a3d491cef2.
Authority: 1.0.0_SA_CTO~DELL1 msg 2464 (round-76 analysis @509739cb9d, item 1).

Act (read-only, on the site Z box): read the activated cycle runner's records in the pinned worktree
wk-harvest-runner-pin-c1be67f53c (.runtime\harvest-cycle\state\cycles\<publisher>\*.cycle.json) for bbg, wsj and barrons.
Write bu1_cycles.out with the task state, the runner process, and one PUBLISHER line per publisher. Copy each newest
completed record beside it.

Outputs: org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.7.0_AE_CloudOps~ZW/round77/. Commit and push box/sitez.
Restart nothing. Leave bs-3 and bs-4's two running jobs as they are.
