# AC11 -- the FIRM-GENERIC guard, specced against Cottonwood's REAL feeder shape

**Author:** 0.4.0_DS_ClientPlatform
**Date:** 2026-07-13
**archetype:** IMPLEMENT (**spec only -- NO CODE, NO RUN**)
**For:** 1.0.0_SA_CTO~B (PRD) -- **and CTO, who has ORDERED that the guard precede Cottonwood.**
**Scope:** Andrew-direct: **canonical storage + ROBUST INGESTION, per figure, at its granularity.** This is the
ingestion half. **No sums. No magnitudes. No combined totals.**

---

## 0. THE SPEC CHANGED SHAPE WHEN I GROUNDED IT -- **"RPS-ONLY FIRM" IS THE WRONG CLASS**

I specced AC11 as *"any firm in the declared partner set that yields no held value must RAISE."* **The firm axis is
not the real axis.** Grounding Cottonwood produced the sharper one:

> # **THE QUESTION IS NOT "DOES THE FIRM HAVE A FALLBACK." IT IS: *WHEN A MEASURED SOURCE IS ABSENT, WHERE DO ITS DOLLARS GO?***

**Three behaviours exist in this estate TODAY. They are not equally bad, and only one is catastrophic:**

| # | behaviour | where | what a reader sees |
|---|---|---|---|
| **1** | **HONEST ABSENCE** -- no row | emitter `build_ownership_rows:680-682` (`if key is None: continue`) | **a gap** -- *safe from relabelling, but **SILENT** (see §3)* |
| **2** | **FALLBACK TO INTENT** -- `target_weight` estimate substitutes for measurement | mdpf `build_etf_decomposition:433-441` | **a number that LOOKS measured and is INFERRED** |
| **3** | 🔴 **ABSORBED INTO A COMPLEMENT** -- `residual = total - sum(parts)` | mdpf `:452` | **THE DOLLARS RELABELLED AS SOMETHING ELSE** -- 49F's ~$528mm became *"owned by the public"* |

## 1. 🎯 **OUR OWN CODEBASE ALREADY STATES THE FIX -- IN THE ADJACENT MODULE**

`opal-assets-daily-emitter/lambda_function.py:611-613 @ bf7269a1e`:

> ```
> # a target weight is INTENT, not an OBSERVATION. When the measured source is
> # absent we emit an honest partial/missing -- never a fallback to intent.
> ```

> ## **THAT IS THE $528mm DEFECT, NAMED, CORRECTLY, IN OUR OWN ESTATE -- IN A FILE THAT DOES THE RIGHT THING, ADJACENT TO A FILE THAT DOES THE OPPOSITE.**
> **The emitter's G4 fold hits an absent source and `continue`s. mdpf's decomposition hits an absent source, falls
> back to INTENT, and -- when no intent exists -- lets the firm VANISH into the residual.** **Same estate. Same
> quantity. Opposite behaviour. The principle was written down and implemented in ONE of them.**
> *Instance #8 of tonight's class, and the most damning: **the fix did not need to be invented. It needed to be
> READ.***

## 2. THE MECHANICAL DETECTOR -- **FIND THE CLASS WITHOUT KNOWING THE FIRMS**

**Behaviour #3 is defined by ONE structural property: A CONSERVATION COMPLEMENT.**

> ### **ANY EXPRESSION OF THE FORM `remainder = total - sum(attributed_parts)`, WHERE `parts` COMES FROM A SOURCE THAT CAN BE ABSENT, WILL SILENTLY ABSORB A MISSING PART INTO THE REMAINDER.**
> **THE LANDMINE IS NOT THE FIRM. IT IS THAT THE MISSING VALUE *HAS SOMEWHERE TO GO*.**

**This is the AC11 scan, and it is firm-agnostic, pipeline-agnostic, and mechanical:**
```
find every  X = TOTAL - SUM(PARTS)   (residual / remainder / "other" / "public" / "unattributed")
  -> for each, enumerate the DECLARED contributors to PARTS
  -> assert: a DECLARED contributor yielding NO MEASURED VALUE *RAISES*.
             THE COMPLEMENT MUST NEVER ABSORB IT.
```
**Known instance:** `mdpf_aggregate_aua.py:452` (`residual = total - held_sum`) -> `public_residual`.
**I have NOT swept the estate for others. That sweep is the natural next task and I am not claiming it is done.**

## 3. 🔴 AND BEHAVIOUR #1 IS SAFE BUT **NOT SUFFICIENT** -- IT IS *HONEST* AND *SILENT*

`build_ownership_rows` emits **no row** for an absent partner. **It never lies. But nobody is told.**

**Contrast the SAME FILE's base rows (`build_rows`)**, which emit an explicit row carrying `vintage_state=missing`,
`staleness=99`. **The ownership fold has no equivalent: a declared partner that never lands produces SILENCE, and
silence is only visible to a reader who is already counting the rows they expected.**

> ### **AN ABSENCE THAT EMITS NOTHING IS HONEST TO THE WRITER AND INVISIBLE TO THE READER.**
> **This is AC17's principle exactly** (*a disclosure carries its own IDENTITY + STATE*): **the fix is not to
> fabricate a value -- it is to emit a ROW THAT SAYS "cottonwood: missing".**

**=> AC11 REQUIREMENT (b): a DECLARED contributor that yields no measured value emits an EXPLICIT `missing` ROW --
never silence, never a zero, never an estimate.**

---

## 4. COTTONWOOD -- **GROUNDED, AND AC14 IS NO LONGER AN INFERENCE**

| channel | Cottonwood today | consequence |
|---|---|---|
| **emitter G4 fold** (`ETFS_CANON`) | **LIVE + FRESH** -- `s3://opal-data-etfs/daily/cottonwood/`, **21 partitions, latest 2026-07-10** | behaviour **#1** -- safe from relabelling, but **silent** if it ever stops |
| **mdpf `etf_decomposition`** | ⚠️ **ABSENT ENTIRELY** -- `cottonwood` appears **0 times in `data/mdpf`** (40 files scanned) | **not yet exposed** |

**AND ITS SOURCE IS POSITIONS-BASED** -- `opal-data-cot/gold/positions_cube/` (A_03 cube, nightly). **It has NO
`model_composition` / `target_weight` rows anywhere.**

> # **=> ON THE DAY COTTONWOOD IS ONBOARDED TO mdpf, IT ENTERS `build_etf_decomposition` WITH NO INTENT-FALLBACK -- AND BECOMES LANDMINE #2 *BY CONSTRUCTION*.**
> **AC14 was an architectural INFERENCE this morning. It now has a NAMED, SCHEDULED, SECOND INSTANCE.**
> **CTO wants Cottonwood as a first-class partner. CTO has ordered that the guard precede it. Those two facts are the
> same fact, and this is the evidence for it.**

**⚠️ AND NOTE THE PERVERSITY, UNCHANGED:** Cottonwood is safe **today** only because it lives in the channel that
does the right thing (#1), and dangerous **tomorrow** because onboarding moves it into the channel that does not
(#3). **The migration is what arms the mine.**

**cot FIRM-SEPARATION (Rule 13) is NOT violated by this spec:** the guard is a property of `build_etf_decomposition`,
which already reads a **cot-free** served body. **Nothing here mirrors, syncs, or crosses bd<->cot.** *(Cottonwood's
`OWNERSHIP_DECLARED_MASTERS` is `[]` -- fund-level, master-agnostic -- so it can never be `coverage_incomplete` on a
master. Its exposure is purely the **absence** axis, not the **coverage** axis.)*

---

## 5. THE SPEC

**AC11 -- ABSENT-CONTRIBUTOR GUARD (firm-generic, complement-scoped).**

**(a) NO COMPLEMENT MAY ABSORB AN UNATTRIBUTED CONTRIBUTOR.** In any `remainder = total - sum(parts)`, a **DECLARED**
contributor that yields **no measured value** must **RAISE**. It must never be silently dropped from `parts` and
absorbed into `remainder`.

**(b) AN ABSENT CONTRIBUTOR EMITS AN EXPLICIT `missing` ROW** -- carrying **its own identity and state** (which
figure, which partner, which master/account, `fresh | rolled_forward | incomplete | missing`). **Never silence.
Never a zero. Never an estimate substituted for a measurement.**

**(c) NEVER FALL BACK FROM MEASUREMENT TO INTENT.** *A target weight is INTENT, not an OBSERVATION* (`:611-613` --
**already law in our own emitter**). Where an intent-fallback is genuinely wanted, the row must be **flagged
`inferred`** and must **not** read as measured.

**(d) THE DECLARED SIDE COMES FROM THE REGISTRY / COHORT SPEC -- NEVER FROM THE ARTIFACT JUST PARSED.** *A guard
whose two sides agree by construction cannot fail* (`:445-475` already enforces this discipline for masters).

**(e) 🔴 NO FIRM ID APPEARS IN THE GUARD.** *A guard written for `49financial` passes GREEN for Cottonwood on the day
Cottonwood lands -- and ships with a passing test proving it works.*

**FALSIFIER -- A MUTANT, NEVER A HEALTHY PARTITION:**
```
empty the measured source for a DECLARED contributor that has no intent-fallback
  -> ASSERT IT RAISES  (and does NOT move `remainder` by that contributor's value)
```
**NOT gated on G1 or on any feeder's health. NOT closable by "the number looks right again."**
> **Fixing the feeder makes the $528mm silently correct itself while the landmine stays armed. THE EVIDENCE OF THE
> DEFECT IS DESTROYED BY THE REPAIR OF ITS TRIGGER.** *`0.5.0_AE_OpalETL` has ACK'd agent-side that his feeder repair
> will NOT be cited as closing this.*

---

## 6. ONE LIVE DISCLOSURE ITEM FOUND WHILE GROUNDING (not a sum, not a magnitude)

**`s3://opal-data-etfs/daily/49financial/` -- latest partition is `2026-06-24`.** Inflection and Cottonwood are both
current to **2026-07-10**. **49F's ownership series is ~12 trading days behind the other two.**
**It IS disclosed** (the emitter stamps `vintage=rolled_forward` when `tdb != 0` -- behaviour is correct). **Recording
it as an INGESTION-ROBUSTNESS observation, not as a variance to explain, and NOT attaching a dollar figure to it.**
**The producer of that series is the ingestion question; whoever owns it should know it stopped 12 trading days ago.**

## 7. FENCES
**No code. No mdpf run. No sentinel. No trigger.** Frozen 3 untouched. cohort-8's `incomplete` untouched.
**No combined totals, no magnitudes, no disjointness analysis** (ruled out of scope, twice).
**Every guard here is specced against a FROZEN artifact and cannot be exercised until the hold lifts. Do NOT run mdpf
to test them.**
