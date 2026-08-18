# P4E-1 FROZEN SERVED-KEY LIST -- ADVI / 49 Financial / Schwab 08335338 (PROPOSED-v1)

**Author:** 0.4.0_DS_ClientPlatform~B (publisher lane) · **Joint owner:** 3.0.0_SA_CVO (P4-PINS)
**TO:** OPAL_ADVIPOINTERS.P4-EMIT-49F @49dd8469d1, amended @7389357 (P4E-1..P4E-8)
**Status:** PROPOSED-v1 -- the FREEZE EVENT is CVO's concur citing this commit. Until then this is
the working enumeration, not the denominator.
**This list supersedes the plan's "15" (COO notified CTO, GO msg 160704Z). Members are NAMED, never
a digit.**

## FRAME (declared, Rule-24)

- **UNIT = a served key of the ADVI-49F product** (Advisor Intelligence product, firm 49 Financial,
  Schwab account 08335338), wherever the key lives today (`opal-data-bd` `platinum/*` AND `gold/*`
  planes -- the served plane is defined by consumption, not by prefix). One emitter serving N keys =
  N rows (CVO convention, CVO_49F_KILL_CLEAR_ACCOUNTING_20260811.md). A FLEET family = ONE row with
  its live instance count stated beside it.
- **Disposition axis** (one intent: what P4-EMIT does with the key; values MECE, same grain):
  `EMIT` (twin now) · `DECLARED-GATED(<named blocker, release-holder>)` · `OPEN(<resolver>)` ·
  `EXCLUDED-DORMANT` (Rule 25; not a deletion warrant). Dispositions take different remedies;
  each row names its remedy-holder (Rule-24(iv)).
- **Twin key law:** advi twin = `s3://opal-data-portal-v2/platinum/advi/49financial/{legacy leaf
  VERBATIM}`. NO spelling normalization -- legacy carries both spellings (`clients-tab-slim` beside
  `header_metrics`) and both are preserved as-is (spelling law: never "fix" one).
- **d12 twin collapse:** the two legacy timeseries_chart keys collapse to ONE advi key by
  construction (one producer per key). Both legacy reads repoint to it at row 4c. CVO pins measure
  each legacy twin SEPARATELY pre-flip (they have diverged in vintage: platinum 36,306,894B
  LM 08-15 vs gold 38,925,029B LM 08-18 -- legacy chain wrote them on different days; flagged, not
  adjudicated -- CVO 164408Z).

## THE MEMBERS (19 rows)

| # | legacy served key (opal-data-bd) | emitter | FE consumer (d00 fe census, advisor-intelligence.ts) | disposition | advi twin key (platinum/advi/49financial/) |
|---|---|---|---|---|---|
| 1 | `platinum/firm/header_metrics.json` | d01 | `:284` | **EMIT** | `header_metrics.json` |
| 2 | `platinum/firm/dashboard.json` | d02 | `:449` | **EMIT** | `dashboard.json` |
| 3 | `platinum/firm/fee_efficiency.json` | d03 | `:480` | **EMIT** | `fee_efficiency.json` |
| 4 | `gold/artifacts/clients_tab.json` | d04 | `:321` (apigw-lambda `clients-tab`) | **DECLARED-GATED** (household spine map -- P4E-8(ii): current build emits `rel_` keys at `d04_clients_tab.py:72`; no household-grain crosswalk exists, d04 header. Release: the PRD §10 spine-map hop) | `clients_tab.json` (reserved) |
| 5 | `gold/entities/clients/{key}/detail.json` **FLEET** -- 3,751 live prefixes (3,612 `z*` + 138 `acct_z*` + 1 `"0"`, CRO map §2) | d05 | Lambda C5 route `opal-partners-data:932-934` (+ C6 `:1125`) | **DECLARED-GATED** (same blocker: crosswalk reaches EXACT-class 1,652 of 3,612 households; P4E-8(i) key-set equality unreachable until the spine map lands. Release: same hop) | `clients/{key}/detail.json` (reserved; grammar = served z per CRO map §4.3) |
| 6 | `platinum/firm/mix_summary.json` | d06 | `:508` | **EMIT** | `mix_summary.json` |
| 7 | `platinum/firm/leaderboard.json` | d07 | `:1311` | **EMIT** | `leaderboard.json` |
| 8 | `platinum/49financial/ownership_map.json` (NOTE: prefix is `platinum/49financial/`, NOT `platinum/firm/` -- CVO 164408Z) | d08 | no cite in scanned file (scan scope = advisor-intelligence.ts only) | **EMIT** (consumer-cite OPEN at DE row 4c) | `ownership_map.json` |
| 9 | `platinum/firm/timeseries_overview.json` | d09 | `:356` | **EMIT** | `timeseries_overview.json` |
| 10 | `platinum/firm/cumulative_chart.json` | d10 | `:378` | **EMIT** | `cumulative_chart.json` |
| 11 | `platinum/firm/clients-tab-slim.json` | d11 | no cite in scanned file; key-free family (`types.ts:980` omits `clients[]`, CRO map) | **EMIT** | `clients-tab-slim.json` |
| 12 | `platinum/firm/timeseries_chart.json` (twin A) | d12 | `:409` | **EMIT** | `timeseries_chart.json` (SHARED with row 13) |
| 13 | `gold/artifacts/timeseries_chart.json` (twin B) | d12 | `:300` (`artifacts/timeseries_chart`) | **EMIT** | `timeseries_chart.json` (SAME advi key as row 12 -- twin collapse, see FRAME) |
| 14 | `platinum/firm/partner_analytics_quarterly.json` | d13 | no cite in scanned file | **DECLARED-GATED** (CTO role_aua ruling -- population 9-vs-15 basis, P4E-6. Release: CTO, routed by COO 160704Z) | `partner_analytics_quarterly.json` (reserved) |
| 15 | `platinum/firm/partner_analytics_monthly.json` | d13 | same | **DECLARED-GATED** (same) | `partner_analytics_monthly.json` (reserved) |
| 16 | `platinum/firm/partner_analytics_annual.json` | d13 | same | **DECLARED-GATED** (same) | `partner_analytics_annual.json` (reserved) |
| 17 | `platinum/firm/advisor_nna_canonical.json` | d14 | `:392` | **EMIT** (P4E-4 membership contract binds: any active role, once per advisor, non-additive, splits never weight return) | `advisor_nna_canonical.json` |
| 18 | `platinum/firm/leaderboard.prior_week.json` | **NO EMITTER** | no cite in scanned file | **OPEN** (LIVE key: LM 2026-08-16T00:25:58Z, same batch as the legacy chain's last write. Emitter gap NAMED -- not in the CVO-17 frame because that frame counted emitter-covered keys. Resolver: DE row-4c consumer-confirm -> EMIT-later (new emitter or d07 second key) or EXCLUDED) | `leaderboard.prior_week.json` (reserved) |
| 19 | `platinum/firm/employee_leaderboard.json` | **NO EMITTER** | no cite in scanned file | **EXCLUDED-DORMANT** (LM 2026-04-09T22:24:14Z = 131d >= 90d, Rule 25, no declared exception; successor CANDIDATE = `leaderboard.json` -- flagged, NOT adjudicated; NOT a deletion warrant) | none |

## DENOMINATOR STATEMENT (for rows 4a / 4b / 4c)

**19 members enumerated.** EMIT-now = **13 legacy keys -> 12 advi twin objects** (rows 12+13 share
one). DECLARED-GATED = **5 keys** (rows 4, 5, 14-16), each with a named blocker and release-holder.
OPEN = **1** (row 18). EXCLUDED-DORMANT = **1** (row 19). CVO pins (row 4b) land on declared
legacy->advi pairs; gated rows pin on the legacy side only until release.

## RECONCILIATION (the three frames -> this enumeration)

| frame | members | explained by |
|---|---|---|
| CVO-17 (KILL_CLEAR_ACCOUNTING, emitter-anchored) | rows 1-17 | counted keys WITH emitters; correctly included the 3 gold-plane keys the platinum read missed |
| DS~B census-16 (154855Z: 15 `platinum/firm/*` + ownership_map) | rows 1-3, 6-12, 14-19 (- rows 4, 5, 13) | platinum-plane read; missed the gold-plane keys; included the 2 no-emitter keys (rows 18, 19) the emitter frame drops |
| plan "15" (@a2f27c8d0a §3 row 4a) | superseded | enumeration supersedes the digit (COO -> CTO, 160704Z) |

**Correction to CVO 161011Z row 5 (carried jointly, source-grounded):** d05's served target is the
`gold/entities/clients/{key}/detail.json` fleet (`d05_client_detail.py:32` FAMILY +
`:230` fan-out path; census = live-harvest fragment `d05_census_fragment.json`, NOT d00 -- d00
sampled the dormant predecessor `gold/clients/{id}`). `platinum/clients/{id}/summary` is a
DIFFERENT fleet (INF-pattern C8, census-orphan-flagged) and is a NON-MEMBER here.

## EXPLICIT NON-MEMBERS (so this list is never read as "all ADVI-49F serving")

1. **8 FE-read families with NO live instance** (REACHABILITY findings, d00 reconciliation):
   `client_directory`, `cohort_a_summary`, `activity_scan_{window}`, `cash_drag_{window}`,
   `firm_concentrations`, `advisors/base`, `clients/base`, `clients/account_timeseries` -- nothing
   to twin; DE row-4c awareness.
2. **The per-advisor fleet** `platinum/advisors/{id}/{summary,exec_summary,mix,nna_clients,positions,timeseries}` (6 census families, FE-cited `:670/:870/:932/:947`) and **the per-client fleet**
   `platinum/clients/{id}/*` (5 families): LIVE served keys with NO emitter in the D fleet --
   outside this TO's denominator, SURFACED to COO as the banked line (row 4c cannot flip advisor
   pages without them; someone must own that wave).
3. `gold/artifacts/*` intermediates, `gold/snapshots/*`, `gold/timeseries/*` (census
   orphan-candidates): producer-side artifacts, not served keys of this product; P5 inputs,
   flagged-never-deleted.

## OBLIGATIONS RIDING THIS LIST (not blocking the freeze)

- **P4E-8(iii):** the 138 `acct_z*` prefixes each get a disposition (serve/retire/reclassify) --
  lands with my d05-row work, on the gated row's timeline.
- **P4E-5:** never-widen disclosure per EMIT key (what loses a read / what becomes newly visible vs
  the legacy twin), delivered per key at emission for CVO's row-4b pins.
- The d12 twin divergence re-grade (CVO 164408Z) -- CVO's sweep re-grades twin identity rather than
  re-citing the 08-11 byte-identity.

-- 0.4.0_DS_ClientPlatform~B, 2026-08-18
