# DSGN_RBNDV2 -- round 7 close run: the LOCAL candidate rehearsal (criterion RB7Z1-AC3)

**Author:** `2.0.0_SA_COO~RB`, 2026-10-15 ~18:1xZ. **Worker record:** `deliverables/0.9.0_WK_DSGN_RBNDV2~22/REHEARSAL_RECORD.md` (merged, workspace `761f221929`). **Nothing is pushed.**

## What was measured

| item | result |
|---|---|
| last PROD | `origin/PROD` `33ad65eef3` (a release merge); `origin/DEV` `ad7c100b` (the feature base) |
| candidate | local branch `cand/laptop/dsgn-rbndv2-light`, tip `c8181090ca`, 39 commits over PROD, replayed by `git cherry-pick -x` of the 39 non-merge commits of `ad7c100b..feature/dsgn-rbndv2-light` (the order said "about 45"; measured 39) |
| conflicts | **0**; 0 empty cherry-picks; 0 skipped |
| files | the 89 files the feature branch changes are byte-identical in the candidate (`check_rehearsal.py`: 89 of 89) |
| remote | `git ls-remote --heads origin cand/laptop/dsgn-rbndv2-light` prints nothing (rc=0); no remote-tracking ref; `portal-merge-forward.sh` not run |
| proof of spec | VALID, re-run from the worker's worktree before the merge; `check_rehearsal.py` printed `VERDICT: REHEARSAL-OK` (12 of 12 arms) |

## The COO's drain reads (the judgment criterion's evidence)

- **Typecheck, real instrument** (`tsc -p tsconfig.app.json --noEmit`): PROD baseline 0 error lines (worker, rc=0); candidate 0 error lines (worker rc=0; re-run by me in the candidate checkout, rc=0). The candidate adds no error over PROD.
- **Design tests** on the candidate checkout: 27 pass 0 fail (14 files); eslint rc=0 (worker).
- **One Market Overview walk on the candidate build** (the dev server on port 5174 was switched from the integration checkout to the candidate checkout, walked, and switched back; the integration server answers 200 again): Trending Topics rows `border-top-color rgba(0, 0, 0, 0)` (class `border-transparent`), footers read "October 15th, 2026, 7:18a ET | Source: Global News." and the others in mixed case, the Fear and Greed gauge needle stroke and hub `rgb(10, 23, 51)` with end labels `rgb(74, 88, 120)`, the Global RSI panel tooltip text `rgb(255, 255, 255)` (labels `rgba(255, 255, 255, 0.85)`) on the indigo box. These read the same as on the feature branch.

## Notes

- The worker's PROD scratch worktree left a directory (`prod-baseline`, holding its own `bun install`, `node_modules.scratch-install`, with names too long for `git worktree remove --force`). It was part of the merged worker worktree, which the standing rule removes at each drain; `wk-provision.sh remove` removed it, the shared `node_modules` (313 entries) is intact, and nothing outside the worker's directory was touched.
- The replay carries no `DEV`-only commits: the candidate is cut from PROD's tip, so PROD's own 10 commits ahead of DEV are in it, and the 26 DEV commits ahead of PROD are not.
- The candidate stays local, kept for Andrew's push word. The feature branch is unchanged (`3509eae8`).

## Carried

Andrew's words: the heat-map answer (at this terminal), call `002b` (tooltip placement), his next page's comments. The push itself (and the client-facing approval) is his; the CTO's ruling: the candidate is what `portal-merge-forward.sh` and the approval row see.
