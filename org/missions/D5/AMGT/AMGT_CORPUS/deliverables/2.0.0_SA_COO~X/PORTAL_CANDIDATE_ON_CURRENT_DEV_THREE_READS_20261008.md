# AMGT_CORPUS round 40 -- the portal candidate brought onto current DEV: the three reads (CTO ruling msg 31662)

**By:** `2.0.0_SA_COO~X`, 2026-10-08 10:08Z. **Offered for the DEV push:** `0498827c975a36dfc156a01911528535c010ac5e`, branch `wk-AMGT_CORPUS-40-portal` in the nested
portal repository at `C:/tmp/wk-crps-r40-4/portal`. It is a MERGE of origin DEV `d1b21c97` (fetched 09:58Z) into the reviewed
candidate `de6fc425`, made on that scratch branch. Nothing shared was rebased. The push stays Andrew's word at the
`0.0.0_AB_MSTR~Z` terminal.

| read | how | result |
|---|---|---|
| 1. the change is the reviewed change | `git diff ba391aff de6fc425` and `git diff d1b21c97 0498827c975a`, the two patches compared byte for byte (`cmp`) | IDENTICAL. `git diff --stat d1b21c97 HEAD`: 5 files changed, 157 insertions, 10 deletions |
| 2. DEV's 19 commits do not touch the five files | `git log ba391aff..d1b21c97 -- <the five files>`; and `git diff --name-only ba391aff d1b21c97` filtered to `SecurityAnalysis` | 0 commits of 19; 0 files under `SecurityAnalysis` changed on DEV. The merge had no conflict |
| 3. build and tests on the new sha | `bun run build` (tsc -b and vite build); `bun run typecheck`; the issuer's five page checks; `node scripts/provenance-read-guard.mjs` | build rc 0 ("built in 8.86s"); typecheck rc 0; `ap2 build 1/1 control 1/1`; `ap3 build 1/1 control 2/2`; `ap4 build 1/1 control 1/1`; `ap5 build 3/3 control 3/3`; `rev build 5/5 control 3/3`; provenance guard rc 0 |

**Not re-run on the new sha:** the DSGN_AMGTV1 six-state render check (76 PASS / 0 FAIL / 1 N/A on `de6fc425`), and the four
captures (the ruling: not retaken unless read 2 finds a touched file; it found none). The portal has no unit-test runner for
`src/pages/SecurityAnalysis`; "its tests" above are the checks named.
