# ADVI_INFREF P1 LEG-1 -- accounts_dim -> accounts_v2 REPOINT (the first per-dim repoint; CTO per-dim co-sign)

**Author:** 0.4.0_DS_ClientPlatform~A | **Date:** 2026-06-30 | **TO:** ADVI_INFREF.P1 LEG-1
**Gate:** CTO per-dim co-sign (build-order pre-blessed) + this is a CORRECTNESS fix (output DELIBERATELY
changes stale->fresh) so it also needs never-widen sign-off (CTO+COO) before the served deploy. Andrew-aware
(COO MODERATE severity: metadata-not-value; served AUA UNAFFECTED -- holdings/positions_mv-derived).
**Grounding:** source-confirmed (the producer `build_accounts_v2` + every consumer read site read this window).

## 1. CENSUS CORRECTION (the gold-read-reconciliation caught a phantom consumer)
The reconciliation doc listed THREE live consumers (INF_09 / INF_C_09 / INF_D_00). Re-grounded against
source THIS window: **INF_09 is NOT a real consumer.** It directly `_read_s3_parquet`s ONLY canonical_nna
(L336) + holdings (L356); its docstring "Inputs" list (silver/aum_snapshot, silver/accounts_dim,
silver/meta/gap_manifest -- L21-23) enumerates the inputs of the CHAIN SCRIPTS it orchestrates via
subprocess, not its own reads. Same stale-docstring class as the partner_analytics writer-map already
corrected in that file. => INF_09 = docstring-only fix, NOT a repoint.

**Real repoint scope (3 -> effectively 2 + 1-already-wired):**
| script | how it reads accounts_dim | repoint |
|---|---|---|
| INF_09.generate_partner_analytics.py | NOT read (stale docstring L21-23) | docstring-only fix (no gate) |
| INF_C_09.fee_status_audit.py | flat `silver/accounts_dim/latest.parquet` (L125, _read_parquet L310) | loader swap -> accounts_v2 latest partition |
| INF_D_00.portal_aggregates.py | flat `latest.parquet` (L49, load_accounts_dim L121) | loader swap -> accounts_v2 latest partition |
| INF_D_00c.portal_leaderboard.py | ALREADY wired accounts_v2 as FALLBACK (load_accounts_v2_dim L292; use_v2 L867) but accounts_dim is PRIMARY for the NMNC cohort fns (_compute_new_clients_per_advisor L492/L529 read accounts_dim.first_trade_date DIRECTLY) | loader swap (make load_accounts_dim source v2-aliased) so the cohort fns get fresh dates with zero logic change |

## 2. SOURCE-CONFIRMED field map (producer build_accounts_v2, convert_orion_api_to_silver.py:395-547)
accounts_v2 is the live primary: daily partitions through 2026-06-30 (today); accounts_dim frozen 04-29
(legacy convert_orion_to_silver.py stopped). Producer keep-map (L429-471):
| accounts_dim contract col | accounts_v2 col | source | note |
|---|---|---|---|
| account_id | account_id | id (L430) | direct, Int64 both |
| household_id | household_id | clientId (L437) | direct, Int64 both |
| first_trade_date | account_start_date | accountStartDate (L442) | **the inception/NMNC signal** -- producer docstring L408-410 explicitly: accountStartDate is the recommended inception field; createdDate is row-creation (can be 6+yr later). The alias is SEMANTICALLY CORRECT (better than the frozen first_trade_date). |
| registration_name | account_name | name (L432) | **SEMANTIC FLAG #1** -- account_name is the ACCOUNT name; registration_name was the registration. For household display (INF_D_00 hh_names) these can differ. See decision below. |
| advisor_key | (none) | -- | **SEMANTIC FLAG #2** -- accounts_v2 has rep_id/representative_name, NOT advisor_key. accounts_dim's advisor_key was all 'firm' (untrusted; INF_D_00c L1079 comment). Dropping it -> INF_D_00 falls back to client_performance.advisor_key (L238) = arguably MORE correct. |

## 3. STRATEGY: repoint at the LOADER, alias to the accounts_dim contract (lowest blast radius)
Rather than rewrite each consumer's logic, change ONLY each script's loader to read the latest accounts_v2
partition and ALIAS columns back to the accounts_dim contract (account_id, household_id, first_trade_date,
registration_name, [advisor_key omitted]). Downstream logic is byte-identical; only the DATA freshness
changes (04-29 -> today) -- which is the entire point of the correctness fix. accounts_v2 is PARTITIONED
(snapshot_date=*/data.parquet) vs accounts_dim's flat latest.parquet, so the loader gains a
latest-partition selector (INF_D_00c already has `_latest_silver_partition` -- reuse the pattern).

## 4. The two SEMANTIC decisions for CTO (these change served output -> never-widen)
- **#1 registration_name <- account_name (household display):** RECOMMEND alias account_name -> registration_name.
  Rationale: without it, INF_D_00 hh_names go blank (the 'registration_name' column-presence check at L230
  fails). account_name is the closest available human label. ALTERNATIVE: leave blank + let the cp-fallback
  / a later dim supply it. CTO call.
- **#2 advisor_key drop -> cp-fallback:** RECOMMEND drop (don't fabricate advisor_key from v2). INF_D_00
  already has the client_performance.advisor_key fallback (L238-240) which is the trusted source; accounts_dim's
  was 'firm'-only and untrusted anyway. Net: equal-or-better. CTO confirm.

## 5. GATE (before the served deploy -- never-widen)
(a) source-confirm accounts_v2 primary -- DONE (daily partitions to 06-30; producer live). [PASS]
(b) sane 2-month delta -- counts/names/account_start_date vs the frozen 04-29 accounts_dim, NOT a regression.
    Verified on the SCHEDULED nightly's artifacts (NEVER#4 -- not an ad-hoc run). Expect: account/HH counts
    within a sane drift band; account_start_date now POPULATED (was frozen); display names sane.
(c) served AUA UNAFFECTED -- AUA is holdings/positions_mv-derived (build_dashboard market_value.sum), NOT
    accounts_dim. The repoint touches counts/dates/names ONLY. Penny-check header_metrics.total.aua unchanged.
(d) CTO+COO never-widen sign-off on the deliberate output change (the display/cohort-date changes).

## 6. Lane split / next
- DS (me): author INF_09 docstring fix (now) + the 3 loader swaps (on CTO co-sign of the 2 semantic calls);
  ds-commit-gate + commit to CLOUD; the served deploy (aws s3 cp to code/gold) is GATED on (d) + the nightly (b).
- CTO: co-sign the 2 semantic decisions (#1, #2) + the never-widen on the output change.
- COO: never-widen co-sign (served display/cohort change); Andrew-aware (already MODERATE-flagged).
- CVO: independently verify the 2-month delta sanity on the nightly artifacts (gate b).
- RAVC CTO EACH script's result after the loader swap (per the build-order directive).
