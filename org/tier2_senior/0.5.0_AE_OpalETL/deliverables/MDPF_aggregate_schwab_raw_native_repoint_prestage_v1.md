# MDPF-Aggregate Adaptation to the Schwab-Raw-Native Canonical Rebuild -- Pre-Stage Scope v1

**Agent:** 0.5.0_AE_OpalETL | **Date:** 2026-06-25 | **archetype:** TRACE (scoping)
**Trigger:** COO idle-redirect (DRIVE) -- pre-stage downstream of the about-to-ship DS Schwab-raw-native canonical-gold rebuild (`0.4.0_DS_ClientPlatform`/DATA_ANALYTICS).
**Status:** PROSPECTIVE forward-exploration -- BANKED/complete (COO RAVC accepted 2026-06-25). RE-BASELINED (COO 172022Z, Andrew-via-DS 171807Z): the Schwab-raw-native canonical is a PARALLEL R&D/foundation build that COEXISTS with the live BD pipeline -- NOT a cutover/excise/lock/served-move; it touches no production path. So there is NO canonical-lock gate to convert this against, and MDPF's production path is NOT changing. This doc characterizes "what WOULD re-point IF the canonical ever fed production" -- useful design input for the parallel build, NOT a pending build-TO. The Fidelity-basis fork (below) is therefore MOOT for production (live served 49F basis unchanged); it remains a design question only for the parallel build.
**RAVC:** COO (cc DS) -- accepted.

## Headline

The MDPF re-point surface is **SMALL and concentrated in exactly ONE function in ONE feeder: `build_mdpf_wse_49f_non_model_aua.py :: compute_partner_custody_total`** (the WS-E non-model feeder). Every other MDPF stage is UNAFFECTED by the BD Schwab-raw-native rebuild:

| Stage | BD-canonical dependency? | Schwab-rebuild impact |
|---|---|---|
| WS-B `wsb_49f_smartx_model_aua.py` | NO -- reads the **SmartX API** directly (identity/api.smartxadvisory.com), writes opal-data-mdpf feeder prefix | NONE (different custodian/system) |
| WS-C `build_mdpf_wsc_inflection_feeder.py` | NO -- Inflection/Orion (Eclipse gold) | NONE (separate INF rebuild track) |
| WS-D.1/D.2 ETF netassets / partner-held-etf | NO -- ETF netassets (own track) | NONE |
| **WS-E `build_mdpf_wse_49f_non_model_aua.py`** | **YES** -- reads `opal-data-bd` silver/allocations + silver/fees + gold/aua_certification | **THE re-point** |
| WS-A `mdpf_aggregate_aua.py` (aggregate) | NO -- reads only the **opal-data-mdpf feeder bucket** (model_aua_positions, non_model_aua) + opal-data-portal-v2 platinum (etf decomp) | NONE structurally; reconciles VALUES that flow up from WS-E (see below) |

## The WS-E re-point (grounded: `build_mdpf_wse_49f_non_model_aua.py:320-369`)

`compute_partner_custody_total(bd_date, crosswalk)` is the only BD-canonical read in MDPF. It:
1. Reads `s3://opal-data-bd/silver/allocations/{bd_date}.parquet`, columns **`[account_id, account_market_value, account_type]`** (:329-331).
2. Excludes liability `account_type` in `LIABILITY_TYPES` (CreditCard, Mortgage, Loans) (:337-338).
3. `certified_aua = sum(account_market_value) over non-liability accounts` (:339).
4. **HARD cross-check** vs `s3://opal-data-bd/gold/aua_certification/{bd_date}.json` `.certified_aua` -- `RuntimeError` (aborts the chain) if delta > $0.01 (:344-359).
5. Custodian decomposition via the crosswalk built from `silver/fees` history (:363-369).

### Re-point deltas (silver/allocations -> Schwab-raw-native canonical)

- **`account_market_value` (account grain).** The new canonical `fact_position` (`opal-data-bd/canonical/silver/fact_position/`) is at **position grain** (date, account_id, security/cusip), not account grain. WS-E needs account-level AUA -> it must either (a) AGGREGATE fact_position to account grain (`groupby account_id sum(market_value)`), or (b) read a pre-aggregated account-AUA **gold** canonical if the rebuild emits one. **CONFIRM with DS:** the canonical column name (`market_value` vs `account_market_value`) + whether an account-grain AUA gold artifact exists (preferred -- avoids WS-E re-aggregating + re-doing the exact $1.63B custody math DS already validated).
- **`account_type` (the liability exclusion).** Per the rebuild, account classification moves to **`dim_account`** (`opal-data-bd/canonical/silver/dim_account/`). WS-E must JOIN fact_position -> dim_account for account_type. **CONFIRM with DS:** dim_account carries account_type with the SAME category values (CreditCard/Mortgage/Loans) the exclusion keys on -- a name/value drift here silently changes the AUA.
- **`account_id` dtype.** Canonical coerces account_id to **padded-string** (leading zeros significant -- the DS zero-pad drift guard). WS-E already has `_norm_account_id`; **CONFIRM** it matches the DS zfill width/convention so the join + crosswalk keys align.

### Re-point delta (gold/aua_certification -> new canonical AUA cert)

- WS-E HARD-FAILs unless its recompute ties to the published `gold/aua_certification/{date}.json .certified_aua` to the cent. The rebuild validates AUA = **$1,631,357,904.10 @06-18** custodian-direct from fact_position. **CONFIRM with DS:** does the rebuild re-emit `gold/aua_certification/{date}.json` (Schwab-native `certified_aua`), or a NEW canonical cert artifact/path? WS-E's cross-check target re-points to whichever. This is the **value-parity-critical seam** -- exactly under the CVO value-parity rider (the Schwab-native chain must reproduce the served certified_aua value); WS-E's $0.01 abort is itself a built-in parity gate.

### NOT re-pointed (important -- bounds the scope)

- **`silver/fees` custodian crosswalk = RETAINED.** Rebuild N1 SCOPES the BD-fees feed to be retained interim (A_02/C_08; exempt from BDAPIMIG Phase-2 decommission; Schwab RPS/ULN/RLD/TRN carry no fee_bps). WS-E's custodian crosswalk (`build_custodian_crosswalk` from silver/fees) is **UNCHANGED**. (This also means MDPF's fees-gate-half -- the FREEZE-DX root just resolved -- is unchanged by the rebuild; the durable bd-49f-fees-runner (0.6.0, bd-v2.36.0) remains the no-re-freeze protection.)

## WS-A aggregate (`mdpf_aggregate_aua.py`)

No structural re-point: it reads only the opal-data-mdpf feeder bucket + platinum. Its Stage-3 reconciliation invariant (`reconcile()`, identity_1: opal_aggregate_aua vs partner feeds, HARD FAIL on ERROR) compares VALUES that flow up from WS-E/WS-B. If value-parity holds (CVO rider), the reconciliation ties exactly as today. **Risk to watch at build time:** if the Schwab-native non-model AUA differs from the BD-reconcile/FIFO-derived value by more than the reconcile tolerance, WS-A's identity_1 trips. The value-parity cert is the upstream guarantee; WS-A's reconcile is the downstream tripwire -- they should agree, but the build-TO must re-validate WS-A's reconcile passes on the Schwab-native values (run on a real partition, not asserted).

## Proposed build-TO shape (on canonical-lock)

1. Re-point `compute_partner_custody_total` (and the crosswalk-independent allocations read) from `silver/allocations` -> canonical `fact_position` (account-grain aggregate) + `dim_account` (account_type join), with padded-string account_id coercion.
2. Re-point the certified_aua cross-check to the new canonical AUA cert artifact.
3. Leave silver/fees crosswalk, WS-B, WS-A, WS-C, WS-D unchanged.
4. Validate end-to-end on a real partition: WS-E certified_aua ties to the canonical cert to the cent AND WS-A reconcile identity_1 passes -> served opal_aggregate_aua value-parity vs the BD-era figure.
5. Standard DS-flow: ds-commit-gate + comp-pipescript io/deployed + comp-validate on the artifact; no force-runs.

## Gating (when does this convert to a build-TO?)

DS silver layer is COMPLETE + validating ($1.63B exact). Canonical LOCKS on: CTO arch-gate (G1-G3 D-tier-waist/excise/49F-first), CVO value-parity cert (FE1 + the rider), DS co-sign on the unified portal contract v1.0. N2 household is DEFERRED and does NOT affect MDPF (MDPF is firm/account-AUA, not household-grouped). 49F-first sequencing aligns -- MDPF's only BD dep is the 49F Schwab-custodied panel.

## Open confirms for DS (route to `0.4.0_DS_ClientPlatform`)

1. Account-grain AUA: a pre-aggregated canonical gold artifact (path + column), or aggregate fact_position in WS-E?
2. `dim_account.account_type`: present with the same CreditCard/Mortgage/Loans liability values?
3. New canonical AUA-certification artifact: path + `certified_aua` field name (the WS-E $0.01 cross-check target)?
4. account_id padded-string: zfill width/convention, to align `_norm_account_id`.

## Compiler Tools

| Tool | Call | Result |
|---|---|---|
| comp-pipescript io | gold/mdpf_aggregate_aua.py (canonical inputs) | PARTIAL (MDPF not in BD-gold registry -- gap; fell back to source-read) |
| comp-which (prior) / Grep+Read | feeder input-source mapping (WS-B SmartX, WS-E BD-canonical, WS-A feeder-bucket) | PASS (grounded each feeder's actual reads) |

Gap found: `comp-pipescript io` doesn't register the MDPF pipeline (separate from BD-gold) -- MDPF feeder->canonical lineage is invisible to the io tool. Worth filing so the build-TO re-point is on-rails (same gap noted in the FREEZE-DX dx).
