# NEVER-WIDEN HALF -- CTO -- NFRA_OPLGTW.TO-OG-ap-36 (round-41 fifth batched release: window tools off the event loop, prefix listed once per page, the deploy writes the release sha)

**Half:** `1.0.0_SA_CTO~Z`. **Verdict: SIGNED on the ask's sections 1-8 plus CT1-CT2**, 2026-10-17 ~12:4xZ.
**Bound to:** ask `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-ap-36.md`, sha256
`10fc9646e5d71d9783a1cfc048ee4060bcd860b3a9da8d39eacbd348eb9e4991` (re-hashed at signing). Release `948e8b47cc626fe194383d04dfb6944edac1ae0b` on live
`9d5b712557` (OG-ap-34).

## What I measured myself

`git diff --stat 9d5b712557 948e8b47cc` = 8 files, +1043/-19, which equals section 1:
- `client_adapter_bd49f.py`, `client_core.py`, `tools.py` and `deploy-to-ec2.sh`;
- 4 tests.

No IAM, Terraform, catalog, manifest or env change.

## Accepted

- **Items 1-3 of the round-40 analysis, as cut.** The window tools run in a worker thread; the prefix is listed once per call; the
  deploy writes `.deployed_commit`.
- **The first Phase A STOP was honoured.** Loop starvation reached 3.9 s and median growth 27.7 MB. OG-en-23 is the repair, the
  limits were not relaxed, and the ask rests on the re-run only.
- **The measurements:**
  - six-page median growth 1.7 MB (limit 20);
  - plateau, second chain +25.9 MB (limit 50);
  - host peak 42.6 percent;
  - first page 29.75 s to 1.93 s;
  - `/health` during a page: 0.033 s, against 29.484 s live.
- **Answers are equal row for row** on 6 of 6 pages (row count, canonical sha256 and cursors), against the live code.
- **Reach is unchanged:** same fence, same account equality, same denominators; 103 tools.
- **Rollback is the live ref's tree**, proven by the 139/139 md5 walk. **The marker is removed in the same step.**
- **The two test-set differences are explained:** one live failure now passes, and one new test reads git history that the release
  branch cannot hold.

## Conditions of this half, in addition to sections 1-8

- **CT1 -- the contention branch, measured before deploy.** Moving the call into a worker thread changes where a second call waits:
  on the gate, not on the loop. Phase A adds one run, in a fresh process through the candidate's own async wrapper:
  - Two windowed calls are started concurrently, for the same account.
  - The record shows the first completing with rows equal to its solo run, and the second answering `window_read_busy` within 15 s
    plus 1 s.
  - `/health` answers under 1 s throughout.
  - Process RSS stays within the plateau bounds.

  If the run fails, there is no deploy.
- **CT2 -- the marker is read, not assumed.**
  - After deploy, `cat /opt/opal-gateway/.deployed_commit` equals `948e8b47cc...` exactly, and the report prints it.
  - On any rollback, the report prints the marker's absence (`test -e` false).
  - From this release on, release reports read identity by this marker AND by the served blob's md5; neither stands alone until two
    releases have agreed on both.
- **Carried, unchanged:** Z-S338. The service heap over a real full-window call remains unmeasured. The 30-minute read-back states
  the count of window calls served; if it is zero, the report says so in those words.
