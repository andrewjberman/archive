# OPAL_RUNNERS W1 -- gold-script census + divergence matrix

**Method:** static enumeration of SOURCE across the four implementations. No sampling. Every count is a denominator.
**Read-only.** Touches no bucket, triggers nothing.

> ## THE AXIS MATTERS, AND MY FIRST PASS GOT IT WRONG
> 
> **248 .py FILES. Only 176 are GOLD SCRIPTS.** The other 72 are LIB / TOOLING / QA-GATE / OPS-ADHOC -- asking which letter group `__init__.py` belongs to is a CATEGORY ERROR, not a finding.
> 
> **v1 of this census published `101 of 248 (40.7%) map to no group contract`. The honest figure is 29 of 176 gold scripts (16.5%).** The number was inflated ~2.5x BY MY OWN CLASSIFIER, not by the estate, and it had already been routed to CTO as the act-first item when I caught it.
> 
> **ENUMERATE WHAT A NUMBER IS *OF* BEFORE YOU EXPLAIN WHY IT DIFFERS.** A rigorous instrument on the WRONG AXIS produces a confident, well-grounded, WRONG answer -- worse than no instrument, because **it survives review**.

## 1. Denominators

| implementation | scripts |
|---|---:|
| `data/black_diamond/scripts/gold` | 89 |
| `data/cot/scripts/gold` | 58 |
| `data/inf/scripts/gold` | 73 |
| `data/canonical/schwab` | 28 |
| **TOTAL** | **248** |

## 1b. What the 248 files actually ARE

| kind | files | can a group contract bind it? |
|---|---:|---|
| GOLD | 176 | **YES -- these are the census** |
| LIB | 42 | no -- shared modules |
| QA-GATE | 14 | no -- validators/gates |
| OPS-ADHOC | 10 | no -- one-shot runners |
| TOOLING | 6 | no -- GLDINC/profiling |

## 2. Letter-group map (PRD 2.2) -- GOLD SCRIPTS ONLY

`?` = does NOT map to a group contract. Per PRD 2.2 that is a **NAMED VARIANCE**, never a silent fork -- these are the scripts a contract lock would otherwise quietly leave behind.

| impl | ? | A | B | C | D | E |
|---|---|---|---|---|---|---|
| **bd** | 4 | 5 | 5 | 11 | 8 | 26 |
| **cot** | 3 | 6 | 5 | 9 | 7 | 8 |
| **inf** | 7 | 6 | 5 | 11 | 22 | 1 |
| **schwab** | 15 | 12 | 0 | 0 | 0 | 0 |
| **all** | **29** | **29** | **15** | **31** | **37** | **35** |

**UNMAPPED GOLD SCRIPTS: 29 of 176** (16.5%) -- each a NAMED VARIANCE owed to the PRD before a contract locks. **This is the real variance list.**

- `bd` **advisor_nna_attribution** (189L, FULL)
- `bd` **build_canonical_prices_v2** (706L, FULL)
- `bd` **nna_flows** (652L, MIXED)
- `bd` **schwab_flows** (235L, UNKNOWN)
- `cot` **build_canonical_prices_v2** (656L, FULL)
- `cot` **nna_flows** (548L, MIXED)
- `cot` **schwab_flows** (235L, UNKNOWN)
- `inf` **INF_09.generate_partner_analytics** (465L, INCREMENTAL)
- `inf` **INF_A_-1.materialize_txn_cache** (156L, UNKNOWN)
- `inf` **INF_build_canonical_prices** (522L, UNKNOWN)
- `inf` **INF_run_c_chain** (129L, INCREMENTAL)
- `inf` **advisor_timelock** (983L, UNKNOWN)
- `inf` **aor_resolution** (1370L, MIXED)
- `inf` **inflection_rep_scope** (814L, FULL)
- `schwab` **build_canonical_daily** (272L, INCREMENTAL)
- `schwab` **build_gold_account_gains** (228L, FULL)
- `schwab` **build_gold_account_performance** (146L, UNKNOWN)
- `schwab` **build_gold_advisor_attribution** (170L, UNKNOWN)
- `schwab` **build_gold_advisor_fee_efficiency** (191L, UNKNOWN)
- `schwab` **build_gold_advisor_split_reconciliation** (191L, UNKNOWN)
- `schwab` **build_gold_canonical_lots** (186L, UNKNOWN)
- `schwab` **build_gold_canonical_nna** (129L, UNKNOWN)
- `schwab` **build_gold_client_performance** (149L, FULL)
- `schwab` **build_gold_client_tax_liability** (207L, FULL)
- `schwab` **build_gold_firm_composition** (127L, FULL)
- `schwab` **build_gold_holdings** (108L, FULL)
- `schwab` **build_gold_partner_analytics** (220L, UNKNOWN)
- `schwab` **build_gold_portal_aggregates** (156L, UNKNOWN)
- `schwab` **build_gold_realized_gains** (191L, FULL)

## 3. Compute profile (PRD 2.3)

Andrew's diagnostic question: *is this full recompute forced by the problem, or by fundamentally bad design?* This column CANNOT answer that -- it is inferred from **source markers**, so it is a **HYPOTHESIS about behaviour, not an observation** (Rule 22). `UNKNOWN` is a first-class result: no evidence either way is not 'probably full'.

| profile | scripts | share |
|---|---:|---:|
| FULL | 101 | 57.4% |
| MIXED | 34 | 19.3% |
| INCREMENTAL | 3 | 1.7% |
| UNKNOWN | 38 | 21.6% |

## 4. Divergence matrix

Siblings = same `(group, seq)` across different implementations. **IDENTICAL here means the same FUNCTION-NAME SET, not the same bytes** -- two scripts can share every name and differ completely inside them. This is a **map of where to look**, not a proof of equivalence.

| script | implementations | fn-set | verdict |
|---|---|---|---|
| `A_00` | bd, cot, inf | 3 distinct | **DIVERGED** |
| `A_01` | bd, cot, inf | 3 distinct | **DIVERGED** |
| `A_02` | bd, cot, inf | 3 distinct | **DIVERGED** |
| `A_03` | bd, cot, inf | 3 distinct | **DIVERGED** |
| `A_04` | bd, cot, inf | 2 distinct | **DIVERGED** |
| `B_00` | bd, cot, inf | 3 distinct | **DIVERGED** |
| `B_01` | bd, bd, cot, cot, inf, inf | 5 distinct | **DIVERGED** |
| `B_02` | bd, cot, inf | 3 distinct | **DIVERGED** |
| `B_03` | bd, cot, inf | 3 distinct | **DIVERGED** |
| `C_00` | bd, inf | 2 distinct | **DIVERGED** |
| `C_01` | bd, bd, bd, cot, cot, cot, inf, inf | 6 distinct | **DIVERGED** |
| `C_02` | bd, inf | 2 distinct | **DIVERGED** |
| `C_03` | bd, cot, inf | 3 distinct | **DIVERGED** |
| `C_04` | bd, cot, inf | 2 distinct | **DIVERGED** |
| `C_05` | bd, cot, inf | 2 distinct | **DIVERGED** |
| `C_06` | bd, cot, inf | 3 distinct | **DIVERGED** |
| `C_07` | bd, cot, inf | 3 distinct | **DIVERGED** |
| `C_08` | bd, cot, inf | 2 distinct | **DIVERGED** |
| `D_00` | bd, bd, bd, bd, cot, cot, cot, inf, inf, inf, inf, inf | 11 distinct | **DIVERGED** |
| `D_01` | bd, cot | 2 distinct | **DIVERGED** |
| `D_02` | bd, cot, inf, inf, inf, inf | 6 distinct | **DIVERGED** |
| `D_03` | bd, cot, inf | 3 distinct | **DIVERGED** |
| `D_04` | bd, cot, inf, inf | 4 distinct | **DIVERGED** |
| `E_00` | bd, cot, inf | 2 distinct | **DIVERGED** |
| `E_01` | bd, cot | 1 distinct | IDENTICAL fn-set |
| `E_18` | bd, cot | 1 distinct | IDENTICAL fn-set |
| `E_20` | bd, cot | 1 distinct | IDENTICAL fn-set |
| `E_21` | bd, cot | 1 distinct | IDENTICAL fn-set |
| `E_22` | bd, cot | 1 distinct | IDENTICAL fn-set |
| `E_23` | bd, cot | 1 distinct | IDENTICAL fn-set |
| `E_24` | bd, cot | 1 distinct | IDENTICAL fn-set |

**31 sibling groups; 7 share a function-name set, 24 diverge.**

## 5. Buckets touched (firm-boundary surface)

| impl | buckets named in source |
|---|---|
| **bd** | `opal-data-bd` |
| **cot** | `opal-data-cot` |
| **inf** | `opal-data-inf` |
| **schwab** | `opal-data-bd`, `opal-data-schwab` |

_A bucket NAMED in source is not a bucket READ at runtime -- a comment, a README line, or a deny-list entry all look identical to a static scan. Cross-firm verdicts require reading the hit, not counting it._

## 6. What this census does NOT establish

| gap | why |
|---|---|
| whether a script is DEPLOYED or RUNNING | static source read; committed-but-dead and deployed-and-hot look identical here |
| whether the compute profile is TRUE | inferred from markers -- a hypothesis (Rule 22). The live check is `gold_prof` + GLDINC data |
| whether diverged siblings are SEMANTICALLY different | fn-set equality is not behavioural equality |
| runtime IO | boto3 verbs present in source != calls made on a run |
