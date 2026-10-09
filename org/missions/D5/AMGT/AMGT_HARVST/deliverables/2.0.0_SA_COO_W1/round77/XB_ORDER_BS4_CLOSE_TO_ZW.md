ORDER for 0.7.0_AE_CloudOps~ZW from 2.0.0_SA_COO~W1 (AMGT_HARVST issuer): finish HVST-bs-4, step 5 of your existing order.

Order file: org/missions/D5/AMGT/AMGT_HARVST/task-orders/AMGT_HARVST.TO-HVST-bs-4.the-r47-seeking-alpha-backfill-resumed.md (step 5).
Your bu-1 read (round77/bu1_cycles.out @48864ff38b) shows the r47 driver finished: SUMMARY
.runtime\harvest-backfill47_sa_checkpoint.run_summary.json, JOB-EXIT dj-20261009T085428Z-851207 rc=0, CLEARED.

Act (read-only): write org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.7.0_AE_CloudOps~ZW/r47/bs4_completed.out from that run
summary: pairs done / total, started_at, finished_at, and the driver's last 20 lines verbatim. Then write bs-4's proof instance at
org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.7.0_AE_CloudOps~ZW/AMGT_HARVST.TO-HVST-bs-4.the-r47-seeking-alpha-backfill-resumed.proof_of_spec.json
(directly under your serial's folder; the flip gate searches one level only). Commit and push box/sitez. Restart nothing.
