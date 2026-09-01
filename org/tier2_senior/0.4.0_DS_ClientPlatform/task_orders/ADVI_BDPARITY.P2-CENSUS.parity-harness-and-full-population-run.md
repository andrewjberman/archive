# TO ADVI_BDPARITY.P2-CENSUS — parity classification harness (4a) + full-population run (LAPTOP)

<task_order id="ADVI_BDPARITY.P2-CENSUS" project="ADVI_BDPARITY">
<issued_to>0.4.0_DS_ClientPlatform~C (build + run); 3.0.0_SA_CVO grades; 4.0.0_SA_CRO methodology [RE-ADDRESSED 2026-08-29T16:0xZ by the issuer 2.0.0_SA_COO: DS limb moves base -> 0.4.0_DS_ClientPlatform~C. REASON: /mstr-spawn step 1d refused seating the BASE -- it holds open TOs on TWO projects -- ADVI_BDPARITY and D3_MODELOVERLAY (TO-D3.1/1b/2, bare-base assignee verified at source) -- a Rule-27 collision at seating time. [CORRECTED same turn: my first note said THREE and named ADVI_COTSNP. FALSE -- those 3 rows carry NO base assignee; they rendered under a base query because to-check --assignee is a SUBSTRING match and they name a class with no instance. The refusal stands on the D3 rows alone.] ~C measured free: 0 open TOs, 0 process-truth hits, 0 spawn markers, and POD4-enumerated so it can commit data/*/scripts/gold/*.py. Remedy named by CTO ledger row 10. Nothing else on these faces changes.]</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-19T20:05Z</issued>
<dated>MON-TUE 2026-08-24/25 (SS7)</dated>
<status>SUPERSEDED-WITH-REHOME 2026-09-01T10:0xZ (2.0.0_SA_COO, issuer) -- 5 of 6 criteria superseded with a printed coverage map; P2-3 RE-HOMED to ADVI_BDPARITY.P3-EXACT and NOT discharged. READ THE ISSUER RULING AT THE END OF THIS FILE; this line is a pointer, not the ruling.</status>
<priority>P1-program</priority>
<authority>D2_ADVI_49F_E2E_PRD.md §4a + §6 row 2 at dispatch vintage @c379cb6521. PLACEMENT RE-HOMED TO LAPTOP: Andrew-direct ~19:3xZ superseded the @a02f9ff5a4 D2-analytics-sitez workstream, VERBATIM "D2 is certainly laptop fabric"; CTO's 193804Z ruling confirms D2 whole-item laptop.</authority>
</task_order>

## Objective
Build the parity classification harness per §4a and run it over the full population.

## §6 EXISTENCE CHECK — THE HARNESS IS GENUINELY NEW
No prior harness file claims exist; the classifier is a **declared-NEW build.** Phase 1 includes
`git log` on the target path — run it and report, rather than inheriting the claim.

## THE DENOMINATOR IS THE DELIVERABLE
- **Report accounts covered / total.** A census without its denominator is a count with no frame.
- **Q1 IS AT ANDREW AND DOES NOT BLOCK YOU** (decision useful by this census; the probe is
  unaffected). Proposed parity universe = accounts BD serves calculated outputs for (the
  6,145-account BD export set intersected with performance-endpoint coverage). **The ~1,925 fam-only
  accounts have NO BD ORACLE to compare against — they are listed OUT-OF-ORACLE, never counted as
  EXACT.** Build to that reading and make the universe a parameter, so Andrew's answer is a config
  change and not a re-run of the harness design.
- **OUT-OF-ORACLE IS NOT A PASS AND NOT A FAILURE.** Counting an un-comparable account as EXACT
  would inflate parity with accounts that were never measured — the single most misleading number
  this census could produce.

## ⚠ A KNOWN INPUT DEFECT IS LIVE IN THIS WINDOW
`c00` emits IC (in-kind) legs with `in_kind_value=0.0` AND `in_kind_unvalued=False`, making
per-account TWR unreliable on in-kind-funded accounts (202/202 IC legs across 4 sampled days, 42
accounts — **a 4-day FLOOR, not the universe**). `ADVI_49F.c00-FIX` is staged at DS~A. **If this
census runs before that fix lands, in-kind-funded accounts must be SEGREGATED and reported as
known-defect-affected, never folded into a parity class** — otherwise the census measures the known
break instead of parity. Coordinate with DS~A on the full-history census result before you fix your
denominator.

## Acceptance criteria
- **P2-1 CENSUS REPORT WITH DENOMINATOR** (accounts covered / total, both printed).
- **P2-2 PER-CLASS COUNTS** across C1-C4 + any NEW-named class.
- **P2-3 ZERO UNEXPLAINED NON-EXACT** — every non-EXACT account lands in a named class or a named
  new one. "Unexplained" is the failure condition.
- **P2-4 OUT-OF-ORACLE SET LISTED SEPARATELY** with its own count.
- **P2-5 IN-KIND-AFFECTED ACCOUNTS SEGREGATED** if the c00 fix has not landed (see above).
- **P2-6 proof instance VALID rc=0 positional: ids P2-1..P2-6.** MEASURED/RULED-class run rows only;
  INFERRED-class expected values are mechanically ineligible.

<proof_of_spec>
  <expected_criteria>P2-1,P2-2,P2-3,P2-4,P2-5,P2-6</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/ADVI_BDPARITY.P2-CENSUS_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Reporting
COO at harness-built and at census-run; CVO grades the census; CRO holds methodology. Session log
w/ Compiler Tools section = deliverable.

---
## ⚖ TWO RULINGS LANDED — 2026-08-19 ~20:12Z (Andrew; records @1e0ec3b079 + @3c8c3f1035)
1. **PARITY DENOMINATOR CONFIRMED as proposed:** universe = accounts Black Diamond serves calculated
   outputs for. The **~1,925 fam-only accounts are OUT-OF-ORACLE** and are **NEVER counted as EXACT**
   (with subclasses per CTO's record). Q1 is CLOSED — build to it, not around it.
2. **COMPARISON PERIODS RULED: QTD / YTD / 1Y / SI.** That is the census spec; do not substitute a
   different period set.


## ISSUER AMENDMENT 2026-08-29T17:5xZ (2.0.0_SA_COO), on 0.4.0_DS_ClientPlatform~C's pre-build read-back 83411

**A2 -- THE RULED PERIOD SET IS NOT OBTAINABLE FROM THE CURRENT PAYLOAD BUILDER. THIS BINDS P1 AND P2 EQUALLY.**
Q2 ruled **QTD / YTD / 1Y / SI**. `lambda_function.py` `body_performance_period` (:168-176) builds
`dateRanges` = Custom(q_start,q_end) + the two trailing full CALENDAR YEARS (`_calendar_year_ranges`) + SinceInception.
  - QTD  OBTAINABLE (parameterise q_start to the quarter start)
  - SI   OBTAINABLE, but see A3
  - YTD  **AT RISK, LOW** -- type ATTESTED in BD's vocabulary, UNVERIFIED on this endpoint;
         two fallbacks exist (a Jan-1 Custom range, or the Dashboard plane)
  - 1Y   **NOT AT RISK** -- obtainable as a Custom with computed dates; NO new type needed.
         (A trailing full calendar year is not a trailing twelve months, but that is a
          statement about the CURRENT builder, not about obtainability.)
Closing it is a code change to the pull vehicle (add a YearToDate range + a trailing-12m Custom).
⛔ **CORRECTED 17:5xZ, WITHIN MINUTES OF WRITING IT, on `1.0.0_SA_CTO` 83444's net table: MY FIRST
VERSION OF THIS AMENDMENT SAID YTD AND 1Y WERE BOTH "ABSENT" AND THAT WAS TOO STRONG.**
**NO PERIOD IS ESTABLISHED AS UNOBTAINABLE, and nothing here justifies reducing Andrew's ruled set.**
What is true: the CURRENT builder does not emit them. What is NOT true: that they cannot be had.
The remaining unknown is one spec read or the `performancePeriod` HAR -- **no vendor call** -- and that
capture was NOT found in the puller's own directory.
**1.0.0_SA_CTO 83444 upgraded the YTD half from GUESS to ATTESTED:** `"YearToDate"` is a real BD dateRange type,
captured in Andrew's own 2026-08-20 HAR. **BOUND, and it is the load-bearing half:** it is attested on
`/advisor/api/v1/Dashboard/data` with a SINGULAR `dateRange` object, while this TO needs it on
`/portfolioreporting/api/performance/performancePeriod` with a PLURAL `dateRanges` array. **A type valid on one
endpoint is EVIDENCE about the other, not proof of it.** Raises the prior; does not close it.

**A3 -- "SINCE INCEPTION" FAILS SILENTLY FOR ANY NON-ROSTER ACCOUNT.** `run()` passes
`inception=acct.get("inception", q_start)`. A payload-injected probe account has no roster `trade_start_date`,
so the SinceInception range **COLLAPSES TO THE CUSTOM WINDOW** and BD returns a figure LABELLED "Since Inception"
that is actually QTD. **Nothing raises.** CONDITIONS: every probe account carries an EXPLICIT inception, and the
probe STATES WHICH inception it used. **And our roster's `trade_start_date` is not BD's funding-inception -- they
are already different questions, so an SI delta is uninterpretable until that is declared on the face.**

**STATUS OF THIS AMENDMENT: OPEN. It is not a build instruction and it does not re-open the ACs --
BP1-2/3/4/5 stand as written. It records that BP1-1's period set is unobtainable as the TO is drafted,
so that a later reader does not treat a 2-of-4 period result as a data finding.**

---

## ⛔ ISSUER RULING -- 2026-09-01T10:0xZ, `2.0.0_SA_COO`. THIS FACE IS SUPERSEDED-WITH-REHOME, NOT CLOSED.

**PROVENANCE OF THE DEFECT, AND IT IS MINE.** This face and
`org/tier2_senior/0.4.0_DS_ClientPlatform~C/task_orders/ADVI_BDPARITY.P2-CENSUS.full-population-parity-census.md`
(2026-08-30) BOTH declare `<task_order id="ADVI_BDPARITY.P2-CENSUS">`, both `issued_by 2.0.0_SA_COO`,
both assigned `0.4.0_DS_ClientPlatform~C`, eleven days apart. **The 08-30 face does not mention this
one** -- I cut it without knowing this face existed. Surfaced by a D2 open-TO census that returned two
rows for one id (COO 91241); dispositioned by `0.4.0_DS_ClientPlatform~C` 91259, which read BOTH faces
at source rather than accept my leading disposition.

### THE COVERAGE MAP -- printed, because a supersede without one is an assertion

```
  P2-1  CENSUS REPORT WITH DENOMINATOR      SUPERSEDED  covered by 08-30 P2-2 census result s.1:
        accounts 5,309 of 5,309; cells attempted 15,927 = compared 15,445 + NOT-COMPARABLE 112
        + NO-LINKABLE-DAYS 370. Reconciles exactly.

  P2-2  PER-CLASS COUNTS across C1-C4       SUPERSEDED BY A LATER RATIFICATION, named here so the
        taxonomy is not silently retired: delivered as EXACT / TIGHT / LARGE per period with
        denominators, on 4.0.0_SA_CRO's ratified bands @9f894ec5d9, which POSTDATE this face.
        "C1-C4" is the D2 PRD s.4a vocabulary. The COUNTS exist; the CLASS NAMES were replaced.

  P2-3  ZERO UNEXPLAINED NON-EXACT          ⛔ NOT SUPERSEDED. RE-HOMED. See below.

  P2-4  OUT-OF-ORACLE SET LISTED SEPARATELY SUPERSEDED under a different name: 08-30 P2-1 prints
        2,061 ours-not-pullable -> UNAVAILABLE-NOT-RESOLVABLE, plus 66 xref-pullable with no
        our-side value. ⚠ VINTAGE-BOUND: 2,061 is against the 08-28 partition's 7,370 accounts;
        the all-history union measures 8,632 twr_daily accounts. Neither is "the" figure without
        its date, and this map does not make one canonical.

  P2-5  IN-KIND-AFFECTED SEGREGATED         SUPERSEDED ON ITS CONDITION BEING FALSE -- see the
        EXCLUSION below, which is part of this ruling and not a footnote to it.

  P2-6  proof instance VALID rc=0           SUPERSEDED. Correctly NEVER WRITTEN (COO 91241 barred
        it: under the shared id an instance for either face validated against the other).
```

### ⛔ P2-3 IS RE-HOMED, NOT DISCHARGED -- AND THE REASON IS THE FINDING

```
  08-19 P2-3   "every non-EXACT account lands in a named class or a named new one.
                UNEXPLAINED IS THE FAILURE CONDITION."
  08-30 P2-4   "every non-EXACT cell carries a named candidate ( ... or UNATTRIBUTED stated )"
```

>> **"UNATTRIBUTED, STATED" IS EXACTLY WHAT P2-3 DECLARES A FAILURE.** The 08-30 face turns the
   unexplained residual from **a bar that must be cleared** into **a value that may be reported.**
   That is not the same criterion under a shared id -- **it is the OPPOSITE DISPOSITION of the same
   question.** A clean supersede would have discharged a FAILURE CONDITION by substituting a
   PERMISSION, and it would have looked like bookkeeping. <<

**AND IT IS UNMET TODAY, ON MEASURED EVIDENCE:** the census carries **1,516 both-sides-linked LARGE
cells** (1,506 after `0.4.0_DS_ClientPlatform~C`'s exclusion) labelled *"genuine calculation
differences"* **with no named mechanism.** P3-EXACT cycle 1 named mechanisms for the day-count
population and one producer class; **it named none for the 1,516.**

**RE-HOMED TO: `ADVI_BDPARITY.P3-EXACT`'s TERMINAL CONDITION** -- *"EXACT across the board, with C3/C4
residuals CARRIED and their account lists PRINTED. A residual carried without its list is an
unfalsifiable claim."* ⛔ **NOT to 08-30 `P2-4`, which would retire it.** P3-EXACT's condition is **at
least as strict as P2-3 and adds the account lists**, so the bar is preserved and strengthened rather
than moved.

### ⚠ DECLARED EXCLUSION carried WITH this ruling -- P2-5 is discharged as AUTHORED, and that is less than it sounds

P2-5 binds only *"if the c00 fix has not landed."* `0.4.0_DS_ClientPlatform~C` measured the condition
FALSE rather than assuming it: `ADVI_49F.c00-FIX` @`89204884d7` is in the SERVED blob
(`s3://opal-data-49financial/_code/c00_flow_ledger.py`, md5 `4807a51e...`, 33,825 B, LastModified
2026-08-28T16:46:07Z, byte-identical to `git show HEAD:<path>`), with a **negative control**
(`89204884d7~1` -> md5 `bee22437...`, 17,703 B, fix sentinel 0 occurrences vs 2 in the served blob),
and the census gold postdates it (twr_daily 539 of 540 partitions written 2026-08-30).

⛔ **THE EXCLUSION, RECORDED SO IT CANNOT BE READ AS AN ALL-CLEAR:** *"the fix was deployed before the
data was built"* **IS NOT** *"the data is free of the defect."* **No in-kind census of the census
population was performed by anyone** -- the delivered census does not mention in-kind at all (0
occurrences). This ruling discharges **the criterion as authored**, whose condition is false. **It
establishes nothing about in-kind correctness, and nothing downstream may cite it as if it did.**
⭐ Written here rather than left out, on `3.0.0_SA_CVO` 91230's distinction: *an ABSENT item and an
EXCLUDED-WITH-REASON item are the same shape to a careless reader and opposite to a careful one.*

### ⛔ WHAT THIS EPISODE ACTUALLY TEACHES, and it is NOT "avoid duplicate ids"

`0.4.0_DS_ClientPlatform~C` 91259 s.6, adopted verbatim as the finding: **the collision is not what made
`P2-3` invisible -- the WEAKENING is, and that would have been invisible under DISTINCT ids too.** An
identity field on a proof instance (routed to `3.0.0_SA_CVO` at 91242) would catch a wrong-FACE
instance and **would still not catch this.** ⛔ **Nothing in the estate compares what two criteria
under one id MEAN.** Both controls are worth having and they are DIFFERENT controls.

⚠ **AND THE WIDER MECHANISM, from `3.0.0_SA_CVO` 91248, read at source:** `proof-of-spec-check.py`
**never reads any face's criterion text** (`:717 _parse_to` extracts only `<decomp_ref>`; every
acceptance arm iterates the INSTANCE's own rows). **`VALID rc=0` means FORM-VALID -- not SATISFIED.**
So no proof instance on either face could ever have caught the weakening. **This ruling rests on
`0.4.0_DS_ClientPlatform~C`'s source reads and the measured 1,516, never on a checker verdict.**

### DISPOSITION

**This face is SUPERSEDED-WITH-REHOME and is no longer an open TO.** `P2-3` travels to
`ADVI_BDPARITY.P3-EXACT` and remains **UNMET**. `0.4.0_DS_ClientPlatform~C`'s cycle-2 work is unblocked
and unchanged. No proof instance is to be written against this face.
