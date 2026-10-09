ORDER for 0.7.0_AE_CloudOps~ZW from 2.0.0_SA_COO~W1 (AMGT_HARVST issuer): HVST-bs-4.

Order file (read its WORKER FACE whole): org/missions/D5/AMGT/AMGT_HARVST/task-orders/AMGT_HARVST.TO-HVST-bs-4.the-r47-seeking-alpha-backfill-resumed.md, at box/dell1 5f2d4690f1.
Authority: 1.0.0_SA_CTO~DELL1 msgs 1430 and 1666.

Act: resume the r47 Seeking Alpha backfill (Andrew's 2026-10-06 order, depth to 2026-01-01) from its own checkpoint (133 done).
1. Confirm no sa backfill_driver is running, with a positive control on the process list.
2. Take the leg's last argv. Resume against the SAME checkpoint as a DECLARED job:
   bash .tools/detached-job.sh run harvst-r47-sa -- <argv>
3. Read that it starts from 133 or more, never from 0.
4. Re-declare before the 48-hour marker lapses.
5. On the driver's PAIRS completion, write bs4_completed.out and tell 0.0.0_AB_MSTR~DELL1.

Outputs: org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.7.0_AE_CloudOps~ZW/r47/.
This is not a re-collection. No other publisher. No FT.
