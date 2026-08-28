# TO ETFS_POSITIONING.TO-12-DE — TAKE THE AS-OF DATES OFF THE POSITIONING PAGE

<id>ETFS_POSITIONING.TO-12-DE.remove-as-of-dates-under-the-stacked-bars</id>
<decomp_ref>⚠ **NO CELL ADDED AND NONE CLAIMED.** This is a RENDER-LAYER REMOVAL on a surface `ETFS_POSITIONING.TO-7` already built and certified (7/7 @`37a69dcdf7`); its own face carries no `decomp_ref`. **Stated plainly rather than fabricating a cell reference to satisfy Rule 27** — the authority here is a direct sovereign product request on a rendered element that exists today.</decomp_ref>
<issued_to>DE-class, `portal/**` on DEV. ⛔ **SEAT IS `0.0.0_AB_MSTR~Z`'s act — Andrew has now asked for it directly.**</issued_to>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-08-28T15:3xZ</issued>
<status>pending -- CUT ON ANDREW'S DIRECT REBUKE THAT IT HAD NOT BEEN CUT.</status>
<priority>P1 — **he asked, it was not worked, and he had to notice the absence himself.**</priority>

<authority>
**ANDREW-DIRECT ~15:3xZ, VERBATIM** (relayed by `1.0.0_SA_CTO~Z`, msg 13311; typos his, preserved):
> *"Theres thing i asked for when you asked me abot the calls that i dont see being worked on, like
> taking the dates off the frontend for the ETFS in Positioning page underneath the stacked bars. I
> know you'll need a DE for these works so why is that not being allocated?"*

**AND THE ORIGINAL ASK, ~15:0xZ, VERDICT 2, VERBATIM:**
> *"Dont need this, timestamps are listed elsewhere."*
</authority>

## 1. ⛔ WHY THIS TO DID NOT EXIST UNTIL NOW — THE FAILURE IS THE ISSUER'S

His verdict 2 arrived **during a certification walk**, so it was classified in that frame: filed as a
disposition on `ETFS_POSITIONING.TO-7` (retire a criterion) rather than as **a product change**.
>> ⛔ **RETIRING A CRITERION DOES NOT DELETE A RENDERED ELEMENT.** *"Don't need this"* about something
   on the page means **take it off the page.**
⚠ **AND THE AMBIGUITY WAS SURFACED AND I DID NOT RESOLVE IT.** `3.0.0_SA_CVO~Z` explicitly asked
whether verdict 2 meant *"do not SHOW the per-fund dates"* or *"the per-fund as-of DATA is not
needed"* — **a render change versus a correctness property.** It named the fork correctly and left it
open as a question to Andrew. **`2.0.0_SA_COO~Z` read that and treated it as the certifier's question
rather than the ISSUER'S**, picked up verdict 5, cut two TOs, and left verdict 2 unclassified.
>> ⭐ **A SOVEREIGN VERDICT DELIVERED IN A CERTIFICATION FRAME CAN STILL BE A BUILD REQUEST. THE FRAME
   IS NOT THE CLASSIFIER.**

## 2. THE SURFACE
`portal/src/pages/Positioning/panels/PositioningSummary.tsx` — the as-of dates rendered **underneath
the stacked bars** on the ETFs Positioning page. (`TO-7` AC4/AC5 @`46f3863e` put them there.)

## 3. ⛔⛔ SCOPE BOUND — DO NOT WIDEN. RENDER-LAYER REMOVAL **ONLY**.

```
REMOVE   the as-of dates DISPLAYED under the stacked bars
KEEP     the per-fund as-of DATA in the artifact, unchanged
```
>> **He did NOT ask to remove the per-fund as-of from the data.** `TO-7`'s producer work is **certified
   7/7 and serving**, and **his own reason — *"timestamps are listed elsewhere"* — PRESUPPOSES THEY
   STILL EXIST SOMEWHERE.** Deleting the data would make his stated reason false.
⭐ **SAME SHAPE AS SATELLITE 98 AND AS `Alternatives`: the DATA KEEPS THE VALUE; THE VIEW DROPS IT.**
⛔ **A producer-side change here is out of scope and would be a regression against a certified TO.**

## 4. ACCEPTANCE CRITERIA

| id | criterion |
|---|---|
| `TO12-AC1` | **The as-of dates no longer render under the stacked bars.** ⚠ **READ A SCREENSHOT** — a class-name grep does not establish what a page draws. Both before and after, both READ by the executing agent. |
| `TO12-AC2` | ⛔ **THE DATA IS UNCHANGED.** The served `positioning_data.json` still carries the per-fund as-of. **Show the served artifact before and after; the diff on that field is EMPTY.** A render change that alters the payload has exceeded this TO. |
| `TO12-AC3` | **NO OTHER ELEMENT MOVED.** The stacked bars, their values and their labels render as before. ⚠ **He named ONE element; a layout reflow that changes others is a widened scope.** |
| `TO12-AC4` | ⛔ **`ETFS_POSITIONING.TO-7` IS NOT REGRESSED.** It is CERTIFIED 7/7 @`37a69dcdf7` on producer behaviour. **State explicitly that no producer/AC-bearing behaviour changed.** |
| `TO12-AC5` | **TYPESCRIPT CLEAN** — `tsc -b`, zero errors. ⛔ `commit-gate` reads `.py`/`.sh`/`.tf` and prints *"checked 0 of N files"* on a frontend diff; **that line is NOT evidence of a clean gate.** |

## 5. NOT YOURS
⛔ The **PROD promote** — Andrew's word, **per promote**, no standing authorization.
⛔ `D1_CATVIEWS.TO-M1-DS` / `TO-S1-DE` — different project, and `TO-S1-DE` is blocked on `TO-M1-DS`.
⛔ Any **producer-side** as-of change.

<proof_of_spec>
  <criterion id="TO12-AC1"/>
  <criterion id="TO12-AC2"/>
  <criterion id="TO12-AC3"/>
  <criterion id="TO12-AC4"/>
  <criterion id="TO12-AC5"/>
  <expected_criteria>TO12-AC1,TO12-AC2,TO12-AC3,TO12-AC4,TO12-AC5</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/ETFS_POSITIONING.TO-12-DE_PROOF_OF_SPEC.json</instance_path>
  <alignment_denominators>criteria: 5. ⚠ NO CELL REFS — this TO deliberately claims none; see decomp_ref. It is a render-layer removal on an already-built, already-certified surface, cut on a direct sovereign request. ⛔ Ids are NOT firm-tokened here for the same reason `TO-8`'s were flagged: the estate's rule says they should be, and `INGEST-TO8` shows what a bare token costs. Recorded so the next issuer tokens them at cut time rather than after.</alignment_denominators>
</proof_of_spec>
