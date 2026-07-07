# ADVI_INFREF.REPOINT-COMPLETE -- account-source map (RAVC-1, DS~A)

**Owner:** 0.4.0_DS_ClientPlatform~A | **Scope (CTO-ruled):** the 06-30 ADVI_INFREF LEG-1/LEG-2 repoint
(silver/accounts_dim -> accounts_v2) was applied INCONSISTENTLY across the INF gold scripts. This maps
which account-source EACH script actually reads, distinguishes correctly-frozen from accidentally-stale,
and lists the stragglers. Grounded from the sweep + a source grep (2026-07-06); per-script USAGE
verification (primary vs fallback vs vestigial) is the next step before any straggler is confirmed --
grounding discipline (the DI-13 false-positive lesson: a defined KEY constant != a live primary read).

## The two sources
- **FRESH:** `silver/api_dims/accounts_v2/snapshot_date={d}/data.parquet` (REST canonical, daily) OR
  `gold/dimensions/accounts_dimension_latest.parquet` (INF_A_00's output, accounts_v2-derived).
- **FROZEN:** `silver/accounts_dim/latest.parquet` -- producer decommissioned, froze **2026-04-29**.
  Any PRIMARY read of this = accounts opened after 04-29 are ABSENT -> silently dropped/mis-served.

## Map (initial -- source grep + repoint-comment evidence)

| Script | References frozen silver/accounts_dim? | Repoint comment? | Classification (pending usage-verify) |
|---|---|---|---|
| INF_A_00 accounts_dimension | no (reads accounts_v2 directly) | n/a | **FRESH** -- but this is the DI-7 ROOT: accounts_v2 has NO reg_type -> tax_status collapsed (durable = un-freeze the reg_type SOURCE; DS~B grounded, folds in here) |
| INF_A_04 client_dimension | no (reads A_00 gold dim) | n/a | FRESH (rides A_00) |
| INF_B_00 canonical_holdings | no (reads accounts_v2) | n/a | FRESH |
| INF_C_09 fee_status_audit | mentions (comment) | YES ("replaces frozen-04-29") | REPOINTED (verify the live read is accounts_v2) |
| INF_D_00 portal_aggregates | KEY defined | YES ("repointed off frozen-04-29") | REPOINTED = DI-7 (repointed but dropped tax_status -- fix under the A_00 durable) |
| INF_D_00c portal_leaderboard | KEY defined | YES ("repointed off frozen-04-29") | REPOINTED (verify) |
| INF_09 partner_analytics | mentions (comment) | "accounts_dim NOT consumed" | N/A (doesn't read it) |
| **INF_D_07 concentration_risk** | ACCTS_DIM_KEY = frozen | **NO** | **STRAGGLER = DI-12 (confirmed)** |
| **INF_D_07a firm_concentrations** | ACCTS_DIM_KEY = frozen | **NO** | **CANDIDATE STRAGGLER (new -- was 'clean' in the sweep; reads frozen dim)** |
| **INF_D_02 advisor_client_detail** | SILVER_ACCOUNTS_DIM = frozen | **NO** | **CANDIDATE STRAGGLER (verify primary vs the accounts_dim-fallback path)** |
| **INF_D_04 client_portal_summary** | SILVER_ACCOUNTS_DIM = frozen | **NO** | **CANDIDATE STRAGGLER (verify -- complex; may be a specific-field read)** |
| **INF_D_05 client_top_holdings** | SILVER_ACCOUNTS_DIM = frozen ("fallback") | **NO** | **CANDIDATE (fallback -- verify if the fallback ever fires / is stale)** |
| **INF_D_06 cash_drag/client_ts** | SILVER_ACCOUNTS_DIM = frozen ("fallback") | **NO** | **CANDIDATE (fallback -- verify)** |
| lib/tax_status.py | doc only (census) | n/a | N/A (comment, not a read) |

## Systemic finding
The repoint touched **3 scripts (D_00, D_00c, C_09)** but left **~6 (D_07, D_07a, D_02, D_04, D_05, D_06)**
still referencing the frozen dim -- confirming CTO's "half-applied repoint" ruling. DI-12 (D_07) was
just the first confirmed; **D_07a is a NEW straggler** the audit surfaced (it read `clean` in the sweep
because the sweep hunted crash/corruption classes, not source-freshness -- exactly why the completeness
audit is a distinct pass).

## Next (this audit's phases)
1. **VERIFY** each CANDIDATE's actual read: primary account-source vs a fallback that rarely fires vs a
   vestigial KEY constant. Distinguish "correctly frozen" (a registration-STATIC use where a frozen dim
   is legitimate) from "accidentally stale". Ground each against source, not the constant.
2. **RECONCILE** to ONE post-repoint source-of-truth (accounts_v2 / A_00 gold dim), + the A_00 reg_type
   un-freeze durable (recovers the DI-7 81 accts, fallback 9.56%->~0.2%; DS~B grounding).
3. **RAVC COO** the verified straggler-list -> COO gates to CTO (arch the reconciled SoT +
   REPOINT-COMPLETENESS invariant NFRA_GLDINV) -> straggler fixes deploy (pipeline, no local).

## Phase-2 findings (role verification -- grounded 2026-07-06, rail-checked s3 mtimes)

Source freshness (the pivot for the fallback-role scripts):
- **accounts_v2** (repoint target / correct SoT): **FRESH** -- latest snapshot_date=2026-07-06. Current.
- **silver/accounts_dim/latest.parquet** (the accounts_dim fallback): frozen **2026-04-29**.
- **silver/api_dims/household/** (the D_05/D_06 PRIMARY household source): **FROZEN at 2026-04-28** --
  a SECOND frozen source-of-truth the audit surfaced, even older than accounts_dim.

Verified roles:
| Script | Role (grounded) | Verdict |
|---|---|---|
| D_07 concentration_risk | PRIMARY read of frozen accounts_dim | **STRAGGLER** (DI-12, confirmed) |
| D_07a firm_concentrations | PRIMARY read of frozen accounts_dim (household map) | **STRAGGLER** (new; accidentally-stale) |
| D_05.client_top_holdings | primary=household dim (frozen 04-28); fallback=accounts_dim (frozen 04-29) | **STRAGGLER** -- BOTH sources frozen, so the served household map is stale regardless of which fires (NOT a rarely-fires fallback) |
| D_06.client_timeseries | same dual-frozen pattern (household-first, accounts_dim-fallback) | **STRAGGLER** (same) |
| D_04 client_portal_summary | frozen accounts_dim -> household_id + hh count (L786/835) + legacy first_trade_date (L982, self-labeled LEGACY HEURISTIC FALLBACK) | **STRAGGLER (hh count/id)** -- the count path reads the frozen dim; first_trade_date is legacy-fallback (lower-pri) |
| D_02 advisor_client_detail | PRIMARY frozen accounts_dim -> household_id (L708) + tax_status per-advisor (L496) + first_trade_date (L463); account_team is a SEPARATE advisor_key source | **STRAGGLER** (household + tax axes) |
| D_06.cash_drag | ACCTS_DIM_KEY = gold/dimensions/accounts_dimension_latest (L75) -- reads the FRESH A_00 gold dim | **NOT a straggler** (already fresh; the D_06 straggler is client_timeseries) |

**SECOND SOURCE-OF-TRUTH GAP:** `silver/api_dims/household` (froze 04-28) is a DISTINCT frozen
dependency from accounts_dim. The reconciled SoT must address BOTH -> the NFRA_GLDINV completeness
invariant widens to the household axis too.

## PHASE-2 COMPLETE -- verified straggler-list + a-vs-b mechanism (for the CTO gate)

**VERIFIED STRAGGLERS (6, all accidentally-stale):** D_07, D_07a, D_05.client_top_holdings,
D_06.client_timeseries, D_04 (hh count/id), D_02 (household + tax).
**NOT stragglers (fresh, refined out by grounding):** D_06.cash_drag + D_05.activity_scan (both read
the FRESH A_00 gold dim). **Already-repointed:** D_00, D_00c, C_09.

### The a-vs-b mechanism (COO Rule-22 ask -- determines the FIX SHAPE), grounded on INF_A_00
The 2 dims froze within a day (household 04-28, accounts_dim 04-29) = common-cause, BUT the fix splits
by AXIS because accounts_v2 (fresh 07-06) CARRIES some-but-not-all of what the consumers need:
- **HOUSEHOLD axis -> fix (a) REPOINT-suffices.** accounts_v2 carries `household_id` directly (INF_A_00
  L27-28/L103-104: household_id is an identical-name passthrough, no rename; A_00 normalizes it to Int64
  at L247-249). So A_00's `gold/dimensions/accounts_dimension_latest.parquet` is a FRESH, complete
  account_id->household_id map. FIX: repoint the 6 stragglers' household map from the frozen
  silver/accounts_dim (and the frozen silver/api_dims/household for D_05/D_06) TO A_00's gold dim. No
  producer un-freeze needed for the household mapping.
- **TAX/reg_type axis -> fix (b) UN-FREEZE-the-producer.** accounts_v2 has NO genuine reg_type --
  A_00 maps `account_type -> reg_type` (L100/L252-255) but account_type is NOT a registration type, which
  is exactly what collapsed tax_status = DI-7. So the tax consumers (D_00, D_02 per-advisor tax) need a
  GENUINE reg_type source un-frozen (DS~B's A_00 durable: refresh the silver reg_type feed or land a
  real reg-type into accounts_v2) -- a repoint alone does NOT fix tax (accounts_v2 lacks the info).

### Recommended reconciled SoT (-> RAVC COO -> CTO arch-gate)
1. Household map: all 6 stragglers repoint to `gold/dimensions/accounts_dimension_latest` (fresh). Retire
   the reads of frozen silver/accounts_dim + frozen silver/api_dims/household.
2. Tax/reg_type: the A_00 reg_type-source un-freeze (DS~B) -- separate durable; D_00 keeps DS~B's DI-7
   interim (silver-rejoin) until the un-freeze lands.
3. NFRA_GLDINV repoint-completeness invariant: assert no served D-script reads a frozen dim -- across
   BOTH the accounts axis and the household axis (consumer-set).
