# NFRA_GATSCP round 4 -- drain trace (issuer 2.0.0_SA_COO~N1, 2026-10-09)

Round 4: FWD-8 ("a commit refused only for what it writes", PRD v0.4 @a33d3bde72) plus row D1-W13-S1. Direct act GS-x-1 (row
D1-S15, 1.0.0_SA_CTO~DELL1 msg 2776) rode the same drain.

## Orders (4 of 4 terminal)

| order | worker | commits | criterion, last line |
|---|---|---|---|
| GS-h-1 attribution replay | ~14 | f95c647336 | GH1-AC1 `GS-H1-REPLAY ok=True arms=3 failed=0` |
| GS-h-2 act-keyed log lines | ~15 | ade077ddb3 | GH2-AC1 `GS-H2-ACTKEY ok=True arms=3 failed=0` |
| GS-h-3 reset-both-ways | ~16 | 989ee27535, 709428981d | GH3-AC1 `GS-H3-RESET ok=True arms=3 failed=0`; GH3-AC2 `GS-T3-FASTLANE ok=True arms=2 failed=0` |
| GS-x-1 close gate, round being closed (direct act) | ~17 | 7d6c43c991 | GX1-AC1 `GS-X1-CLOSEGATE ok=True arms=2 failed=0` |

All four proof instances: proof-of-spec-check VALID (rc=0) on the merged tree.

## Drain

Merged in `coo-n1-gatscp-r4` (0431f232c4, 1ed38d171e, a804f5f45b, 71c88bc5c4; dropped 0 each); landed on box/dell1 @6587dcdde5
(tree check: 16 needed, dropped 0, foreign 0; index check 0 of 16 differ). Battery on the merged tree: `DRAIN-CHECKS bad=0 of 39`
(rounds 1-4 checks, the six tool self-tests, `bash -n` on five hooks/tools, py_compile, ruff).

## Measured by the issuer at the drain

- **GS-h-1 counts:** 19 OWN-PATH, 5 OTHER-ACT, 2 UNATTRIBUTED (40786, 44486), against the base measurement's 19 / 6 / 1. The pair
  at line 40786 has no one-file commit by its author after its OVERRIDE; the blocked logs landed through a merge (exempt) and a
  1.0.0_SA_CTO commit. Row D1-W14-S1 records it and that 39887 is a same-lane pair differing in path count. The census pairs each
  OVERRIDE with the earliest unmatched BLOCK, not the one it answered.
- **Check defect (issuer's):** `r4_replay.py` arm 3 passes any UNATTRIBUTED entry with a null commit, and no arm requires a tie
  where one is findable; the worker saw it read ok=True on an all-UNATTRIBUTED intermediate run. The committed report was graded by
  arm 2 for every OWN-PATH tie (19 re-measured against git). Recorded here for the round-4 analysis; not re-cut.
- **GS-h-3 negative run:** the new test with the PRE-change `.tools/safe-merge.sh` (b5f9287e72) in a throwaway detached worktree
  reads `SM-CONTINUE ok=False cases=16/17` with `FAIL clean-path-reset-both-ways-refused` and `PASS conflicted-keep-ours-admitted`;
  with the change, 17/17. The worker shared the clean-path case with case b's merge to stay under the 115 s check timeout.
- **GS-x-1:** the gate derives the round as the highest `<round>` among the project's staged task orders (`git grep --cached`)
  and passes `--round`; none found -> WARN, all rounds. Its real run is this round's ROUND_CLOSE commit (project.json alone).

## Real runs

- FWD-8 (GS-h-2): this file's own commit through `.tools/safe-commit.sh`; its owned-paths-check line in
  `org/git-author-override-audit.log` is quoted in the close commit message.
- GS-x-1: the ROUND_CLOSE commit's close-gate line, quoted in the close commit message.
