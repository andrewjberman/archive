# A5 AMENDED SPLIT — PRE-REGISTRATION (A5a / A5b), 2026-08-26

**Author:** `0.4.0_DS_ClientPlatform~T` (the A9 grader) · **Requested by:** `1.0.0_SA_CTO` 72807
**Status:** PRE-REGISTRATION. Written BEFORE the next grade and before the DIVZ re-cut exists,
so a later pass is a prediction met and not a number tuned to. **Not a gate, not a ruling.**
**Every figure below is MEASURED off the 2026-08-26 x 2026-08-25 vintage, not assumed** —
`1.0.0_SA_CTO` 72807 asked for exactly that ("to be CONFIRMED by measurement not assumed").

---

## 1. THE RULING BEING PRE-REGISTERED

Andrew-direct 17:42/17:45Z, recorded `@9261c99991`: the `DIVZ SMA` sleeve in `Anna *9237` is an
**Opal SMA** and buckets to **SMAs (L0) → DIVZ (L1)** — *not* to `Client - Opal Supervised`.
The supervised-account bucketing is now **three-way and complete on his words**:

```
Opal Models -> Models (Primary / Custom)
Opal SMAs   -> SMAs (by strategy)
remainder   -> Client - Opal Supervised
```

His attribution BASIS is unchanged and was confirmed by his own account-level look
(*"you have the correct approach... your estimate of 2.87m checks out"*). A1–A4 / A6–A8 are untouched.

---

## 2. ⛔ THE EXPECTED VALUE IN 72807 IS RIGHT AT ONE GRAIN AND WRONG AT THE OTHER

72807 states `Client - Opal Supervised ~= $1,476,313.07 (the unallocated-weight portion)`. That is
derived as `$2,869,379.04 − $1,393,065.98`, and **`$2,869,379.04` is the TWO-ACCOUNT non-Opal-parent
subset, not the whole segment.** It therefore excludes a third account's $780,381.91 of sleeve
dollars, which under his own *"remainder → Client - Opal Supervised"* clause belong in the segment.

**This is the THIRD time today this one figure has travelled with the wrong denominator** — first as
the struck $38.1M, then as "$2,869,379.04 across ALL 129 dropped accounts", now here. The number is
right each time; the population attached to it is not. **So both grains are pre-registered below and
neither is presented alone.**

---

## 3. MEASURED COMPOSITION — the whole segment, per account, per leaf

Vintage: assignment `2026-08-26` × value `2026-08-25`. Population: accounts reaching ≥1 Opal **Model**.

| account | parent | parent_is_opal | leaf | $ | routes to |
|---|---|---|---|---|---|
| `z0926705231` | `Anna *9237` | False | DIVZ SMA (w 0.0700) | **1,393,065.98** | **SMAs → DIVZ** *(new)* |
| | | | (unallocated, w 0.0300) | **597,028.28** | Client - Opal Supervised |
| `z0926819471` | ` Anna *9238` | False | (unallocated, w 0.0330) | **879,284.79** | Client - Opal Supervised |
| `z0926768741` | `Blended Opal / Satellite 50` | True | Sleeve - Equity (w 0.3750) | **390,190.96** | Client - Opal Supervised |
| | | | Sleeve - Tax-Free Bond (w 0.3600) | **374,583.32** | Client - Opal Supervised |
| | | | Sleeve - Core Money Market (w 0.0150) | **15,607.64** | Client - Opal Supervised |
| | | | (unallocated, w 0.0000) | 0.00 | — |

Segment total is **unchanged at $3,649,760.96** — this ruling MOVES money between two named buckets,
it does not create or destroy any. That invariant is itself a check arm.

---

## 4. THE PRE-REGISTERED VALUES — BOTH GRAINS, STATED TOGETHER

### GRAIN 1 — FULL SEGMENT (every account containing Opal Models). **This is what the artifact emits.**

| id | criterion | expected |
|---|---|---|
| **A5a** | `Client - Opal Supervised` | **$2,256,694.98** |
| **A5b** | SMAs → DIVZ gains | **$1,393,065.98** |
| **A5-sum** | A5a + A5b == prior segment total | **$3,649,760.96** (unchanged) |

A5a decomposes as sleeve **$780,381.91** + unallocated **$1,476,313.07** = **$2,256,694.98**.

### GRAIN 2 — NON-OPAL-PARENT SUBSET (the 2 Anna accounts; the grain 72807's figure is on)

| id | criterion | expected |
|---|---|---|
| A5a′ | `Client - Opal Supervised`, 2-account subset | **$1,476,313.07** — matches 72807 exactly |
| A5b′ | SMAs → DIVZ, 2-account subset | **$1,393,065.98** |
| sum | | **$2,869,379.05** (the corrected `$2,869,379.04`, 1c float) |

**72807's expected value is CONFIRMED at grain 2 and must not be read at grain 1.**

---

## 5. ⛔ ONE THING I AM NOT DECIDING, BECAUSE DECIDING IT WOULD BE MINTING

Account `z0926768741` carries `Sleeve - Equity`, `Sleeve - Tax-Free Bond`, `Sleeve - Core Money
Market`. **I route all three to `Client - Opal Supervised` as remainder**, because they are not on the
ruled SMA enumeration (`Tax · Muni · DIVZ · PFOE`) *by name*.

**OPEN QUESTION for `1.0.0_SA_CTO` / Andrew, surfaced not answered:** is `Sleeve - Tax-Free Bond`
the SMA `Tax` (or `Muni`) under a different vendor label? The taxonomy calls the SMA list an **OPEN
enumeration** (*"so far, maybe others will eventually be added"*), so a name that is absent today is
not evidence of non-membership. Mapping it on resemblance would be exactly the predicate-minting
72604 forbids, and it moves **$374,583.32** across an L0 boundary on a client-facing surface.
**Whichever way it is ruled, the DIVZ limb above is unaffected.**

---

## 6. WHAT WOULD FALSIFY THIS

- Segment total moving off `$3,649,760.96` → money created/destroyed by a routing change; refuse.
- `A5a + A5b != ` prior total → the split is not a partition.
- The DIVZ leg appearing in BOTH buckets → double-count.
- `itemisation_breaks > 0` on the emitted artifact → the parts stopped summing per account.

---

## 7. SCOPE

This document pre-registers values. It does not sequence the work — that fork ((i) fold a second
re-cut into the same pin vs (ii) apply as-is and amend before 13:30Z) is `2.0.0_SA_COO`'s, and an
apply already in flight FINISHES first (NEVER#6). The SERVE decision remains Andrew's.
