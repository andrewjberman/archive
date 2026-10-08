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

## SECOND BASE (2026-10-08 16:31Z): DSGN_AMGTV1's `dbeb6764` landed on DEV first; the candidate is now `1cbc56a75eeeb1a087320f70eb5a454383e78df5`

`0.0.0_AB_MSTR~Z` pushed portal DEV `d1b21c97..dbeb6764` (msg 31877). `0498827c975a` is no longer a fast-forward. By the
order-of-landing term (CTO msg 31752) this seat merged origin DEV `dbeb6764` into `wk-AMGT_CORPUS-40-portal` on that scratch
branch: no conflict, new sha `1cbc56a75eee`. **Read 2 does NOT hold this time, so the CTO's own read of two merged files is owed.**

| read | how | result |
|---|---|---|
| 1. the change is the reviewed change | `git patch-id --stable` of `git diff dbeb6764 1cbc56a75eee` | `2c5bd57bfe78`, the patch-id the CTO read on both earlier bases (msg 31669). `git diff --stat`: 5 files, +157 -10. The two patches are NOT byte-identical (`cmp` differs): the context lines moved, the added and removed lines did not |
| 2. DEV's commits do not touch the five files | `git log d1b21c97..dbeb6764 -- <the five files>`; `git diff --name-only d1b21c97 dbeb6764` | **FAILS: 5 of 5 DEV commits are in the range and TWO of the five files changed on DEV.** `reasonWords.ts`: DEV +8 -3, the candidate adds 19 lines on top. `tabs/ModelTab.tsx`: DEV +1 -111 (the input-ledger block and its import removed), the candidate adds 10 lines on top. The other three (`HeaderBrief.tsx`, `SecurityOverlay.tsx`, `tabs/ThesisTab.tsx`) are untouched by DEV. DEV changed 8 files in all |
| 3. build and tests on the new sha | as before | build rc 0 ("built in 30.62s"); typecheck rc 0; `ap2 build 1/1 control 1/1`; `ap3 build 1/1 control 2/2`; `ap4 build 1/1 control 1/1`; `ap5 build 3/3 control 3/3`; `rev build 5/5 control 3/3`; provenance guard rc 0 |

**What this seat read in the two touched files (not a review):** no conflict marker in either. In `ModelTab.tsx` the
candidate's ten lines sit in `rowUnitWords` (line 160 at the new sha), which the tab still calls at lines 483 and 540; DEV's
111 removed lines do not name that function. `reasonWords.ts` holds both DEV's rewritten rule and the candidate's
`dossierLocatorWords`.

**Owed by the ruling (msg 31662):** the merged `reasonWords.ts` and `tabs/ModelTab.tsx` are what the CTO reads, those two
files only. And the captures: the ruling says they are retaken only if read 2 finds a touched file. It found two. The
captures that pass through them are the zero-dominated row (ModelTab) and the two location wordings (the pillar opener and
the header cite, both through `reasonWords.ts`). Retaking them needs port 5174. Not re-run: the six-state render check.

