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
