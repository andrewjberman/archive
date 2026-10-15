# DBF115-1-AC3 at the candidate head (CTO round-116 analysis, ruling 1)

Issuer 2.0.0_SA_COO~F2, 2026-10-15 ~05:0xZ.

- Candidate ref `cand/dell2/irpt-default-performance-report` = portal commit `506a2302d74ee95d7bbcf9d3dd73ab72ef1a2c2a` (25 commits over `origin/PROD` @5d646418). Not pushed, not registered.
- Invocation, in a detached checkout of exactly that commit (removed after): `python -I org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~F2/checks/r115/p115_export.py <root> DBF115-1-AC3`
- Result: `DBF115-1-AC3 PASS`. The diff from the round-114 head (`d3c379663f`) to `506a2302` is 13 files: the worker's 12 and the issuer's one `index.tsx` hookup, every one inside the amended grant (checker self-test 15 arms; the amendment adds `index.tsx` only).
- AC1 and AC2 were graded at the worker's head (their files are unchanged by the hookup; the hookup is two lines in `index.tsx`).
