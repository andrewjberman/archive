# SUITE_SAMPLE -- TO-IV-e-82: three whole-scope runs of the Investor Reporting suite at portal DEV 7bb81fa89792

Worker 0.9.0_WK_DSGN_IRPTV1~43, 2026-10-11. Record: `SUITE_SAMPLE.json` beside this file. Full logs (outside both repos):
`C:/dev/_irpt_private_evidence_20261009/DSGN_IRPTV1/0.9.0_WK_DSGN_IRPTV1~43/` (run1/2/3.log, ANSI-stripped c1/c2/c3.txt, ids1/2/3.txt).

**Sample.** Command `bun test src/pages/InvestorReporting` from the portal worktree (HEAD 7bb81fa8..., equal to the issuer's ls-remote read; not re-fetched). 370 test files, 1157 tests.
Workspace half: `docs/contracts/` and `lib/` are read from the workspace worktree at box/dell2 9c9f20e08a (see row D2-W43-S2).

| run | start (UTC) | duration | pass | fail | skip |
|---|---|---|---|---|---|
| 1 | 05:29:46 | 108.16 s | 1087 | 43 | 27 |
| 2 | 05:31:58 | 94.72 s | 1087 | 43 | 27 |
| 3 | 05:33:33 | 92.21 s | 1087 | 43 | 27 |

**The three failing SETS are identical** (43 distinct ids by file path plus full test name; set equality checked by program, 43 of 43 in each pair). The runner's own fail count (43) equals the distinct ids;
it prints 49 failure marker lines per run because three content-pins tests print three times each. No run crashed or timed out; no environmental failure.

**Proposed rulings (for the reviewer):** KNOWN-LEGACY 14 (row S59: 9; W35-S3: 3; W38-S1: 1; W21-S4: 1); REGRESSION 29 (row D2-W43-S2: 18 contract-vs-portal drift;
D2-W43-S1: 6 hardcoded other-user bun path; D2-W43-S3: 5 unrecorded). Each id carries its basis in the JSON. No FLAKE: three identical failures show no nondeterminism.

## What the sample says about the five rows

- **S7** (8 new failures, 95 -> 103 of 656 -> 671, at DEV a3f4c860): RE-STATES at a new tip and a new size (43 of 1157). None of the 8 test names S7 quotes is in today's 43. The number it cites is superseded; the row's own claim (8 new at that landing) is history, not re-measured here.
- **W21-S2** (19 of the original 77 base rows still failing; set not equal to the table's Q rows): RE-STATES. Four of its named files still fail (fe-s-1 fixtures and source-bounds, fe-s-25, fe-s-57, the last for a different cause now); the Q-row cap question is the CTO's and this sample does not answer it.
- **W23-S1** (16 failing, run-to-run instability reaching 9+ files): DOES NOT REPRODUCE on this device in three runs (identical sets), and does not close it: three in a row did not rule out a regime shift (W29-S10), and the failing set today is 43, not 16.
- **W29-S10** (two different internally-stable regimes, 15 then 7): RE-STATES. This sample landed in one stable regime (43); it neither shows a second regime nor rules one out. The row's remedy, a set not a count as the bar, is what this record supplies: a named 43-id set for one device and one (portal, workspace) pair.
- **W34-S1** (fe-s-45/residuals fails about 1 in 2 three-run samples): NOT OBSERVED. No fe-s-45 id is in any run's failing set (0 of 3 runs). One sample of 3 cannot close an intermittent claim; the row stands.

## Not done / limits

Root causes were not diagnosed beyond each failure's own error text (read-only sample, no product edit). The ls-remote time (~05:11Z) is the issuer's, not re-read.
