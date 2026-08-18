# OPAL_ADVIPOINTERS.P1-CLOSE-49F -- D-fleet family inventory + backfill determination (0.4.0_DS_ClientPlatform~A, 2026-08-18 ~16:4xZ)

**TO:** `OPAL_ADVIPOINTERS.P1-CLOSE-49F.d-fleet-inventory-and-backfill-determination~A` @49dd8469d1 (COO GO 160631Z).
**Authority:** Andrew-direct 2026-08-18 ~1500Z (49F end-to-end push) + CTO push plan @a2f27c8d0a s3 row 1. CTO attests; this is the evidence table.
**Product/account:** Advisor Intelligence, 49 Financial, Schwab 08335338.

## GRAIN STATEMENT (P1C-4, load-bearing)

**This table is at FAMILY grain** (the run-8d census's own grain: a family is a served-key
TEMPLATE, e.g. `platinum/advisors/{id}/timeseries` is ONE family over N per-advisor keys).
It is NOT the frozen served-KEY list -- that is DS~B + CVO's deliverable (P4E-1). Do not read
family rows as key counts; do not conflate the two frames.

## DENOMINATORS (every count's frame, printed first)

| set | count | source |
|---|---|---|
| run-8d census live families | **104** | `data/assets/scripts/gold/runners_49f/d00_census_out.json` (census_version `caa2dc28...-r8d`, bucket opal-data-bd, 16,452 objects, 10 enumerated prefixes) |
| FE-read families | **24** (16 matched-live + 8 REACHABILITY dead routes) | `d00_fe_routes_input.json` (portal DEV HEAD 08-11, advisor-intelligence.ts line-cited) + census reconciliation |
| D-fleet emitter target families | **17** (14 emitter scripts; d12 covers 2 families, d13 covers 3) | emitter FAMILY constants, `runners_49f/d01..d14` |
| proof-of-spec instances | **14**, all schema-valid, **0 non-PASS acceptance rows** (PASS or N/A-BY-CONSTRUCTION only) | `org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/PROOF_OF_SPEC_49F_*.json`, checked mechanically this session |
| inventory rows below | **113** = 104 census + `gold/entities/clients/detail` (absent from census -- gap G3 below) + 8 REACHABILITY families (absent by construction: no live instance) | this document |
| accounting tie | 16 emitted-in-census + 1 emitted-not-in-census + 14 platinum-no-emitter + 2 gold/clients dormant pair + 72 out-of-frame + 8 reachability = 113 | ties exactly; no family silently dropped |

Classification axis (the TO's enum, EXACTLY ONE per row): **EMITTED-with-instance /
DECLARED-GATED / UNKNOWN**. Per Rule 24 (intent coherence) the DECLARED-GATED rows carry a
separate **gate-kind** FIELD -- BUILD / ROUTE-DISPOSITION / PUBLISHER-ACT / P5-DISPOSITION --
so one axis is not made to carry two intents. **UNKNOWN rows: 0** (stated, not silent).

## SECTION A -- EMITTED-with-instance: 17 families

Instance paths are under `org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/`.
CVO grade state: per CVO's 154146Z frame (9/17 BAR-CLEARED, 8/17 SCOPE-VALIDATED; residuals
P3/P4-phase by declaration) -- the per-family grade join is CVO's record (P1-SWEEP-49F), not
re-asserted here.

| family | emitter | instance | notes |
|---|---|---|---|
| platinum/firm/header_metrics | d01 | PROOF_OF_SPEC_49F_OVERLAY_HEADER_METRICS_20260811.json | archetype |
| platinum/firm/dashboard | d02 | ..._FIRM_DASHBOARD_... | windows plane rides the consumption pass (D below) |
| platinum/firm/fee_efficiency | d03 | ..._FEE_EFFICIENCY_... | windows.* exclusion EXPIRES at consumption pass; fee-model plane V7 |
| gold/artifacts/clients_tab | d04 | ..._CLIENTS_TAB_... | V9 windows; identity spine V8 rides two-writers @c127712198 (FILED-not-fixed, carried not chased) |
| gold/entities/clients/detail | d05 | ..._CLIENT_DETAIL_... | live successor of gold/clients/{id} (COO 174237Z); V16 windows; V8 @c127712198 |
| platinum/firm/mix_summary | d06 | ..._MIX_SUMMARY_... | mix_periods history at consumption pass; A_07 gate CLOSED (built+certified @d76402f87e) |
| platinum/firm/leaderboard | d07 | ..._FIRM_LEADERBOARD_... | narrowed typed-zero rows (period_start_aua etc.) at consumption pass |
| platinum/49financial/ownership_map | d08 | ..._FIRM_OWNERSHIP_MAP_... | structural, no monetary plane |
| platinum/firm/timeseries_overview | d09 | ..._TIMESERIES_OVERVIEW_... | V22 blanket |
| platinum/firm/cumulative_chart | d10 | ..._CUMULATIVE_CHART_... | V23 blanket |
| platinum/firm/clients-tab-slim | d11 | ..._CLIENTS_TAB_SLIM_... | V26 two-kind (D3-title / D7-lot + window) |
| platinum/firm/timeseries_chart | d12 | ..._TIMESERIES_CHART_TWINS_... | twin 1 |
| gold/artifacts/timeseries_chart | d12 | ..._TIMESERIES_CHART_TWINS_... | twin 2, graded 2x in one pass |
| platinum/firm/partner_analytics_quarterly | d13 | ..._PARTNER_ANALYTICS_TRIO_... | trio |
| platinum/firm/partner_analytics_monthly | d13 | ..._PARTNER_ANALYTICS_TRIO_... | trio |
| platinum/firm/partner_analytics_annual | d13 | ..._PARTNER_ANALYTICS_TRIO_... | trio; V33 pre-floor rows are D9 FLOOR-BOUND, never fillable (see D) |
| platinum/firm/advisor_nna_canonical | d14 | ..._ADVISOR_NNA_CANONICAL_... | V34 blanket; windows at consumption pass |

## SECTION B -- DECLARED-GATED: 24 families (each blocker NAMED with the artifact/ruling that clears it)

**B1. gate-kind=BUILD (fleet extension), FE-READ, legacy-served live -- 4 families**
`platinum/advisors/{id}/timeseries` (ai.ts :870) - `platinum/advisors/{id}/nna_clients` (:932) -
`platinum/advisors/{id}/exec_summary` (:947) - `platinum/accounts/{id}/summary` (:1274).
Blocker: NO canonical emitter exists; production serving continues on the legacy bd chain
(unchanged, P5-protected). Cleared by: a fleet-extension build decision at the P4E-1 key frame
(DS~B+CVO) -- the pattern spec s4 names per-advisor scoping as THE advi parameter whose full
decomp "is the first advi work package, not a formality". These 4 have a DECLARED consumer today.

**B2. gate-kind=BUILD (fleet extension), consumer edge UNCONFIRMED at run-8d -- 8 families**
`platinum/advisors/{id}/{mix,positions,summary}` (3), `platinum/clients/{id}/{composition,concentration,mix_timeseries,summary,views}` (5).
Live-served, NOT in the FE-24 direct-read set (possible reads via dynamic drills the run-8d FE
leg did not capture). Blocker: same fleet-extension gate as B1 PLUS the consumer edge must be
established first. Cleared by: DE's P4 route census (T-A/T-C lane) resolving read-vs-dead, then
the B1 path if read.

**B3. gate-kind=ROUTE-DISPOSITION (dead FE routes) -- 8 families**
`platinum/firm/{client_directory,cohort_a_summary,activity_scan,cash_drag,firm_concentrations}` (5),
`platinum/advisors/base`, `platinum/clients/base`, `platinum/clients/{id}/accounts/{acct}/timeseries` (3).
FE code reads them (line-cited in d00_fe_routes_input); **NO live instance exists on ANY plane**
(census run-8d reconciliation REACHABILITY findings) -- the legacy chain never served them either,
so the D fleet creates no regression by not emitting them. Blocker: a build-the-family vs
retire-the-read ruling that does not yet exist. Cleared by: CTO/DE disposition at P4 (routed in
this report's SECTION E -- a decision ask, not a build gap).

**B4. gate-kind=PUBLISHER-ACT -- 1 family**
`platinum/firm/leaderboard.prior_week` (live 08-11). A rotation artifact of the publisher leg
(prior-week copy at publish time), not an emitter computation. Cleared by: DS~B's
d_publisher_base rotation handling inside P4-EMIT-49F (P4E frame).

**B5. gate-kind=P5-DISPOSITION (dormant/superseded -- NOT build gaps, NOT deletions) -- 3 families**
- `platinum/firm/employee_leaderboard`: last write 2026-04-09 = **131d stale -> Rule 25 DORMANT**
  (>90d, no declared exception found; margin is far past any trading-calendar effect).
  Successor-check per Rule 25: candidate successor `platinum/firm/leaderboard` (live daily) --
  adjudication belongs to P5's methodology, NOT concluded here.
- `gold/clients/` + `gold/clients/{id}` (2,948 instances, last write 2026-04-07): dormant-superseded,
  successor `gold/entities/clients/{z}/detail.json` **documented** (d05 docstring + COO 174237Z --
  reader AND writer moved). KEY-MIGRATED kind, the exact Rule-25 twin hazard: a leaf-name census
  reads the live successor as the orphan. P5 input, flagged never deleted.

## SECTION C -- OUT-OF-FRAME (stated with denominator, not classified on the D-fleet axis)

**72 families**: the legacy producer plane -- `gold/artifacts/*` (incl. the 24 partner_analytics
quarterly snapshots 2020Q3..2025Q4, which are CLOSED-PERIOD-IMMUTABLE, Rule 25's second exception
kind: frozen CORRECTLY, a refresh would be the defect), `gold/timeseries/*`, `gold/snapshots/*`,
`status/*` markers. These are P5 census/teardown inputs under the ratified debt methodology
@db365bb06c; the census's own orphan_law governs (FLAGGED, never deleted here). Two of the
`gold/artifacts/*` families ARE in-frame and sit in Section A (clients_tab, timeseries_chart twin).

**Census-instrument gaps, for the run-9 vintage (banked, no action taken):**
- **G3 (NEW, this session):** `gold/entities/` is ABSENT from d00's PREFIXES list, so the census
  structurally cannot see the live client-detail successor family (worked around at build time via
  `d05_census_fragment.json`, but the enumerator still has the hole). Same class as the two patched
  gaps (@2685dd34f1 prefix absent; @76d225de9b size cap). Fix belongs to the next census run, not
  to this TO.

## SECTION D -- THE BACKFILL DETERMINATION (P1C-2): what remains, enumerated

**D0. The spine fill is DONE and live-confirmed -- nothing of it remains.** Live listing this
session (paginated boto3, denominator = 10 tables under `opal-data-assets/portal/gold/advi/49financial/`):

| table | partitions | range |
|---|---|---|
| canonical/canonical_valuation | 526 | 2024-07-08..2026-08-10 |
| canonical/flow_ledger | 526 | 2024-07-08..2026-08-10 |
| canonical/nna_canonical | 526 | 2024-07-08..2026-08-10 |
| canonical/twr_daily | 525 | 2024-07-09..2026-08-10 (525 BY DESIGN: TWR needs a prior day) |
| canonical/nna_atomic | 1 | 2026-07-15 (see D2 -- NOT a gap) |
| dimensions/dim_account | 2 | ..2026-07-15 (P3 scope, see D3) |
| dimensions/dim_relationship | 2 | ..2026-07-15 (P3 scope) |
| dimensions/dim_boundary | 1 | 2026-08-11 (P3 scope) |
| dimensions/dim_calendar | 1 | 2026-08-11 (P3 scope) |
| dimensions/dim_security | 1 | 2026-08-11 (P3 scope) |

This confirms ledger CLOSED @61d9600bf2 (fill-2 2,103/2,103) at the artifact. The framework
CURRENT-STATE unlock (1) ("the 525-partition BACKFILL ... 20-date timing sample authorized;
Andrew's fill-word arrives as a priced card", vintage @11908b1835 ~1750Z 08-11) and PRD s5 A.2 /
s6 #3 **predate the fill's execution and close (17:45-19:03Z 08-11)** and are SUPERSEDED -- routed
to CTO in Section E for the plan-line correction. **The closed spine fill is NOT re-priced**
(the TO's named forbidden shortcut).

**D1. WHAT REMAINS -- the WINDOW-CONSUMPTION PASS (not a data fill).** The typed-zero
window/series planes were built when the spine had one day; the spine now has 526. Remaining
work = re-emit each window/series family over the filled spine + NARROW its divergence rows
(the _GOVERNANCE tuning law: narrowing is free; a post-pass diff is a REAL failure) + CVO
re-grade. Enumerated scope (12 of the 17 families; the list, not a digit):
d02 dashboard - d03 fee_efficiency (windows.*) - d04 clients_tab (V9) - d05 client_detail (V16)
- d06 mix_summary (mix_periods) - d07 leaderboard (narrowed typed-zero rows) - d09 tso (V22)
- d10 cumulative (V23) - d12 twins x2 (V27) - d13 trio in-floor trailing periods - d14
advisor_nna_canonical (V34 windows). Excluded from the pass: d01 header_metrics (no window
plane gated on the fill), d08 ownership_map (structural), d11 slim (its gated planes are
D3/D7-kind, not fill-kind). **Cost basis: 1 emission per family (each family is ONE current
artifact whose windows read history) -- there is NO per-date scope.** Priced in the P1C-3 card.

**D2. nna_atomic 1/526 is NOT remaining backfill.** Consumer census (grep over the runners_49f
corpus + all gold script trees + infra; denominator = the repo): **ZERO readers** of the
`canonical/nna_atomic` table -- only its own runner (c03_runner) writes it. Its successor
derivation `nna_canonical` (C_01, NNA re-based ON the flow ledger, the ratified flow exception)
is FILLED 526/526 and is what d14 consumes (`runner_common.nna_weekly_account_sums` reads the
nna_canonical series). Classification: dormant-superseded predecessor (Rule 25 KEY-MIGRATED
kind), P5 disposition input. Filling it would spend hours producing partitions nothing reads.

**D3. The dimensions are P3 scope, not backfill.** Dims are as-of snapshots (current vintage),
not per-date series to fill: historical boundary truth is already embedded per-date in the spine
via fill-2's contemporaneous truncated-leg sweeps (@5b93cb68e0: boundary_version DISTINCT per
date in the artifact bytes). What the stale dim vintages (07-14/07-15) actually evidence is
production-bar criterion (i) unmet -- the producers are session acts -- which is EXACTLY
P3-CLOSE-49F's deliverable (dims into the scheduled chain, newest partition = T-1 from the
scheduled run). No dim backfill exists to price.

**D4. NOT-BACKFILL design gates (named so the card cannot silently absorb them):**
V17-CD-TENURE / V10-CT-TENURE (D8 first-seen semantics) - V18-CD-TAX / V11 / V26 two-kind rows
(D7 lot canonicalization; D3 title wiring) - V8/V14 identity-spine grammar (rides two-writers
@c127712198) - V33 PRE-FLOOR trailing periods (D9: history before the monolith floor 2024-07-08
does not exist in silver -- structurally unfillable, permanent floor-bound rows) - V3-class
vendor-universe rows (DIVERGE-PENDING-SOVEREIGN). Each has its named cell/owner; none is
purchasable with compute.

**VERDICT (P1C-2): the remainder is NON-EMPTY but contains ZERO per-date data fill.** It is
one consumption pass: 12 family re-emissions + divergence-row narrowing + CVO re-grade.
The P1C-3 card prices exactly that remainder.

## SECTION E -- ROUTED (decision/correction asks carried by this report; no action taken here)

1. **CTO:** plan-line correction -- framework CURRENT-STATE unlock (1) + PRD s5 A.2 / s6 open-decision
   #3 supersede to "spine fill EXECUTED + CLOSED @61d9600bf2 (08-11); residual = the window-consumption
   pass" (D0/D1 evidence above).
2. **CTO/DE (P4):** the 8 dead-FE-route families (B3) need a build-vs-retire disposition; the census
   recon is the finding artifact; no ruling exists.
3. **DS~B (P4E-1):** B4 prior_week rotation + the B1/B2 fleet-extension frame land in the served-key
   list work; this table's family rows are inputs, grain stated.
4. **Census run-9 owner:** G3 -- add `gold/entities/` to the PREFIXES enumeration.
5. **COO (already banked 161056Z):** comp-pipescript io cannot see the runners_49f corpus (Phase-1
   tool mismatch on all three runner TOs).

**Two-writers @c127712198:** carried as a named blocker note on the identity-spine riders (d04/d05
rows) and in D4 -- FILED-not-fixed per the TO's Do-not.
