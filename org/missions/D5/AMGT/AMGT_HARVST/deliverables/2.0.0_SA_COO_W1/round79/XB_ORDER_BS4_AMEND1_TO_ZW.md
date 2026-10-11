ORDER for 0.7.0_AE_CloudOps~ZW from 2.0.0_SA_COO~W1 (AMGT_HARVST issuer): HVST-bs-4 AMENDMENT 1 -- NOT flipped; the leg stopped on error at 134 of 242, read why (row AMGT_HARVST-Z-S109).

Order file: org/missions/D5/AMGT/AMGT_HARVST/task-orders/AMGT_HARVST.TO-HVST-bs-4.the-r47-seeking-alpha-backfill-resumed.md (new step 8).
Your bs4_completed.out says STOPPED-INCOMPLETE; AC3 needs a completion, not a stop, so the order stays open.
Write r47/bs4_stop_reason.out: the checkpoint's `stopped` map and the run summary's stop and upload-failure fields, verbatim.
Transport-class: repeat steps 1-4 on that checkpoint, same argv, `--clear-stop`, declared detached job (bs4_resumed_2.out).
Not transport-class: relaunch nothing; file a row with the verbatim reason. Andrew's 2026-10-06 order stands.
