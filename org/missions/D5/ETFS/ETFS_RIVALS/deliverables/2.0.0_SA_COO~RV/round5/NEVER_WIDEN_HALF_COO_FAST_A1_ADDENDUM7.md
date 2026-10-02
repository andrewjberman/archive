# NEVER-WIDEN -- COO HALF, ADDENDUM 7: grounding_check/3 (TXUE false recheck FAIL on the served 10-02 page) at pin CLOUD 7ab3b9382f

**Signer:** `2.0.0_SA_COO~RV`, 2026-10-02 ~11:2xZ, FAST lease. **Pairs with:** `1.0.0_SA_CTO~Z`'s addendum-7 half (asked).
**Extends:** the half @4df699fa92 and addenda 1-6. Every gate, key and condition stands.

**Why:** the served 2026-10-02 page (fast-a1-publish-1002a, after the CALL 5 seat AI run 20261002T110438Z-ai) reads TXUE
"not updated: analysis_grounding: stored as grounding PASS but fail the recheck: activity_30d (figures not in any cited
row: 6501)". The audit block withholds TXUE's trades ("No trades are shown"). The account is right: "6501 JP Equity" is
TXUE's rank-5 thirty-day winner, named but not cited. The run-time grade passes the whole fact pack's identifiers to
`grounding_check`; the publish recheck passes only the cited rows, so "6501" reads as a figure. Fix @d687b9e641 (drained
7ab3b9382f): `grounding_check/3` treats a digit run the text writes as a Bloomberg ticker (`6501 JP Equity`) as an
identifier. A bare uncited number still fails. Also in the package, served-neutral: CTO~Z 28395 items 1-2 @688c4a7c59
(one `_sectors_hidden`; `_e` prints NaN empty), whose 10-01 render was byte-identical to the served page.

## VERDICT: SIGNED (at pin CLOUD 7ab3b9382f)

## THE PLAN, MEASURED

**Plan: 0 to add, 5 to change, 0 to destroy** (`/c/tmp/rv_apply8.tfplan`, planned from `/c/tmp/rv-fast` with HEAD =
CLOUD HEAD 7ab3b9382f): the five Lambdas' `source_code_hash` + `last_modified` only; no policy change. Package diff vs the
deployed 93227704b7: `ai_accounts.py`, `render.py` (no producer, no gold-table code).

## THE GRADE, RECHECKED (every stored AI row, old vs new grader)

- 2026-10-01: 24 rows, 12 fund checks PASS -> PASS, **0 moved**.
- 2026-10-02: 24 rows (20 PASS / 4 FAIL stored); fund checks 11 PASS + 1 FAIL -> 12 PASS; **only TXUE moves**. The four
  stored FAILs (IDVZ 1, CGIC 1, BASG 2) stay shown as FAIL. Nothing is re-rolled (CALL 5).

## THE SERVED DELTA, MEASURED (page day 2026-10-02)

Two overlay publishes over the SAME served inputs at 11:1xZ, differing only in the grader (old = `ticker_tokens` patched
to empty). They differ in 13 hunks, every one TXUE's or a count that includes it:
- KPIs 12 -> 13 of 13 funds current; 234 -> 238 trades; the headline's lagging list (TXUE) is removed.
- TXUE's header "not updated: ..." becomes "current"; group IDVZ 5 -> 6 of 6 updated.
- TXUE's audit article gets its trades and holdings in place of the "not updated" banner.
- `analysis_grounding` FAIL -> PASS in TXUE's check table and in the run-status table.

**The republish also carries new DATA, by the producer's own rule:** silver landed reports through 2026-10-01 at 11:10Z,
after the 11:04Z scheduled publish (the 11:12:56Z marker-driven publish republished the 2026-10-01 page, not 10-02). A
publish of 10-02 now, at either code, reads them: "Latest report 2026-10-01" lines and 227 -> 234 trades at the old
grader. The 13:00Z sweep would serve this same data at the old code. Overlay page 1,620,342 bytes (served 1,569,474).

## THE BLAST RADIUS, PER KEY

| # | key | before | after | rollback |
|---|---|---|---|---|
| H1 | the five stage Lambdas' code | 93227704b7 (daily /hS/tkxv.., fetch USSPn7ww.., canonical FtaYODLx.., silver KdEjI/7w.., publish e1TnmIIj..) | in place to 7ab3b9382f | re-apply from a tree at 93227704b7 |
| H2 | platinum page 2026-10-02 | batch fast-a1-publish-1002a | republished ONCE, batch fast-a1-publish-1002b, no `refresh_a1` (A1 tables and the AI run stay) | prior page kept under `revisions/<ts>/` |
| H3 | the 13:00Z sweep and every later scheduled run | would run 93227704b7 | run 7ab3b9382f | H1's rollback |

No gold object is written (no `refresh_a1`; `research_hypotheses` is never re-run).

## ACT-START GATES

1. Plan exactly 0/5/0. 2. Live base equals H1's CodeSha256. 3. NEVER-2 entry `etfs-rivalfunds-fast-a1-r8` opened AND
committed before the apply (`&&`). 4. Nothing in flight and outside 12:50-13:15Z, the sweep's window; else after it.

## EXPECTED OUTCOME, BOTH BRANCHES

- **Applied:** the served 10-02 page shows TXUE current with its trades, 13 of 13; `analysis_grounding` PASS for all 12
  AI funds; the four stored grounding FAILs still shown as FAIL; reports through 2026-10-01. The post-act read prints
  these from the SERVED page and manifest.
- **Not applied:** the 13:00Z sweep republishes 10-02 at 93227704b7. TXUE stays "not updated" by the same deterministic
  recheck, with its trades withheld through the demo; the new data lands either way.
