# OPAL_RUNNERS W1 — the 29 unmapped gold scripts, dispositioned

**TO:** OPAL_RUNNERS W1 (variance list) · **Author:** `0.4.0_DS_ClientPlatform` · 2026-07-14 ~03:30Z
**Source of the 29:** the CORRECTED census (`3bf78a328`) — 29 of 176 gold scripts (16.5%), *not* the
retracted 101/248. **READ-ONLY.** Every disposition is a PROPOSAL; the lock gate is per-script IO.

> **Disposition classes** (PRD 2.2): **CONTRACT-MAPPED** (maps to A/B/C/D/E by function) · **NAMED
> VARIANCE** (a real fork the PRD must name — sovereign-ruled logic, or a partner-specific model) ·
> **NAMED RETIREMENT** (reclassifies out of the daily chain).
>
> ### The one caveat that governs every row below
> **A group assignment from a script's NAME is a CLAIM, not a fact** — the whole lesson of this night's
> W1 (I counted files as scripts) and W4 (a reader that could not see FAM's format). So each CONTRACT-
> MAPPED row is marked **[IO-verified]** (I read what it actually reads/writes) or **[name-proposal]**
> (mapping inferred from the name, pending `comp-pipescript io`). **No contract locks on a [name-proposal].**

---

## A. The 14 schwab `build_gold_*` — CONTRACT-MAPPED (the "G-series by another name")

These are not unmapped in substance — they are `canonical/schwab`'s gold layer, named `build_gold_*`
instead of `G1..G14`. The PRD's `G` label was the claim; the filenames are the fact (CTO folded this into
the census already). Proposed group by function; the four I read are IO-verified, the rest are
name-proposals pending IO.

| script | → group | basis |
|---|:---:|---|
| `build_gold_holdings` | **B** | **[IO-verified]** reads `silver/fact_position` + `dim_account` → `gold/canonical_holdings` (event/holdings) |
| `build_gold_canonical_lots` | **B** | [name-proposal] lots = event layer |
| `build_gold_realized_gains` | **B** | [name-proposal] realized-lot event |
| `build_gold_account_gains` | **B** | [name-proposal] |
| `build_gold_canonical_nna` | **C** | [name-proposal] NNA = derived metric |
| `build_gold_account_performance` | **C** | [name-proposal] |
| `build_gold_client_performance` | **C** | **[IO-verified]** reads `gold/*_performance` + `dim_relationship` (derived) |
| `build_gold_client_tax_liability` | **C** | [name-proposal] |
| `build_gold_firm_composition` | **C** | [name-proposal] |
| `build_gold_advisor_attribution` | **A** | **[IO-verified]** reads `silver/dim_advisor_role` + `dim_relationship` → `gold/advisor_attribution` |
| `build_gold_advisor_fee_efficiency` | **A/C** | [name-proposal] — **the 49F split-fee-adjacent one; verify before mapping** |
| `build_gold_advisor_split_reconciliation` | **A** | [name-proposal] — **49F split-fee; likely a NAMED VARIANCE, not a clean A** |
| `build_gold_partner_analytics` | **D** | [name-proposal] presentation aggregate |
| `build_gold_portal_aggregates` | **D** | **[IO-verified]** reads `gold/*` → portal aggregates (presentation) |

> **W4 cross-connection, surfaced not adjudicated:** `build_gold_advisor_attribution` reads
> `silver/dim_advisor_role`. **The canonical/schwab silver ALREADY carries an advisor-role dimension.**
> That is directly relevant to W4's open Group-A question — the 49F role model may already exist here as a
> silver dim, sourced from something. Whether it is sourced from the FAM/SLM identity I found, or
> elsewhere, is the thread to pull, and it is CTO's / Andrew's, not mine.

## B. The 10 inf named-variances — NAMED VARIANCE (mostly sovereign)

These do not map to a clean group contract because they ARE the variances the PRD names explicitly. The
AoR/timelock pair carry **sovereign rulings preserved verbatim** (memory: NNA time-lock by account-to-
advisor) and MUST NOT be "mapped away."

| script | class | why |
|---|---|---|
| `aor_resolution` (1,370L) | **NAMED VARIANCE — SOVEREIGN** | the AoR resolver; sovereign time-lock rulings verbatim. Untouchable. |
| `advisor_timelock` (983L) | **NAMED VARIANCE — SOVEREIGN** | account→advisor time-lock; immutable-once-written rule. Untouchable. |
| `inflection_rep_scope` (814L) | **NAMED VARIANCE** | inf rep-scope filter (the cross-firm scoping fix) |
| `advisor_nna_attribution` (bd) | **A (named variance)** | attribution logic; verify IO |
| `nna_flows` (bd, cot) | **C (named variance)** | NNA flow derivation; forked bd/cot |
| `INF_09.generate_partner_analytics` | **D** | [name-proposal] partner presentation |
| `INF_run_c_chain` | **ORCHESTRATION** | a chain runner, not a table builder — arguably OPS, not gold |
| `INF_A_-1.materialize_txn_cache` | **B (named variance)** | a `-1` pre-stage txn cache; genuinely pre-A |
| `INF_build_canonical_prices` | see §C | shared-logic (prices) |
| *(nna_flows cot counted in §C shared)* | | |

## C. The 5 cross-impl shared-logic — SHARED-LOGIC CANDIDATES

The same logical script forked across implementations. These are the clearest **consolidation** targets —
one canonical implementation, not four — but consolidation is a decision, not a mapping.

| script | impls | note |
|---|---|---|
| `build_canonical_prices_v2` | bd, cot | forked price-canonicalizer; near-identical name, divergence unmeasured |
| `INF_build_canonical_prices` | inf | the inf sibling of the same function |
| `build_canonical_daily` (schwab) | schwab | the schwab price/daily builder |
| `schwab_flows` | bd, cot | Schwab-sourced flow logic, forked bd/cot |
| `nna_flows` | bd, cot | (also in §B) NNA flows forked |

**These are where the divergence matrix earns its keep** — before consolidating, diff the siblings (my
census showed every `A_*`/`B_*` sibling DIVERGES, so "they're the same script" is exactly the assumption
that must be checked, not assumed).

---

## Summary

| class | count | of 29 |
|---|---:|---|
| CONTRACT-MAPPED (schwab `build_gold_*`) | 14 | 48% |
| NAMED VARIANCE (incl. 2 sovereign) | ~10 | 34% |
| SHARED-LOGIC / consolidation candidate | ~5 | 17% |

**So the true act-first item is not "40.7% of the estate is unmapped chaos."** It is: **14 scripts just
need their group assignment confirmed by IO (a mechanical pass), ~2 are sovereign and untouchable, a
handful of 49F split-fee scripts are genuine named variances, and ~5 are consolidation candidates.** That
is a tractable list, and it was a manufactured crisis at 40.7%.

## The lock gate (PRD 2.1) — what must happen before any contract locks

- **Run `comp-pipescript io` on every [name-proposal]** — turn each into [IO-verified] or a variance.
  Naming is a claim; IO is the fact. I verified 4; 10 remain.
- **Diff the §C shared-logic siblings** before consolidating — the divergence matrix says do not assume.
- **The 2 sovereign scripts are recorded, not mapped** — the ruling is the contract.
