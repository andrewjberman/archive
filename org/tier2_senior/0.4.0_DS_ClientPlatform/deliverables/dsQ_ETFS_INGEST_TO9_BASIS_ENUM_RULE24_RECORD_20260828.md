# RULE 24 RECORD — a SIXTH member for `INDUSTRY_GROUP_BASIS_VOCAB`

**Seat:** `0.4.0_DS_ClientPlatform~Q` · **Project:** `ETFS_INGEST` · **TO:** `TO-9-DS`
**Status: PROPOSAL. NOT MINTED, NOT WIRED.** Routed to `1.0.0_SA_CTO~Z` / `2.0.0_SA_COO~Z`.

---

## 0. ⛔ WHY THIS EXISTS — WIRING THE DECODE BREAKS AN EXISTING TEST

`gics_industry_group_decode.py` returns `basis="inferred-from-truncation"`. That value is **NOT in
the 5-member vocab** at `etf_positioning_gold.py:210`. Two live assertions reject it:

```
  test_etf_positioning_industry_group.py:146   all(r["industry_group_basis"] in
                                               g.INDUSTRY_GROUP_BASIS_VOCAB ...)
  test_etf_positioning_industry_group.py:341   the same assertion on SERVED rows
```

>> **SO THE WIRING IS NOT A ONE-LINE PUBLISHER EDIT. It is an enum change, and Rule 24 governs it.**
   Neither `13679` (COO co-sign) nor `13676` (CTO co-sign) saw this — both signed the never-widen
   radius, which is a DIFFERENT control. **Surfacing it rather than emitting an undeclared value.**

⚠ **AND THIS IS THE HAZARD MY OWN LANE ALREADY NAMED** (`dsq_etfs_ingest_to6_to8` log): *"If DS mints
one spelling and DE reads another the adapter drops it, the page looks untouched, and BOTH HALVES
PASS THEIR OWN CHECKS."* Consumers reading this field: `portal-proxy.ts`, `etfAdapter.ts`,
`HoldingsTab.tsx`.

## 1. THE CONFLICT TO RULE — THE TO NAMES A DIFFERENT SPELLING THAN I MINTED

`TO-9-DS` §4 says a repaired value *"needs its own `industry_group_basis` member reading
**`RESOLVED`**."* I minted **`inferred-from-truncation`**. **I am not choosing between them here.**

**WORD-BOUNDARY TOKEN CENSUS (Rule 24 requirement, `comp-find -i --all`, corpus=default,
denominator 27,844 files):**

| candidate | hits | verdict |
|---|---|---|
| `inferred-from-truncation` | **3** (1 DEF + 2 my own records) | collision-free |
| `inferred` | 4,663 | overloaded |
| `resolved` | **33,401** | **catastrophically overloaded** |

>> **`resolved` at 33,401 occurrences is unusable as a searchable enum token** — a census of it can
   never be scoped, which is the exact property Rule 24's census requirement exists to test. <<

## 2. THE FOUR POSTULATES

**(i) MECE over the DECLARED DOMAIN** — *"why does this row's `industry_group` hold what it holds"*:

| member | covers | owner |
|---|---|---|
| `observed` | vendor returned a value; served unchanged | vendor |
| **`inferred-from-truncation`** ⭐ NEW | vendor returned a value **the vendor truncated**; we completed it by inference | DS decode table |
| `not-applicable-non-equity` | no industry group **by construction** | no remedy, permanent |
| `field-not-in-source` | the pull has not fired since the field landed | the next scheduled pull |
| `security-not-in-characteristics` | ticker has no characteristics row | INGEST coverage |
| `absent-from-source` | vendor returned no value for a security it has a row for | vendor |

**THE UNCOVERED MEMBER HUNTED FOR — FOUND, AND DELIBERATELY NOT MINTED:**
*"vendor value is TRUNCATED but NOT completable"* (a group whose 30-char form the decode has never
seen). Today it returns `observed`.
⛔ **NOT MINTED BECAUSE IT IS UNASSIGNABLE BY CONSTRUCTION:** we cannot detect it. `len` 29–30 is
INDETERMINATE — `'Consumer Staples Distribution'` (29, truncated) sits beside `'Household & Personal
Products'` (29, complete). **A member no producer can ever assign is not a member; it is a comment.**
And `observed` is not a lie there — the served string IS the vendor's own, faithfully.

**(ii) SAME GRAIN** — one value per HOLDING ROW, the same grain as the field it explains. Unchanged.

**(iii) INTENT COHERENCE — ONE AXIS, ONE INTENT. THIS IS THE ARGUMENT AGAINST `RESOLVED`.**
The axis is **PROVENANCE**: *how did this value come to be*. Every existing member answers that.
```
  inferred-from-truncation   PROVENANCE -- names the origin and the mechanism.   ON AXIS.
  resolved                   LIFECYCLE  -- names a STATE something reached.      OFF AXIS.
```
`resolved` describes a workflow status, not an origin, and mixing a lifecycle rung into a provenance
enum is the Rule 24(iii) violation this estate has hit repeatedly (banked: *"Rule 24(iii) applies
INSIDE a value's wording"*). **The TO's own §4 sentence — "A REPAIRED VALUE IS DERIVED, NOT
OBSERVED" — argues for a PROVENANCE word; `RESOLVED` is not one.**

**(iv) STATE COHERENCE — what one remedy does NOT move.** If an authoritative GICS vocabulary ever
arrives, it moves **`inferred-from-truncation` ONLY**. It does not move `not-applicable-non-equity`
(true by construction, permanently), `field-not-in-source` (moves on a scheduled pull),
`security-not-in-characteristics` (an INGEST coverage question), or `absent-from-source` (the
vendor's). **Four different owners — which is what makes these real members rather than
re-spellings.**

## 3. WHAT I RECOMMEND, AND WHAT I AM NOT DOING

**REC:** adopt **`inferred-from-truncation`** as the sixth member, and record that it supersedes the
TO's `RESOLVED` on (iii) + the census, so the TO face and the code do not carry two spellings.

⛔ **NOT DOING:** minting it, editing `INDUSTRY_GROUP_BASIS_VOCAB`, or wiring the publisher. A served
enum member is read by three portal consumers and one gold test; **my predecessor's log names this
exact class as needing "the one ruled key-name string both lanes cite."** The wiring is HELD on this
ruling — not on judgement, on a named taxonomy law.

⚠ **AND THE DECODE MODULE IS ALREADY CONSISTENT WITH EITHER OUTCOME**: the basis string is a single
module-level constant (`BASIS_INFERRED`). A different ruled spelling is a one-line change, no logic.

---
**Author:** `0.4.0_DS_ClientPlatform~Q`
