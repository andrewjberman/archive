# DSGN_RBNDV2 round 8 addendum 4 -- RV-q-1 and RV-r-1 drained, read live (2026-10-15 ~23:2xZ)

Seat: 2.0.0_SA_COO~RB. Direct acts (round-less, LOCAL); the COO's live read is the close and Andrew's smoke test is the grade. RV-s-1 (worker ~30) is still in flight and is recorded when it drains.

## Drain (measured)

- RV-q-1, worker ~28: portal cc368d50 (PanelHeader.tsx, 35 lines changed, and the new test); merge into feature/dsgn-rbndv2-light 7b84bc81; workspace merge 5d414efa14. Real tsc rc=0, 0 diagnostic lines; tests 52 pass 0 fail in 37 files; eslint clean; non-ASCII bytes added 0.
- RV-r-1, worker ~29: portal c2e0802f (RSIModal.tsx, 4 lines, and the new test); merge 5fbc527a; workspace merge eddd38ed3d. Real tsc rc=0; tests 54 pass 0 fail in 38 files; eslint clean; non-ASCII bytes added 0.
- Worktrees 28 and 29 and their branches removed. Nothing pushed.

## Live read (5174, rbndv2-int @5fbc527a)

- Panel titles (/market): Trending Topics, Top / Bottom Performers, Daily Cloud and Global RSI each hold the help icon inside the title element, right of the text (offsets 128 of 142, 198 of 212, 96 of 110, 84 of 98 px), with the 2px underline; none draws a help icon in the right-hand group.
- Global RSI modal, Spotlight cards: three Hottest and three Coldest cards, each with a 1px rgb(196,203,219) outline; HOTTEST labels rgb(20,113,59), COLDEST labels rgb(187,27,48); the modal title holds its icon.

## Issuer rulings

- DSGN_RBNDV2-W28-S1 and -W29-S1 (the order names no commit instrument for the portal repo, which has no `.tools/`; each worker committed the portal files through the workspace `safe-commit.sh` run from inside `portal/`): OBSERVATION, INERT. Ruled: valid; the next order's bounds name the instrument.

## Open

- Census: see the last section (read from source, output capped at 120 lines, so not a complete count).
- RV-s-1 (Trending Topic drilldown): drained below. Call laptop-20261015T230503Z-bea4 (rank numbers and arrows) queued at Andrew.

## RV-s-1 (worker ~30), drained and read live (2026-10-15 ~23:3xZ)

- Worker report: RB10S1-AC1, AC2, AC3 PASS-by-output; portal 5d92f971, workspace head 4bd3348abe; no surprise rows.
- Diff reviewed: ExecutiveSummary.tsx 19 lines inside DrilldownModal (three constants inkColor, inkTint, inkBar; pill, score, circles and bar on them; artInk and the hairline outline on each source-article row; `sentimentColor` deleted as unused) and the new test; non-ASCII bytes added 0; getSentimentColor, accentColor and the lead gradient untouched.
- Portal merge 9db2045b into feature/dsgn-rbndv2-light; real tsc rc=0 with 0 diagnostic lines; tests 56 pass 0 fail in 39 files; eslint clean. Workspace merge 1d9526146d. Worktree 30 and its branches removed. Nothing pushed.
- Live read (5174, a Bullish topic, score +0.688): pill and score rgb(20,113,59), pill tint rgba(20,113,59,0.125); the 1, 2, 3 circles rgb(20,113,59) on rgba(20,113,59,0.125); four source-article rows each with a 1px rgb(196,203,219) outline and a score rgb(20,113,59). A negative-sentiment topic was not opened; the red branch is read from source only.

## Census of help icons outside PanelHeader (read from source, 2026-10-15 ~23:3xZ)

A native Grep for `<HelpCircle` across `src/pages` (output capped at 120 lines with 3 lines of context, so the list below is what that page showed, not a denominator) returned these sites: MacroHeatmap, ModelTab, AlphaTab, AssetAllocationSummary, OptimizationSummaryHeader (two), ModelPortfolios (two), FactorBankTab, InflectionInsightsPanel, FeeEfficiencyPanel, DistributionTab (two), AdvisorPublicProfile, TaxCostBasisPanel (two), PartnerAnalytics, ModelTiltTimeSeriesView (two), SummaryMetricsTable (five shown). Every one I could see sits directly after the heading, label or column text it explains (Macroeconomic Indicators, the Model Portfolios chart titles, the FactorTilts and Optimization table headers, the factor-name cells). Not verified as a panel title: AssetAllocationSummary (line 355), OptimizationSummaryHeader (line 316), DistributionTab (lines 3206 and 3429) and PartnerAnalytics (line 1182). None draws the icon in a right-hand group the way PanelHeader did.

