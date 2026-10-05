# Y-6 reliability -- each page case twice in a row, one job at a time (2026-10-05)

For 2.0.0_SA_COO~Y msg 105158 (CTO fold-in `CTO_FOLD_IN_IRPT_THREE_BRIEFS_20261002.md` Y-6; Andrew R2: YCharts calls for
cases A, B, C, D and the typo file APPROVED, one at a time with the queue empty).
- Driver: `yh-submit-case.mjs`, live, `--queue-empty`, `--ready-ceiling-min 23`, on localhost:5174.
- Every run is under the UI-walker ARM/DISARM protocol with 0.0.0_AB_MSTR, and each disarm is proved by a refused login.
- ~Y watches every REQ to terminal and records the backend states.

**Cases:**
- Aproxy: easy file, TIMXX named SGOV, Overview.
- Bproxy: plus Opal Ultra Long-Term, Comparison.
- Cproxy: plus Opal Ultra Long-Term and IWM, Multi-Comp.
- Dproxy: the Stevens file with its four untracked rows named SGOV, Overview.
- typoAccept: the typo file, Use AAPL for APPL and SGOV for TIMXX, Overview.

**Timings:**
- Submit to READY: from the submit answer to the first page read of the row as READY. The page is polled once a minute, so the value is an upper bound to within 1 minute.
- Open to sections: from the row's press to the first section card.

| Run | Case | Portal | REQ | Submitted (Z) | Page READY (Z) | Submit to READY | Open to sections | Section cards | Outcome | Packet (local) |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Aproxy #1 | 3e1aa46f | REQ-777d75467393aafe6f351cc5 | 05:01:19 | 05:19:30 | 18.2 min | 2.0 s | 60 | READY | tmp/yh-submit/20261005T045848Z-Aproxy |
| 2 | Aproxy #2 | 99c6ae08 | REQ-14fe69cf6ead8a9436379dc2 | 06:40:55 | 06:58:51 | 17.9 min | 1.4 s | 60 | READY | tmp/yh-submit/20261005T063830Z-Aproxy |

Between runs: site Z held the walker 05:27-05:48Z (MSTR 105172). ~Y's YCharts research held the session 05:40-06:32Z (105181, 105190) and 07:05-07:09Z (105195, 105202).
