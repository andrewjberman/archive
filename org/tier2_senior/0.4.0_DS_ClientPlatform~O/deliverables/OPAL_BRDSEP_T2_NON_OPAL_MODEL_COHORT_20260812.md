# ⛔ DESCOPED — OPAL_BRDSEP.T2 (superseded shape): three-firm wallet-share cohort

> **THIS DOCUMENT IS DESCOPED. It is NOT the T2 deliverable.** CTO issued a `[STOP]` at
> 2026-08-12 ~1933Z: Andrew narrowed T2 at their terminal ~1925Z and CTO recorded the narrowing as
> **their own mis-spec, not a change of his mind** — a three-firm wallet-share question had been
> written from an ambiguous phrase while he was describing one specific structure.
>
> **The real T2 is Cottonwood only, a within-strategy decomposition by constituent model:**
> `OPAL_BRDSEP_T2_COTTONWOOD_STRATEGY_DECOMPOSITION_20260812.md`.
>
> **OUT of scope as of that STOP:** 49 Financial · Inflection · the whole (A)/(B) denominator
> construction · the $285,429,409.86 cross-check · the Eclipse-vs-Orion basis question.
>
> **Retained, not deleted**, per the same discipline applied to the descoped June section in T1:
> deleting measured evidence when a scope moves is how a record stops being trustworthy. Three
> findings here survive on their own merits and are cited from the live deliverable:
> the platinum `by_model`-vs-`model_aua` SMA-sleeve decomposition, Inflection's account-level
> `modelName` grain, and the $12,110,899.35 SmartX-vs-platinum disagreement.
> **Nothing below feeds the board deck.**

*(Original document follows, unaltered.)*

---

# OPAL_BRDSEP.T2 — the NON-Opal-model cohort (wallet share), value + counts

**Author:** `0.4.0_DS_ClientPlatform~O` · 2026-08-12
**TO:** `OPAL_BRDSEP.T2` @`cbf5a9d63d` · **Issued by:** `1.0.0_SA_CTO` · Andrew's words verbatim in TO §0
**Predecessor:** `OPAL_BRDSEP.T1` (@`7a3916acd8`, revised @`e2991bf495`)
**Type:** Measurement. Changes no served artifact; `platinum/` read-only throughout.
**Determinism (T2-A9):** extraction run twice, byte-identical, 0 differing lines of 137.

---

## ⛔ 0. WHAT THIS NUMBER IS, AND WHAT IT IS NOT

> **This is an OPPORTUNITY DENOMINATOR, not an asset claim.** It measures assets sitting *beside*
> Opal models in relationships Opal already touches. **It must never be added to the T1 asset base,
> and must never be presented as Opal AUA.** Adding T1 and T2 double-counts nothing but *asserts*
> something false: that we manage money we do not manage.

Andrew's ask, verbatim (2026-08-12 ~1910Z): *"I want to get a cohort value count on all values in
these accounts that are* **NOT** *contained in an opal model, because we may want to include those
figures as well somewhere."*

---

## 1. THE ANSWER — both denominators, all three firms

**"These accounts" has two readings and they differ materially. Both are reported; the choice is
presentational and is Andrew's.**

### Denominator A — WALLET SHARE (accounts/clients that already hold an Opal model)

| Firm | as-of | Accounts | Clients | Total value | Opal-model value | **NON-Opal value** |
|---|---|---:|---:|---:|---:|---:|
| 49 Financial `08242234` | 2026-08-11 | 5,678 | 3,616 | $1,597,056,386.04 | $1,463,630,228.14 | **$133,426,157.90** |
| Inflection *(client grain)* | 2026-08-11 | 254 | 137 | $196,710,049.67 | $155,943,297.84 | **$40,766,751.83** |
| Cottonwood | 2026-08-10 | 322 | 172 ʳ | $187,928,913.13 | $136,530,322.99 | **$51,398,590.14** |
| | | | | | **TOTAL A** | **$225,591,499.87** |

ʳ Cottonwood client count is `Relationship ID` (223 firm-wide), its household-equivalent key.

### Denominator B — FIRM-WIDE (all in-scope accounts)

| Firm | as-of | Accounts | Clients | Total value | Opal-model value | **NON-Opal value** |
|---|---|---:|---:|---:|---:|---:|
| 49 Financial `08242234` | 2026-08-11 | 7,190 | 4,268 | $1,736,948,738.65 | $1,463,630,228.14 | **$273,318,510.51** |
| Inflection | 2026-08-11 | 948 | 318 | $209,129,912.97 | $155,943,297.84 | **$53,186,615.13** |
| Cottonwood | 2026-08-10 | 926 | 223 ʳ | $482,567,772.65 | $136,530,322.99 | **$346,037,449.66** |
| | | | | | **TOTAL B** | **$672,542,575.30** |

**The two readings differ by $446,951,075.43.** That is the whole reason the TO required both: "these
accounts" is a three-times-larger number under the firm-wide reading.

---

## 2. THE 49F CROSS-CHECK **DISAGREES**, and the disagreement is the finding (T2-A3)

CTO supplied a T1-derived cross-check: $1,736,948,738.65 − $1,451,519,328.79 = **$285,429,409.86**.

**My independent measurement gives $273,318,510.51 — a disagreement of $12,110,899.35 (4.2%).**

I did not reconcile it away. **The entire difference sits in the Opal-model base, not in my
complement arithmetic**, and the two bases are different instruments measuring the same quantity:

| Source | Opal-model value @2026-08-11 |
|---|---:|
| SmartX `fact_allocation_account_map` (account-level, what I measured) | $1,463,630,228.14 |
| platinum `model_aua` (what the T1 subtraction used) | $1,451,519,328.79 |
| **difference** | **$12,110,899.35** |

**Localised per model** — the two agree closely everywhere except one line:

| Model | platinum `by_model` | SmartX | diff |
|---|---:|---:|---:|
| `opal_long_term_conservative` / Opal Conservative Growth | $790,375,699.03 | $783,586,102.11 | **+$6,789,596.92** |
| `opal_intermediate` / Opal Intermediate-Term | $297,026,972.30 | $297,289,712.48 | −$262,740.18 |
| `opal_long_term_aggressive` / Opal Long-Term Aggressive | $206,591,286.13 | $206,456,862.04 | +$134,424.09 |
| `opal_short_term` / Opal Short-Term | $107,387,156.35 | $107,432,428.43 | −$45,272.08 |
| `opal_ultra_short_term` / Opal Ultra Short-Term Income | $50,138,214.97 | $50,124,814.43 | +$13,400.54 |
| `opal_div_sma` / Opal Dividend Income | $18,744,873.12 | $18,740,308.64 | +$4,564.48 |
| `opal_growth_sma` / Pathfinder Focused Opportunities | $4,154,314.49 | $4,150,736.38 | +$3,578.11 |

**Six of seven models agree to within 0.1%. One — Conservative Growth — differs by $6.79M (0.86%).**
That is where any reconciliation should start; I have not attempted one because it is a producer
question, not an arithmetic one.

### A structural fact found while cross-checking, which is NOT a defect

**platinum's `by_model` rows sum to $1,474,418,516.39 while its own `model_aua` field reads
$1,451,519,328.79** — a $22,899,187.61 gap. That gap is *exactly* `opal_div_sma` ($18,744,873.12)
+ `opal_growth_sma` ($4,154,314.49). **`model_aua` deliberately excludes the two SMA sleeves; `by_model`
lists them.** Clean decomposition, ties to the cent, no defect — but anyone summing `by_model` and
comparing to `model_aua` will find a discrepancy that is really a scope difference.

⚠ **Noted, not concluded:** SmartX carries **"Pathfinder Focused Opportunities"** as a model, and its
value sits within $3,578 of platinum's `opal_growth_sma`. That *suggests* the two are the same sleeve
under different names. **The value proximity is suggestive, not a proven mapping** — resolving it needs
the model-id tie, which belongs to the crosswalk owner.

---

## 3. INFLECTION — the account-grain answer is $0, and that is a structural fact, not a gap (T2-A4)

**BASIS DECLARED (T2-A4): these figures complement the ORION-INCLUSIVE base** — `fact_positions`
rows whose `modelName` contains "opal". **This is not the platinum Eclipse-crosswalked base**, and the
complement of that other base is a different number (§3c).

### 3a. Why denominator A is degenerate here

| Check | Result |
|---|---|
| Accounts at Inflection (2026-08-11) | 948 |
| Accounts with **more than one** distinct `modelName` | **0** |
| Rows with null `modelName` | **0** of 35,262 |

**`modelName` is strictly account-level.** Every account is wholly in exactly one model, so an account
holding an Opal model holds *nothing else*. **Non-Opal value inside Opal-holding accounts is $0.00 BY
CONSTRUCTION — not $0 because we failed to find any.** A reader shown a bare zero would reasonably
suspect a broken join; it is not.

### 3b. The meaningful cut at Inflection is CLIENT grain

| | Clients | Accounts | Value |
|---|---:|---:|---:|
| Clients holding ≥1 Opal account | 266 of 318 | — | $196,710,049.67 total |
| — their Opal value | | | $155,943,297.84 |
| — **their NON-Opal value** | 137 | 254 | **$40,766,751.83** |
| Clients with **no** Opal account | 52 | 94 | $12,419,863.30 |

**Opal already holds 79.3% of the wallet of the clients it serves at Inflection.** The three legs sum
to $209,129,912.97 = the firm total, exactly.

### 3c. The basis choice moves this number, and moves it the *other* way

| Base being complemented | Firm-wide NON-Opal |
|---|---:|
| Orion-inclusive (`modelName` contains "opal") — **used above** | $53,186,615.13 |
| platinum Eclipse-crosswalked (`model_aua` $144,978,896.75 @08-10) | $64,151,016.22 |

**A complement inherits its base's frame.** T1 found $914,144.89 of Opal-*named* Orion rows that
platinum reads as zero — on the platinum basis those dollars fall **into** the non-Opal cohort; on the
Orion basis they fall **out** of it. The two bases here differ by $10,964,401.09 (partly the T1
$914,145, partly the 08-10 vs 08-11 date difference).

---

## 4. COTTONWOOD — an Opal *strategy* is not an Opal *model*, and the gap IS the wallet share (T2-A5)

**Matcher: the T1 normalized resolver, reused as built** — 18 of 18 resolved against a 63-strategy
roster. **on-list-not-found = EMPTY; found-not-on-list = 5** (unchanged from T1).

| | Accounts | Relationships | Value |
|---|---:|---:|---:|
| **A — accounts on an Opal-18 strategy** | 322 | 172 | $187,928,913.13 |
| — of which Opal **MODEL** component | | | $136,530,322.99 |
| — **NON-Opal inside those accounts** | | | **$51,398,590.14** |
| **B — all Cottonwood accounts** | 926 | 223 | $482,567,772.65 |
| — **NON-Opal firm-wide** | | | **$346,037,449.66** |

**The distinction that produces the A figure:** an account running *"Opal Satellite 50"* is on the
18-list, but the strategy is a **blend** — only part of it is Opal models and the rest is core/satellite
sleeves. Attributing the whole account to "Opal" overstates by **$51.4M**. That $51.4M is not an error;
**it is precisely the in-account wallet share the TO asks for.**

**Two exact ties validate the whole frame** (both `True` in the extraction output):
- deduped holdings total **$482,567,772.65** = platinum `partner_custody_total` @08-10, to the cent
- denominator-B non-Opal **$346,037,449.66** = platinum `non_model_aua` @08-10, to the cent

**Relationship-grain control (the double-count trap):** cot `fact_holdings` is
Relationship×Account×Asset. Naive sum = $482,772,843.42; deduped to (AccountID, AssetID) =
$482,567,772.65. **$205,070.77 phantom** from 2 pairs of 17,138 appearing under two relationships. Small
here — but it is the deduped figure that ties to the producer, which is the evidence the collapse is right.

**Off-list Opal-named strategies (T2-A6) — reported as their own line, neither included nor excluded:**

> **$2,143,273.89 across 2 accounts** (`Opal Hendrickson LT/UST`, `Opal Sat 50+ 15% cash`; the other
> three off-list names carry 0 accounts). **Whether these count as Opal models is a CLASSIFICATION
> question and it is Andrew's.** Excluded from both tables above; add $2,143,273.89 to the Opal side
> and subtract it from non-Opal if he rules them in.

---

## 5. COTTONWOOD ACCOUNT + CLIENT DELTAS — the T1 gap, now closed (T2-A7)

| Basis | Accounts | Relationships |
|---|---|---|
| **Andrew-ruled 0 start** (2026-04-01 → 2026-08-10) | 0 → 926 = **+926** | 0 → 223 = **+223** |
| **Measured coverage window** (2026-06-09 → 2026-08-10) | 680 → 926 = **+246** | 206 → 223 = **+17** |

⛔ **The measured +246 is NOT clean growth — the count-ramp check fires (T2-A8).**

| Date | Rows | Accounts | Relationships | Value |
|---|---:|---:|---:|---:|
| 2026-06-09 | 10,183 | 680 | 206 | $373,157,665.00 |
| 2026-06-30 | 11,453 | 813 | 218 | $436,654,607.00 |
| 2026-07-15 | 16,615 | 845 | 221 | $435,714,870.67 |
| 2026-07-20 | 16,762 | 913 | 221 | $458,114,003.10 |
| 2026-08-10 | 17,138 | 926 | 223 | $482,567,772.65 |

**Accounts rise 36% while relationships rise 8%** — the feed picking up more accounts inside existing
relationships, which is onboarding, not client acquisition. Rows jump 45% between 06-30 and 07-15
against a 4% account rise, i.e. more *assets per account* appearing. This is the same coverage-onset
shape T1 found three times, and it lands on the producer's declared `first_tracked_date` of 2026-07-20.
**The +$109,410,107.65 measured value change over that window should not be read as growth.**

---

## 6. HAZARD LEDGER — all three T1 hazards recurred, all three fired (T2-A8)

| Hazard | Where it bit in T2 | Outcome |
|---|---|---|
| **Absent is not zero** | Two SmartX partitions (`fact_account_detail`, `fact_account_allocations`) are **present but EMPTY** at 2026-08-11 (0 rows) | Not used. An empty partition differencing as a minuend would have zeroed the base. |
| **Coverage onset presents as growth** | Cottonwood `fact_holdings` 06-09 → 08-10 | **FIRED** — +246 accounts is onboarding; §5 |
| **Subtraction starts at its weakest input** | SmartX platform silver begins **2026-07-14** | No T2 figure is dated before it; point-in-time only, no cross-window subtraction attempted on this feed |

---

## 7. DENOMINATORS (T2-A9)

| Scan | Denominator |
|---|---|
| SmartX `fact_allocation_account_map` @08-11 | 7,265 rows · 5,718 accounts · 7 model_ids |
| SmartX `fact_model_allocation_roster` @08-11 | 9,713 rows · 8 model_ids |
| 49F `dim_balance` @08-11 | 7,190 rows, `net_mv_plus_cash` non-null 100% |
| 49F `fact_acc` @08-11 | 7,189 rows, tin present 100% |
| 49F join after leading-zero normalization | 5,686 of 5,718 map accounts matched; 32 unmatched; 1,504 balance-only |
| Inflection `fact_positions` @08-11 | 35,262 rows · 948 accounts · 318 clients |
| Cottonwood `fact_holdings` @08-10 | 17,140 raw → 17,138 deduped · 926 accounts · 223 relationships |
| Cottonwood rebalancer accounts | 921 rows · 921 account numbers · 47 distinct strategies |
| Cottonwood roster | 63 of 63 (`pageCount`=1) |
| Cottonwood account-number join | 917 matched · 9 holdings-only · 4 accounts-only |

---

## 8. WHAT SURPRISED ME

1. **Inflection's account-grain wallet share is exactly $0, and it is correct.** A structural property
   of how Orion assigns models, not a measurement failure — and a bare zero in a table would have read
   as a bug. The question only becomes answerable one grain up.
2. **At Cottonwood the wallet share is *inside* the Opal accounts, not outside them.** $51.4M of the
   money in accounts running Opal strategies is not in an Opal model. An account-level "is it Opal?"
   flag cannot see that.
3. **platinum's `by_model` does not sum to its own `model_aua`** — and the gap is exactly the two SMA
   sleeves. Correct by design, and a trap for anyone who checks one against the other.
4. **The 49F cross-check disagreed**, and the disagreement localised to a single model line out of
   seven. Six models agreeing to 0.1% is what makes the seventh interesting.
5. **1,504 accounts inside `08242234` hold no Opal model at all** — 21% of the account count carrying
   $273M. The wallet-share opportunity at 49F is mostly in accounts we already custody but do not model.

---

## 9. COMPILER TOOLS

| Tool | Call | Result |
|---|---|---|
| `comp-find` | `collapse_relationship_grain` | PASS — 53 hits, DEF=3; located the canonical collapse in 3 implementations |
| `comp-find --name` | (T1, reused) `rebalance` | reused T1's location of the BD pipeline |
| comp-rail gate | blocked a raw `aws s3 ls` mid-command | **Correctly fired.** I reworked the check to a row-count ramp, which was the better instrument anyway |
| `commit-gate.sh` | `extract_brdsep_t2.py` | PASS |
| `proof-of-spec-check.py` | instance + 9 ids | VALID |

**What worked:** `comp-find` on `collapse_relationship_grain` — memory flagged the relationship-grain
double-count and the tool put the three implementations on page 1, so the control took one call.
**Gap:** none new; the `comp-estate` `etfs`-vs-`etf-reports` naming gap from T1 is unchanged.

---

## 10. EVIDENCE INDEX

| Figure | Source |
|---|---|
| 49F account→model→value | `s3://opal-data-assets/smartx/platform/silver/fact_allocation_account_map/date=2026-08-11/` |
| 49F model names | `.../fact_model_allocation_roster/date=2026-08-11/` |
| 49F account totals + clients | `s3://opal-data-assets/schwab/08242234/silver/{dim_balance,fact_acc}/date=2026-08-11/` |
| Inflection positions | `s3://opal-data-assets/orion/inflection/silver/fact_positions/date=2026-08-11/` |
| Cottonwood holdings | `s3://opal-data-assets/blackdiamond/cottonwood/silver/fact_holdings/date=…/` |
| Cottonwood strategies + accounts | `s3://opal-data-assets/blackdiamond/cottonwood/bronze/rebalancer_{models,accounts}/2026-08-12/` |
| platinum comparators (read-only) | `s3://opal-data-portal-v2/platinum/mdpf/{firm}/aggregate-aua-timeseries.json` |
