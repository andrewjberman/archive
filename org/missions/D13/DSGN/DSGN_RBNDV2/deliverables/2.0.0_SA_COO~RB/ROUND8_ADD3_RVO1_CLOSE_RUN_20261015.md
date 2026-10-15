# DSGN_RBNDV2 round 8 addendum 3 -- RV-o-1 drain and close run (2026-10-15 ~21:5xZ)

Seat: 2.0.0_SA_COO~RB. Direct act (round-less, LOCAL); the COO's live read is the close and Andrew's smoke test is the grade.

## Drain (measured)

- Worker 0.9.0_WK_DSGN_RBNDV2~27 report: RB9O1-AC1, AC2, AC3 PASS-by-output; worker portal commit d52fc657, workspace head 45b190325e.
- Diff reviewed at the portal: 3 files (index.css +19, ExecutiveSummary.tsx 17 lines, the new test +245); non-ASCII bytes added: 0.
- Portal merge into feature/dsgn-rbndv2-light: 4299f28a (local, never pushed). Real `tsc -p tsconfig.app.json --noEmit` rc=0 with 0 diagnostic lines; tests 50 pass, 0 fail in 36 files; eslint clean on the two changed TS files.
- Workspace merge: `.tools/safe-merge.sh wk-DSGN_RBNDV2-27` -> e15cf1770a. Worktree 27 and both branches removed.

## Live read on /market (5174, rbndv2-int @4299f28a)

- Four nested groups: border 1px rgb(196,203,219), radius 3px, left bar 3px rgb(20,113,59) on the two success groups and rgb(187,27,48) on the two danger groups.
- Eight rows and tiles read: border 1px rgb(196,203,219).
- Badges (EQ, FI, CM): positive rows text rgb(20,113,59) on rgba(20,113,59,0.19); negative rows rgb(187,27,48) on rgba(187,27,48,0.19). The number beside each reads the same tokens.
- Row hover outline (`--rb-ink-3`) read from source only; not measured live.

## Issuer rulings on the worker's rows

- DSGN_RBNDV2-W27-S1 (criterion names /tmp for the tsc output; worker face says worktree scratch): OBSERVATION, INERT, same as W26-S1. Ruled: the verdict does not depend on the path; no amendment; the next typecheck criterion names the worktree scratch path.
- DSGN_RBNDV2-W27-S2 (the header comment of `NestedCard.tsx`, lines 4 and 6, says data-accent sets no visual; the new CSS paints an outline and bar): ruled stale-comment only. Not edited in this order (outside its paths); carried to the next order that touches that file.

## Open

- Andrew's reload and smoke test of the outlines and the badges.
- The Trending Topics rank numbers and arrows (same lighter colour source) proposed for his next word.
- Owed from Andrew: heat-map answer (FWD-4), call 002b, the next page's comments, the push word and client-facing approval.
