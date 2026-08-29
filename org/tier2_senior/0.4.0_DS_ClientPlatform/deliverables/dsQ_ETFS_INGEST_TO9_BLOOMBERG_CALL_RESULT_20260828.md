# ETFS_INGEST.TO-9-DS — THE GRANTED BLOOMBERG CALL: FIRED, AND IT SETTLES THE FORK

**Seat:** `0.4.0_DS_ClientPlatform~Q`
**Fired:** 2026-08-28, after `1.0.0_SA_CTO~Z` msg **13578**/**13585** ruled FIRE and `2.0.0_SA_COO~Z`
msg **13581** issued the GO adopting that ruling in full.
**Grant:** Andrew-direct ~17:0xZ, per-use, **SCOPED TO ONE CALL**. **SPENT — this is the one.**

---

## 1. THE CALL — ONE `ReferenceDataRequest`

```
securities  11   8 suspect groups (every observed value with len >= 29, so the 29-char trap is
                 INSIDE the set) + 3 complete-value controls (Banks/Energy/Utilities)
fields      12   the incumbent + 11 candidate mnemonics
field errors 0   ALL 12 mnemonics resolved. No BAD_FLD, no NOT_APPLICABLE.
```
Health read first (`ok: true`, `//blp/refdata`) so the grant could not be spent on a signed-out
terminal. **One request. Breadth in FIELDS costs no extra call, and a wrong candidate would have
self-reported as `BAD_FLD` rather than being fatal.**

## 2. ⛔ RESULT ONE — **THE VENDOR HAS NO UNTRUNCATED GICS NAME FIELD. FORK A IS DEAD.**

The 30-char cap is **FAMILY-WIDE**, not a property of the one field we pull:

| field | distinct | max len | AT 30 | **OVER 30** |
|---|---|---|---|---|
| `GICS_INDUSTRY_GROUP_NAME` | 11 | 30 | 6 | **0** |
| `GICS_INDUSTRY_NAME` | 11 | 30 | 4 | **0** |
| `GICS_SUB_INDUSTRY_NAME` | 11 | 30 | 5 | **0** |
| `GICS_SECTOR_NAME` | 8 | **22** | 0 | 0 |

**15 distinct values sit at exactly 30 across THREE independent GICS name fields; ZERO exceed 30.**
`GICS_SECTOR_NAME` maxes at 22 — it never reaches the cap, which is exactly why sectors were never
affected and why this looked like an industry-group problem rather than a field-family one.

>> **ANDREW'S OPTION (b) — *"just whatever field we're using for that pull make sure it has more
   character count"* — HAS NO FIELD TO POINT AT.** It was the right instinct and the measurement
   closes it. `BICS_LEVEL_2_INDUSTRY_GROUP_NAME` is also capped at 30, and is a DIFFERENT taxonomy
   (BICS, not GICS) so it was never a substitute. <<

## 3. ⭐ RESULT TWO — THE CALL BOUGHT SOMETHING BETTER: **AN AUTHORITATIVE, LOSSLESS KEY**

`GICS_INDUSTRY_GROUP` returns the **4-digit GICS industry-group CODE**, and a number cannot truncate.

```
1010 Energy(6)          2020 [30] TRUNC   2550 [30] TRUNC   3010 [29] TRUNC
3030 Household...(29)   3510 [30] TRUNC   3520 [30] TRUNC   4010 Banks(5)
4520 [30] TRUNC         4530 [30] TRUNC   5510 Utilities(9)
```

**CONTROL — the codes are genuinely the GICS hierarchy, not an arbitrary vendor id:**
`group//100 == sector` AND `industry//100 == group` AND `sub_industry//100 == industry`,
**11 of 11 securities, 0 mismatch.** A coincidental id space would not nest three levels deep.

## 4. ⛔ WHAT THIS CORRECTS IN MY OWN PRIOR REPORT — I WAS WRONG AND `1.0.0_SA_CTO~Z` CALLED IT FIRST

In msg 13569 s.4 I reported: *"`GICS_INDUSTRY_GROUP`: exactly ONE mnemonic in the estate, the
incumbent. **No NUM/CODE sibling.**"*

**THE NUM/CODE SIBLING EXISTS. It is `GICS_INDUSTRY_GROUP` and it is the best thing the call
returned.** My sentence was true of OUR ESTATE and false of BLOOMBERG, and I let an estate census
stand in for a vendor-catalog claim. `1.0.0_SA_CTO~Z` named this gap in 13585 s.2 **before the call
was fired** — *"that is a census of our usage, not of Bloomberg's catalog"* — and the call proved
that office right. **A measured zero inside our repo says nothing about the surface next door**;
`integrations/bloomberg/READ_HERE.md` s.4 records the same class costing three days.

## 5. WHAT REMAINS, STATED AS A GAP AND NOT ROUTED AROUND

The code is an authoritative **KEY**. It is not the **NAME TEXT**. The residue is exactly:

> **25 code -> name strings.**

⛔ **NO WORKAROUND IS BEING IMPROVISED.** `1.0.0_SA_CTO~Z` 13585 s.2 and `2.0.0_SA_COO~Z` 13581 s.1
both bound this in advance: *"if it returns truncated values too, that is a RESULT ... and the next
step is a QUESTION FOR ANDREW, not a workaround."* This document is that result; the question goes
to Andrew.

⭐ **BUT THE SHAPE OF THE REMEDY IMPROVES REGARDLESS OF HOW HE ANSWERS**, and this is the part worth
carrying forward. Keyed on the CODE rather than on our truncated string:

```
  prefix-match our 23 observed strings   ambiguity is POSSIBLE -> AC5 needs fail-loud machinery,
                                         and the key is OUR OWN PRIOR OUTPUT (what AC1 forbids)
  key on the vendor's 4-digit CODE       ambiguity is STRUCTURALLY IMPOSSIBLE. No prefix, no
                                         length heuristic, key is VENDOR-AUTHORITATIVE.
```
**`INGEST-TO9-AC5`'s two requirements — fail loud on an ambiguous prefix, and never key on string
length — are satisfied by CONSTRUCTION under a code key rather than by machinery.** And
`1.0.0_SA_CTO~Z`'s load-bearing condition (13578 s.2) is met in the strongest available form: the
table is keyed to the vendor's own authoritative code, **not** derived from our observed 23.

⚠ **`GICS_INDUSTRY_GROUP` IS NOT CURRENTLY PULLED.** Adding it to `CHAR` in
`etf_daily_pull.py:238-240` is *"ONE MORE FIELD ON A CALL THAT ALREADY RUNS"* — the pull's own
phrase at `:232` for the identical act. **NOT DONE IN THIS TURN:** `2.0.0_SA_COO~Z` owns the
implementation cut (13581 s.3) and had deferred it pending this result, and on site Z an edit to
that file **IS a deploy the moment it touches disk** (`READ_HERE.md` s.3). It is proposed, not taken.

## 6. SCOPE OF THIS RESULT — SAID PLAINLY

**COVERED:** 4 GICS name fields on 11 securities spanning 11 of the 23 observed industry groups.
**NOT COVERED:** Bloomberg's full field catalog. This establishes the cap across the GICS `*_NAME`
family as measured; it is not a census of every mnemonic Bloomberg offers. Given s.4, that
distinction is stated rather than glossed. **A second vendor call needs its own word from Andrew.**

---
**Author:** `0.4.0_DS_ClientPlatform~Q`
