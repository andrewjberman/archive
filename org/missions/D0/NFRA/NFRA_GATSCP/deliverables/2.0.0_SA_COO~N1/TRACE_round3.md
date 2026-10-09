# NFRA_GATSCP round 3 -- the close (issuer 2.0.0_SA_COO~N1, 2026-10-09 ~13:4xZ-15:xxZ)

Round 3 served the round-2 analysis's remediation rows (R2-R6) plus row D1-S5's fix (CTO msg 2258). FWD-1..FWD-7 were already
REALIZED (ROUND_ANALYSIS.round2.md ADDENDUM 1); this round's analysis is the project's close read.

## Orders

| order | row(s) | criterion lines (issuer re-run on the merged tree) |
|---|---|---|
| GS-f-1 POINTER is not an order | D1-S11, D1-S4 | `GS-F1-POINTER ok=True arms=2 failed=0` |
| GS-f-2 CRLF reads like LF | D1-S6 | `GS-F2-CRLF ok=True arms=3 failed=0`; to-pipeline-gate self-test 0 of 117 failed |
| GS-f-3 round-close-check reads the order | D1-S9 | `GS-F3-CLOSE ok=True arms=3 failed=0`; selftest 21/21 |
| GS-f-4 crossbox record custody | D1-S10, Z-S1 | `GS-F4-LANE ok=True 3/3`; `GS-F4-RESOLVER ok=True 2/2`; owned-paths self-test 0 of 20 |
| GS-f-5 seven-gate census | D1-S7 | `GS-F5-CENSUS ok=True arms=3 failed=0` (7 gates, 3 logs, 8,323 lines) |
| GS-f-6 --continue refuses a partial | D1-S5 | `SM-CONTINUE ok=True cases=14/14` (planted partial: rc 7, the REFUSED line names the path) |

Drain: the six branches merged in the issuer's worktree onto box/dell1 (the fast lane resolved every channel conflict by section
union), 34 of 34 drain checks ok, landed @b600261e98 (21 files, dropped 0).

## Real reads on live data (box/dell1 f16252a512)

- GS-f-1: `_open_tos_census` on MDPF_DEMQUE -- 25 files, 1 open, `1 seat-home POINTER file(s) not counted: MDPF_DEMQUE.R4-ZQ.POINTER.md`;
  on AMGT_HARVST -- 181 files, 5 open, `AMGT_HARVST.R75-ZW.POINTER.md` not counted. The two pointers that forced D1-S4/S11's
  overrides no longer count.
- GS-f-3: `round-close-check --project LGIC_BLANKFIX --round 12` -- `orders=1 judgment=1 graded=1 ... verdict=MAY-CLOSE` (it read
  complete=0 judgment=0 at the base).
- round-close-check `--project NFRA_GATSCP --round 3`: MAY-CLOSE.
- GS-f-6's real `--continue` arm: this round's drains needed none (the fast lane resolved each conflict), so the real exercise is
  the test's two arms in throwaway worktrees; the next conflicted drain on any box is the organic arm.

## The census (GS-f-5), for the CTO's R6 read

Window 2026-10-02T1357Z..2026-10-09T1402Z. False refusals / audited overrides, 7 days: owned-paths-check 26 / 51 (the 26 a
heuristic pairing of 118 BLOCK lines with a later OVERRIDE by the same author, no linking key in the log); to-pipeline-gate 4 / 14
(the 4 the POINTER overrides); commit_gate_runner, to-decomp-ref-lint, mstr-ledger-check, pipescript-suite-check, manifest_check
0 / 0 (three of them write no override log at all). Report: `deliverables/0.9.0_WK_NFRA_GATSCP~12/GATE_CENSUS_round3.md`.

## Defects on the way

- The PROOF_OF_SPEC schema defect from e7c10e5b4b (a prose sentence in a `type` value) made proof-of-spec-check exit rc=2 on every
  instance at the workers' base; five of six could not flip. Fixed on box/dell1 at 6b65ca5a52; the issuer re-validated and flipped
  (2c0ca029cb). The same defect was row D1-S13's cause: the row gate self-test reads 0 of 247 failed on the fixed tree (D1-S14).
- GS-f-1's instance carried two placeholders the rc=2 had hidden; repaired @02c260744e (audited TREE_DELIVERABLES escape).
- Issuer check defect, row D1-W11-S1: r3_xbox_custody's clash arm plants a change that is one-sided against HEAD's record by the
  face's strict rule; the worker's block-then-subfield fold satisfies both arms and stays within R5.
- D1-W13-S1: GS-f-6 exempts a path resolved by keeping the first parent's bytes; a path reset in both index and working copy is not
  caught (open question for the analysis).
- R2's tool was misnamed (to-pipeline-gate); the limb lives in surprise-row-gate.py; re-pointed at the cut.
