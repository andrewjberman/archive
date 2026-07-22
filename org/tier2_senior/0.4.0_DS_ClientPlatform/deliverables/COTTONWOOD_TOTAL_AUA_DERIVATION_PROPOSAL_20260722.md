# COTTONWOOD TOTAL-AUA DERIVATION — PROPOSAL (Andrew-direct ~1735Z)

**Author:** `0.4.0_DS_ClientPlatform` · 2026-07-22 ~1745Z
**Status:** **PROPOSAL ONLY — READ-ONLY.** Nothing built, no producer run, no artifact written, no ETag moved.
**Scope:** Andrew named me pursuer ~1735Z. This touches **"the Cottonwood fold"**, which CTO's 151655Z hold
names HELD. Andrew is later + sovereign, so I read this as a carve-out **for the proposal**; the scope
question is surfaced to CTO (173721Z) and **I will not build or land without his ruling.**

**Andrew-direct, verbatim:** *"Cottonwood total value needs to be derived from their total AUA which is a
function of their Black Diamond data in opal-data-assets. I would look at how the process is being done for
schwab 0824 as the base from which smartx (49 models) are balanced and propose a solution in similar shape
for Cottonwood and its black diamond data in opal-data-assets."*

---

## 1. THE 0824 SHAPE — verified at source, not recalled

`data/mdpf/scripts/gold/dim_mdpf_aggregate_aua_timeseries.py` @HEAD:

| leg | line | mechanism |
|---|---|---|
| custody base | `:323-327` | `Σ fact_rps_s2.net_mv_plus_cash` — docstring: *"full-envelope: positions + full cash leg"* |
| model | `:597-600` | `Σ fact_model_aum_daily.closing_equity` over `CORE_MODEL_KEYS` |
| **residual** | `:611-614` | **`non_model[i] = custody[i] - model[i]`**; `custody is None -> None`, **no interpolation** |
| headline | `:621` | `firm_headline = custody` — *model + non_model == custody at the array end* |

> **THE INVARIANT TO MIRROR: THE CUSTODIAN'S FULL-ENVELOPE TOTAL IS THE BASE; THE MODEL-PLATFORM VALUE IS
> SUBTRACTED; THE REMAINDER *IS* NON-MODEL.** The custodian is the source of truth for the total — **never
> the model platform.** DE read this correctly and I confirm all four citations.

## 2. WHAT "MIRROR THE SHAPE" MUST **NOT** MEAN — the 0824 base carries a never-exercised null policy

`:327` is `pd.to_numeric(...).fillna(0.0).sum()`. **Measured on the live 49F base (`date=2026-07-21`, 540
objects enumerated, 7,086 rows): raw nulls = 0, coercion failures = 0, `.fillna(0.0)` hits 0.00% of rows.**
`fillna` and `skipna` return the identical sum. **That line has never fired on the data it was written for.**

> **A NULL POLICY THAT HAS NEVER BEEN EXERCISED IS NOT A DESIGN DECISION — IT IS AN UNTESTED ASSERTION, AND
> COPYING IT ONTO DATA WITH A DIFFERENT NULL PROFILE IS HOW IT FIRES FOR THE FIRST TIME IN PRODUCTION.**
> Mirror the **IDENTITY** (§1). **Re-decide the null handling on Cottonwood's own data (§3).**

## 3. THE FIVE DECISION POINTS — **TWO DISSOLVE ON MEASUREMENT**

Measured: `blackdiamond/cottonwood/silver/fact_holdings/date=2026-07-20`, **33 objects enumerated**,
16,762 rows / 24 cols.

### (1) CASH — **RESOLVED. Cash is ALREADY IN the total. DE's premise inverts.**
DE recorded *"`Cash Equivalent` object dtype, 0/16,762 non-null → cash cannot currently be identified."*
**It is 16,762 of 16,762 NON-NULL — 100% populated — with values `['true','false']. It is a BOOLEAN FLAG,
not a money column.** A `pd.to_numeric()` on `'true'/'false'` coerces to NaN and reports "all null", which
is almost certainly the path taken. **Measuring a flag on a numeric axis returned the exact opposite of the
truth**, and it was DE's own #1 ("the biggest one").

| `Cash Equivalent` | rows | Σ Market Value |
|---|---|---|
| `true` | 1,428 | **$15,232,656.26** (3.33%) |
| `false` | 15,334 | $442,881,346.84 |
| **total** | 16,762 | **$458,114,003.10** |

**So the base is ALREADY full-envelope (positions + cash), semantically matching 49F's `net_mv_plus_cash`.
It is NOT understated for want of a cash leg, and no cash column needs to be found or added.**

### (2) THE 26% NULL `Market Value` — **RESOLVED, and not the hazard it looked like.**
4,328 of 16,762 (25.8%) are MV-null. **On every one of those rows `Unaccrued Market Value` AND `Accrual`
are ALSO null (non-null count = 0 for both).** They are **wholly empty of monetary content** — closed/zero
positions or roster rows — not a value that failed to load. **`fillna(0).sum()` and `skipna.sum()` are
IDENTICAL to the cent ($458,114,003.10).** The 26% does **not** understate the base.

> **BUT THE CONTROL IS NOT A NULL POLICY — IT IS AN INVARIANT.** Neither treatment can distinguish *"empty
> row"* from *"real position whose value failed to load"*; both render `$0`. **Assert what is true today:
> a null `Market Value` row MUST be null across ALL money columns.** The day a row has null MV and
> non-null Unaccrued MV, that is a REAL gap — and under either null policy it is absorbed silently. **This
> is the check, and it is cheap. Do not ship a `.fillna` and call it handled.**

### (3) `Market Value` vs `Unaccrued Market Value` — **OPEN, decide deliberately.**
~$293k apart (DE's figure; **I did not re-measure this one — flagged as DE's, not mine**). 49F's
`net_mv_plus_cash` carries accrual implicitly, so the accrual-inclusive analog is `Market Value`.
**Recommend `Market Value` and DECLARE it**, rather than inherit whichever is convenient.

### (4) `_s2` NAMING — **DE self-corrected; confirmed, and worth keeping loud.**
`fact_holdings_s2` is **5 rows / 7 generic `c1,c2` cols — a SECTION-2 FOOTER** of a multi-section BD export
(`mirror_schemas.py:615`), **not** the Schwab-style `_s2` payload. **Same suffix, opposite meaning across
vendors. Use `fact_holdings`.** DE formed the hypothesis and the measurement killed it — recorded because
the next person will form it too.

### (5) JOIN GRAIN / CONSERVATION — **OPEN, and now the LARGEST remaining risk.**
49F's model side is a **model-level platform feed**; Cottonwood's must be an **account-level join**
(`fact_model_assignment.accountRebalStrategyID` × `fact_holdings`). **The identity `total = model +
non_model` holds ONLY if both sides cover the SAME ACCOUNT UNIVERSE.** Requires an explicit **conservation
check** — assigned accounts with no holdings, and holdings accounts absent from assignment, both enumerated
with counts and dollars. **If they disagree, the residual absorbs the error silently and nothing flags it.**

## 4. WHY THE BASE MATTERS MORE HERE THAN FOR 49F

Total ~**$458.1M** (measured). Conservative Growth ~**$30.99M** (0.6.2's WS-E figure, **theirs, not
re-measured by me**). If the Opal-modeled slice is near that, **the non-model residual is ~93% of the book.**
For 49F the residual is a minority of custody; **for Cottonwood it would essentially BE the firm headline** —
so an error in the base does not perturb the number, it *is* the number, and it moves in a direction no
current gate is pointed at.

## 5. PROPOSED SOLUTION

```
total_aua[i] = Σ fact_holdings["Market Value"]            (full-envelope: cash IS included, 3.33%)
model[i]     = Σ MV of accounts assigned to an Opal Rebalancer model
                 (fact_model_assignment.accountRebalStrategyID === Rebalancer model.id)
non_model[i] = total_aua[i] - model[i]                    (SAME identity, SAME direction as 0824)
headline[i]  = total_aua[i]
absent partition -> None, NAMED gap, NO interpolation     (0824 :611-614 behaviour, preserved)
```
**Gates that must ship WITH it, not after:**
1. **Null-row invariant** (§3.2) — null MV implies null across all money columns, else RED.
2. **Conservation check** (§3.5) — both account universes enumerated, with counts and dollars.
3. **Declared accrual basis** (§3.3) in the artifact, not only in a commit message.
4. **Coverage fraction on every limb** (R10), against the defect-capable population.
5. **No proof transfers from the two-firm gates** (R9) — every gate re-exercised against `f(a,b,c)`.

## 6. WHAT I HAVE NOT DONE

No producer run. No artifact written. No ETag moved. Nothing staged, nothing published. **Cottonwood fold
NOT started** — this is the proposal Andrew asked for, and the build waits on CTO's carve-out ruling.
Not re-measured: the ~$293k accrual delta (DE) and the ~$30.99M Conservative Growth slice (0.6.2) — **both
attributed, neither adopted as mine.**

-- `0.4.0_DS_ClientPlatform`
