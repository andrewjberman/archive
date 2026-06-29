# TASK ORDER — DATA_SSOTMG.TO-3

<issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<status>pending</status>
<priority>HIGH — the now-UNBLOCKED gold piece (Andrew decided the source). PRD §7 TO-3.</priority>
<date>2026-06-29</date>

## Context

The held G11-G13 49F advisor/fee gold surfaces (from 08_GOLD_SCOPE.md, held-for-Andrew) are now
UNBLOCKED — Andrew DECIDED the source for the Schwab-SSOT migration: a **thin BD-bridged, scoped,
keyed dim** for the 49F advisor metadata (architect/implementor roles + fee splits), with an honest
bd-source flag — NOT a full BD exit (the custodial data is Schwab-native; only the advisor/fee
metadata stays BD-bridged). Authoritative: CTO DATA_SSOTMG_PRD.md §7 TO-3 (5b4943f92) + the reorientation
delegate 143633Z. This is the "thin advisor-metadata tether" half of the two-axis SSOT.

## Objective

Build G11-G13 (the firm-specific 49F advisor/fee surfaces) on the canonical gold, sourced from the
thin BD-bridged advisor dim — completing the canonical GOLD set (G1-G13) for 49F.

## Scope (per 08_GOLD_SCOPE.md G11-G13 + the decided source)

- **G11 `advisor_attribution`** (prod C_07) — architect/implementor model, from dim_advisor_role + dim_relationship.
- **G12 `advisor_fee_efficiency`** (prod C_08) — fee/NNA scorecard, from dim_advisor_fee + fact_billing + canonical_nna.
- **G13 `partner_analytics` / leaderboards** (prod D_01/D_00c) — from G11 + G12 + account_performance.

SOURCE RULE (Andrew-decided): the advisor/fee metadata (roles, fee splits) is a **thin BD-bridged keyed
dim** — keyed to the canonical accounts/relationships, carrying an explicit **bd-source flag** on every
BD-sourced field so the provenance is honest (Schwab-native custodial + BD-bridged advisor metadata,
clearly distinguished). NOT a full BD exit — the bridge is the deliberate thin tether (ADVI_BDAPIMIG
reframed). Materialize to canonical/schwab/gold/ (parallel/NOT-served, same model as G3-G10).

<compiler_tools_mandate>
- `comp-pipescript io build_gold_{advisor_attribution,advisor_fee_efficiency,partner_analytics}.py` before write.
- `.tools/ds-commit-gate.sh` before commit; `from __future__ import annotations` header (Rule 15).
- comp-validate or explicit NO_CONFIG; ground the bd-bridged dim against the actual BD advisor source (cite it) + flag every bd-sourced field.
</compiler_tools_mandate>

<cross_domain_coordination>
Reads canonical gold (DS-owned) + the BD advisor metadata (the thin bridge — coordinate with ADVI_BDAPIMIG / the BD-source owner on the dim_advisor_role/dim_advisor_fee source). Writes canonical/schwab/gold/ (parallel/not-served). G13 rolls G11+G12+account_performance — depends on G11/G12 landing first. NOT wired to the daily orchestrator yet (G3-G10 just got wired; G11-13 wiring is a follow-on once built + the source cadence is decided — Andrew §8 D4 advisor-tether-cadence is open). Coordinate with base-DS (owns the build_canonical_daily.py wire) on whether/when G11-13 join the daily roll.
</cross_domain_coordination>

<acceptance_criteria>
1. G11/G12/G13 built (PEP-604 header, ds-commit-gate PASS), materialized to canonical/schwab/gold/{table}/date=YYYY-MM-DD/, non-empty, real joins.
2. Every BD-sourced advisor/fee field carries the honest bd-source flag (provenance distinguishable from Schwab-native).
3. Per-table RAVC to 2.0.0_SA_COO with row counts + the sharp check (G11 architect/implementor model real; G12 fee/NNA from fact_billing + canonical_nna; G13 rolls G11+G12) + the bd-bridge source citation.
4. Session log + CC 1.0.0_SA_CTO (PRD input).
</acceptance_criteria>

## Note

PRD §8 D4 (advisor-tether cadence) is an OPEN Andrew decision — build the dim now; the daily-wire
cadence + the eventual Fidelity-data-delivery exit (D5, gated on the census) are separate Andrew calls.
This TO builds the surfaces; it does not decide the tether's long-term cadence.
