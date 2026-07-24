# GC-W1 — Global Holdings-Count Composition: MEASUREMENT

**TO:** `MDPF_3FIRMS.GC-W1` @`939376b88` (amended @`157278cb3`)
**Agent:** `0.4.0_DS_ClientPlatform~A` · **Date:** 2026-07-24 · **archetype:** VALIDATE
**Status:** COMPLETE — measurement only, no fix, no code change, read-only on the producer.

---

## 0. WHAT I MEASURED ON, AND THE DENOMINATORS

| Item | Value |
|---|---|
| **Primary artifact (SERVED bytes)** | `s3://opal-data-portal-v2/json/mdpf/global/aggregate-aua-timeseries.json` |
| LastModified / ETag / size | **2026-07-23T21:18:53Z** · `55a8b379fb22a9c1ed02db1eef5d2a18` · 254,419 B |
| Per-firm artifacts | `json/mdpf/{49financial,inflection,cottonwood}/aggregate-aua-timeseries.json`, all **2026-07-23T21:47:0[6-7]Z** |
| **Spine denominator** | **447** rows (`n_dates`=447, `len(dates)`=447), 2024-11-01 → 2026-07-22 |
| **Trading-day denominator** | **429** NYSE trading days · **18** non-trading rows on the spine |
| `account_count_total` | **407 non-null / 40 NULL** (of 447) |
| Calendar resolver | **`lib/trading_calendar.py` @`0cbb0ad17`** (`calendar_source()` = `NYSE/hardcoded-fallback-2024-2027`) |
| Mechanism vintage | **`data/mdpf/scripts/gold/dim_mdpf_aggregate_aua_timeseries.py` @`3efc9dc6d`** (last commit touching the file; worktree clean; 1,926 lines — positive control run on every cited line) |
| Method | Retrieve served bytes via `s3api get-object` (explicit-Z metadata), index by date, compare Global cells against per-firm cells. No gold run (NEVER#4). No producer self-report used. |

> **Vintage note:** the TO cites `:1720-1741 @275b51aee`. The file has moved since; at `3efc9dc6d` the same block is **`:1716-1741`**. All cites below are `@3efc9dc6d`. Session HEAD advanced `939376b88`→`67ea1930e` mid-measurement (other agents); the producer file was untouched by that.

---

> **ADDENDUM 2026-07-24 — "THE TWO 429s" HAZARD CHECKED AGAINST THIS REPORT, AND IT HOLDS.** `3.0.0_SA_CVO`
> (@`b8727a1f07`) found that two INF builds both reporting `n_dates = 429` cover **different date sets** (the
> 07-18 build carried 22 non-trading dates; the current carries 0 — the axis was re-based, preserving
> cardinality while changing membership), and warned that *"a denominator of 429 is meaningless without the
> build it was measured on."* **This report uses 429 for TWO things** — the count of NYSE trading days among
> the 447 spine rows, and the per-firm axis length — **and treats them as the same set.** I tested that rather
> than assume it, on the build pinned in §0:
>
> | check (current build, Global ETag `55a8b379…`, per-firm @2026-07-23T21:47:0[6-7]Z) | result |
> |---|---|
> | NYSE trading days among the 447 spine rows | 429 |
> | 49financial served axis | 429 dates, **0 non-trading** — **identical set** (symmetric difference 0 both ways) |
> | inflection served axis | 429 dates, **0 non-trading** — **identical set** (symmetric difference 0 both ways) |
> | cottonwood served axis | 447 — **identical to the full spine** |
>
> **So the two 429s ARE the same 429 here, and §1.2's class-D reasoning stands as written.** The claim is now
> *verified and build-pinned* rather than assumed. CVO's general caution still applies to anyone comparing a
> "429" across builds — including future readers of this report.

## 1. AC-1 — THE 40 NULL DATES (40 of 447)

**Enumeration method:** index every position `i` where `account_count_total[i] is None`; for each, read all 5 core cells from `by_model[k].account_count[i]`, then read the same date out of each per-firm served artifact.

### 1.1 The finding that reframes Defect A

> **On all 40 null dates, ALL FIVE core cells are absent — never a partial core set.**

The PRD's §3.1 law (*one* missing core cell nulls the whole day) **is real in source** (`:1719-1721 @3efc9dc6d`) but **has never been the operative cause**: there is no date in the served bytes where a *partial* core set produced the null. So "which cell was missing" has one answer for all 40, and the discriminating question moves one level up — **which FIRM's leg was missing**, because a firm's `None` poisons the Global per-model cell before the core-completeness test ever runs (`:1656 @3efc9dc6d`, `acct.append(None if (cgap or not cparts) ...)`).

**Exercised proof of the firm-level poison, not inferred** — `2026-05-21`, where 49F is fully PRESENT:

| model | GLOBAL | 49F | INF | COT |
|---|---|---|---|---|
| opal_ultra_short_term | **None** | 167 | None | None |
| opal_short_term | **None** | 660 | None | None |
| opal_intermediate | **None** | 1567 | None | None |
| opal_long_term_conservative | **None** | 2974 | None | None |
| opal_long_term_aggressive | **None** | 1420 | None | None |

49F served 6,788 real accounts that day. Global publishes `None`. **The all-or-nothing operates at the FIRM axis, and that is a materially different defect from the one the PRD describes.**

### 1.2 The 40 rows

Legend — `49F/INF/COT` = that firm's state on that date in **its own served artifact**: `present` / `all-None` / `OFF-AXIS` (date not on that firm's 429-day axis at all).
Reason classes: **A** 49F legacy-omitted · **B** both legs absent · **C** INF-only absent (49F present) · **D** non-trading spine row · **E** past `count_coverage_end`.

| # | date | dow | class (served) | label src | 49F | INF | COT | reason |
|---|---|---|---|---|---|---|---|---|
| 1 | 2025-12-24 | Wed | exempt_absorbed | ENUM | all-None | present | all-None | **A** |
| 2 | 2025-12-30 | Tue | exempt_absorbed | ENUM | all-None | present | all-None | **A** |
| 3 | 2025-12-31 | Wed | exempt_absorbed | ENUM | all-None | present | all-None | **A** |
| 4 | 2026-01-02 | Fri | exempt_absorbed | ENUM | all-None | present | all-None | **A** |
| 5 | 2026-02-02 | Mon | exempt_absorbed | ENUM | all-None | present | all-None | **A** |
| 6 | 2026-03-02 | Mon | exempt_absorbed | ENUM | all-None | present | all-None | **A** |
| 7 | 2026-04-01 | Wed | exempt_absorbed | ENUM | all-None | present | all-None | **A** |
| 8 | 2026-05-01 | Fri | exempt_absorbed | ENUM | all-None | present | all-None | **A** |
| 9 | **2026-05-21** | Thu | exempt_absorbed | **FALLBACK** | **present** | all-None | all-None | **C** |
| 10 | 2026-05-30 | Sat | exempt_absorbed | FALLBACK | OFF-AXIS | OFF-AXIS | all-None | **D** |
| 11 | 2026-05-31 | Sun | exempt_absorbed | FALLBACK | OFF-AXIS | OFF-AXIS | all-None | **D** |
| 12 | 2026-06-01 | Mon | exempt_absorbed | ENUM | all-None | all-None | all-None | **B** |
| 13 | 2026-06-06 | Sat | exempt_absorbed | FALLBACK | OFF-AXIS | OFF-AXIS | all-None | **D** |
| 14 | 2026-06-07 | Sun | exempt_absorbed | FALLBACK | OFF-AXIS | OFF-AXIS | all-None | **D** |
| 15 | 2026-06-08 | Mon | exempt_absorbed | ENUM | all-None | present | all-None | **A** |
| 16 | 2026-06-13 | Sat | exempt_absorbed | FALLBACK | OFF-AXIS | OFF-AXIS | all-None | **D** |
| 17 | 2026-06-14 | Sun | exempt_absorbed | FALLBACK | OFF-AXIS | OFF-AXIS | all-None | **D** |
| 18 | **2026-06-19** | Fri | exempt_absorbed | FALLBACK | OFF-AXIS | OFF-AXIS | all-None | **D** (Juneteenth) |
| 19 | 2026-06-20 | Sat | exempt_absorbed | FALLBACK | OFF-AXIS | OFF-AXIS | all-None | **D** |
| 20 | 2026-06-21 | Sun | exempt_absorbed | FALLBACK | OFF-AXIS | OFF-AXIS | all-None | **D** |
| 21 | 2026-06-26 | Fri | exempt_absorbed | ENUM | all-None | present | all-None | **A** |
| 22 | 2026-06-27 | Sat | exempt_absorbed | FALLBACK | OFF-AXIS | OFF-AXIS | all-None | **D** |
| 23 | 2026-06-28 | Sun | exempt_absorbed | FALLBACK | OFF-AXIS | OFF-AXIS | all-None | **D** |
| 24 | 2026-06-29 | Mon | exempt_absorbed | ENUM | all-None | present | all-None | **A** |
| 25 | 2026-06-30 | Tue | exempt_absorbed | ENUM | all-None | present | all-None | **A** |
| 26 | 2026-07-01 | Wed | exempt_absorbed | ENUM | all-None | all-None | all-None | **B** |
| 27 | **2026-07-03** | Fri | exempt_absorbed | FALLBACK | OFF-AXIS | OFF-AXIS | all-None | **D** (July 4 observed) |
| 28 | 2026-07-04 | Sat | exempt_absorbed | FALLBACK | OFF-AXIS | OFF-AXIS | all-None | **D** |
| 29 | 2026-07-05 | Sun | exempt_absorbed | FALLBACK | OFF-AXIS | OFF-AXIS | all-None | **D** |
| 30 | 2026-07-09 | Thu | exempt_absorbed | ENUM | all-None | present | all-None | **A** |
| 31 | 2026-07-10 | Fri | exempt_absorbed | ENUM | all-None | present | all-None | **A** |
| 32 | 2026-07-11 | Sat | exempt_absorbed | FALLBACK | OFF-AXIS | OFF-AXIS | all-None | **D** |
| 33 | 2026-07-12 | Sun | exempt_absorbed | FALLBACK | OFF-AXIS | OFF-AXIS | all-None | **D** |
| 34 | 2026-07-13 | Mon | exempt_absorbed | ENUM | all-None | all-None | all-None | **B** |
| 35 | 2026-07-14 | Tue | exempt_absorbed | ENUM | all-None | all-None | all-None | **B** |
| 36 | 2026-07-15 | Wed | exempt_absorbed | ENUM | all-None | all-None | all-None | **B** |
| 37 | 2026-07-18 | Sat | exempt_absorbed | FALLBACK | OFF-AXIS | OFF-AXIS | all-None | **D** |
| 38 | 2026-07-19 | Sun | **lag_window** | FALLBACK | OFF-AXIS | OFF-AXIS | all-None | **D** |
| 39 | 2026-07-20 | Mon | exempt_absorbed | ENUM | all-None | present | all-None | **E** (+ also A) |
| 40 | 2026-07-21 | Tue | **lag_window** | FALLBACK | all-None | present | **present** | **E** |

**Reason distribution — sums to 40, every date EXAMINED, zero NOT-YET-EXAMINED:**

| class | n | mechanism, with its source |
|---|---|---|
| **A** — 49F legacy-omitted trading day | **14** | 49F's served-real count import runs on a **429-legacy axis that structurally lacks these canonical trading days**. Named by the artifact itself: `49F meta.count_exempt_reason` — *"enumerated legacy-omitted trading days … enumerated-never-a-flag (a 21st omitted day goes RED); RETIRES with the 49F count-axis decouple"*. Enumerated at `:1158-1164 @3efc9dc6d` (20 dates), byte-identical to `49F meta.count_exempt_dates`. |
| **B** — both legs absent | **5** | 49F omitted (as A) **and** INF's model partition absent. `Global meta.honest_none.by_date`: *"model_partition_absent — custody partition PRESENT, so this is an honest custody-only day"*, feed `eclipse/inflection/silver/fact_portfolios_full`. |
| **C** — INF-only absent, 49F present | **1** | 05-21. INF model partition absent; **49F served 6,788 real accounts and was discarded** by the firm-level poison at `:1656`. |
| **D** — non-trading spine row | **18** | The date is not on the 49F/INF axes at all (both `OFF-AXIS`). These rows exist on the 447-spine **only because the cottonwood axis is 447** while 49F/INF are 429 (`meta.firm_axis_reconciliation`: `n_49f`=429, `n_inflection`=429, `n_cottonwood_axis`=447). 16 weekend + **2 market holidays** (06-19, 07-03). |
| **E** — past `count_coverage_end` | **2** | `count_coverage_end` = **2026-07-18**; the served-real import does not cover beyond it. 07-20 matches the ENUM branch first (`:1723`) so it is *labelled* `exempt_absorbed` though its operative cause is the lag window — **a label collision, flagged for W-2.** |

**Sub-finding (label integrity):** `exempt_absorbed` is served on **38** dates but only **20** are on the enumerated shelf. The other **18** reach that label through the `else` fallback at `:1729-1731` — whose own comment says such a date *"would be a cross-axis violation the gate refuses upstream."* They are not violations; they are non-trading rows. **A label that means "enumerated exemption" is being applied to 18 dates that were never enumerated.** No number is wrong; the *provenance label* is, and W-4 intends to render exactly this label.

---

## 2. AC-2 — THE 24/40 SPLIT: **CORRECTED to 22/40**

| measure | value | resolver |
|---|---|---|
| nulls that are **NYSE trading days** | **22** | `lib/trading_calendar.py::is_trading_day` @`0cbb0ad17` |
| nulls that are **weekdays (Mon–Fri)** | **24** | `datetime.weekday() < 5` |
| difference | **2** | `2026-06-19` (Juneteenth), `2026-07-03` (July 4 observed) — both weekdays, both NYSE closures, both in `NYSE_HOLIDAYS_FALLBACK` |
| nulls that are non-trading | **18** (16 weekend + 2 holidays) | — |

**CTO's 24 is exactly reproducible as a WEEKDAY count.** I derived 22 independently and then found the 24 by switching predicates — so this is a **named axis difference, not a disagreement about a date**. Under NEVER#1 ("count in TRADING DAYS, never wall-clock") the trading-day figure **22** is the one that binds. His "16 weekend rows" is correct as a weekend count; the non-trading total is 18.

**Second instance of the same root — the density claim.** PRD §3.1: *"Only 3 of the last 12 trading days carry a Global count (07-16, 07-17, 07-22)."* Measured on the **trading-day axis**, the last 12 trading days (07-07 → 07-22) carry **5** (07-07, 07-08, 07-16, 07-17, 07-22). The stated 3 reproduces **exactly** as the last 12 **spine rows** (07-11 → 07-22), a window containing 4 weekend rows.

> **Both corrections have one root: the 447-row spine is being used where the 429-day trading axis is meant.** That is W-7's subject, and it has now demonstrably leaked into two load-bearing numbers in the closeout brief itself. Recommend W-7 be treated as a correctness item, not hygiene.
> Trading-day null rate: **22 of 429 = 5.1%**. All 18 non-trading rows are null (verified, not assumed).

---

## 3. AC-3 — THE +408, DECOMPOSED BY FIRM

Global: 07-17 = **7,686** (`band_2firm`) → 07-22 = **8,094** (`frontier_stamp`) = **+408**.
07-22 is the first non-null after 07-17; the four dates between are all null, so the chart bridges this seam as one straight segment.

### 3.1 Per-firm, each traced to its own served artifact

| firm | 07-17 | 07-22 | delta | class @07-17 | class @07-22 |
|---|---|---|---|---|---|
| 49financial | 7,140 | 7,026 | **−114** | measured | **frontier_stamp** |
| inflection | 546 | 534 | **−12** | measured | measured |
| cottonwood | *absent* (`source_absent`) | 442 | **+442** | — | measured |
| **Σ firms** | **7,686** | **8,002** | **+316** | | |
| **GLOBAL (served)** | **7,686** | **8,094** | **+408** | | |
| **residual (Global − Σfirms)** | **0** | **+92** | **+92** | | |

### 3.2 The residual is not noise — it is unique in the entire series

Swept across **all 407 non-null dates**: Global total equals the sum of the per-firm cells on **406**. The **single** exception is **2026-07-22**, residual **+92** — **the one and only `frontier_stamp` date in the series.**

### 3.3 What the +92 is made of (per-model, 07-22)

| model | GLOBAL | 49F | INF | COT | Σfirms | resid |
|---|---|---|---|---|---|---|
| opal_ultra_short_term | 184 | 169 | 10 | 7 | 186 | −2 |
| opal_short_term | 815 | 687 | 25 | 104 | 816 | −1 |
| opal_intermediate | 2,023 | 1,600 | 200 | 223 | 2,023 | 0 |
| opal_long_term_conservative | 3,378 | 3,180 | 89 | 96 | 3,365 | **+13** |
| opal_long_term_aggressive | 1,430 | 1,390 | 31 | 12 | 1,433 | −3 |
| **opal_growth_sma** | **45** | None | — | — | 0 | **+45** |
| **opal_div_sma** | **40** | None | — | — | 0 | **+40** |
| opal_blend_5050_int_ltc | 155 | — | 155 | — | 155 | 0 |
| opal_blend_5050_st_int | 24 | — | 24 | — | 24 | 0 |
| **TOTAL** | **8,094** | 7,026 | 534 | 442 | **8,002** | **+92** |

- **+85 = SMA count preserve.** 49F serves `None` for both SMA keys on 07-22; Global carries 45/40 forward from last-known via the FLAG-2 preserve, enumerated-keys-only (`:1665-1672 @3efc9dc6d`, `SMA_COUNT_PRESERVE_KEYS` at `:1156`). Declared behaviour, in-band `count_as_of` — **not a defect, but it means Global ≠ Σfirms by construction on any date where an SMA count lags.**
- **+7 = core-model roster residual** (−2, −1, 0, +13, −3). The Global's core cells on 07-22 **do not equal** the sum of the firms' core cells for the same date. Mechanism: the frontier stamp overwrites the last axis position per model (`:1657-1658 @3efc9dc6d`, `acct[-1] = ad_frontier[mkey]`) from `load_account_dist_frontier_counts` (`:604`) — **a second count source carrying its own `as_of`** (`49F meta.frontier_count`: *"stamped on the latest axis date only; NOT covered by count_coverage_end"*). Global and 49F each get stamped independently, so their per-model splits need not agree.

### 3.4 The arithmetic identity

```
+442  cottonwood entering (absent -> 442)
-126  49F (-114) + INF (-12) declining across the same seam
 +92  composition residual (SMA preserve +85, frontier-stamp roster split +7)
-----
+408  the served step   <- verified against by_model deltas, which sum to 408 independently
```

---

## 4. AC-4 — VERDICT ON THE COTTONWOOD ATTRIBUTION

**Claim under test (CTO, explicitly labelled INFERRED):** *the +408 is Cottonwood entering via the frontier stamp.*

> ## VERDICT: **CONFIRMED in direction and dominant driver — REFUTED as to magnitude, sufficiency, AND MECHANISM.**
>
> **AMENDED 2026-07-24 post-CVO (`3.0.0_SA_CVO` @`6e6c8af47`, verified on my own bytes before folding).**
> My original verdict line claimed two refutations and my §3.1/§4 data supported a **third** that the line did
> not state. The claim under test is *"the +408 is Cottonwood entering **via the frontier stamp**."* On the
> served bytes, **cottonwood's `count_provenance` @2026-07-22 is `measured`** — the `frontier_stamp` belongs
> to **49F and Global**, not to cottonwood. **Cottonwood does not enter via the frontier stamp.** I had the
> fact (finding #4 identifies the 49F class flip) but left the mechanism clause unchallenged in the verdict
> line. Corrected here because verdict lines are what downstream readers quote.
>
> | firm | `count_provenance` @2026-07-22 | count |
> |---|---|---|
> | 49financial | **frontier_stamp** | 7,026 |
> | inflection | measured | 534 |
> | cottonwood | **measured** | 442 |
> | GLOBAL | **frontier_stamp** | 8,094 |

**What my decomposition confirms (from served bytes, not from the brief):** Cottonwood *does* enter at 07-22 — `source_absent` → 442 accounts across 5 core models, its first contribution to the Global count — and it is by far the largest single mover. That much of the inference survives contact with the data.

**What it refutes:**

1. **The magnitude is wrong, and wrong in the direction that misleads.** Cottonwood's entry is **+442**, not +408. Reading "+408 = Cottonwood" understates Cottonwood by 34 accounts and, more importantly, implies the step *is* the entry.
2. **The +408 is a NET of three independent movements, two of which the attribution omits.** 49F **−114** and INF **−12** move the other way and **mask** the entry. A reader told "+408 is Cottonwood" cannot see that 49F's contribution fell across this seam.
3. **+92 of the step is not a firm at all.** It is composition: +85 SMA-preserve and +7 frontier-stamp roster split. **No firm-level decomposition can ever sum to 408**, because 92 of it is not firm-attributable — which is exactly why the "+408 by firm" framing needed measuring rather than inheriting.
4. **The mechanism clause is misattributed across firms** (added post-CVO). Cottonwood enters as `measured`;
   the frontier stamp is 49F's and Global's. So "Cottonwood entering via the frontier stamp" conflates two
   different firms' basis changes that happen to land on the same date. **This matters for W-2/W-3:** the
   +92 residual is a *frontier-stamp* effect (49F/Global) and the +442 is a *measured cottonwood* entry —
   two independent mechanisms, and a fix aimed at one will not touch the other.
5. **49F's −114 is itself a basis artifact, not attrition.** 49F flips `measured` → `frontier_stamp` at 07-22, i.e. its count stops coming from the served-real import and comes from the account-distribution roster frontier with **its own `as_of`**. So −114 is a *source swap*, not 114 lost accounts. **The seam is wider than the PRD states: it is not "Cottonwood arrives," it is "two of three firms change count source on the same date."**

**The discriminating evidence** (what would have falsified me): if the attribution were complete, Σ(per-firm deltas) would equal +408 and the Global-vs-Σfirms residual would stay 0 as it does on the other 406 dates. It is +316 and +92 respectively. The residual sweep across all 407 non-null dates is the control — it finds 07-22 and nothing else, so this is not a systemic reconciliation gap I mis-measured, it is specific to the one frontier-stamp date.

**Net effect on the PRD:** §3.4's conclusion — *"that step is a basis seam, not account growth"* — **stands, and is strengthened.** It is *more* of a basis seam than described: three distinct basis changes land on 07-22, not one.

---

## 4A. DIRECT INPUT TO W-2 — **THE DATA DOES CHANGE THE ANSWER**

Added after the Andrew-direct re-point (~1432Z, relayed 143710Z). COO relayed CTO's framing: options **(a)**
all-or-nothing today, **(b)** sum-what-is-present + carry the basis, **(c)** threshold at N firms — *"he leans
(b) and will rule the same hour your measurement arrives — unless your data shows the missing cells are
concentrated somewhere that changes the answer."*

> **They are concentrated, and it does change the answer. `49financial` is 92.9% of the Global count
> (7,140 of 7,686 on 2026-07-17, the last clean date), and 49F's leg is the absent one on 21 of the 22
> trading-day nulls.** So "sum what is present" is, on almost every hole, "sum the 7%."

I simulated both readings of (b) against the served bytes. **This is a CORRECTNESS-grade test with a pinned
expected value, not an existence check.**

### (b) applied at the MODEL axis — where the code composes today (`:1716-1741`)

Publishing `sum(non-None cells)` on the 40 null dates yields:

| would publish | n dates |
|---|---|
| **0** | **26** |
| 86 / 88 / 94 / 95 | 6 |
| 254 / 255 / 262 / 267 | 8 |

**The producer's own comment at `:1710-1712 @3efc9dc6d` names the historical defect values: *"a sum over
mixed-None dates FABRICATES partial totals (0 / 94 / 255 on exempt dates — Andrew's 'choppy')."*
My simulation reproduces `0` ✓, `94` ✓, and `255` ✓ — all three, exactly.**

**Model-axis (b) is not a new option. It is a bit-for-bit reversion to the defect the current rule was
written to fix, against a true base of ~7,500.** Recommend it be taken off the table on evidence.

### (b) applied at the FIRM axis — the defensible reading, but it needs a guard

Publishing only firms whose legs are **fully** present, on the 22 trading-day nulls:

| outcome | n | assessment |
|---|---|---|
| publishes **0** (INF-only basis; INF's count series is a genuine `measured` 0 until 2026-05-15 — 383 of its 429 dates) | **8** | **Unacceptable** — a drop-to-zero spike, the exact thing `connectNulls` exists to prevent |
| publishes **462–546** (INF-only) against a true base of ~7,500 | **7** | **Unacceptable unlabelled** — a ~93% understatement that *looks like* a Global count. Arguably worse than a null: a null renders as a gap, this renders as a cliff |
| publishes **6,882** (49F-only, 2026-05-21) | 1 | **Genuinely useful** — 91% coverage, real, complete, nameable |
| publishes **988** (INF+COT, 2026-07-21) | 1 | understated, same class as row 2 |
| still `None` (no firm complete) | 5 | unchanged |

> **Naive firm-axis (b) is materially WORSE than today's honest null on 15 of the 22 dates, and clearly
> better on 1.** It becomes correct only with a **coverage qualifier** — publish a partial only when the
> carried basis covers a stated share of the base (the 05-21 case passes at 91%; the INF-only cases fail at
> 7%). That is closer to CTO's option **(c)**, except the threshold that matters is **share of accounts, not
> count of firms** — a 2-of-3-firms threshold would still pass the 7% cases.

**Precedent already in the artifact:** `band_2firm` (24 dates) *is* firm-axis sum-with-carried-basis for
49F+INF — and it is safe precisely because it always carries 49F. That is the existing proof the mechanism
works when the dominant firm is in the basis, and only then.

**On "is the simple edit simple?"** — the honest answer from the data: **no, but it is small.** The
all-or-nothing rule is not what makes the 40 dates null; the firm-level poison at `:1656` is, and 21 of 22
trading-day holes are one firm's import axis, which 49F's own meta says retires *"with the 49F count-axis
decouple."* Relaxing the model-axis rule alone changes nothing about the 40 dates except to fabricate
partials. **The cheap, correct win is the coverage-qualified firm-axis partial; the durable fix is the 49F
count-axis decouple.**

---

## 5. NOTES FOR THE HELD LIMBS (input only — no design, per scope)

**For W-2 (composition law, CTO gate + likely Andrew):**
- The real all-or-nothing is at the **FIRM** axis (`:1656`), not the model axis (`:1719-1721`). A law written against "one missing core model cell" would not have changed a single one of the 40 dates. 05-21 is the case to reason from: 6,788 real 49F accounts discarded.
- **21 of the 22 trading-day nulls** (classes A=14, B=5, E=2) have **49F's leg absent**; the 22nd (05-21, class C) is INF's. So the trading-day hole is almost entirely **one firm's import axis**, and 49F's own meta says it retires *"with the 49F count-axis decouple"* — a mechanism already named elsewhere. Worth knowing before designing a partial-with-named-basis.
- The `exempt_absorbed` label collision (18 fallback-labelled dates; 07-20 mis-branched) matters because **W-4 renders this label.**

**For W-3 (basis coherence) — lines I believe the writer will need, so it inherits my reading:**
- `:1656 @3efc9dc6d` — firm-level poison; the value axis has no equivalent, which is precisely why value and count diverge.
- `:1657-1658` — `acct[-1] = ad_frontier[mkey]`; the frontier stamp, last-axis-position-only. **Source of the +7 and of `frontier_stamp` itself.** (Twins at `:775-776` and `:982-983` — per-firm paths, same pattern; W-3 should check whether all three need to move together.)
- `:1665-1672` + `:1156` — SMA preserve; source of the +85 and a **standing** reason Global ≠ Σfirms.
- `:1716-1741` — the Global composition block.
- Confirms §3.3 on served bytes: `meta.count_basis_note` says count composes **49F+INF only** on interpolated-cottonwood dates while `model_value` includes the cottonwood band; `n_cottonwood_covered` = **47 of 447**.

**For W-6(count-reconcile)** *(explicitly NOT the wave W-6 bell clobber)*: `json/mdpf/aggregate-aua-timeseries.json` is **byte-identical** to the global key — same ETag `55a8b379fb22a9c1ed02db1eef5d2a18`, 254,419 B. It is a duplicate, not a disagreeing artifact; the 7,419/7,830 series lives in `json/portfolios/aum-timeseries.json`. **Two of the three keys in scope are one artifact** — that reduces W-6 to a genuine two-way reconcile plus a retire-or-repoint of the duplicate.

**For W-7:** 18 non-trading spine rows (not 16) — 16 weekend + 2 market holidays; they are on the spine because the cottonwood axis is 447 vs 49F/INF's 429. The 447-vs-429 confusion has already produced two wrong numbers in the closeout brief (§2 above).

---

## 6. REPRODUCIBILITY (AC-6)

```bash
aws s3api get-object --bucket opal-data-portal-v2 \
  --key json/mdpf/global/aggregate-aua-timeseries.json out.json      # + the 3 per-firm keys
python -c "import json,sys; sys.path.insert(0,'.'); \
from lib.trading_calendar import is_trading_day; d=json.load(open('out.json')); \
n=[x for x,v in zip(d['dates'],d['account_count_total']) if v is None]; \
print(len(d['dates']), len(n), sum(1 for x in n if is_trading_day(x)))"
# expect: 447 40 22
```
Residual sweep: for each date with non-null Global total, compare against the sum of all `by_model.account_count` cells across the three per-firm artifacts → **0 on 406, +92 on 2026-07-22.**

## 7. GROUNDING LEDGER (Rule 22 / 22a)

| claim | grade | grounding |
|---|---|---|
| 40 of 447 null; 22 trading days | **MEASURED** | served bytes @ETag `55a8b379…`; resolver `lib/trading_calendar.py` @`0cbb0ad17` |
| all-or-nothing is FIRM-level | **SOURCE-CONFIRMED + EXERCISED** | `:1656 @3efc9dc6d` + the 05-21 cross-section where 49F is present and Global is None |
| +408 = +442 −126 +92 | **MEASURED** | four served artifacts, per-model and per-firm |
| +92 unique to 07-22 | **MEASURED** | sweep over all 407 non-null dates (denominator printed) |
| +85 SMA preserve / +7 frontier stamp | **SOURCE-CONFIRMED** | `:1665-1672`, `:1157-1158`, `:1657-1658`, `:604` @`3efc9dc6d` |
| CTO's 24 = weekday axis; 3-of-12 = spine axis | **MEASURED** | both reproduce exactly under the stated predicate |
| 49F −114 is a source swap not attrition | **SOURCE-CONFIRMED** | class flip `measured`→`frontier_stamp` in served bytes + `49F meta.frontier_count` |
| Model-axis (b) reproduces 0/94/255 | **MEASURED vs PINNED EXPECTED** | simulation on served bytes vs the values named at `:1710-1712 @3efc9dc6d` — a test that could have failed and did not |
| Firm-axis (b) is worse on 15 of 22 | **MEASURED** | simulation on served bytes; INF's zero-run verified as a real `measured` 0 (383 of 429 dates, first non-zero 2026-05-15) |
| *Why* 49F's legacy axis omits those 20 dates | **INFERRED — NOT CLAIMED** | the artifact self-labels them *"UNCHECKED, not clean."* I did not open the upstream import; the 20 dates and the mechanism NAME are measured, the upstream root cause is not. |

**Timestamps:** every S3 timestamp above is explicit-Z via `s3api` (never `aws s3 ls`, never a local-rendered `LastModified`).
