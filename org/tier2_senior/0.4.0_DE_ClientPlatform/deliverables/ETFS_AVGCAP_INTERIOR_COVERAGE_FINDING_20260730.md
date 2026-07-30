# ETFS_AVGCAP -- INTERIOR COVERAGE FINDING (analysis only, no remedy proposed)

**Author:** `0.4.0_DE_ClientPlatform` · **Date:** 2026-07-30 · **archetype:** DIAGNOSE
**Commissioned by:** `2.0.0_SA_COO` 20260730T070606Z -- *"the evidence base Andrew needs for question (b)"*
**Scope bound (COO, verbatim):** *"Do not propose a remedy; (b) is Andrew's and the remedy shape is not
an engineering call."* This document contains **no recommendation**. It establishes what is true.

**Status of the related change:** the per-partner carried-forward disclosure in `render_month_end.py` is
**READY BUT UNLANDED**, held pending Andrew. Backup patch: `carried_disclosure_20260730.patch` @`75c66b8733`.
This record is independent of that hold -- it is a record, not a renderer change.

---

## 1. THE FINDING IN ONE LINE

**`partial` detects a LATE START and nothing else.** It cannot detect interior gaps, and it cannot detect
a dead tail -- because the quantity it compares against the window is produced by carry-forward itself,
and therefore equals the window **by construction**. The discriminating evidence is already emitted in
the same object, one field away, and the flag does not read it.

Live proof, production artifact, `s3://opal-data-etfs/monthly/2026-06.json`:

```
49financial  DIVZ   written_days = 17     calendar_days_covered = 30     partial = FALSE
                    ^ real data              ^ what `partial` compares       ^ says "complete"
```

**17 days of real data in a 30-day billing window, flagged NOT PARTIAL.** Thirteen carried days, on the
artifact family that decides what a partner is paid.

---

## 2. MECHANISM -- SOURCE-CONFIRMED

`data/etfs/scripts/gold/avgcap_monthly_average.py:187-205` @ HEAD `75c66b8733`:

```python
carried: list[float] = []
last_val: float | None = None
for cd in calendar_days:                 # EVERY calendar day in the window
    if cd in day_vals:
        last_val = day_vals[cd]          # a real day updates the value
    if cd >= first_written and last_val is not None:
        carried.append(last_val)         # ...but EVERY day appends, real or carried
...
covered_days = len(carried)              # == calendar days from first_written to window_end
partial = covered_days < n_window_days
```

`carried` gains exactly one entry per calendar day from `first_written` onward, **whether or not that day
had data**. So `covered_days` is a function of `first_written` alone. The comparison therefore reduces to:

> `partial == (first_written > window_start)`

- 8 missing interior days, first day present -> `covered_days == n_window_days` -> **`partial = False`**
- last 10 days dead, first day present -> `covered_days == n_window_days` -> **`partial = False`**
- only the first day missing, all others present -> `covered_days < n_window_days` -> **`partial = True`**

**The flag is at its most confident exactly where coverage is worst**, provided the gap is anywhere other
than the leading edge. This is the same anti-correlation class as the orphan-watcher REACHABLE verdict:
the mechanism that is supposed to detect the fault is satisfied *by* the fault's own repair mechanism.

### 2a. Confirmed on every partner in the artifact, both flag levels

| partner (June) | window | `written_days` (DIVZ) | `calendar_days_covered` | etf `partial` | window `partial` |
|---|---|---|---|---|---|
| 49financial | 06-01..06-30 (30) | **17** | 30 | **False** | **False** |
| inflection | 06-01..06-30 (30) | 24 | 30 | False | False |
| cottonwood | 06-08..06-30 (23) | **10** | 23 | **False** | True |

`calendar_days_covered == window_calendar_days` in **all three** cases -- it cannot be otherwise once
`first_written == window_start`.

**Cottonwood is the instructive one.** Its window-level `partial=True` looks like the flag working. It is
not: `window_partial` is `(window_start > month_start) or (window_end < month_end) or any(etf partial)`
(`:219-220`), and cottonwood trips the **first** disjunct -- its onboarding clock starts the window at
06-08. Its actual coverage, 10 written days in 23, contributed nothing to that verdict. **A True here is
not evidence the flag can see coverage; it is a different fact wearing the same field name.**

### 2b. The discriminating evidence is already in the artifact

`written_days` is emitted at `:211`, four lines above `partial` at `:215`, in the same dict, alongside
`window_calendar_days` at `:213`. **The pair that exposes this (17 vs 30) is already written to
production on every run.** Nothing consumes it as a coverage signal.

*Stated as a property of the current artifact, not as a proposed fix. What to do about it is (b).*

---

## 3. THE CENSUS -- TWO PREDICATES, BOTH CORRECT, DELIBERATELY NOT MERGED

COO: *"your weekday count and ~A's trading-day count differ slightly and both are right -- say which is
which and why, rather than reconciling them into one number."*

**Predicate A (`0.4.0_DE_ClientPlatform`) -- CALENDAR-WEEKDAY.** Mon-Fri, no holiday calendar. Denominator
= weekdays in July. Chosen because the **billing window is calendar-based**, so it counts what the CSV
actually carries.

**Predicate B (`0.7.0_AE_CloudOps~A`) -- TRADING-DAY.** `lib/trading_calendar.is_trading_day` over
2026-07-01..07-29, excluding 07-30 as not-yet-due. Denominator = 20 trading days. Chosen because it
measures **producer health** -- did the feed deliver when a delivery was owed.

Both, as of 2026-07-30:

| partner | A: real keys | A: missing weekdays | B: trading-day coverage | B: missing |
|---|---|---|---|---|
| 49financial | 19 | 3 (07-03, 07-29, 07-30) | **19/20 (95%)** | 07-29 |
| inflection | 15 | **10** (07-01, 07-03, 07-13, 07-14, 07-15, 07-20, 07-21, 07-22, 07-23, 07-30) | **12/20 (60%)** | 07-01, 07-13/14/15, 07-20/21/22/23 |
| cottonwood | 17 | 5 (07-03, 07-20, 07-28, 07-29, 07-30) | **17/20 (85%)** | 07-20, 07-28, 07-29 |

**They reconcile exactly, and the difference is informative rather than noise.** A counts raw in-month
date keys; B counts trading days. Inflection's A-count of 15 = 12 trading days + **3 weekend keys** --
inflection emits some weekend slices, the other two emit none. Neither number is wrong; they answer
different questions, and merging them would destroy that.

### 3a. `07-03` is the control that makes the rest legible

**07-03 is missing for all three partners.** It is the observed July 4 holiday (2026-07-04 is a Saturday,
observed Friday 07-03). It is *expected* absence.

Its value here is as a **positive control on the census itself**: a shared, explainable absence confirms
the instrument sees real gaps rather than manufacturing them, which is what licenses reading the
**unshared** absences as anomalous. Without it, inflection's nine other missing weekdays would be a bare
count with no baseline.

### 3b. The two contiguous runs

Inflection's gaps are not scattered:

```
2026-07-13  Mon  |
2026-07-14  Tue  |  RUN 1 -- 3 consecutive trading days
2026-07-15  Wed  |

2026-07-20  Mon  |
2026-07-21  Tue  |  RUN 2 -- 4 consecutive trading days
2026-07-22  Wed  |
2026-07-23  Thu  |
```

Seven of the nine anomalous days fall in two blocks. A scattered miss-rate reads as flaky delivery; two
multi-day blocks read as **outages**, which is a different producer question. Recorded as an observation
-- the cause is not established here and I did not investigate it.

---

## 4. MAGNITUDE ON THE AUG-1 FIRE (interval, not point estimate)

On 2026-08-01 the complete-month branch fixes `cap = 2026-07-31` and `window = 31` for **every** partner
(`render_month_end._month_cap:164-175`), so `carried = 31 - real_in_month_keys`.

```
July 2026: 31 calendar days = 22 trading days + 8 weekend days + 1 holiday (07-03)
FLOOR: a partner landing EVERY trading day still shows 9 of 31 carried.
       That floor is the full-calendar-month billing convention working exactly as ruled -- NOT a defect.

partner       real-now  outstanding  carried @ Sat   as % of the billing window
49financial      19          2         10 - 12          32% - 39%
inflection       15          2         14 - 16          45% - 52%
cottonwood       17          2         12 - 14          39% - 45%
```

Low end assumes every outstanding trading day lands before the 14:00Z fire; high end assumes none does.
**Backfill of already-missed interior days would push below the low end -- it is not a hard bound.**

> **Inflection is projected at 45-52% of its billing window carried.** Against a 29% floor
> (9/31), that is roughly 5-7 excess carried days beyond convention. **~A's flag stands: this figure has
> never been visible on a partner-facing document, and it should reach COO/~C before Saturday rather than
> in the email.**

**Ranking inverts by axis.** On the TAIL, inflection is the cleanest partner (T+0). On INTERIOR coverage
it is the worst of the three (60% vs 95% / 85%). ~A corrected their own "12/12, HIGH CONFIDENCE" on
exactly this point: *"a rate over date-keys that EXIST, not over dates EXPECTED"* -- the denominator of
the retrieval, not of the claim. **Tail-cleanliness does not imply interior cleanliness**, and no single
number orders these partners.

---

## 5. WHY THIS IS THE SAME DEFECT AS THE CARRIED TAIL, ONE AXIS OVER

The recorded ETFS_AVGCAP defect is the **carried tail** -- a dead tail looking identical to a healthy
month. Its two guards are recorded as structurally blind: AC6 reports the OLDEST input, and `partial`
keys off calendar coverage.

This finding is the **same mechanism on the interior**. Section 2 shows why one sentence covers both:
`partial == (first_written > window_start)`. A dead tail and a hollow interior are both invisible to it
for the identical reason -- carry-forward supplies the coverage the test measures.

So this is not a second defect. **It is the same defect, and the tail was only the first place it was
looked for.**

---

## 6. WHAT IS ESTABLISHED vs WHAT IS NOT

**ESTABLISHED (source- or artifact-grounded):**
- `partial == (first_written > window_start)` -- source, `avgcap_monthly_average.py:187-205` @`75c66b8733`.
- 49F June: 17 written days, 30 covered, `partial=False` -- production artifact `monthly/2026-06.json`.
- Cottonwood's June `window.partial=True` comes from the onboarding-clock disjunct (`:219`), not coverage.
- The July per-partner census, on two independently-derived predicates that reconcile exactly.
- `written_days` and `window_calendar_days` are both already emitted, adjacent to the flag.

**NOT ESTABLISHED -- do not let these travel as findings:**
- **The CAUSE of inflection's two runs.** Not investigated. Outage, vendor gap, and producer defect are
  all consistent with what I measured. **Unknown, and it should stay labelled unknown.**
- **Dollar impact.** Not computed. Carried days move the average, but by how much depends on the values
  carried, which I did not evaluate.
- **Whether any other consumer reads `partial`.** I did not census consumers.
- **Whether June's 49F 17/30 is typical.** Two months looked at; `monthly/2026-07.json` does not yet exist
  (`NoSuchKey`, expected -- the month is in progress). **n=1 month for the artifact-level proof.**

**Instruments used:** `comp-grep` (12 matches / 1 file, scanned 7 of 7 in scope), `comp-glob` (11 files),
native `Read` on source, direct `GetObject` on the artifact. Zero S3 writes; all S3 access read-only.

---

## 7. OPEN AT ANDREW (question (b)) -- stated, not answered

> *Is a ~40%-carried month a valid rebate basis at all, disclosed or not?*

This record deliberately stops here. The engineering facts are Sections 1-6. Whether a billing convention
that is **working exactly as ruled** produces an acceptable basis at this coverage level is a business
judgment about what the number is *for*, and no measurement settles it.

One factual note bearing on it, offered without a recommendation: the full-calendar-month convention and
the carry-forward rule were both ratified when the question on the table was **weekends and holidays** --
a 9-of-31 floor. Whether they were intended to extend to a 45-52% carried month is a question about the
scope of the original ruling, not about the code, which is implementing that ruling faithfully.
