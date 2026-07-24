# GC-W2b — WHAT THE SERVED COUNT ACTUALLY COUNTS

**TO:** `MDPF_3FIRMS.GC-W2b` @`e4a2724577` · **Agent:** `0.4.0_DS_ClientPlatform~A` · 2026-07-24
**archetype:** DIAGNOSE · **Read-only. No repoint, no build, no producer change, no gold run (NEVER#4).**
**Gate:** CTO 154238Z — *"No repoint is authorized until that definition exists and reproduces the served figure exactly."*

---

## 0. VERDICT — SPLIT ACROSS THE SEAM, and the split is the answer

> ### SIDE A — the FRONTIER STAMP: **`reproduces-exactly`** ✅
> A definition exists, is **source-confirmed AND measured-exact**, and reproduces **four independent
> quantities** simultaneously: the count, all five per-model cells, the total AUM **to the cent**, and the max.
>
> ### SIDE B — the SERVED-REAL IMPORT (dates ≤ `count_coverage_end`): **`NOT-DERIVABLE-FROM-RETAINED-SOURCES`** ❌
> Ten variants tested (5 filters × 2 date alignments) on 2 dates. Closest miss is **1 account**; no consistent
> rule. This is the legacy pipeline's definition, and per GC-W2a the legacy artifact is the only surviving
> record of it.

**WHY THE SPLIT IS THE USEFUL ANSWER, not a hedge:** the two sides correspond exactly to the two hole
generators from GC-W2a. The **open-ended** one (the build-gap / frontier-stamp generator, which mints new
permanent holes forever) sits on **Side A — and Side A is now solved.** The **closed** historical set sits on
Side B. **So the half that keeps producing the complaint is the half where an exact definition exists.**

> **I did NOT report `open` at −3 as the definition.** That near-miss was the forbidden shortcut named in this
> TO, and it was my own GC-W2a finding wearing this TO's hat. The real definition was three predicates away
> and reproduces exactly; the near-miss was wrong, not close.

---

## 1. THE DEFINITION (Side A) — each element with its citation

Producer: `data/mdpf/scripts/gold/dim_mdpf_account_distribution.py` @**`34e38a8e5`**, `_units_49financial()`
`:211-240`.

| element | rule | grounding |
|---|---|---|
| **Universe** | `fact_model_allocation_roster` ⋈ `fact_allocation_valuation` on `allocation_id` (inner) | `:217-221`, `:233-234` |
| **Firm** | `advisor_name == ADVISOR_49F` | `:224` |
| **Status** | `status == ROSTER_OPEN_STATUS` (`"open"`) | `:224-225`, constant at `mdpf_revamp_model_crosswalk.py:43` |
| **Models** | core only — `model_key in CORE_MODEL_KEYS`, non-core mapped to `None` and dropped | `:227-232` |
| **Model attribution** | `.drop_duplicates("allocation_id")` — **ONE model per allocation, keep-first** | `:232` |
| **Value** | `equity` summed per `(allocation_id, model_key)`; non-numeric → `0.0` | `:222`, `:235` |
| **FUNDING FLOOR** | **`equity >= $1,000`** — `DISTRIBUTION_FLOOR = 1_000.0  # >= $1K accounts count` | **`:89`** |
| **Grain** | per-**ALLOCATION**, described in source as *"the served 'account' grain"* | `:212` |
| **As-of** | `period = max(as_of).date()` over the valuation partition | `:238-240` |
| **Partition selection** | **`_latest_date(...)` — resolved SEPARATELY for roster and valuation** | `:214-215` |

**In one line:** *distinct 49F allocations, status `open`, attributed to exactly one core Opal model, whose
summed equity is at least $1,000, as of the latest retained valuation partition at producer run time.*

## 2. RECONCILIATION — Side A, EXACT on four independent quantities

Definition applied to `date=2026-07-21` partitions vs the served `account_distribution` meta
(`gold/mdpf_revamp/49financial/account_distribution.json`, ETag `865919f2be40c6c44a58fdb15dbefe23`,
LastModified **2026-07-21T19:19:27Z**, `period` = `2026-07-21`):

| model | DEFINITION | SERVED | match |
|---|---|---|---|
| opal_ultra_short_term | 169 | 169 | ✅ |
| opal_short_term | 687 | 687 | ✅ |
| opal_intermediate | 1,600 | 1,600 | ✅ |
| opal_long_term_conservative | 3,180 | 3,180 | ✅ |
| opal_long_term_aggressive | 1,390 | 1,390 | ✅ |
| **TOTAL** | **7,026** | **7,026** | ✅ |

| cross-check | definition | served | match |
|---|---|---|---|
| `total.total_aum` | 1,399,317,335.17 | 1,399,317,335.17 | ✅ **to the cent** |
| `total.max` | 33,630,390.73 | 33,630,390.73 | ✅ |
| `total.min` | 1,036.06 (smallest included) | 1,036.06 | ✅ |
| excluded by the floor | 35 | `excluded_unfunded_count` semantics `:354` | ✅ consistent |

**THE FLOOR IS BRACKETED, not assumed.** The 7,026th-largest equity is **1,036.0639**; the next is
**999.1700**. So the threshold lies in **(999.17, 1036.06]** — and `$1,000` sits cleanly inside that interval
*and* is the source constant at `:89`. **Measurement and source agree independently.**
**This is a CORRECTNESS-grade test:** it had four ways to fail (count, per-model, AUM-to-the-cent, max) and
failed none. And it reproduces the served figure **exactly**, which is the bar CTO set.

## 3. RECONCILIATION — Side B, and why it is a real negative

Served-real-import dates (`≤ count_coverage_end` = 2026-07-18) carry `measured` class and come from a
**different source**: the self-referential legacy import (`dim_mdpf_aggregate_aua_timeseries.py:557-591
@3efc9dc6d`), *not* from `account_distribution`.

| target | SERVED core | open≥$1K | open>0 | open all | +workingClose | any-status>0 |
|---|---|---|---|---|---|---|
| 2026-07-16 (src 07-16) | **7,041** | 7,003 | 7,036 | 7,038 | 7,040 | 7,040 |
| 2026-07-16 (src 07-15) | **7,041** | 7,001 | 7,035 | 7,037 | 7,037 | 7,037 |
| 2026-07-17 (src 07-17) | **7,055** | 7,006 | 7,040 | 7,042 | 7,045 | 7,045 |
| 2026-07-17 (src 07-16) | **7,055** | 7,003 | 7,036 | 7,038 | 7,040 | 7,040 |

**No variant reproduces either date.** Closest is **off by 1** (07-16), and the same rule is **off by 10** on
07-17 — so even the near-miss is not a consistent rule. **A rule that is off by one on one date and by ten on
the next is not a definition with a residual; it is a different quantity.**

> **VERDICT for Side B: `NOT-DERIVABLE-FROM-RETAINED-SOURCES`.** Stated plainly rather than reporting the
> off-by-one as a success — that is precisely the failure this TO forbade.

## 4. AC-4 — THE PER-MODEL vs DISTINCT RELATIONSHIP, as part of the definition

**For 49F the two are EQUAL BY CONSTRUCTION**, and the construction is the citation:
`:232` `.drop_duplicates("allocation_id")` collapses each allocation to exactly ONE core model *before* the
count. Measured @2026-07-21: per-model sum **7,026** = distinct funded `allocation_id` **7,026**; allocations
holding >1 core model: **0**; max models per allocation: **1**.

**So W-1's 442-vs-294 divergence is NOT the same relationship — it is a DIFFERENT CODE PATH.** The cottonwood
fold enters through the sidecar (`cot_by_model`, `:344-347`, `:362-364`), which concatenates per-model value
lists **without** passing through `drop_duplicates`. **The divergence is a property of the cottonwood sidecar
path, not of the count definition.** Two paths, two relationships — an important distinction for W-2, because
a composition law written against "the per-model relationship" will be wrong on one of them.

**Also note the attribution rule is UNEXERCISED on 49F today** (0 multi-model allocations). `drop_duplicates`
keep-first is *arbitrary-order* — if a 49F allocation ever holds two core models, which model it lands in is
undefined. Flagging as a latent, currently-dormant behaviour; not a live defect.

## 4A. SUM vs DISTINCT — RESOLVED. The field is the SUM, and the divergence is real, not coincidental

Routed in by COO 161106Z: CTO and `0.6.2~B` both measured `account_count_total == sum(per-model cells)` on the
INF artifact (423/423 and 40/40 respectively) and drew **opposite** conclusions — ~B: *"INF has no multi-model
accounts, so distinct == sum COINCIDENTALLY"*; CTO: *"the field has always carried the SUM — universal."*

**CORRECTION OF A PREMISE FIRST (VERIFICATION LAW 3 — ask for the artifact, not the number).** The routing
message attributes *"294 distinct vs 442 per-model"* to my W-1. **`294` does not occur anywhere in my W-1
deliverable** (checked: zero occurrences; W-1 reports cottonwood's 442 and never a distinct figure). The real
number is **`total.active_accounts_count` = 294** in cottonwood's `account_distribution` — which is **not a
distinct count either**; the distinct funded count there is **291**. Flagging rather than reasoning from it,
because a number attributed to a measurement that never made it will otherwise return as corroboration.

**THE DISCRIMINATOR, MEASURED.** Both readings are testable, and they separate cleanly:

| evidence | result | grade |
|---|---|---|
| Global `account_count_total` vs `sum(by_model cells)` | **equal on 407 of 407 non-null dates, 0 mismatches** | MEASURED |
| the composition itself | `total = sum(c for k in by_model ...)` — **the field IS the sum by construction** | **SOURCE-CONFIRMED** `dim_mdpf_aggregate_aua_timeseries.py:1732-1734 @3efc9dc6d` |
| the frontier stamp's source | `meta.account_count_by_model_key` (the per-model SUM basis, 8,009), **not** `total.account_count` (the distinct basis, 7,862) | MEASURED + `:1657-1658`, `:604` |

**Where distinct and sum actually diverge, by firm** (`account_distribution`, `total.account_count` vs
`sum(by_model.account_count)`):

| firm | distinct | sum(by_model) | divergence |
|---|---|---|---|
| 49financial | 7,026 | 7,026 | **0** — by construction, `drop_duplicates("allocation_id")` at `:232` |
| inflection | 534 | 534 | **0** — confirms ~B's INF observation |
| **cottonwood** | **291** | **438** | **+147** |
| global | 7,862 | 8,009 | **+147** — *the entire Global divergence is cottonwood's* |

> **VERDICT: CTO is right about the FIELD; ~B is right about INF, but INF cannot support the inference drawn
> from it.** The field is **definitionally the SUM** — source-confirmed, and measured 407/407. INF's
> `distinct == sum` is a property of INF's *data* (no multi-model accounts), not evidence about the field's
> definition; that is why INF alone could never discriminate, exactly as COO said. Cottonwood is the
> discriminator and it says **SUM**.
>
> **AND THE CONSEQUENCE CTO ANTICIPATED IS REAL: the +147 is not an anomaly — it is the field working as
> designed.** A per-model count summed across models is **model MEMBERSHIPS**, not distinct accounts. So on
> current data the Global "Count" **exceeds the distinct funded account count by 147 (~1.8% of 8,009)**, and
> that gap grows with every multi-model account onboarded.
>
> **Both quantities are legitimate; only one is labelled.** Whether "Count" on this chart should mean
> memberships or accounts is a **product question at CTO's gate (W-2)** — I am not ruling it. What I can say
> is that it is pre-existing, applies to every date equally, and is **not** introduced by any landing.

**Bearing on this TO's Side A definition (§1):** none — my definition reproduces the served figure exactly
*because* it is built on the same per-model sum basis. The sum/distinct question is about what the number
MEANS, not about whether I have reproduced it.

## 5. THE AS-OF SEMANTICS — a finding that compounds GC-W2a's build-gap generator

`:214-215` resolves the roster and valuation partitions with **`_latest_date()` — independently, each to
whatever is newest at producer run time.** There is no requested date. Consequences, all measured:

1. **The stamped value's as-of is "whenever `account_distribution` last ran" — NOT the axis date it lands on.**
   `account_distribution` has **2 object versions** (2026-07-20T21:33:01Z, 2026-07-21T19:19:27Z) and has **not
   been rebuilt since 2026-07-21**. The 49F served artifact was rebuilt **2026-07-23T21:47:06Z** and stamped
   the frontier onto the **2026-07-22** axis position. **So 07-21 data is carried on the 07-22 position.**
2. **This is NOT a designed T-1 offset** — I tested that reading and it does not hold. `DEFN(2026-07-22)` =
   **7,038**, but the served 07-22 cell is **7,026** = `DEFN(2026-07-21)`. Had `account_distribution` run on
   07-22, the stamp would have been 7,038. **The offset is whatever the gap between two independent clocks
   happens to be — it was 1 day here, and nothing bounds it.**
3. **Roster date and valuation date are resolved separately** (`:214` vs `:215`), so they can diverge — the
   "foreign-day roster" class that `_assert_cross_axis_coherence` clause (vi) exists to catch.

> **Why this matters beyond this TO:** GC-W2a found that build gaps leave axis dates permanently un-stamped.
> This adds that the values which *do* get stamped carry an **unbounded, undeclared as-of skew**. The count
> series therefore has two independent defects on the same mechanism: **dates that get nothing, and dates that
> get something whose vintage is not the date's.**

## 6. WHAT THIS UNBLOCKS (input to CTO's gate — not a decision)

CTO gated the decouple on a definition reproducing the served figure exactly. **For the forward-looking half,
it now does**, and it is derivable from **retained silver** (`fact_model_allocation_roster` ⋈
`fact_allocation_valuation`, both accumulating daily from 2026-07-14). Restated as scoping input only:

- **Mechanism (2) — the open-ended generator — is FIXABLE.** A count sourced per-date from these two feeds
  under §1 reproduces the frontier figure exactly, so it would not be an approximation.
- **The historical 20 remain NOT-DERIVABLE.** Side B is a different quantity and nothing we retain reproduces it.
- **The as-of skew (§5) is a separate defect from the missing dates** and would not be fixed by filling holes.
- **Retention caveat carried forward from GC-W2a:** both feeds start 2026-07-14 and I have **not** read a
  lifecycle policy on either prefix.

## 7. GROUNDING LEDGER

| claim | grade | grounding |
|---|---|---|
| the full inclusion predicate | **SOURCE-CONFIRMED** | `dim_mdpf_account_distribution.py:211-240 @34e38a8e5` |
| `$1,000` funding floor | **SOURCE-CONFIRMED + MEASURED** | `:89` **and** independently bracketed to (999.17, 1036.06] from the data |
| Side A reproduces exactly | **MEASURED, 4 independent quantities** | count, 5/5 per-model, AUM to the cent, max — vs served `account_distribution` ETag `865919f2…` |
| Side B not derivable | **MEASURED** | 5 filters × 2 alignments × 2 dates = 10 variants, none exact, no consistent residual |
| per-model == distinct for 49F | **SOURCE-CONFIRMED + MEASURED** | `:232` drop_duplicates; 0 multi-model allocations measured |
| cottonwood divergence is a different path | **SOURCE-CONFIRMED** | `:344-347`, `:362-364` — sidecar bypasses the dedup |
| as-of is producer-run-time, not axis date | **SOURCE-CONFIRMED + MEASURED** | `:214-215` `_latest_date()`; 2 object versions; `DEFN(07-22)`=7,038 ≠ served 7,026 = `DEFN(07-21)` |
| the T-1-by-design reading | **TESTED AND REJECTED** | would require served(07-22)=`DEFN(07-22)`=7,038; it is 7,026 |
| the field is the SUM, not a distinct count | **SOURCE-CONFIRMED + MEASURED** | `:1732-1734 @3efc9dc6d`; 407/407 non-null dates, 0 mismatches |
| divergence is cottonwood-only, +147 | **MEASURED** | four `account_distribution` artifacts; 49F 0, INF 0, cot +147, global +147 |
| `294` is not a W-1 figure | **MEASURED** | zero occurrences in my W-1 deliverable; 294 = cottonwood `total.active_accounts_count`, distinct funded there is 291 |
| whether SUM is the RIGHT convention | **NOT RULED — product question** | W-2 / CTO gate. I quantified the gap; I did not decide the label. |
| *what the legacy producer counted* | **UNDETERMINED** | Side B's source is the legacy chain; GC-W2a established the legacy artifact is its only surviving record. I did not identify a legacy script that still runs. |

**Explicit-Z throughout** (`s3api`/`list-object-versions` only; never `aws s3 ls`). Denominators printed.
Read-only affirmed: no producer edit, no repoint, no gold run.
