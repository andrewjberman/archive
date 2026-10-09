# GS-h-1 -- attribution replay of the census's 26 owned-paths refusals (NFRA_GATSCP round 4, 0.9.0_WK_NFRA_GATSCP~14)

Tool: `replay_owned_paths.py` (this folder). Output: `OWNED_PATHS_REPLAY_round4.json`, 26 objects. Read-only on git and the log;
only `git log` and `git show --name-only` listings were used, no commit content, no W73 path kept or printed.

## Denominator

- Log read: `org/git-author-override-audit.log` at this worktree's HEAD (47,224 lines; the window's lines are all inside it).
- Window 2026-10-02T13:57Z..2026-10-09T14:03Z: 120 BLOCK lines and 51 OVERRIDE lines.
- Pairing re-run exactly as the census: each BLOCK, in log order, takes the first later OVERRIDE by the same author within 400
  lines that no earlier BLOCK has taken. Result: **26 pairs** (the census's 26). The census said 118 BLOCK lines and the issuer's
  base measurement 119; this tree's log gives 120 (the log has grown since; the 26 pairs are unchanged).

## Counts per tie

| tie | n of 26 |
|---|---|
| OWN-PATH | 19 |
| OTHER-ACT | 5 |
| UNATTRIBUTED | 2 |

- OWN-PATH (19): block lines 39076, 39084, 39145, 39147, 39788, 40246, 40320, 40324, 40407, 40623, 40682, 40683, 41266, 42011,
  42650, 42756, 43222, 43331, 45274. Each names the author's own non-merge commit carrying a blocked path, landed after the BLOCK.
  Two commits serve two BLOCK lines each (2b3048bd22 for 39145 and 39147; 9f56c40993 for 40320 and 40324; c7adf21d10 for 40682 and
  40683): the same path was refused twice before the commit landed.
- OTHER-ACT (5): 39887 -> 98d439936a, 39959 -> 9f56c40993, 40602 -> 83d5e34919, 40874 -> ed79639e4a, 42229 -> b44b5d76df. In each, the
  paired OVERRIDE served a different commit (file count equal to the OVERRIDE's n, same author, within seconds of the OVERRIDE stamp,
  a path in the OVERRIDE's lane) that carries none of the BLOCK's paths.
- UNATTRIBUTED (2): 40786 and 44486 (commit null; the evidence field says what was searched).

## The rule

1. Pair as the census did (above).
2. **OWN-PATH**: the earliest non-merge commit whose author name equals the BLOCK's serial exactly, committer stamp at or after the
   BLOCK and no later than OVERRIDE+30 min, whose `git show --name-only` carries at least one path of the BLOCK line (the hook logs
   the first three violating paths only).
3. **OTHER-ACT**: else, the one non-merge commit by that author stamped within [OVERRIDE-15 s, OVERRIDE+10 min] whose file count equals
   the OVERRIDE line's n, which carries none of the BLOCK's paths, and (where the OVERRIDE's lane is a lane in `.owned-paths.yaml`,
   resolved with the repo's own `resolve_lane`) carries a path that resolves to that lane. The log's committer stamps sit 1-6 s
   either side of the OVERRIDE stamp, so the window is stated, not the order.
4. **UNATTRIBUTED**: else; commit null. Merge commits are not counted as the refused act (the hook exempts them).
5. No tie is "likely": a tie is a commit hash that the checker re-measures, or it is UNATTRIBUTED.

## What the replay found beyond the counts

- **The OVERRIDE's n is the key the census lacked.** The OVERRIDE line's second number is the staged-path count; in all five
  OTHER-ACT ties it equals the file count of the served commit, and the BLOCK's n differs from it (39887: 3 vs 2; 40602: 3 vs 6;
  40874: 1 vs 3; 42229: 1 vs 8; 39959: 1 vs 1 but different lane and path). The census's pairing artifact is greedy first-fit: an
  OVERRIDE is taken by the earliest unmatched BLOCK of the author, not the BLOCK it answered. Example: OVERRIDE 40888 (05:54:02Z, n=1)
  follows BLOCK line 40887 (05:50:27Z, DEVICES.json, n=1) by 4 minutes, yet it was taken by 40786 (00:03Z).
- **40786** (0.0.0_AB_MSTR, agent-spawn-audit.log + drive-mode.log, n=2): the two files were committed by another author, 1.0.0_SA_CTO,
  in 9f01c965cd at 00:05:50Z (PASS line n=2 at 00:05:53Z; the CTO is in lane BASE_EXEC). The author's own landing of them was a merge
  (ba32125d62 at 00:20:51Z, exempt from the hook). The paired OVERRIDE 40888 (n=1, NFRA_CTLPLN_FAST_C) matches no one-file commit by
  0.0.0_AB_MSTR: the only commit near it, ed79639e4a (3 files at 05:55:31Z), is the one OVERRIDE 40889 (n=3) served.
  So: UNATTRIBUTED, with the CTO commit named in the evidence as a fact about the paths, not as the tie.
- **44486** (2.0.0_SA_COO~G2, infra/logic/registry/reporting_policies.json, n=1): no commit touches that path after the BLOCK, and
  the author's only commit near the OVERRIDE (33ba944f23, 7 files, 10:54:25Z) is not one file and not in lane IRPT_COMPLETION_REGISTRY.
  Agrees with the base measurement: never committed by anyone.
- **39887 is not a different-lane pair.** BLOCK lane and OVERRIDE lane are both TREE_DELIVERABLES; it is OTHER-ACT because the
  OVERRIDE (n=2) served 98d439936a and the BLOCK (n=3) was a different attempt. See surprise row NFRA_GATSCP-D1-W14-S1.
