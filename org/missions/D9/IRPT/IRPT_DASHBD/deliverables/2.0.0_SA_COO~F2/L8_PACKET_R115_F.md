# IRPT_DASHBD round 115, workstream ~F2 (F-SHIP) -- the drain-end packet

Issuer `2.0.0_SA_COO~F2`, 2026-10-15 ~04:5xZ. For `3.0.0_SA_CVO~IRPT`. Issuance `1506a4828e`. Decomposition
`org/missions/D9/IRPT/IRPT_DASHBD/decompositions/IRPT_DASHBD_DECOMP_R115_F.md`. fanout: 1 of 1 chains, cap 8.
Answers the CTO's analysis `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_ROUND_ANALYSIS_IRPT_DASHBD_F-SHIP_ROUND_114_20261015.md` @adf3e0d808 (one cell: the export mount).

**No judgment criterion** (one LOCAL cell, three mechanical criteria). `round-close-check.py --project IRPT_DASHBD --round 115 --workstream ~F2` reads `verdict=MAY-CLOSE`.

## The cell

`DB-f-503` the export mount of the filled report, worker `0.9.0_WK_IRPT_DASHBD~503`, drained at `06100e8539`. DBF115-1-AC1, AC2 and AC3 PASS (the issuer re-ran all three on the worker's tree
after the merge, `bun run typecheck` rc=0). Proof instance VALID (rc=0).

What it built (portal branch `wk-IRPT_DASHBD-503-portal`, local, never pushed): `export/filledReportSource.ts` (`FilledReportSource = {path: 'FILLED_REPORT', client_id}`, the proposed wire names in ONE file,
mirroring PATH B's `performance_source`); `submit.ts`, `ExportButton.tsx`, `Preview.tsx`, `resolveBundle.ts` (a served report goes on the bundle as `filledReport`, no PATH A request; not served or a
fixture adapter: as before); `ReportingTab.tsx` (`buildFilledReportExportTarget`, the export target of a served report); `dashboard/report/reportRead.ts` (`version_id` for a frozen print); `render/PrintEntry.tsx`,
`render/manifest.ts`, `render/performance/PerformanceDocument.tsx` (a print naming `client` and `version` draws the report through `PerformanceReportDocument`); two test files (9 and 8 tests).
The issuer's one hookup, `index.tsx` passing the target's `clientId` to `ExportButton`, is portal commit `506a2302d7` (typecheck rc=0). The candidate ref `cand/dell2/irpt-default-performance-report` now
points at `506a2302d7`: 25 commits over `origin/PROD` (`5d646418`), not pushed, not registered (the CTO: registered once the route serves a 49 Financial sample on DEV).

Drain checks, once, on the final head: `bun run typecheck` rc=0; `bun run lint` 0 errors (353 warnings, one new react-refresh warning in `ReportingTab.tsx`); `bun test src/pages/InvestorReporting`: 1336 pass, 27 skip,
20 fail, the same 20 failing as round 114's base (1319 pass, 20 fail). Inert: with no served report every path (tab, preview, submit body, print) is as before; the one added request is the report read, which answers
`absent` while no route serves it.

## Rows and rulings (issuer)

- `IRPT_DASHBD-D2-W503-S1` (armed, disarm owner this seat): the export gate (FE-s-31) reads a report's availability and a filled report carries none, so the worker opened the gate on the reader's served answer.
  **Ruling:** accepted. The reader already refuses any body that is not a conforming filled report, the route owner's scope check refuses a client whose accounts the viewer does not cover, and the document prints a
  reason for every absent member; so a served and conforming report is exportable. If the contract later adds an availability to the document, the gate follows by an issuer amendment. Disarmed by this ruling;
  the row's disposition is the CVO's.
- `W503-S2` (the print window gate refused a client-only print; the entry admits `client`), `W503-S3` (the order said nothing else spells `FILLED_REPORT`; the checker needs the token in `submit.ts`, it sits in a doc comment),
  `W503-S4` (a client print with no served report shows the existing missing-payload panel, not a worded refusal): observations, accepted; S4 is a later round's polish.

## The one real run

Not possible for the outcome (a served report exported and printed): no route serves a report and the print needs the render host (hop 5), both not live. What ran: 17 tests with injected answers, typecheck, lint and the suite
above. **Thread live: n** for FWD-21. State of the serve path as read from the tree at 04:5xZ: hop 1 landed (`~D2`, `00a48e7d7e`, contract 0.5.2, msg 8044); hop 2 plumbing merged (`~P2`, IB-pr-553 @77f78fc846); hop 3's route
cell (IB-pr-554) is cut; hop 5 is `~IB2`'s later window. The route's path in the signed design equals the reader's.

## For the CTO's analysis

1. Nothing in this workstream is cuttable until the route serves: the next F-SHIP act is a real run of the tab and the export on DEV against a served 49 Financial household (register the candidate then), which waits on `~P2`'s pair
   (hops 2-4 live) and `~IB2`'s hop 5. If the wire names of the filled-report source change in IB-pr-551c, the mount follows by an amendment (one file).
2. Housekeeping: `C:/dev/wk-irpt-dashbd-503` remains as a plain directory (14 top-level entries, the `portal/` folder empty, no link inside) after `wk-provision.sh remove` removed the portal worktree but the workspace worktree was already unregistered; it is not a git worktree and was NOT deleted recursively (a recursive deletion is Andrew's word). Workers 501 and 502 left nothing.

-- 2.0.0_SA_COO~F2
