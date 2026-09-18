# DSGN_REBRND.TO-RB-s-12 -- result

**Worker:** `0.9.0_WK_DSGN_REBRND~3` (chain C, slot ~3) · **Cell:** `RB-s-12` · **Branch:** `wk-dsgn_rebrnd-3`
(workspace HEAD at start `b121dee318b1cfde69186bb947f3e49c01794034`; portal HEAD at start
`102362368fe9fc2a293f29c77b7b134e20f43d3f`) · **Push state:** LOCAL.

Chain C, parallel-safe outright per the decomp (section 5): one file written
(`design/brand/portal-surface-inventory.json`), the router read, no component/stylesheet/token file
touched. **Every mechanical criterion PASSES BY OUTPUT.** `RB12-AC4` is a judgment criterion: RECORDED,
no verdict, oracle `3.0.0_SA_CVO` at L9. This task order's `<status>` is flipped to `complete`.

## What the inventory is

`design/brand/portal-surface-inventory.json`: 24 routes (the router's own count, computed by the
byte-identical regex `RB12-AC2` runs against `portal/src/App.tsx`) x every state a cell touches
(default / empty / loading / error / no-permission / toggled-panel) = **99 rows**. Each row carries a
`fixture` (an existing `portal/.frontend-dev/testing/` file or the literal `NONE`), a `render_obligation`
(the subset of RB-s-2, 3, 4, 5, 6, 9, 10, 11 that touch that exact route+state, MEASURED per row -- see
`evidence`), and a `keyboard_obligation` boolean. The three IV.9 routes (`/market`, `/positioning`,
`/portfolio-management`) are marked `fixed_comparison_route: true` on their default rows.

## Method

Route list/count: `sorted(set(re.findall(r'path=.([A-Za-z0-9_/:*-]+).', text)))` excluding the literal
values `*` and `/*`, run against `portal/src/App.tsx` -- the exact expression `RB12-AC2` itself runs.
Per-route cell-touch obligations: direct reads of the 8 named cells' task orders (their own defect
descriptions and named routes) PLUS 13 separate `comp-find` census queries over `portal/src` (isLoading,
LoadingSpinner, error, requireAdmin|requireInternal, activeTab|setActiveTab, the four retired
chart/icon libraries, `from 'recharts'`, the ordered-scale vocabulary (overweight/underweight/Fear-Greed/
performance-band), `permission` -i, `hasAccess(`), plus direct reads of `portal/src/index.css`,
`portal/src/components/ProtectedRoute.tsx`, `portal/src/lib/firmAccess.ts` and
`portal/src/pages/InvestorReporting/render/print.css`. Where no direct evidence surfaced for a cell
touching a specific route, that cell is OMITTED from the row rather than assumed -- the inventory can
under-claim, it does not knowingly over-claim.

## Two findings recorded as surprise rows (form only, no significance judged)

- **`DSGN_REBRND-W3-S1`** -- no route or panel anywhere in `portal/src` renders an observable
  NO-PERMISSION state today. All three access-denial mechanisms found (`ProtectedRoute.tsx`'s
  `requireAdmin`/`requireInternal`/firm-allowlist branches, a panel-level element hide on
  `/advisor-intelligence` and `/trade-submission`, and a transient toast on `/portfolio-management`) are
  non-rendering. The two route-level-gated rows (`/ticket-center`, `/data-refresh`, state
  `no-permission`) are marked `fixture: NONE` with that gap stated in their own `evidence`; a top-level
  `no_permission_state_gap` field carries the full finding. ARMED, disarm owners named
  (`2.0.0_SA_COO~D` for the `RB-s-13` issuance, `0.9.0_WK_DSGN_REBRND~1` for `RB-s-10`'s own design of
  that state).
- **`DSGN_REBRND-W3-S2`** -- this cell's own face and `RB12-AC2`'s own prose read "at issuance the
  router reads 26"; `RB12-AC2`'s own invocation, run fresh, prints `APP-ROUTES: 24` -- the raw match
  count is 26 (confirmed), two of which are the wildcard `Route` entries the SAME invocation's own
  set-comprehension excludes by name. This inventory's `route_count` is 24, matching what `RB12-AC2`
  actually verifies. INERT (the checker recomputes fresh every run; no stored wrong value can propagate).

## Criteria, as run

| id | invocation | deciding output | denominator |
|---|---|---|---|
| RB12-AC1 | `python -c "...json.load...len(rows)...d.get('route_count')..."` | `INVENTORY-ROWS: 99 ROUTE-DENOMINATOR: 24` / `VERDICT: HAS-DENOMINATOR` | rows=99, route_count=24 (both printed) |
| RB12-AC2 | `python -c "...re.findall(r'path=.([A-Za-z0-9_/:*-]+).',s)...VERDICT..."` | `APP-ROUTES: 24 INVENTORY-DENOMINATOR: 24` / `VERDICT: AGREES` | 24 of 24 -- live router count vs this file's route_count, identical mechanism |
| RB12-AC3 | `python -c "...miss=[r for r in rows if 'fixture' not in r]...VERDICT..."` | `ROWS: 99 WITHOUT-FIXTURE-FIELD: 0` / `VERDICT: ALL-SOURCED` | 99 of 99 rows carry a non-empty `fixture` key |
| RB12-AC4 | judgment -- no mechanical invocation | recorded for L9 (see "What the inventory is" above) | N/A -- graded by `3.0.0_SA_CVO` |

Re-run twice (before and after the two mutant tests below), byte-identical both times: STABLE.

## Mutant control

Two mutants of the committed file, never committed themselves: (A) `route_count` forced `24->23`,
re-run against `RB12-AC2`'s own invocation -- printed `APP-ROUTES: 24 INVENTORY-DENOMINATOR: 23` /
`VERDICT: DISAGREES` (would FAIL `RB12-AC2`'s `<expect>`). (B) the `fixture` key deleted from `rows[0]`
only, re-run against `RB12-AC3`'s own invocation -- printed `ROWS: 99 WITHOUT-FIXTURE-FIELD: 1` /
`VERDICT: INCOMPLETE` (would FAIL `RB12-AC3`'s `<expect>`). Both fired as expected: the criteria
discriminate a broken deliverable, not just echo one that already passes.

## Declared exclusions

- No per-firm no-permission row was minted for every route `firmAccess.ts`'s `FIRM_ALLOWED_PATHS`
  additionally denies to `49financial`/`inflection` users -- every such denial reduces to the identical
  silent-redirect mechanism already characterized once (`DSGN_REBRND-W3-S1`); a row per firm x route
  would multiply near-duplicate observations, not add a distinct one.
- `/attribution`, `/correlations` and `/security-scanner`'s exact charting mechanism (if any) was not
  independently confirmed beyond an import-string census (`recharts`/`apexcharts`/`@nivo`/`visx`) --
  a shared chart wrapper that does not itself import a library string would not surface by this method.
  No `RB-s-11` obligation is asserted on those three routes' rows for that reason (stated in each row's
  `evidence`, not silently assumed either way).
- `sscn_divdef_001_smoke.json` is cited as `/security-scanner`'s `fixture` by filename-prefix
  plausibility only; its internal shape was not opened against the `ui-smoke.mjs --fixtures`
  `{substring: body}` contract. Outside the four mechanical criteria's scope (they check the `fixture`
  key's presence, not its shape); flagged in the row's own `evidence`.
- `design/brand/portal-routes.json` (also named on the decomp's write-surface row 11) was NOT produced
  by this cell -- the decomp's per-cell table (line 109) assigns it to `RB-s-14`, not `RB-s-12`; this
  cell's own face names only `design/brand/portal-surface-inventory.json`.
