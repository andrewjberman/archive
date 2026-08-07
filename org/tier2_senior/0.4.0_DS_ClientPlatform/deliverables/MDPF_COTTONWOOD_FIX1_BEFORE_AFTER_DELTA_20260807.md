# MDPF_COTTONWOOD.FIX1 — before/after delta, and the upstream blocker the delta exposed

**Author:** `0.4.0_DS_ClientPlatform` · **TO:** `MDPF_COTTONWOOD.FIX1` @03b975ac13 (amended @505747e886)
**Date:** 2026-08-07 · **Measurement vintage:** assignment_date `2026-08-07`, value_date `2026-08-05`
**Diagnosis inherited, not re-derived:** AE~Z @924c3b669 (on `origin/SITEZ`), re-derived at the COO seat.

---

## THE HEADLINE, AND IT IS NOT THE ONE THE TO PREDICTED

**The gold fix is landed, correct, and tested. Its measured delta on today's data is `$0.00`.**

That is not a fix that did nothing. It is a fix whose data never arrives, because **there is a
SECOND filter of the same shape one layer upstream, at the BRONZE HARVEST, and it is the binding
one.** The gold producer cannot attribute a blend edge that was never fetched from the vendor.

> **Acceptance criterion 4 — "Opal Fixed Income must APPEAR in the gold dim" — IS NOT MET, and
> cannot be met by this TO alone.** Stated plainly rather than absorbed into a successful-fix
> narrative. The gold half is necessary; it is not sufficient.

---

## 1. THE BEFORE/AFTER DELTA (criterion 3)

Produced by running the **same** `build()` twice against the **same live silver**, with
`attributes` mutated back to the parent-only rule for BEFORE — so the two sides differ in exactly
one thing. Harness: `delta.py` (scratch, reproducible).

**HARNESS CONTROL, run first and allowed to fail loudly:** the BEFORE output must reproduce the
**live served artifact** (`s3://opal-data-assets/blackdiamond/cottonwood/gold/dim_model_portfolio/date=2026-08-07/data.parquet`).
→ 10 rows vs 10 rows, identical `model_id` set, identical counts, dollars equal within $0.005.
**VERDICT: FAITHFUL.** Without this control the delta below would be an unanchored claim.

| measure | BEFORE | AFTER | delta |
|---|---:|---:|---:|
| **Opal AUA** (`is_opal=True` dollars) | $134,113,436.27 | $134,113,436.27 | **$0.00** |
| non-Opal sleeves (carried for visibility) | $779,478.54 | $779,478.54 | $0.00 |
| dim rows | 10 | 10 | 0 |
| `opal_assigned_accounts` (PRD sec-5 tie) | 306 | 306 | 0 |
| `assigned_unresolved_to_roster` (third state) | 0 | 0 | 0 |
| **parent strategies newly reached** | — | **0** | — |
| **accounts newly attributing** | — | **0** | — |
| reconcile gate | PASS | PASS | — |
| rows that LOST count or dollars | — | **0** | — |

**Per-model: every one of the 10 rows is byte-identical across the change.** No row appeared, none
disappeared, none moved.

### The two measured cases from the TO, answered honestly

| AE~Z's sharpest test | result |
|---|---|
| `Opal Fixed Income` must APPEAR | ❌ **STILL ABSENT** — blocked upstream (§2), not by the gold rule |
| Conservative Growth 96 + 2 = 98 | ❌ **still 96** — same cause |

### The pre-registered negative controls HELD

I pre-registered before running anything that the `−1/−1/−1` residuals AE~Z flagged as unexplained
must **stay** unexplained, and that Intermediate-Term / Short-Term / Long-Term Aggressive must be
**unchanged**. Both held: all three residuals are untouched and all three strategies are unchanged.
Nothing moved that I did not intend to move — which is the only reason a `$0.00` result is
readable as *"the fix is inert today"* rather than *"the fix is broken."*

---

## 2. THE UPSTREAM BLOCKER — source-confirmed, with a positive control

**`infra/aws/lambda/cot-pipeline/cot-rebalancer-runner/lambda_function.py:303`** @HEAD:

```python
queue = [mid for mid, m in by_id.items() if _is_opal(m.get("name"))]   # <- SEED
...
if MODEL_DETAIL_SCOPE != "all":
    for cid in _child_model_ids(json.loads(raw)):
        queue.append(cid)                    # transitive closure -- but only DOWNWARD from a seed
```

`MODEL_DETAIL_SCOPE` defaults to `"opal_closure"` (`:70`). The closure walks children correctly —
but it is **seeded on Opal-NAMED roster models only.** A non-Opal-named parent is never a seed, so
its detail is never fetched, so its Opal children never land in bronze, never become silver blend
edges, and are structurally invisible to gold. **It is the identical defect to the gold one, one
layer up, and it binds first.**

### Measured, 2026-08-07

| observation | value |
|---|---|
| roster models (silver `fact_model_roster`) | **62** |
| bronze `rebalancer_model_detail/2026-08-07/` objects | **28** |
| silver `fact_model_blend` edges | 33 |
| **distinct blend parents that are NOT Opal-named** | **0** |
| `Anna *9237` / `*9238` in roster + assignment | **present** (2 live accounts) |
| `1ae61190-…` / `6ae9e540-…` (the Anna ids) in bronze | **ABSENT** |
| any blend child named `*fixed income*` | **0 rows** |

**Positive control on the ABSENT verdict:** the same grep for `bef02495-…` (Opal Satellite 70, a
known-blended Opal parent) returns **1**. The search discriminates, so ABSENT is a measurement and
not a broken retrieval.

⚠ `:31` records the scope as **"Andrew-ruled, CTO-ratified."** Changing it is a routing decision,
not a unilateral edit — and the file is a **Lambda (infra), which is not the DS lane** (Rule 13).
**Owner: not me. Routed to COO, surfaced not adjudicated.** A supported switch already exists
(`MODEL_DETAIL_SCOPE=all`), so the remedy is cheap; the *ruling* is the gate, not the code.

---

## 3. WHAT LANDED IN GOLD

`data/assets/scripts/gold/build_dim_model_portfolio.py` — the Opal test moves from the assigned
PARENT to a **disjunction evaluated at leaf grain** (`attributes()`):

> a leaf attributes if **EITHER** the assigned strategy is Opal-named (pre-existing rule, unchanged)
> **OR** the leaf itself is an Opal model (Andrew-direct 2026-08-07).

**Why a disjunction and not either single-sided form** — both move the same client-facing number, in
opposite directions, and neither would be questioned:

| form | effect | measured cost |
|---|---|---|
| delete the filter | attributes genuinely non-Opal exposure | **OVERSTATES** — the named forbidden shortcut |
| move the test to leaf-only | drops non-Opal sleeves of Opal-named parents | **UNDERSTATES by $779,478.54** across 3 live rows |
| **disjunction (landed)** | strictly additive | **no row loses count or dollars** |

The leaf-only form was the TO's original criterion 1; COO amended it @505747e886 after I measured
the three sleeve rows it would have deleted. No renormalization: a non-Opal remainder (the real
case is `Anna *9237`'s DIVZ SMA at 7%) stays **out** rather than being spread across the Opal
leaves, and remains in `non_model`, which is a downstream balance.

**Report additions** so the delta is readable off the run report itself, not only off this document:
`nonopal_parent_accounts_attributing`, `nonopal_parent_strategies_reached`,
`attributing_accounts_total`, `attributing_accounts_without_value`, `dim_dollar_total_opal`,
`dim_dollar_total_non_opal`. `opal_assigned_accounts` and `opal_assigned_without_value` **keep their
original definitions** — the PRD sec-5 gate ties the former to the vendor roster's own accountCount
sum, and widening it would let the new rows silently satisfy an old gate while it still read PASS.

---

## 4. TESTS — and the mutation matrix, because a passing suite is not evidence

`data/assets/scripts/gold/tests/test_dim_model_portfolio.py`: **26 pass** (16 pre-existing + 10 new).

A green suite only proves the tests pass. Each wrong form was **run as a mutant** to prove the suite
could fail:

| mutant | what it is | caught by |
|---|---|---|
| control (real rule) | — | **0 failures** ✅ |
| `parent-only` | the ORIGINAL DEFECT | **6 tests** |
| `always-true` | filter deleted → overstates | **8 tests** |
| `leaf-only` | test moved not disjoined → understates | **3 tests** |

⚠ **`TRAP_3` (strictly-additive) initially MISSED the leaf-only mutant** — its fixture had no
non-Opal sleeve, so it was asserting additivity over a book with nothing to lose. Adding the sleeve
to the fixture is what makes it catch that mutant; the fixture comment records this so the sleeve is
not later removed as decoration.

Also exercised: the PRD sec-5 reconcile tie still **breaks under mutation** of the roster's own
`account_count` — proving this change did not quietly turn the gate into a tautology that passes on
anything.

---

## 5. THE 09:00 ET FIRE — what Andrew will see

**Nothing changes on his screen.** The measured delta is `$0.00` across every row, so the next
scheduled emission produces the same numbers whether or not this fix is deployed. That is stated
explicitly per the TO's cross-domain requirement: a corrected number must not arrive unannounced —
and here, no number moves at all.

**When the upstream scope is widened, it will move**, and this document is the pinned baseline to
measure that move against: **Opal AUA $134,113,436.27 as of assignment 2026-08-07 / value 2026-08-05.**

---

## 6. RESIDUAL / NOT CLAIMED

- **The `−1/−1/−1` residuals AE~Z flagged remain unexplained.** I did not investigate them and do
  not claim to have; they need the account-level join AE~Z named as their task 1.
- **I did not re-run AE~Z's live BD Rebalancer scan** and do not inherit its figures as my own
  measurement. Their scan hit the vendor API directly (62/62 details); the silver plane I measured
  carries 33 edges from 28 harvested details. **Those are different planes, and the gap between
  them IS the finding in §2** — not a disagreement between instruments.
- **The 49F side is untested for the same defect.** Flagged once to COO, who owns it; the code path
  is shared, so if the harvest seeds the same way there, a different firm's numbers carry the same
  understatement. Not my scope, not chased.
- **Deploy:** gold producer only. The platinum publisher and serving projection were not touched.
