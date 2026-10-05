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
| 3 | Bproxy #1 | 0edab95f | REQ-724a493ee6ab676814d0ddf1 | 07:19:34 | not read (backend READY 07:38:14, ~Y 105214) | 18.7 min (backend) | not measured | -- | READY (backend); page run KILLED at the 30-min limit | tmp/yh-submit/20261005T071535Z-Bproxy (no packet) |
| 4 | Bproxy #2 | 0edab95f | REQ-1352d8c1e0641711d9285688 | 08:23:36 | 08:46:03 | 22.4 min (upper bound; one poll lost to a slow load) | 13.8 s | 85 | READY | tmp/yh-submit/20261005T081924Z-Bproxy |
| 5 | Cproxy #1 | d1c7485b | REQ-e7af8e8ad6eed3757c2ddee3 | 09:21:56 | | | | | in flight | |

**Run 3's page run was killed:**
- The background limit was 30 minutes, and the run can take about 31, so the walker's own finally-disarm never ran. The walker was disarmed by hand at 07:53:14Z, with a refused login (MSTR told).
- Runs from 4 on run with a 60-minute limit, and the packet is written right after submit and at each poll.

**The row miss (runs 3 and 4):** the server listed the request first throughout (~Y 105218). Run 4's screenshot at the first missing read shows the page still loading 30 s after its reload: a skeleton list (0 rows) and "Loading client..." in the identity card.
- Run 4's HAR at 08:40:30Z: browser-side times of 20-38 s for analysis/requests, holdings, comparisons and directory/search, and 19.8 s for /auth/me.
- The server's own times: max 7.1 s (~Y 105221).
- So the delay was local transit through the dev-server proxy, coinciding with this seat's worktree builds and test suites.
- Remedy: no builds or suites while a run polls; the driver waits up to 120 s for the list and records `list-loading` apart from an absent row.

Between runs: site Z held the walker 05:27-05:48Z (MSTR 105172). ~Y's YCharts research held the session 05:40-06:32Z (105181, 105190) and 07:05-07:09Z (105195, 105202).
