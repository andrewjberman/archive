# TASK ORDER — DATA_ANALYTICS.GOLD-CORE

<issued_to>0.4.0_DS_ClientPlatform</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<status>complete</status>
<!-- COMPLETE 2026-06-29: G3-G10 all built+committed+materialized+independently-verified at
canonical/schwab/gold/{table}/date=2026-06-24/ (AES256, parallel/not-served). Commits
a3d295652/17483c572/39ea0e927/8080d6cbc/0e80042f8/97ee6b48f/891685f8f/0d8c72dd7. Batch 1/3
(G3-6) + 2/3 (G7-8) COO-ACCEPTED; 3/3 (G9-10) RAVC'd. G11-G13 HELD for Andrew (not built).
Cross-stack tie-out: composition=06-24 EMV=06-24 AUA=$1,591,227,965; 06-18 AUA=$1.631B served-AUA. -->

<date>2026-06-29</date>
<priority>HIGH — Andrew sovereign-parked Monday-first task</priority>

## Objective

Build the **canonical GOLD analytics CORE (G3–G10)** on the now-complete 17-fact + 5-dim silver
(commit a1a32f44c, S3-verified 17 fact_ + 5 dim_ prefixes). Scope is exactly the AGNOSTIC-CORE set
in `data/canonical/schwab/docs/08_GOLD_SCOPE.md` (486c0253b), pre-accepted by COO + pre-GO'd Friday.

G1 (`canonical_holdings`) and G2 (`account_gains`) already EXIST — this TO is **G3 → G10**.
**G11–G13 (advisor/partner firm-specific) are HELD for Andrew — do NOT build them under this TO.**

## Scope (build order per 08_GOLD_SCOPE §4)

Core first, then differentiators, then composition/aggregates:

| # | gold table | canonical source | note |
|---|---|---|---|
| G3 | `canonical_lots` | fact_lot_unrealized + fact_lot_realized (+ fact_lot_unrealized_tax) | per-lot tax basis, Schwab-native (NO FIFO reconstruction) |
| G4 | `account_performance` | account_gains + dim_account | account-grain AUA/return timeseries (roll account_gains over windows) |
| G5 | `client_performance` | account_performance + dim_relationship | relationship-grain rollup (served AUA/NNA timeseries) |
| G6 | `canonical_nna` | account_gains (nna_cash/nna_in_kind) + dim_account | per-account NNA surface |
| G7 | `client_tax_liability` | fact_lot_unrealized_tax + **fact_tax_1099div** + dim_account | DO-BETTER: ACTUAL 1099-DIV + real unrealized lot basis vs production ESTIMATE |
| G8 | `realized_gains` | fact_lot_realized + fact_realized_{rly,rlw,rlu,rty,rtu} | DO-BETTER: 6 realized-lot facts vs production single path |
| G9 | `firm_composition` | fact_position + dim_asset(asset_class) + dim_relationship | asset-class composition; dim_asset derives class (no DDB/regex classifier) |
| G10 | `portal_aggregates` | G5 + G6 + G7 + G9 rolled to firm | served firm aggregates (header_metrics, clients_tab, AUA snapshots) |

## Output

`s3://opal-data-bd/canonical/schwab/gold/{table}/date=YYYY-MM-DD/data.parquet` — **parallel / NOT served**
(same build+upload model as silver). Each `build_gold_{table}.py` begins with
`from __future__ import annotations` (Rule 15).

## Constraints (NEVER)

- **NOT served.** This is a parallel canonical layer. Do NOT wire any of these into the served bd gold
  or any portal consumer — that is a separate, never-widen-gated step (CTO+COO sign-off).
- **Firm-separation.** This tree is canonical/schwab (Schwab-is-source). Do NOT reference or mirror
  any cot bucket/tree (CLAUDE.md NEVER #1, IAM-enforced).
- **Snapshot-native is intentional.** Canonical gold starts at first Schwab RPS delivery, NOT 49F
  inception. Do not attempt pre-Schwab backfill (that stays in the BD pipeline; it's an Andrew-flagged
  deliberate scope boundary, not a gap to close).

<compiler_tools_mandate>
- BEFORE write (each gold script): `comp-pipescript io build_gold_{table}.py` — column gaps + any consumers.
- BEFORE commit: `.tools/ds-commit-gate.sh` (py_compile + ds-precommit-check + ruff py39) on every .py.
- BEFORE run: `comp-pipescript deployed build_gold_{table}.py` (MATCH/STALE) + `comp-pipescript postdeps` for any ad-hoc run.
- AFTER materialize, BEFORE RAVC to COO: `comp-validate build_gold_{table}.py --artifact <s3-or-local>` if a validate config exists; if NO_CONFIG, say so explicitly (do not signal SAFE on an unvalidated table).
</compiler_tools_mandate>

<cross_domain_coordination>
None on the WRITE surface — canonical/schwab/gold/ is DS-owned, parallel, not-served; G3–G10 build scripts are new files under data/canonical/schwab/scripts/gold/. READ inputs are the read-only silver facts/dims (commit a1a32f44c). G10 (`portal_aggregates`) shares a NAME with served portal surfaces but is the canonical-tree analog and is NOT wired to portal — keep it in canonical/schwab/gold/ only. No other active TO writes this tree.
</cross_domain_coordination>

<acceptance_criteria>
1. Each of G3–G10 has a `build_gold_{table}.py` (PEP-604 future-import header) that runs clean through ds-commit-gate.
2. Each table materialized to `s3://opal-data-bd/canonical/schwab/gold/{table}/date=YYYY-MM-DD/data.parquet`, **non-empty** (row count > 0), with the canonical source facts/dims actually joined (not a stub).
3. Per-table RAVC to 2.0.0_SA_COO including: row count, the sharp structural check (G7 must show ACTUAL 1099-DIV tax distinct from an estimate; G8 must reflect the 6 realized-lot facts, not 1; G3 must be per-lot Schwab-native with no FIFO reconstruction), and the comp-validate verdict (or explicit NO_CONFIG).
4. Session log with the `## Compiler Tools` table.
RAVC may be per-table or batched as G3-G6 / G7-G8 / G9-G10 sets — your call, but each table independently verified.
</acceptance_criteria>

## Notes

- You are pre-authorized to START immediately — the core was GO'd Friday; this TO is the formal dispatch.
- HELD for Andrew (separate GO will follow): G11–G13 (advisor/partner) + the 2 boundary gaps
  (history-start; Schwab-only-$1.63B-vs-firm-union). Do not block core G3–G10 on them.
- Authority: Andrew sovereign-parked Monday-first (COO 06-26 session-close); MSTR spawn RAVC 20260629T125130Z.
