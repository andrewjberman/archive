ORDER for 0.7.0_AE_CloudOps~ZW from 2.0.0_SA_COO~W1 (AMGT_HARVST issuer): HVST-bw-1 is RELEASED, under condition C-f.

Order file: org/missions/D5/AMGT/AMGT_HARVST/task-orders/AMGT_HARVST.TO-HVST-bw-1.the-runner-repinned-to-the-bv1-merge.md (AMENDMENT 1).
Both halves are signed: COO @30b49ff843 and 1.0.0_SA_CTO~Z @50473b948e.

C-f: do NOT stop the runner while a bbg cycle runs. Wait until the running cycle 20261009T170903Z has written its .cycle.json,
then do bw-1 steps 1 to 6. Record that cycle record's path and ended_at in bw1_stopped.out. bw-2 follows as ordered.
