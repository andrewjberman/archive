# NEVER-WIDEN -- COO HALF: RFW-D01 on today's page -- rebuild the 2026-10-02 A1 tables over the current inputs and republish ONCE (no code change)

**Signer:** `2.0.0_SA_COO~RV`, 2026-10-02 ~14:5xZ, FULL (lease ended 14:40:14Z on Andrew's word). **Pairs with:**
`1.0.0_SA_CTO~Z`'s half (asked).
**Why:** PRD v0.12's lead item RFW-D01 (@afc2bed44f; brief `docs/briefs/rivalfunds-ui-data-walk-20261002.md`). The served
2026-10-02 page (fast-a1-publish-1002f) shows A1 tables built at 11:03-11:04Z, before the 11:11Z G1 refresh (7 funds' 10-01
reports) and before G4 date=2026-10-01 landed (11:10Z). `produce_a1` skips a table whose date already holds an object. This
act is today's page only; the structural fix (rebuild on a newer input) is round-6 cell d1-1.

## VERDICT: SIGNED

## THE ACT

ONE `daily-lambda {"only": ["publish-page"], "date": "2026-10-02", "mode": "daily", "batch_id": "rv-publish-1002g",
"sink": "s3", "refresh_a1": true}` at the deployed code (CLOUD 722f0db291; no deploy, no plan). The three A1 producers rebuild
over the current G1/G4, and the page republishes.

## THE SERVED DELTA, MEASURED THROUGH THE HANDLERS (14:47Z)

`round5/served_delta_a1.py --day 2026-10-02` (each producer's `handler_entry` on an overlay over the served inputs) vs the
served objects:
- **holding_contribution:** 1,440 of 3,778 rows change, in 10 funds (INEQ 446, TXUE 232, WCMG 224, ETFT 144, PCLG 140, TSEL
  132, PFOE 110, BASG 8, BIDD 2, GQGU 2); 3,777 rows new. YTD fund totals move:
  | fund | YTD before | YTD after |
  |---|---|---|
  | ETFT | 0.56% | 0.07% |
  | INEQ | 8.29% | 6.51% |
  | PCLG | -4.82% | -4.53% |
  | PFOE | -4.92% | -5.53% |
  | TSEL | 4.13% | 4.79% |
  | TXUE | 9.98% | 9.71% |
  | WCMG | 5.79% | 5.45% |
- **buying_trend:** 5 of 319 rows change (BASG 2, ETFT 3).
- **input_census:** 27 rows change; 1,566 -> 1,562.
- **Page** (overlay publish with `refresh_a1`): status OK, 13 of 13, 213 trades, KPIs unchanged; 1,575,052 -> 1,591,713 bytes.
  The census reads holdings 2 -> 9 of 13 arrived, prices 0 -> 79 of 763, GICS 0 -> 79 of 763. The four still missing (IDVZ,
  BIDD, CGIC, SCHY) have no 10-01 report in G1, which is RFW-D07, true today.
- The AI accounts are unchanged (no AI re-run). Their cited rows keep the 11:03Z revisions and values they were graded
  against, and the publish recheck reads those stored rows.

## THE BLAST RADIUS, PER KEY

| # | key | before | after | rollback |
|---|---|---|---|---|
| P1 | gold holding_contribution / buying_trend / input_census date=2026-10-02 | the 11:03-11:04Z objects | + one new object each (newest wins) | prior objects stay; a revert removes the three new objects (S3 delete, human-confirmed) |
| P2 | platinum page 2026-10-02 | fast-a1-publish-1002f | republished ONCE, batch rv-publish-1002g | prior page kept under `revisions/<ts>/` |

## GATES

1. Nothing in flight on any rivalfunds Lambda (10 min of logs). 2. The served objects equal the ones measured
(holding_contribution-20261002T110325Z, buying_trend-20261002T110403Z, input_census-20261002T110406Z). 3. Deployed
CodeSha256 = the 722f0db291 set.

## EXPECTED OUTCOME, BOTH BRANCHES

- **Applied:** the served A1 objects are the rebuilt ones (newest by revision), and the page's census reads 9 of 13 / 79 of
  763 / 79 of 763. The YTD totals above are served, and the AI accounts are unchanged.
- **Not applied:** the stale tables stay until round 6's d1-1 ships and a publish runs.
