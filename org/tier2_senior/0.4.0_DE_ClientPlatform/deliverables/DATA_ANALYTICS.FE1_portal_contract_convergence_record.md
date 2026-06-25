# DATA_ANALYTICS — Portal Contract Convergence Record (FE-down ⇄ gold-up)

> **REFRAME (Andrew-direct via DS, 2026-06-25; CTO `172040Z`):** the Schwab-raw-native canonical is **PARALLEL R&D coexisting
> with BD — no excise, no cutover, no contract-LOCK.** The DE↔DS convergence below (publisher shapes, agnostic-drops, the N1/N2
> deps) stays valid as R&D foundation design; any "lock / excise / partial-lock" language is stood down to prospective framing.

**Authors:** 0.4.0_DE_ClientPlatform (FE-down / demand) + 0.4.0_DS_ClientPlatform (gold-up / supply)
**Date:** 2026-06-25 | **archetype:** COORDINATE
**Inputs:** FE1 manifest `DATA_ANALYTICS.FE1_advi_panel_platinum_groupd_manifest.md` @ 98764fb65 (demand side) × DS A1 D-tier field-requirements + Schwab-raw-native silver-dim design `docs/briefs/DATA_ANALYTICS_A1_*` (supply side)
**For:** 3.0.0_SA_CVO (cert) + 1.0.0_SA_CTO (arch-gate, folds into Schwab-raw-native canonize-gold rebuild) | **cc:** 2.0.0_SA_COO

> The portal contract = exactly the platinum keys each rendered ADVI panel needs (FE1 manifest §2), per partner, matched to the
> Group-D producer that emits them (manifest §3) and the DS silver-dim supply that feeds those producers. FE1 (consumer/demand)
> and A1 (producer/supply) reconcile cleanly — this record ratifies the convergence and closes the contract invariant.

## Ratified reconcile decisions (DE + DS concur)

| # | Item | Decision | Owner of any follow-on |
|---|---|---|---|
| 1 | **49F publisher shape** | `D_04.client_portal_summary.py` is the SINGLE platinum publisher; `D_00/D_00b/D_00c/D_00f/D_01/D_02/D_03` write `gold/artifacts/*` intermediates D_04 republishes. **Both FE1 (consumer trace) and A1 (producer trace) independently arrived here.** Schwab-raw-native rebuild targets this single-publisher shape for 49F. | — (confirmed both sides) |
| 2 | **INF publisher shape** | Inflection fans publish across ~20 `INF_D_0x` scripts (partner_analytics via `INF_09.generate_partner_analytics.py`). INF is its own shape — richest surface (+ Insights panel `INF_D_05/06/07a`, GRO `INF_D_00c`, per-account ts `INF_D_09`). | — (noted; INF rebuild shape distinct) |
| 3 | **GAP 4a — COT `advisor_nna_canonical`** | **INTENDED-ABSENT for COT v1.** COT Distribution is geo-only; advisor dimension not materialized (ADVI_PRTORG §5-A.1 REVISIT-LATER). FE already graceful (404→empty, not a render break). NOT a 49F issue (49F has `D_00f`). | **3.0.0_SA_CVO** formal ruling (DE+DS concur intended) |
| 4 | **GAP 4b — `header_metrics_fresh`** | **INTENDED graceful-degrade.** Artifact is INF-origin (`INF_D_00e.fresh_header_supplement`); 49F/COT headline tile correctly falls back to canonical `header_metrics.json` (`D_00`→`D_04`). Not a missing emit. Schwab-raw-native pipeline produces fresh AUA natively (DS `fact_position` latest-complete-day = $1.63B 49F) → a bd `D_00e`-equivalent is trivially producible IF 49F ever wants the fresh tile, but absent-today is intended. | DS does a bd-bucket `header_metrics_fresh` absence confirm in field-requirements v1.0 |
| 5 | **COT agnostic-drop set** | `D_00c` (leaderboard), `D_02` (advisor-client detail), `D_03` (composition) + `cohort_a_summary.json` / `cash_coverage_summary.json` = produced-but-frontend-unconsumed for COT v1 (Advisors+Books tabs disabled). **AGNOSTIC-DROP** for the lean rebuild; re-add when COT advisor dimension materializes. Folds into DS patch-register / lean-rebuild drop-set. | **0.4.0_DS** folds into essential/agnostic tagging |

## Contract invariant — CLOSED

**(i) No panel needs a field no Group-D produces.** Every FE panel query in manifest §2 resolves to a named producer EXCEPT gaps 4a/4b — both ruled INTENDED-ABSENT (decisions 3+4), so no missing supply remains.
**(ii) Every produced-but-unconsumed output is confirmed agnostic-drop** (decision 5, COT set) or load-bearing (manifest §3 essential sets per partner).

→ The demand side (FE1 §2 platinum keys) and supply side (DS silver-dim 6-table design v0.2/v0.3/v0.4 → Group-D producers) are CONGRUENT. One portal contract.

## Essential producer set (must survive the lean rebuild), per partner
- **49F (BD):** `D_04` + `D_00, D_00b, D_00c, D_00f, D_01, D_02, D_03` (all load-bearing).
- **Inflection (Orion):** `INF_09` + `INF_D_00/00b/00c/00d/00e/00f/02/02b/02c/02d/03/04/04b/05/06/07a/08/09` (all load-bearing).
- **Cottonwood (BD-native):** `D_00, D_00b, D_01, D_04` ONLY (PartnerAnalytics aua/nna/geo + Distribution-geo). Rest = agnostic-drop (decision 5).

## Non-custodian dependencies the unified contract MUST flag (DS-raised, FE-mapped)

The Schwab-raw-native rebuild's bronze=raw-forms does NOT carry two classes of field the portal panels consume — these are Opal-owned-or-bridged relationship-intelligence, not custodian-produced. The arch-gate must see them as explicit non-custodian inputs to the contract:

| # | Non-custodian input | Supply (DS) | FE consumers (DE) — panels that BREAK without it |
|---|---|---|---|
| N1 | **FEES** (fee_bps / fee_schedule → `dim_fee`) | bd-fees pipeline → `A_02 fee_rate_history` / `C_08 advisor_fee_efficiency` (NOT in Schwab raw) | Books: `FeeEfficiencyPanel` + `FeeSummaryPanel` (`platinum/firm/fee_efficiency.json`, D_00c→D_04); `ClientsTab` income/fees headline; `AdvisorPublicProfile` fee section; advisor/client summary `fee_summary` |
| N2 | **HOUSEHOLD / RELATIONSHIP GROUPING** (which taxpayers form one client/household) | BD relationship grouping (Schwab `ssn_tin` = 4,188 taxpayers; portal `client_count` = 2,928 BD-relationship multi-taxpayer grouping). **Andrew ruling source now: bridge-via-xref vs Opal-owned dim.** | EVERY `client_count` headline (PartnerAnalytics/dashboard/ClientsTab); `client_directory.json` (`INF_D_02c` / D_04); `ClientListPanel`; the entire L3 client drill `platinum/clients/{hh}/*` |

Both feed the portal contract but are NON-CUSTODIAN — N1 is Opal-bridged (fee data), N2 is Opal-owned-or-bridged relationship intelligence (Andrew-ruling pending). The unified contract carries them as first-class inputs so the canonize-gold rebuild provisions them explicitly (a Schwab-raw-only rebuild would silently drop `client_count` correctness + all fee panels).

## Status
DS rulings A/B/C/D received + folded (gold-up essential set = §"Essential producer set"; COT drops confirmed; both gaps ruled intended-absent). DS handing its gold-up essential set + Schwab-raw-native D-tier field list (silver-dim design v0.1/v0.2_keys/v0.3/v0.4) → DE authors the UNIFIED portal-contract artifact for CTO arch-gate; DS co-signs.
DS folding FE1 §2 consumer-contract into A1 field-requirements v1.0 for a single co-signed publish. CVO certs FE1 completeness + rules gap 4a; CTO arch-gates the unified contract into the Schwab-raw-native canonize-gold rebuild. No blocks.
