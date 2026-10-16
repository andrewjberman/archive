# IRPT_DASHBD round 119, workstream F-SHIP (~F2) -- the drain-end packet (FWD-3 and FWD-5, the first round)

Issuer `2.0.0_SA_COO~F2`, 2026-10-16 ~00:3xZ. For `3.0.0_SA_CVO~IRPT`. Issuance `ee3271cbbf`. Decomposition
`org/missions/D9/IRPT/IRPT_DASHBD/decompositions/IRPT_DASHBD_DECOMP_R119_F.md`. fanout: 3 of 3 chains, cap 8.
On Andrew's go ("stop waiting") through the CTO's parallelization ruling, Move 2 (`org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULING_DELL2_IRPT_PARALLELIZE_WORKSTREAM_ASSIGNMENTS_20261015.md`, msg 8740). No CTO analysis answered these outcomes: the cuts follow the PRD
(FWD-3, FWD-5, surface rows S09, S11) and what this seat measured. The CTO's analysis of THIS packet is the first for them.

**No judgment criterion** (all three cells LOCAL, five mechanical criteria). `round-close-check.py --project IRPT_DASHBD --round 119 --workstream ~F2`: `verdict=MAY-CLOSE` (3 orders, 0 judgment).

## The cells

| cell | worker | criteria | merged |
|---|---|---|---|
| `DB-f-601` the FWD-3 thread read | `0.9.0_WK_IRPT_DASHBD~601` | DBF119-2-AC1 PASS (re-run by the issuer after the merge) | `c17cd4c4e3` |
| `DB-f-602` the class-window view model and section (new portal files from PROD, not mounted) | `~602` | DBF119-1-AC1, AC2, AC3 PASS (re-run by the issuer on the worker tree: PASS; `bun run typecheck` rc=0) | `389d494f63` |
| `DB-f-603` the FWD-5 thread read | `~603` | DBF119-3-AC1 PASS (re-run by the issuer) | `e6b408e330` |

The class feature lives on the portal branch `wk-IRPT_DASHBD-602-portal` (head `7fa808c9`, one commit over `origin/PROD` `e0e69da7`: four new files, 841 lines: `tabs/reporting/classes/classWindowModel.ts`, `AssetClassSection.tsx` and two test files, 16 and 7
tests). Its candidate ref `cand/dell2/irpt-asset-class-performance` is LOCAL, not pushed, not registered. Mutant: dropping the cumulative factor fails 3 model tests. The model's window contribution is the sum over days of `C(t-1) * contribution(c,t)`, which makes the classes add up to the
account's window return exactly (a plain sum of daily contributions would not); a window with a non-measured day or class values that do not sum to the account prints words and no figure; unclassified is listed whenever non-zero and last.

## What this round found (measured)

**FWD-3.** (record `0.9.0_WK_IRPT_DASHBD~601/RD_FWD3_THREAD_R119.json`)
1. The gold table `account_class_daily` is BUILT, both release halves are SIGNED and it is APPLIED: the R37 apply's deploy-completion ledger entry is CLOSED and its first-fire log shows class rows landed for 2026-10-07 and 2026-10-08 (a claim from records, not a live read).
2. The SERVED series carries NO class keys (the series contract lists them as optional; the publisher writes none).
3. Smallest route change: one member added to `OBJECTS` in `reporting/entry.py` (line 88); the route key is generic, so no new route; a new publisher object is still needed.
4. The portal can import the class type, the color map and the order from `tabs/holdings/assetClass.ts` unchanged; the Performance tab holds no asset-class code today.
5. Seven hops from the gold table to the section: gold table (`~D2`, exists); publisher code change; publisher redeploy (`~DB2`, WORLD); the scheduled publish writing the class object; route change in `entry.py`; route redeploy (`~DB2`, WORLD); the Performance-tab section (this seat). **The worker named `~D2` for the publisher change and left the route change UNOWNED:
   the CTO's Move 1 gives the export and route code under `infra/aws/lambda/investor-reporting/` to `2.0.0_SA_COO~S2`, so hops 2 to 6 are `~S2`'s unless the CTO rules otherwise.**
6. Observations: the contract's `served` flag and the publisher's round-1 comment still say the table does not exist (stale: row W601-S2); the portal's class type has an eighth class `Other` that the gold enum does not hold (W601-S3).

**FWD-5.** (record `0.9.0_WK_IRPT_DASHBD~603/RD_FWD5_THREAD_R119.json`)
1. There is NO `account_transaction` contract under `org/standards/` and no producer; `applied` false (the bucket was not read; a read-only listing by `~D2` settles it).
2. Sources exist for all three firms (49 Financial silver `fact_trn`, Cottonwood `fact_transactions`, an Inflection bronze pull); Opal's own words for the custodian's action and type are defined in no file read (row W603-S2).
3. Smallest route: the same reporting read route with a `transactions` value in the `which` set; the portal reuses the securities list's filter and sort helpers; no export writer or virtualised list exists in InvestorReporting.
4. Six hops: custodian sources (UNOWNED), contract and builder (`~D2`), apply (`~DB2`), paged publisher and route (the worker names `~P`; Move 1 says `~S2`), portal client, portal section (this seat).

## Rows (all OBSERVATION or the one issuer-resolved BLOCKING, INERT)

W601-S1 (BLOCKING, INERT): the worker's sparse worktree lacked `data/` and `infra/aws/`; resolved by this issuer (the folders were materialized and the worker resumed): an issuer provisioning gap (the order's paths named only its own folder). W601-S2, S3; W602-S1 to S5 (the branch name differs from CONTRIBUTING-BOXES `cand/<box>/<slug>`, now corrected by the candidate ref;
a reason `CLASS_RETURN_NOT_SERVED` the spec did not name; an inverted window and a missing mix-date value fail closed; a repo-wide lint error outside the grant); W603-S1 to S3 (the sparse cone; the action and type vocabulary; the Cottonwood reader has no transaction read).

## The one real run

None possible: no class object or transactions file is served, and the section is not mounted. What ran: 16 + 7 tests of the new files with made-up rows, two thread reads against code and records, typecheck, lint of the new files. **Thread live: n** for FWD-3 and FWD-5.

## For the CTO's analysis (the enrichment list this seat proposes, in order)

1. **FWD-3: rule the owner of hops 2 to 6** (the class object in the publisher, its schedule, the `OBJECTS` member, the redeploys) between `~S2`, `~P2` and `~D2`; then cut the publisher and route cells as a WORLD pair (a new served object), after `~D2` fixes the class document's shape (the worker's proposal: `account_id`, `firm`, `as_of`, `method_version`, `schema_version`, `date`, `class_names`, `coverage`, `market_value_eod`, `class_return_daily`, columnar like the series).
2. **FWD-3 (this seat, after item 1):** the reader and the mount of `AssetClassSection` in the Performance tab on that route, inert until served (the model and section are built).
3. **FWD-5:** `~D2` writes the `account_transaction` contract and builder after the CTO rules Opal's action and type vocabulary (who defines it); this seat's portal client and section follow on the contract's shape.
4. The default-report candidate and the class candidate are separate features; both register for approval only once a route serves a sample.

-- 2.0.0_SA_COO~F2
