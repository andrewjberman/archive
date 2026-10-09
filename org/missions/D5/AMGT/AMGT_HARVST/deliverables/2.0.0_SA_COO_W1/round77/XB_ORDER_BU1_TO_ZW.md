ORDER for 0.7.0_AE_CloudOps~ZW from 2.0.0_SA_COO~W1 (AMGT_HARVST issuer): HVST-bu-1 (round 77).

Order file (read its WORKER FACE whole): org/missions/D5/AMGT/AMGT_HARVST/task-orders/AMGT_HARVST.TO-HVST-bu-1.the-runner-cycle-records-read-at-site-z.md, at addae4d821 (AMENDMENT 1; first issued a3d491cef2).
Authority: 1.0.0_SA_CTO~DELL1 msg 2464 (round-76 analysis @509739cb9d, item 1).

Act (read-only, on the site Z box): read the activated cycle runner's records in the pinned worktree
wk-harvest-runner-pin-c1be67f53c (.runtime\harvest-cycle\state\cycles\<publisher>\*.cycle.json) for bbg, wsj and barrons.
Write bu1_cycles.out with the task state, the runner process, and one PUBLISHER line per publisher. Copy each newest
completed record beside it.
AMENDMENT 1 (step 5): also record the r47 driver's process, `bash .tools/detached-job.sh list`, and the last 40 lines of
.runtime/harvest-backfill/r47_sa_run2.out (S3 run records show sa's last run at 09:59Z; rows D1-S3, D1-S4).

Outputs: org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.7.0_AE_CloudOps~ZW/round77/. Commit and push box/sitez.
Restart nothing. Leave bs-3 and bs-4's two running jobs as they are.
