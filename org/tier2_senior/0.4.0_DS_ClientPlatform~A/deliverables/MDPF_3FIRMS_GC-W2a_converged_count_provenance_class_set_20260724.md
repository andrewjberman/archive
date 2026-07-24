# CONVERGED `count_provenance` CLASS SET — joint DS~A / DE

**Joint precondition on W-4** (CTO: *"DE and DS~A must converge on the class set BEFORE W-4 renders it, or we
will ship a chart that faithfully displays a mislabel"*).
**Parties:** `0.4.0_DS_ClientPlatform~A` (producer/source axis) + `0.4.0_DE_ClientPlatform` (wire/render axis).
**Exchange:** DS~A 145852Z → DE 150215Z. **Both parties cite THIS set.**
**Measured on:** `s3://opal-data-portal-v2` served bytes, 2026-07-24. Global ETag `55a8b379fb22a9c1ed02db1eef5d2a18`
@**2026-07-23T21:18:53Z**. Source axis @`3efc9dc6d`.

> **Convergence method (not "whoever states a set first"):** each party measured independently and then
> checked the other's numbers against their own bytes. **DE's four-key cross-tab reproduced exactly on DS~A's
> artifacts, control included.** The one open question and the one crux were each resolved by measurement,
> not by concession — and on the crux both parties' hypotheses FAILED, which is recorded as a bounded negative
> rather than a proof.

---

## 1. THE CLASS VOCABULARY IS PER-PATH — the apparent 5-vs-6 disagreement was never a disagreement

DE measured 6 classes over **four** keys; DS~A measured 5 over the **Global** key alone. DE's six is the
**union**. `source_absent` is **per-firm only** — the Global composition block never emits it.
Independently reproduced by both parties:

| served key | n dates | class distribution |
|---|---|---|
| `json/mdpf/global/…` | 447 | measured 382 · exempt_absorbed 38 · band_2firm 24 · lag_window 2 · frontier_stamp 1 |
| `json/mdpf/49financial/…` | 429 | measured 407 · exempt_absorbed 20 · lag_window 1 · frontier_stamp 1 |
| `json/mdpf/inflection/…` | 429 | measured 423 · source_absent 6 |
| `json/mdpf/cottonwood/…` | 447 | source_absent 445 · measured 2 |

**Consequence flagged for W-2/W-3 (DE's observation, DS~A concurs):** the Global and per-firm composition
paths have **DISJOINT class vocabularies** — Global emits no `source_absent`; per-firm emits no
`band_2firm`/`exempt_absorbed`. And **cottonwood is `source_absent` on 445 of 447** — a firm that is almost
entirely "no source" on the count axis while rendering in the same chart.

---

## 2. THE BINDING FINDING — `exempt_absorbed` carries TWO provenances under ONE label

Producer branch order, `:1722-1731 @3efc9dc6d`:

| served label | n | how the date reached it | grade |
|---|---|---|---|
| `exempt_absorbed` | **20** | **ENUMERATED** — date is in `GLOBAL_CROSS_AXIS_EXEMPT_DATES` (`:1723`, set at `:1158-1164`) | a declared decision |
| `exempt_absorbed` | **18** | **FALLBACK** — the `else` at `:1729-1731`, whose own comment says such a date *"would be a cross-axis violation the gate refuses upstream"* | a default |
| `lag_window` | 2 | DERIVED from `count_coverage_end` (`:1725`) | principled |
| `frontier_stamp` | 1 | DERIVED from `count_coverage_end` (`:1737`) | principled |
| `band_2firm` | 24 | DERIVED from `cot_covered` (`:1739`) | principled |
| `measured` | 382 | **FALLBACK** default (`:1741`) | neutral default, not an assertion |

The 18 fallback dates are **not** violations: 17 are non-trading spine rows, 1 (`2026-05-21`) is an INF
model-partition absence.

### 2.1 THE CRUX — NO READ-TIME DISCRIMINATOR EXISTS. Two independent searches, both failed.

**DS~A** (source axis): the enumerated and fallback branches write the **identical string**; no companion
field is emitted.
**DE** (wire axis): searched all six top-level series, all 17 `meta` keys including every nested list, and
tested a derived predicate. **DE formed a hypothesis and reported it REFUTED rather than dropping it:**

- *Hypothesis:* fallback dates are non-trading rows → the FE's existing `isTradingDay()` is a free
  discriminator, dissolving the finding with zero producer change.
- *Refuted:* the 38 split **15 weekend / 23 weekday**, matching neither 18 nor 20.
- *Control (that the signal is not merely weak):* **0 of 382** `measured` dates are weekends — weekend-ness
  IS a real signal in this artifact, just not this one.
- `meta.trading_day_calendar` is the **string** `"NYSE/hardcoded-fallback-2024-2026"`, not an enumerable set.
- Closest meta lists: `honest_none.total_none_dates` (24, 23 intersect), `model_absent_dates` (6, all
  intersect). Neither is 18 or 20; both describe null-ness, not exemption provenance.

**DS~A refinement — the sharper form of DE's test also fails, which STRENGTHENS the conclusion.** DE tested
*weekend*; the stronger predicate is *non-trading* (NYSE, `lib/trading_calendar.py` @`0cbb0ad17`), which
catches the two weekday closures 06-19 and 07-03. That gives **17 non-trading / 21 trading** — it separates
**17 of the 18** fallback dates correctly, and then **misclassifies `2026-05-21`**, a trading day in the
fallback bucket. **A discriminator that is right 37 of 38 times still ships a confident false statement on one
date**, and it would fail silently on exactly the date whose cause (INF model-partition absence) is most
unlike the others.

> **JOINT VERDICT — both parties, independently, by different routes:**
> **No read-time signal separates an ENUMERATED exemption from a FALLBACK default.**
> This is a **bounded negative with its search space named** (six series, 17 meta keys + nested lists, two
> derived calendar predicates, two independent readers) — **not a proof of absence.**
> **Therefore the label CANNOT carry a decision claim.** Either the producer splits it, or nobody renders it
> as one.

---

## 3. THE AGREED SET — what W-4 may and may not assert

| class | render may assert | binding constraint |
|---|---|---|
| `band_2firm` | ✅ a named 2-firm basis | derives from one named condition |
| `lag_window` | ✅ past declared coverage end | derives from one named condition |
| `frontier_stamp` | ✅ roster-stamped, own `as_of` | derives from one named condition |
| `measured` | ⚠️ **neutral only** | it is the `else` default (`:1741`); absence-of-a-basis-note is the honest rendering, **not** a positive completeness badge |
| `exempt_absorbed` | ❌ **must NOT assert a declared exemption** | 18 of 38 were never declared |
| `source_absent` | ✅ per-firm only | never appears on the Global key |

**DE's landed render treatment** (working tree, per DE 150215Z): the reader now carries the producer's raw
class string per point instead of collapsing five classes into one `interpolated_estimate`; the
`exempt_absorbed` label renders as **"Exempt / absorbed elsewhere"** — deliberately *not* "declared
exemption" — and the **banded visual is driven only by value-bearing classes** (`band_2firm`,
`frontier_stamp`), so `exempt_absorbed`'s unreliability cannot propagate into the band (its value is null on
all 38). **Both parties record this as routing around the defect, not fixing it. The fix is producer-side.**

## 4. `2026-07-20` — RESOLVED AS TO RELIABILITY, ATTRIBUTED AS DS~A's SOURCE READ

| date | enumerated? | past `count_coverage_end` (2026-07-18)? | served label |
|---|---|---|---|
| 2026-07-20 | **TRUE** | **TRUE** | `exempt_absorbed` |
| 2026-07-21 | FALSE | TRUE | `lag_window` |

Two adjacent dates, **same operative mechanism**, different served labels — purely because the enumerated
branch is tested first (`:1723` before `:1725`) and 07-20 also sits on the legacy shelf.

- **AGREED by both, on measurement:** 07-20's served label is **unreliable**.
- **DS~A's reading, explicitly NOT co-signed by DE:** its operative cause is the **lag window**, and
  `exempt_absorbed` is a branch-order artifact. This rests on the source read of `:1722-1741 @3efc9dc6d`,
  which DE has not independently verified. **DE states no contradicting wire evidence and does not contest
  it; it is cited as DS~A's.** Recorded this way deliberately — DE declining to agree quickly is the
  convergence working, not a gap.

## 5. WHAT THIS GATES

W-4 may render §3 as written **now**. The producer-side split of `exempt_absorbed` into enumerated-vs-fallback
is **input to W-2**, not a W-4 blocker — DE's treatment is safe in the interim because it makes no decision
claim on that class.
