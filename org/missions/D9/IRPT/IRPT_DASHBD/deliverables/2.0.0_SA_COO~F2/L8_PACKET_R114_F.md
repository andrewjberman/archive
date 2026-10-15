# IRPT_DASHBD round 114, workstream ~F2 (F-SHIP) -- the drain-end packet

Issuer `2.0.0_SA_COO~F2`, 2026-10-15 ~02:5xZ. For `3.0.0_SA_CVO~DELL2`. Issuance `b4e770b83d` (amendments `75d7d92cf1`, `4aaf4dbb29`).
Decomposition `org/missions/D9/IRPT/IRPT_DASHBD/decompositions/IRPT_DASHBD_DECOMP_R114_F.md`. fanout: 2 of 2 chains, cap 8.

**No judgment criterion this round** (both cells LOCAL, three mechanical criteria in all). `round-close-check.py --project IRPT_DASHBD --round 114
--workstream ~F2` reads `verdict=MAY-CLOSE` (reviewer 3.0.0_SA_CVO~DELL2 present, 2 orders, 2 complete, proofs 2 of 2 structurally OK).
No CTO analysis answered this workstream (the ruling said the first analysis follows this first slug), so the cells were cut on the ruling and the CRO's
assessment; the CTO's analysis of THIS packet is the first.

## The two cells

| cell | order | worker | criteria | merged |
|---|---|---|---|---|
| `DB-f-501` the report reader and the Performance tab mount, inert until a route serves a filled report | `IRPT_DASHBD.TO-DB-f-501...` | `0.9.0_WK_IRPT_DASHBD~501` | DBF114-1-AC1 PASS, DBF114-1-AC2 PASS (re-run by the issuer on the worker tree after the merge: both PASS, `bun run typecheck` rc=0) | `3e6aaab01d` |
| `DB-f-502` the serve-path read | `IRPT_DASHBD.TO-DB-f-502...` | `0.9.0_WK_IRPT_DASHBD~502` | DBF114-2-AC1 PASS (instance VALID) | `f39e304d24` |

Portal commits live in the portal repo, never pushed: branch `wk-IRPT_DASHBD-501-portal`, head `d3c37966` (3 commits on `wk-IRPT_DASHBD-180-portal`
@c81d54ff31, which is `origin/PROD` plus the 20 report commits). The local candidate ref `cand/dell2/irpt-default-performance-report` points at `d3c37966`
(23 commits over `origin/PROD`); it is NOT pushed and NOT registered for approval (decomposition decision (d)). Files changed by this round, all new except
the tab: `dashboard/report/reportRead.ts`, `tabs/reporting/ReportingTab.tsx` (the report as the OUTER choice, the existing dashboard/body choice unchanged inside it),
and two test files (11 and 8 tests). Whole-scope suite: 20 failing before, the same 20 after (worker run); the neighbour test `iv-e-135` stays green by the wrapping.

## What this round found (measured)

1. **The filled report has no served path.** `RD_REPORT_SERVE_PATH_R114.json` (worker 502; route, publisher and export lines checked by the criterion against the code):
   the read route `reporting/entry.py` serves per-account `manifest` and `series` and a per-client `summary`; the publisher `reporting-publish/handler.py` writes
   them on a weekday schedule; no code publishes a filled report (`exists_in_platinum` false, `producer_exists` false beyond the private sample builders); the export is
   built on an EC2 host from a frozen bundle and reads no filled report.
2. **Six hops carry one household's filled report to the tab and the export**, in order: (1) build it from gold, `~D2`, LOCAL, a sample exists; (2) publish it to
   platinum, `2.0.0_SA_COO~P`, SERVED, absent; (3) serve it on `.../reporting/client/{client_id}/report` under the summary's every-account scope check, `~P`, WORLD, absent;
   (4) the export bundle's source kind, `~P`, WORLD, absent; (5) the export render host's print of it, **UNOWNED**, WORLD, absent, and the host is stopped (row W502-S2);
   (6) the portal reader and mount, `~F2`, LOCAL, **built this round, inert**.
3. The files issue the publisher and the read route under `2.0.0_SA_COO~P`, not `~P2` as the ruling's overlap rule 4 and the CRO's table suppose (row W502-S1).
4. The mount adds one request per selection that answers `absent` while no route serves a report (row W501-S3, accepted: markup unchanged; the branch is not to be
   promoted before the route exists).

## Issuer omissions and rulings (for the record)

- The orders named row ids `IRPT_DASHBD-F2-W...`: F2 is a lane, the id takes the device coordinate (`D2`). The gate refused worker 502's rows, and worker 501's merge. Amended at
  `75d7d92cf1`. Worker 501's five rows under F2 were never merged (the merge refused them); its branch was rebuilt clean off the shared tree and its rows are the six D2 rows
  `IRPT_DASHBD-D2-W501-S1..S6`.
- Rulings on worker 501's rows (`4aaf4dbb29`): S1 (the mount removed a literal that `iv-e-135` pins) by wrapping, not by editing the test; S2 the checker strips colour;
  S3 accepted; S4 the firm id is `scope.scope.firmId`; S5 the reader's shape check requires what `buildReportModel` reads; S6 (two FE-s-90 arms fail when FORCE_COLOR is unset,
  not caused by this round) is an observation for the owner of that test.

## The one real run

The mount's outcome (a served report shows on the tab) cannot be run for real: no route serves a report. What was run: the 19 tests of the reader and mount (renderToStaticMarkup
of the tab shell with an injected served answer), typecheck, lint (0 errors) and the whole-scope suite. **Thread live: n** for FWD-21. The first real run of this workstream's outcome
waits on hops 2 to 5 above.

## For the CTO's analysis (the enrichment list this seat proposes, ordered)

1. **Rule the owner of hops 2 to 5** (a filled-report publisher and route under `~P`, the export source kind, and the unowned render host) or confirm `~D2` builds the publisher;
   without a served report the tab's report never shows and FWD-21's "on DEV, on the tab and as the export" cannot be exercised.
2. The export mount (F-SHIP's `export/` folder) after hop 4's shape is ruled.
3. Register the candidate `cand/dell2/irpt-default-performance-report` for approval (client-facing) once a route can serve a sample, so Andrew's "sample display" is a page he can open.
4. The disclosure page still waits on call a252.

-- 2.0.0_SA_COO~F2
