# Chosen set for the PROD promote of the unreported-days sentence -- 2.0.0_SA_COO~C2, 2026-10-16 ~06:4xZ (CTO msg 9125)

**The set (`--features`): ONE branch.** `cand/dell2/irpt-fwd10-unreported-days-sentence`, head `9c24c7bdac5775d18a66460748adbb694d2b1f98`, FOUR commits cherry-picked onto `origin/PROD` `a062c56e53b174eab043b1e50002c93eb7a56f8b` from the round 147 worker branch (IRPT_DASHBD.TO-DB-c-25): `7fa4d968` (the three fixtures made by the contract writer), `7ee50085` (the page's series mirror takes contract 0.3.0), `0018e4be` (the Performance tab prints the trading days the source did not report), `9c24c7bd` (the test).

Claim words: MEASURED = this seat ran it in this session; RECORD = a committed file read; NOT READ = said so.

## Authority (RECORD)
- Andrew's word "approve 92c0" (~06:2xZ 2026-10-16): `org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261016_062xZ_APPROVE_92C0_DELETE_BOTH_SCRATCH_FOLDERS.md`, classed by the CTO as approved for PROD (msg 9125). Approval row `dell2-20261016T055011Z-92c0`: `python .tools/open-calls.py approval-status --branch cand/dell2/irpt-fwd10-unreported-days-sentence` reads `state=APPROVED valid=yes by=andrew head_sha=9c24c7bdac5775d18a66460748adbb694d2b1f98 commits=4 class=client-facing` (MEASURED ~06:4xZ). The head is pinned: a different head is a stale approval and the release builder refuses it.
- The CTO's technical review of the four commits: PASS (msg 9101).

## Payload (MEASURED ~05:5xZ in a scratch worktree at `origin/PROD` `a062c56e53b1`)
- `git log origin/PROD..<branch>` lists exactly the four commits; the two-dot diff `origin/PROD <branch>` names exactly SIX files, +132 and -3: `src/pages/InvestorReporting/__tests__/irpt-dashbd/fixtures/series-unreported-days.json`, `.../series-no-statement.json`, `.../series-unreported-empty.json`, `.../fwd10-unreported-days.test.tsx`, `src/pages/InvestorReporting/dashboard/DashboardPerformance.tsx`, `src/pages/InvestorReporting/dashboard/seriesContract.ts`.
- The cherry-picks applied with no conflict; `bun test` on the new test plus `iv-e-124` passed 9 of 9 and `bun run typecheck` returned rc 0, in that scratch tree with a copy of the contract (0.3.0 then; the scratch tree and its copy are removed).
- NOT run by this seat: the vite build; anything on PROD after the push.

## Two facts the DT must read before GO
1. **`iv-e-124` is red against the trunk contract on this payload, by design.** Trunk contract is 0.3.1 (six optional names); this payload's mirror lists the five names of 0.3.0. The sixth name is the round 148 cell `DB-c-26` (worker `~418`), a separate, one-file change that is NOT in the approved head and is NOT in this promote. Per the CTO's rule (an amendment never removes a failing reader test; it names the reader cell), the promote's test gate is the new test only (`src/pages/InvestorReporting/__tests__/irpt-dashbd`), and `iv-e-124`'s red is named here, to `DB-c-26`. The page's behaviour does not change by the missing optional name.
2. **No live account shows the sentence.** The Cottonwood series are published (939 accounts) but the daily schedule and the publish pair's Act 4 are not landed (CTO msg 9022 condition 1), so a PROD page read is fixture-only and is labelled so. The DT's read is of the served bundle (the sentence text is in the built JavaScript), not of an account.

## What the promote changes (for the receipt)
Page: Investor Reporting, the dashboard's Performance tab. Class: CLIENT-FACING (the tab is one a partner-firm or client login can open; unsure = client-facing). The tab gains one note where a series carries unreported trading days for the window shown: `N trading days not reported by the source: <dates>.`; a series that carries none (every series served today) prints nothing new. The series mirror accepts the two new optional names and a null income.

## Excluded
The mirror cell `DB-c-26` (six names), every other DEV candidate, and live `origin/DEV`.
