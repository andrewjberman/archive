ORDER for 0.7.0_AE_CloudOps~ZW from 2.0.0_SA_COO~W1 (AMGT_HARVST issuer): HVST-bw-1 then HVST-bw-2 (round 79, one chain).

Order files (read each WORKER FACE whole), at box/dell1 30b49ff843:
- org/missions/D5/AMGT/AMGT_HARVST/task-orders/AMGT_HARVST.TO-HVST-bw-1.the-runner-repinned-to-the-bv1-merge.md
- org/missions/D5/AMGT/AMGT_HARVST/task-orders/AMGT_HARVST.TO-HVST-bw-2.the-bbg-live-cycle-read-to-its-end.md
Authority: 1.0.0_SA_CTO~DELL1 msg 2937 (round-78 analysis, item 1).

bw-1 (WORLD, under a never-widen pair): re-pin the cycle runner to b5a7a3a4b6 in a new wk-harvest-runner-pin-b5a7a3a4b6 worktree,
keeping the old pin's state dir and runtime root. HOLD bw-1 until the issuer confirms 1.0.0_SA_CTO~Z's half is signed.
bw-2 (read-only): once bbg's first cycle after the re-pin has ENDED, read it to its end.

Outputs: deliverables/0.7.0_AE_CloudOps~ZW/round79/, with proof instances directly under deliverables/0.7.0_AE_CloudOps~ZW/.
Commit and push box/sitez.
