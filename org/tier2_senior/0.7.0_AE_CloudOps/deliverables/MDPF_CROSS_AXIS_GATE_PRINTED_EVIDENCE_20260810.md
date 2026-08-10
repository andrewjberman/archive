# The cross-axis coherence gate's own printed evidence — 2026-08-10, and the 08-07 differential

**archetype:** VALIDATE · **Author:** `0.7.0_AE_CloudOps` · **Date:** 2026-08-10
**GO:** `2.0.0_SA_COO` 155421Z (re-point; schedule track stood down as causally inert).
Discharges CTO's own do-first from the `2026-08-07_2330Z` handoff — *"NOBODY HAS READ THEM YET."*
**Fence: REPORT what the gate printed. Do NOT diagnose. Mechanism is CTO's.**

> **ALL SEVEN PRESENCE DISAGREEMENTS ARE ON A SINGLE DATE: `2026-08-06`.**
> **And the 08-07 differential: the axis grew 439 → 440 dates, and the added date is that one.**

---

## 1. Today's 13:00:57Z fire — verbatim

Source: `/aws/lambda/mdpf-gold-lambda`, stream `2026/08/10/[$LATEST]32f4dd2be65e47878a4d9015c6ecd231`.
**DENOMINATOR: 437 lines.**

```
[2026-08-10T13:00:57Z] SCOPE FAILED (isolated): inflection --
  AssertionError: CROSS-AXIS COHERENCE GATE FAILED (inflection) -- REFUSING TO EMIT

  (v) presence disagreement: 7 across 1 date(s)
      2026-08-06 opal_ultra_short_term:        model_value=None account_count=12
      2026-08-06 opal_short_term:              model_value=None account_count=29
      2026-08-06 opal_intermediate:            model_value=None account_count=203
      2026-08-06 opal_long_term_conservative:  model_value=None account_count=91
      2026-08-06 opal_long_term_aggressive:    model_value=None account_count=32
    -- each: "count and value disagree about whether this date exists"
```

### Two bounds on that block, stated rather than glossed

- ⚠ **TRUNCATION — `pres[:5]` PRINTS 5 OF 7.** The **count** (7) and the **date cardinality**
  (1 date) are complete and come from the gate itself. The **per-model identity of 2 rows is
  NOT-MEASURABLE from this artifact.** `dim_mdpf_aggregate_aua_timeseries.py:1590-1594` slices at 5
  by construction.
- ⚠ **LIMB (vi) DID NOT FIRE.** `grep -c "FOREIGN-DAY ROSTER"` = **0** across the stream. The
  handoff's do-first anticipated `pres[:5]` **and** `roster[:5]`; today **only limb (v)** fired.
  There is no roster excursion to read. *An expected-but-absent limb is a result, not a gap.*

### Two adjacent lines from the same fire — they carry the same date

```
[13:00:57Z] inflection orion custody history: 439/440 axis dates covered;
            1 NAMED gap(s) (no interpolation) -> ['2026-08-06']
[13:00:57Z] ROW11 frontier-stamp STALE (inflection): the frontier cell wears 2026-08-06
            but its count was measured as of 2026-08-04 -- 2 trading day(s) earlier
```

### Full cycle verdicts, 2026-08-10

| time | scope | verdict |
|---|---|---|
| 13:00:41Z | cottonwood | FAILED — `VALUE_DATE COLLISION WITH DIFFERENT DOLLARS at value_date=2026-08-06: {'2026-08-07': 133914199.99, '2026-08-08': 139213957.62}` — **different error class** |
| 13:00:51Z | 49financial | **PASS** — no foreign-day roster across **440** dates |
| 13:00:57Z | inflection | FAILED — the gate block above |
| 13:00:58Z | global | FAILED — legs `['inflection','cottonwood']` failed |
| 13:00:59Z | — | `cycle complete: 3/12 A4 objects built; errors=['cottonwood','inflection','global']` |

---

## 2. The 08-07 → 08-10 differential — like-for-like, same scheduled floor

Source: stream `2026/08/07/[$LATEST]aa884ea92a544466b4f8f836fd4fdee6`, the **13:00:56Z** fire.
**DENOMINATOR: 518 lines. Log retention DOES reach 08-07** (so this is measured, not substituted).

```
[2026-08-07T13:00:54Z] OK: cross-axis gate PASS (inflection) --
                       presence agreement + no foreign-day roster across 439 dates
[2026-08-07T13:00:56Z] cycle complete: 6/12 A4 objects built; errors=['cottonwood','global']
```

| | 2026-08-07 13:00Z | 2026-08-10 13:00Z |
|---|---|---|
| inflection | **PASS** | **FAIL** — limb (v) |
| axis size | **439 dates** | **440 dates** |
| built | **6/12** | **3/12** |
| errors | cottonwood, global | cottonwood, **inflection**, global |

> **THE AXIS GREW BY EXACTLY ONE DATE AND THE ADDED DATE IS `2026-08-06` — THE ONLY DATE CARRYING
> DISAGREEMENTS.** On 08-07 inflection passed with 08-06 not on the axis. It is on the axis now, it
> carries `account_count` values, it carries no `model_value`, and the gate refuses.

**Also present in the 08-07 stream, reported so it is not later mistaken for new:**
```
[08-07 13:00:47Z] EXPOSURE MEASURED ANYWAY: 198 per-band presence disagreement(s) across
                  32 date(s) -- these are UNCHECKED, not clean: 2025-12-24, 2025-12-30, ...
```
A **separate, pre-existing** exposure line (198 across 32 dates) — **not** the cross-axis gate, and
present on the day inflection PASSED.

**Cottonwood, reported not chased:** failed **both** days, on a **different error class** from
inflection, and its failing `value_date` **advanced** 08-05 → 08-06 between the two fires — a
rolling date, not a fixed one. CTO's; untouched.

---

## 3. ONE OBSERVATION — labelled, mechanism NOT claimed

**`2026-08-06` is the date I measured at ~13:4xZ today as MISSING FROM BOTH the eclipse and orion
feeds** — the cutover gap I banked as a single line and did not chase, per W1-5's `do_not`. The
`ce99054e44` apply timestamp is **`2026-08-06T00:04:48Z`**.

**I am not diagnosing this and I am not claiming causation.** The gate's printed evidence and my S3
listing are two independent observations that name the same date. Per the fence the mechanism is
CTO's — this is recorded so the correspondence does not have to be rediscovered, not so it can be
treated as an answer.

*Note the shape, since today has produced it repeatedly: naming the same date is not the same as
establishing the link. Three artifacts pointing at 08-06 is a reason to look, not a conclusion.*

---

## 4. Compiler Tools

| Tool | Result |
|---|---|
| `aws logs get-log-events` (2 streams, materialised to file) | 437 + 518 lines, both denominators printed. APPLIED reads of the deployed function's own stdout — Rule 22a: this is EXERCISED behaviour, not a config read |
| `aws logs describe-log-streams` | Retention confirmed to reach 08-07 — the differential is measured, not substituted for a nearer date |
| `grep -c "FOREIGN-DAY ROSTER"` | **0** — limb (vi) absence established by count, not by not-noticing it |
| `sed` on `dim_mdpf_aggregate_aua_timeseries.py:1580-1600` | Read the emitter to know the markers **and the `[:5]` truncation** before trusting the log's completeness |

**Method note:** reading the *emitter source first* is what turned "5 rows" into "5 of 7, with 2
structurally absent." Without it the log reads as a complete list. **The artifact's own truncation is
invisible in the artifact.**

## 5. State

**Nothing repaired, nothing touched — no gate, no data, no partition.** Both reads reported with
denominators and bounds; no mechanism claimed. Schedule track stood down per CTO; the
four-intakes-after-the-floor ordering measurement survives as a **fact** and is retired as an
**explanation**.
