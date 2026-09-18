# IRPT_BCKEND -- ROUND 3 ANALYSIS (L10)

**Seat:** `1.0.0_SA_CTO`. **Slug:** `3.0.0_SA_CVO` msg 97937, rows at `598b334f13`. **Drain packet:**
`2.0.0_SA_COO~B` @`c5fd5d2057` (blob `ce3a8e392a`). **Set:** 9 orders, 19 criteria -- **NINE judgment, ten
mechanical, all nine judgment PASS.** **Channel: 219 items, 0 undispositioned, 0 unknown `adjudicates` targets, 101
remediation rows (was 97), 0 open orders of 45.** **ROUND 4 IS UNBLOCKED.**

**Outcome array:** `FWD-1,2,3,4,5,7,8,9,10,11` (10 outcomes; **there is no FWD-6 in the array**). **Round 2 baseline:
ZERO of 10 REALIZED** -- six ADVANCED/NOT REALIZED, three NOT NARROWED, one ADVANCED.

## 1. THE ID CORRECTION, recorded because a grader keys on it

The hand-off's shorthand reads `R31/R32/R34/R35/R36-AC2`. ⛔ **`IB-rtc-1`'s JUDGMENT criterion is `R31-AC3`;
`R31-AC2` is one of its MECHANICAL criteria and passed by output.** The list is right in substance. ⭐ **Naming it
rather than silently fixing it is correct** -- a later grader re-deriving from the shorthand would grade the wrong
criterion and find it already PASS.

## 2. ⭐ THE ROUND'S KEEPER: **A CRITERION THAT PREDICATES ON A FUTURE STATE OF A SHARED ARTIFACT CANNOT BE SATISFIED BY ANY AMOUNT OF CARE**

`R38-AC2` asked whether **the bundle THE HOST WILL RUN at `IB-rtc-7`'s fire** is byte-identical to the tree the
applies are cut from. **The cell's numbers are exact and I accept them: `directory_runner.py` is blob `0351bce745` at
all three named cuts; `data/firm_registry.json` carries 136 CR bytes against 0 in the blob, equal only after
CRLF-to-LF normalisation and NOT equal raw** -- precisely the condition row `S63` records.

⛔ **AND THE WORLD MOVED BETWEEN THE ANSWER AND THE EVENT.** `IB-rtc-8` minted at **02:31:37** with that member at
`0351bce745`; `IB-rtc-9` landed at **03:54:43 -- EIGHTY-THREE MINUTES LATER** -- changed the same member to
`30ffce2eff` (+22/-3) and re-minted the bundle as `VersionId 0XLkiPt4`; **and `IB-rtc-9`'s merge is a STATED
PRECONDITION of `IB-rtc-7`.** ⭐ **SO THE HOST RAN `IB-rtc-9`'s BUNDLE, NOT THE ONE `R38` CERTIFIES -- and the cell
could not have known, because `IB-rtc-9` had not happened at its write time.**

⛔ **THE CELL PASSED AND THE CRITERION IS WHAT FAILED.** A grader reading `R38-AC2 PASS` learns nothing about whether
the host ran the certified bytes. ⭐ **This is exactly R-68's `C6R4-AC8` shape -- A GAP IN THE CRITERION, NOT IN THE
GRADING OF IT -- and it is the second instance in one night, on a different project, found by a different seat.**

⭐ **ADOPTED AS A BAR:** **A FORWARD-LOOKING CRITERION IS UNFALSIFIABLE AT ITS OWN CUT AND FALSIFIED LATER BY EVENTS
NOBODY CONTROLS. BIND THE CLAIM TO THE ARTIFACT'S CONTENT HASH AT THE EVENT, NEVER TO A PREDICTION MADE BEFORE IT**
-- which **R-40 already carries**, so this is a second instance of a ruled remedy rather than a new rule.

⭐ **THE CONTRAST IS INSIDE THIS ROUND, TWICE, WHICH IS WHY THE BAR IS REACHABLE AND NOT ASPIRATIONAL:**
1. **`R31-AC3` VOLUNTEERS exactly this supersession for a different artifact, UNASKED -- and could only do so because
   it was looking BACKWARD at one.**
2. **The `IB-rtc-7` never-widen sign-off's two mechanical conditions were EVALUATED AT THE APPLY** (plan exactly 1 to
   change; post-apply writer census membership) **rather than predicted before it.** Both branches were covered
   whichever way the producer went, and both behaved: condition 1 held, condition 2 did not fire.

⚠ **AND IT IS THE SAME SHAPE AS RULE 27's "NO FWD IS A WAIT" ONE LEVEL UP** -- an outcome whose only proof is an event
nobody controls. The CVO named that connection and it is correct.

## 3. FWD GRADING -- round 3 moves the DIRECTORY outcomes and nothing else reaches REALIZED

⭐ **THE ROUND'S REAL-WORLD OUTPUT: three directories built through the DEPLOYED dispatch on a REAL FIRE --
`49financial` 4562 entries (FIRST MINT EVER), `cottonwood` 259, `inflection` 291**, under
`s3://opal-data-bd/investor-reporting/directory/2026-09-16/` (legacy destination until D14).

| outcome | round 2 | round 3 | why |
|---|---|---|---|
| **FWD-1** advisor finds an authorized client | ADVANCED, NOT REALIZED | **ADVANCED FURTHER, NOT REALIZED** | the directory now EXISTS for all three firms; the advisor-facing flow still bars at EXERCISED |
| **FWD-7** the directory cannot go quietly stale | ADVANCED, NOT REALIZED | **ADVANCED FURTHEST, NOT REALIZED** | see s.4 -- the mechanism is EXERCISED; the ORGANIC fire is the acceptance |
| **FWD-2, 5, 9, 10, 11** | ADVANCED / NOT REALIZED | **NOT NARROWED THIS ROUND** | round 3's nine cells are the directory/principal/runner chain |
| **FWD-3, 4, 8** | NOT NARROWED | **NOT NARROWED** | ⚠ **FWD-8 explicitly: `R35`'s control ran on the LOCAL DEV plane, NOT the plane FWD-8's DONE WHEN names** -- the cell said so itself |

⛔ **ZERO of 10 REALIZED AT ROUND 3's CLOSE.** ⭐ **That is not a failed round -- it is a round that built the
substrate three outcomes stand on and refused to claim any of them.**

## 4. FWD-7 and the 13:00Z fire: **CORRECTLY SHAPED, NOT A WAIT-DEFECT** -- and here is the test I applied

`R37` reports the scheduled organic fire as an open WAIT it did not observe. ⛔ **Rule 27 forbids an FWD whose only
proof is an event nobody controls, and the Agent-Autonomy line calls "waiting for the scheduled run" a coast-failure.
BOTH ARE SATISFIED HERE, AND THE REASON IS THAT THE AD-HOC WAS FIRED RATHER THAN WAITED ON.**

⭐ **THE MECHANISM WAS DRIVEN DELIBERATELY: three directories built through the deployed dispatch on a real fire.
THE ORGANIC CASE IS KEPT AS THE NEGATIVE ARM**, which is precisely the re-cut Rule 27 prescribes. **`irpt-directory-
refresh` at `cron(0 9 ? * MON-FRI *)` America/New_York fires 13:00Z -- the first fire meeting the fixed runners, the
K5 env and the principal together. NO RE-CUT IS OWED AND NOTHING NEEDS ANDREW'S QUALIFYING WORD.**

⛔ **BUT A CRITERION THAT CERTIFIES WHAT THAT FIRE WILL FIND IS s.2's DEFECT AND MUST NOT BE WRITTEN.** Round 4 grades
the fire by reading **what it actually loaded**, at the bundle's `VersionId` **at invocation** -- never by a
prediction cut beforehand. ⚠ **And EventBridge `Invocations` certifies nothing: bind the trigger's proof to the
ARTIFACT it produced, not to the rule that fired.**

## 5. S56 DOES NOT DISCHARGE, and the round that was meant to absorb it produced a fresh instance

`2.0.0_SA_COO~B` routed this to the CVO explicitly and the answer is measured, denominator printed: **across all NINE
judgment records, 4 line citations, and 4 of 4 are BARE with NO vintage pin** -- all four in `R39-AC2`
(`export/bundle.py:82`, `holdings/snapshot.py:119`, `narrative/handler.py:74`, `performance/normalize.py:390` and
`:398`).

⛔ **THE GRAIN IS THE WHOLE ANSWER: `S56`'s condition names JUDGMENT RECORDS, not faces.** The faces may well have
improved; **the GRADED EVIDENCE did not.** ⭐ **The round armed against this produced a fresh instance of exactly it,
on the surface the row names** -- and this is CLAUDE.md's own Rule 22 line, *"a citation without a vintage is not a
citation."* **`S56` stays ARMED and OPEN. Correct, and untouched by the CVO.**

## 6. The other clocks

- **`S65`, `W4-S32` CLOSE DISARMED/REMEDIATED** on `2.0.0_SA_COO~B`'s evidence rows `S72`/`S61`, **and `S65` was
  confirmed ON THE LIVE PLANE** -- the role exists at `CreateDate 2026-09-18T08:49:34Z`.
- ⛔ **`S68` STAYS ARMED, and the reason is the sharp one: `IB-rtc-7` avoided its hazard by TARGETING the apply rather
  than removing it, SO THE EXPOSURE SURVIVES THE ACT THAT WORKED AROUND IT.** ⭐ **A workaround that succeeds is the
  most likely thing to be mistaken for a fix.**
- **`W3-S39` STAYS ARMED, correctly** -- it exists because `R34`'s cell **REFUSED a three-way verdict its instrument
  could not by construction settle**, and closing it would undo that refusal.

## 7. Nineteen INERT rows dismissed -- fifteen of them a cell correcting the face it was handed

Member globs excluding required closure members; **a declaration that would FREEZE THREE LIVE PRODUCTION DEPLOY
LEGS**; a negative control naming the wrong prior; a live control now the OPPOSITE SHAPE to its face's description;
⭐ **a `<paths>` grant binding the lane gate only for a `0.9.0_WK_*` worker and NOT for the Tier-2 seat the order was
handed to** (the longest-prefix resolution trap, live); and **a contract file the holdings runner actually reads that
is NOT IN THE BUNDLE.** ⭐ **The issuer FILED THE DISARMS RATHER THAN ARGUING, which is the thing worth keeping about
this round.**

⚠ **ONE OF THOSE NINETEEN IS INERT ONLY BECAUSE A SCHEDULE IS OFF.** `S71` -- `holdings_snapshot`'s contract path is
not a bundle member -- **is INERT because that schedule is DISABLED.** ⛔ **IT ARMS THE MOMENT ANYONE ENABLES IT, AND
NOTHING WATCHES THAT TRANSITION.** That is the same family as tonight's repeated finding: **a condition that changes
underneath a sentence which stays true-looking.** **Round 4 carries it as a NAMED re-arm trigger, not as a closed
row.**

## 8. `S73` is an ESTATE-INSTRUMENT defect and does not belong to this project

⛔ **`comp-iam roles` prints `"IAM ROLES (210 found)"` with NO VINTAGE LINE and does not carry
`irpt-49f-directory-read-role`, live since `08:49:34Z`.** ⭐ **So a seat checking a fresh apply through the estate's
OWN IAM tool gets a confident, denominator-bearing ABSENCE -- the exact inverse of the phantom-backstop class its own
HUD advertises catching.** The sibling `comp-iam live` discloses everything properly **including both of its own
unverified halves**, so this is a **DISCLOSURE ASYMMETRY INSIDE ONE TOOL.**

⭐ **REMEDY ADOPTED AS PROPOSED: carry `live`'s provenance header onto `roles`, `role`, `service` and `services`.**
⛔ **It is NOT this project's surface and must not ride round 4** -- it is routed with a named owner. ⚠ **And it is
tonight's class in a NEW DIMENSION: a denominator narrower in TIME than the sentence it supports.**

## 9. What round 4 owes

1. **The 13:00Z organic fire**, graded on what it ACTUALLY LOADED at the bundle's `VersionId` at invocation (s.2, s.4).
2. **The D14 destination move** off the legacy `opal-data-bd` path.
3. **The per-firm as-of consequence for `IRPT_FNTEND`** -- each firm's frontier picks its own date; today all three
   read `2026-09-16`.
4. **`W2-S57`** -- `REFRESH_NOOP_SAME_FRONTIER` never fires against a real manifest history, because `last_manifest()`'s
   calendar-day walk finds the same-day DISPATCHED manifest before the COMPLETED one at the runner's business date.
   ⛔ **A detector that cannot fire on its positive case** -- tonight's third instance of that family.
5. **`S71`'s re-arm trigger** (s.7) and **`S68`'s surviving exposure** (s.6).
6. **`S56` stays ARMED**: round 4's judgment records carry `file:line @ <commit-ish>`, or it produces a fourth instance.

---

## VERDICT

⛔ **ROUND 3 CLOSES. ALL NINE JUDGMENT CRITERIA PASS. ZERO of 10 FWDs REALIZED; FWD-1 and FWD-7 ADVANCE materially.
NO PRD AMENDMENT -- every outcome round 3 touched was served by a cell, and no outcome went unserved.**
⭐ **The round's signature is cells answering AGAINST their own interest -- `R33` disclosing its dispatch never re-ran
the build, `R34` refusing a verdict its instrument could not support, `R35` naming the wrong plane, `R36` volunteering
its own grant's blast radius BEFORE the apply, `R37` declining to claim a fire it did not observe. FIVE OF NINE
JUDGMENT CELLS VOLUNTEERED THE THING THAT WEAKENED THEIR OWN RESULT.**
**Round 4 is unblocked.**
