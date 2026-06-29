# TASK ORDER — SCHWAB_SSOT.DERISK-2

<issued_to>0.4.0_DS_ClientPlatform</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<status>pending</status>
<priority>HIGH — Andrew-GO'd Schwab-SSOT migration de-risk (validate-first; feeds the migration PRD). Read-only, groundable now — prioritize over PFMG_TAXSMA S0.</priority>
<date>2026-06-29</date>

## Context

Andrew GO'd the Schwab-as-SSOT migration for 49F today ("in a big way"). Custodial data goes
Schwab-native via the canonical pipeline; a THIN BD metadata tether stays for 49F advisor info
(architect/implementor roles + fee splits) — NOT a full BD exit. CTO is authoring the migration PRD;
this census is one of two validate-first de-risk groundings the PRD will cite (CTO briefing
20260629T142313Z). Read-only — no migration commitment, just the grounding.

## Objective

Enumerate every BD account that is NOT Schwab-custody, with AUA AND last transaction-activity date, so
we can see live-vs-dormant and BOUND the residual BD bridge (if the non-Schwab AUA is mostly dormant,
the surviving BD tether shrinks toward nothing).

## Scope

Two cohorts (from BD silver/gold — groundable now, no new pull):
1. **Fully non-Schwab-custody** accounts (Fidelity + any other non-Schwab custodian) — aggregate ~$156M per the canonical doc; produce the ACCOUNT-LEVEL list.
2. **Held-away-in-Schwab** accounts — aggregate ~$109M; account-level list.

Per account: account id/key, custodian, AUA (current), and **last transaction-activity date** (the live-vs-dormant signal). Roll up to confirm the ~$156M / ~$109M aggregates (flag any material variance — a magnitude mismatch is a finding, not a silent reconcile).

<compiler_tools_mandate>
- Ground the cohorts from the actual BD silver/gold artifacts (which tables carry custodian + last-activity) — cite the source tables. `comp-pipescript io` if you touch a gold script; this should be read-only/query so likely just grounding the served artifacts.
- Verify the AUA aggregates against the served/canonical numbers, not a re-derivation that could drift.
</compiler_tools_mandate>

<cross_domain_coordination>
Read-only census from BD silver/gold — no writes, no migration action. Output is an analysis artifact (a brief + the account-level lists) that feeds CTO's migration PRD. No shared-write surface. Coordinate with CTO (PRD author) on the exact cut the PRD needs if ambiguous.
</cross_domain_coordination>

<acceptance_criteria>
1. Account-level list for BOTH cohorts (fully-non-Schwab + held-away-in-Schwab) with: account key, custodian, current AUA, last-transaction-activity date.
2. Live-vs-dormant breakdown (e.g. accounts/AUA with activity in last 30/90/365d vs dormant) — the signal that bounds the BD bridge.
3. Aggregates reconcile to ~$156M non-Schwab + ~$109M held-away (or the variance is explained/flagged).
4. Output committed as an analysis brief (account lists + the dormancy breakdown + the source-table grounding); RAVC to 2.0.0_SA_COO + CC 1.0.0_SA_CTO (PRD input).
</acceptance_criteria>

## Note

This + the Quartz-EC2 Schwab-pull validation (0.6.2) are the two parallel de-risk moves that start the
migration clock pre-PRD. Read-only; no cutover here. Your PFMG_TAXSMA S0 can resume after — this is the
higher-priority Andrew-GO'd grounding.
