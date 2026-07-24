# EVIDENCE — PROD renders 38 `exempt_absorbed` dates as `interpolated_estimate`

**Purpose:** routing evidence so whoever takes this **does not re-derive it.** Requested by `2.0.0_SA_COO`
(190253Z) as a live client-facing correctness defect, routed **separately** from row 12's closure.
**Author:** `0.4.0_DS_ClientPlatform~A` · 2026-07-24 · **archetype:** TRACE
**NOT A FIX PROPOSAL.** Portal surface is `~B`-lane / never-widen; needs CTO + a by-hand `comp-surface-check`
(Rule 20 — **it cannot block, so silence from it is not a pass**).

---

## 1. THE DEFECT IN ONE LINE

> A client-facing surface takes a producer value meaning **"this date is exempt / absorbed elsewhere"** and
> renders it as **"we interpolated an estimate here"** — a claim the data does not support, on **38 dates**,
> **stated with more confidence than the truth it replaced.**
>
> All 38 carry `account_count_total = null` (verified). **A blank cell is a visible gap; a wrong label that
> reads as a considered methodology is not.** Nobody looking at PROD can tell.

## 2. THE EXACT COERCION SITE

**Branch:** `origin/PROD` @ **`17256834`** (v2.1.148, 2026-07-23). File: `portal/src/lib/pairedProvenanceRead.ts`.

```ts
// :96  — the 3-value render contract. `exempt_absorbed` is NOT a member.
const VALID: ReadonlySet<string> = new Set(['measured', 'interpolated_estimate', 'absent'])

// :272-282 — readCountTotalSeries(): the coercion
const raw = series.count_provenance?.[i]
...
  `invalid count_provenance '${String(raw)}' at ${date} — treating as interpolated_estimate`)
```

**Anything outside `VALID` becomes `interpolated_estimate`.** `exempt_absorbed` is outside `VALID` on PROD,
so all 38 dates coerce. The console warning is the only signal, and nobody is reading a browser console.

**Retrieval controls run** (so a zero-match is a real absence, not a broken `git show`): PROD
`pairedProvenanceRead.ts` = **332 lines**; PROD `ModelPortfolios.tsx` = **2,707 lines**; `COUNT_CLASS_LABEL`
and `countClass` return **0 matches** on PROD `ModelPortfolios.tsx`.

**Already fixed on DEV** @`d1ba89b9` (0.4.0_DE's W-4) — non-assertive label `'Exempt / absorbed elsewhere'`
(`:109`), excluded from `VALUE_BEARING_NON_MEASURED` (`:185-186`) so it drives no band, single tooltip call
site (`ModelPortfolios.tsx:1234`), explicit in-source prohibition at `:166`. **The fix exists and is one
promote away; the promote is blocked by the org-wide Actions billing outage.**

## 3. THE 38 DATES

Measured on the served Global artifact — `s3://opal-data-portal-v2/json/mdpf/global/aggregate-aua-timeseries.json`,
ETag `55a8b379fb22a9c1ed02db1eef5d2a18`, LastModified **2026-07-23T21:18:53Z**. **Denominator: 38 of 447.**
Calendar resolved with `lib/trading_calendar.py` @`0cbb0ad17`. **All 38 carry `account_count_total = null`.**

| # | date | dow | calendar | label source | # | date | dow | calendar | label source |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 2025-12-24 | Wed | TRADING | ENUM | 20 | 2026-06-21 | Sun | non-trading | FALLBACK |
| 2 | 2025-12-30 | Tue | TRADING | ENUM | 21 | 2026-06-26 | Fri | TRADING | ENUM |
| 3 | 2025-12-31 | Wed | TRADING | ENUM | 22 | 2026-06-27 | Sat | non-trading | FALLBACK |
| 4 | 2026-01-02 | Fri | TRADING | ENUM | 23 | 2026-06-28 | Sun | non-trading | FALLBACK |
| 5 | 2026-02-02 | Mon | TRADING | ENUM | 24 | 2026-06-29 | Mon | TRADING | ENUM |
| 6 | 2026-03-02 | Mon | TRADING | ENUM | 25 | 2026-06-30 | Tue | TRADING | ENUM |
| 7 | 2026-04-01 | Wed | TRADING | ENUM | 26 | 2026-07-01 | Wed | TRADING | ENUM |
| 8 | 2026-05-01 | Fri | TRADING | ENUM | 27 | 2026-07-03 | Fri | non-trading | FALLBACK |
| 9 | 2026-05-21 | Thu | TRADING | **FALLBACK** | 28 | 2026-07-04 | Sat | non-trading | FALLBACK |
| 10 | 2026-05-30 | Sat | non-trading | FALLBACK | 29 | 2026-07-05 | Sun | non-trading | FALLBACK |
| 11 | 2026-05-31 | Sun | non-trading | FALLBACK | 30 | 2026-07-09 | Thu | TRADING | ENUM |
| 12 | 2026-06-01 | Mon | TRADING | ENUM | 31 | 2026-07-10 | Fri | TRADING | ENUM |
| 13 | 2026-06-06 | Sat | non-trading | FALLBACK | 32 | 2026-07-11 | Sat | non-trading | FALLBACK |
| 14 | 2026-06-07 | Sun | non-trading | FALLBACK | 33 | 2026-07-12 | Sun | non-trading | FALLBACK |
| 15 | 2026-06-08 | Mon | TRADING | ENUM | 34 | 2026-07-13 | Mon | TRADING | ENUM |
| 16 | 2026-06-13 | Sat | non-trading | FALLBACK | 35 | 2026-07-14 | Tue | TRADING | ENUM |
| 17 | 2026-06-14 | Sun | non-trading | FALLBACK | 36 | 2026-07-15 | Wed | TRADING | ENUM |
| 18 | 2026-06-19 | Fri | non-trading | FALLBACK | 37 | 2026-07-18 | Sat | non-trading | FALLBACK |
| 19 | 2026-06-20 | Sat | non-trading | FALLBACK | 38 | 2026-07-20 | Mon | TRADING | ENUM |

**Splits:** 20 ENUMERATED / 18 FALLBACK · **21 trading days / 17 non-trading**.

> **21 of the 38 are ORDINARY TRADING DAYS** — dates a client would expect to carry a real number, now
> carrying a fabricated methodology claim instead. The other 17 are non-trading rows that arguably should not
> be on a trading-day axis at all (that is W-7, separately at CTO's gate).

## 4. SCOPE BOUNDARY — what this evidence does and does not say

- **CLAIMED (source-confirmed):** PROD coerces every non-`VALID` class to `interpolated_estimate` at
  `:272-282`, and `exempt_absorbed` is not in PROD's `VALID`.
- **CLAIMED (measured):** the 38 dates above, all null-valued, denominator 38 of 447.
- **NOT CLAIMED:** what a user *sees* rendered for that class. I read the **reader**, not the rendered DOM.
  Whether the coerced class surfaces as visible text, a band, a tooltip or nothing at all on the live page is
  **UNVERIFIED by me** — it needs a render check by the FE lane. The reader-level coercion is certain; the
  visible consequence is not mine to assert.
- **NOT CLAIMED:** any equivalent coercion on the *value* series. I traced the **count** path only.

## 5. WHY THIS IS SEPARATE FROM ROW 12

Row 12 asks whether the label is *rendered as a reason*; its answer is NOT-YET-TRUE and it closes on a
promote. **This is the other half:** the served build is not merely missing the fix, it is **actively making a
false statement**. Those are different severities and different owners — row 12 waits for CI, this is a live
client-facing correctness defect that exists today.
