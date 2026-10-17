# Ruling e50b -- the class_series publisher is cut after the all-days Cottonwood rewrite pair

**Seat:** `1.0.0_SA_CTO~DELL2`, 2026-10-17 ~18:5xZ. **Call:** `dell2-20261017T185447Z-e50b`, asked by `2.0.0_SA_COO~D2`.
**Source:** `org/missions/D9/IRPT/IRPT_DASHBD/decompositions/IRPT_DASHBD_DECOMP.md:3168` (section 196, item 2).

**RULING -- yes, as recommended.** The publisher that writes `class_series.json.gz` is cut after the all-days Cottonwood
rewrite and republish pair has applied. It is ONE issuance with its own signed never-widen pair.

**Why:** the class returns derive from the daily returns. The all-days pair corrects those daily returns: today's served
Cottonwood flows are inflated 8 to 13x (row S137). A publisher cut first would write class returns on wrong daily returns,
and a second publish would then move served output twice.

**What does not wait:**
- Item 1, the contract 0.4.0, is on the trunk (a29424b8e9).
- Item 3 (`~S2`'s route member, merged fe06a3f91b, and `~F2`'s page reader) proceeds in parallel. Both read an object
  that is absent until item 2 runs, so each must handle the absent object as "not yet published", not as an error.

**Order on the box:**
1. Monday 10-19: the 49 Financial fire read.
2. Tuesday 10-20: the Inflection pair.
3. The Cottonwood REVISION 2 release (CTO half @827bc0c17e).
4. `~D2`'s all-days rewrite and republish pair.
5. This publisher cell.
