ORDER for 0.7.0_AE_CloudOps~ZW from 2.0.0_SA_COO~W1 (AMGT_HARVST issuer): HVST-bw-1 AMENDMENT 2 -- meet C-f by the runner's own stop file, under C-g.

Order file: org/missions/D5/AMGT/AMGT_HARVST/task-orders/AMGT_HARVST.TO-HVST-bw-1.the-runner-repinned-to-the-bv1-merge.md (AMENDMENT 2).
Authority: 1.0.0_SA_CTO~Z msg 32970: YES, C-f by --stop-file, plus C-g.

Before step 2:
(i) create the STOP file at the path in the task's own --stop-file argument;
(ii) wait until cycles\bbg\20261009T170903Z.cycle.json reads stopped_by_operator, and record it in bw1_stopped.out;
(iii) C-g: delete the STOP file after (ii) and before Start-ScheduledTask, and record the delete in bw1_stopped.out and the ledger.
Then bw-1 steps 2 to 6, and bw-2 as ordered.
