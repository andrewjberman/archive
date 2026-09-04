# INSTRUMENT MISATTACHMENT: four measured instances in one exchange, and what comp-read could absorb

**Author:** 4.0.0_SA_CRO~Z (Chief Research Officer, site-Z lane)
**Home:** org/tier1_exec/4.0.0_SA_CRO/
**Recon ID:** RCN-0007 -- registered in RECON_REGISTER.md
**Date:** 2026-09-03. **Commissioned:** Andrew-direct at this terminal, verbatim: *"write a brief about this and commit it"*,
following *"is there an obvious way to make this tool better from this?"*
**Subject:** `.tools/comp-read` (1250 lines), exercised against `.tools/deploy_ledger.py` and
`org/missions/D12/NFRA/NFRA_OPSEC202609/surprise-channel/investigations/INVESTIGATION_v1.md`.

---

## 0. What this is, and its denominators

A teardown of an INTERNAL instrument, in the RCN-0004 / RCN-0006 pattern (the target is Opal's own
estate rather than a competitor). It is not a defect report against comp-read: **every instrument
call in it returned a CORRECT result.** It is a report on the gap between what those calls measured
and what their readers concluded.

```
  EVIDENCE BASIS -- every figure below was re-run at a stated vintage, not recalled
    subject A   .tools/deploy_ledger.py            1328 lines / 43 sections   @79c0e68071, worktree clean
    subject B   INVESTIGATION_v1.md                1969 lines (this seat) vs 2017 (peer) -- SEE 1.4
    subject C   .tools/comp-read                   1250 lines / 32 sections
    seats       4.0.0_SA_CRO~Z, 0.0.0_AB_MSTR~Z, 3.0.0_SA_CVO~Z
    calls       9 comp-read invocations, 2 modes (--for, --enumerate)
```

**DECLARED GAP, in-band:** no base rate was measured for anything in section 3, and section 4's
`--schema` proposal is UNTESTED for feasibility -- comp-read's AST backend was not read to confirm it
can enumerate dict literals by binding. Both are marked at their point of use. Nothing here was
measured on a second device.

---

## 1. THE FINDING: four errors, one class

⛔ **In every case the tool was CORRECT, the answer was attached to a DIFFERENT QUESTION than the one
asked, and NO OUTPUT SAID SO.** Three of the four are this author's; one is a peer's.

| # | call, pattern verbatim | it answered about | it was read as | outcome |
|---|---|---|---|---|
| 1.1 | `--for` "what fields does a LEG carry, is there any field for ATTEMPTED, and who writes them" | the file's commentary | the file's schema | 1 of 6 fields returned; both schema constructors unread |
| 1.2 | `--enumerate 'attempt'` | one token | the concept ATTEMPTED | true zero, and a peer offered to retract it |
| 1.3 | `--enumerate 'leg\['` | bracket-access | the predicate set | 17 hits; predicate count reported as 5, true count 7 |
| 1.4 | `--enumerate 'deploy_ledger\|attempted\|write-ahead'` | the ASKER's vocabulary | the row's subject | FALSE ABSENCE: concluded no row existed; Z-S47 exists |

### 1.1 A ranker cannot answer an existence question
The question carried three limbs. A salience ranker produces ONE ranking, so it served the limb the
file talks about most. The two functions defining the leg schema (`_canonical_pipeline_legs` :227-259,
`_lambda_leg` :262-286) never entered the salient set; one sat in the unread ledger at score 2.01,
beneath commentary at 4.36. **A ranker can only show what it found, so it fails toward
absence-looking output whether or not the thing exists.**

### 1.2 A class is not a pattern
Reported as "attempt-class tokens: 3." The peer measured 0. Both were TRUE at one vintage:

```
  'attempt'                                          -> 0 hits
  'attempt|applied|started|initiated|fired|invoked'   -> 3 hits, DOCSTRING 1 / COMMENT 2 / CODE 0
```

⛔ **A census without its pattern is a citation without its vintage.** Neither number was wrong; the
missing pattern made them look contradictory, and the peer then volunteered to withdraw a sound
measurement to resolve a conflict that did not exist. **An unpublished pattern does not merely block
reconciliation, it invites a correct result to be retracted.**

⛔ **AND THE WIDER PATTERN WAS NOT THE BETTER INSTRUMENT.** It caught anything only because six
synonyms were guessed, and **there is no denominator on the synonyms not guessed.** A field named
`ran_at` defeats both patterns and returns an honest zero with a false conclusion.

### 1.3 A denominator certifies the SWEEP, not the PATTERN
The `leg\[` probe is a bracket-access probe. The predicates appeared in five of its 17 hits **as
incidental content on lines matching for another reason** (`leg["id"]`, `state["legs"]`). The count
was read off the line and given the sweep's denominator. The anchored probe:

```
  'not [a-z]+\.get\("proof"\)'  ->  7 hits / 1328 lines, CODE 7
  :346 :355 :441 :467 :707 :758 :1081     (:441 and :758 bind `lg`, invisible to `leg\[`)
```

**A side-effect finding carries no denominator, and this one was given one.** CLAUDE.md Rule 22 states
this exactly; it was cited in the same report that broke it.

### 1.4 A positive control proves the ENGINE and the FILE. It never proves the PATTERN.
Concluding that no row existed on the channel, this seat ran a control: `'Z-S4[0-9]'` returned 100
hits with rows Z-S40..Z-S44 present. **The control PASSED and did not save the conclusion.** It fired
on ROW IDS while the failing probe's risk lived entirely in its SUBJECT TERMS, so it shared none of
that risk. Z-S47 exists and is written in the row's own vocabulary ("the contract gap", NEVER-2, leg,
target, proof) -- none of the probe's tokens.

⛔ **Two further tells sat unread in that same output.** The control matched only S40-S49 by
construction, so it could not see S50+. And the file read 1969 lines here against 2017 at the peer's
HEAD: **a stale vintage, undetected, on the very read used to claim an absence.**

>> **THE TRANSFERABLE SENTENCE, and it is `3.0.0_SA_CVO~Z`'s formulation of this author's finding:
   A CONTROL THAT SHARES NONE OF THE PROBE'S RISK VOUCHES FOR NOTHING.** Choose the control on the
   axis the probe can fail on, not on the axis that is easy to verify. <<

---

## 2. THE TOOL GAP, MEASURED

comp-read has **exactly one** degeneracy warning. Census of its own source:

```
  .tools/comp-read --enumerate 'WARN'  ->  2 hits / 1250 lines / 32 sections
    :566  CODE       the FRAGMENT warn  ("an anchored probe would report ZERO against this file")
    :405  DOCSTRING  its design rationale, in the author's words: RETURNED AND PRINTED, NOT JUST TESTED
```

⛔ **Both belong to `--enumerate`. `--for` has none.** And `--for` is the mode CLAUDE.md mandates as
the estate's default read instrument, over measured traffic of ~340 single-file reads/day.
**The mode with no self-check is the one everything routes through.**

The principle is already articulated at `:405` by comp-read's own author -- print the degeneracy, do
not merely test it. **The gap is that it was applied to a degenerate PATTERN and never to a degenerate
QUESTION SHAPE.** Every proposal below is a continuation of an argument this tool already makes.

---

## 3. WHY THIS IS ALREADY LAW

CLAUDE.md: **A VALUE MUST CARRY ITS CLAIM, in a field a consumer can reject on**, and *the consuming
half is the whole mechanism.* comp-read prints values that do not carry their claim: its numbers say
what was found and never what they are evidence OF.

The law also anticipates this exact hazard and scopes the worry one mode too narrowly. It warns that
*"a comp-read that failed toward ABSENCE would be the estate's DEFAULT read instrument failing toward
absence, strictly worse than the grep it replaces"* -- written about `--enumerate`'s design.
**Instances 1.1 and 1.4 show `--for` has the property the law was worried about.**

---

## 3a. WHY `--for` EXISTS, AND WHY DEFAULTING TO `--enumerate` WOULD HAVE MADE THIS WORSE

**Andrew-direct at this terminal, verbatim:** *"is there a reason why we have --for? it seems like if
you defaulted to --enumerate that would be better in every case. is there any case where --enumerate
is not the best use? or is what youre saying that regardless of how the function works, it should have
enumeration, even if the intent is not explicitly to enumerate?"*

⛔ **THE PREMISE INVERTS ON THIS BRIEF'S OWN DATA. THREE OF THE FOUR ERRORS IN SECTION 1 ARE
`--enumerate` ERRORS.**

```
  1.1  --for        ranked commentary over schema        <- the ONLY --for failure
  1.2  --enumerate  wrong token for the concept
  1.3  --enumerate  probe aimed at a different question
  1.4  --enumerate  FALSE ABSENCE on the asker's vocabulary
```

**Defaulting to `--enumerate` would have prevented one of four and caused the other three.**

### The two modes fail in OPPOSITE directions, and neither is the safe one

```
  --for        fails toward FALSE COMPLETENESS   always returns a ranked something; it looks like an answer
  --enumerate  fails toward FALSE ABSENCE        returns a clean, honest zero when your token is wrong
```

⛔ **THE ASYMMETRY THAT SETTLES IT: `--enumerate` REQUIRES THE VOCABULARY YOU DO NOT YET HAVE.** You
must name the token before you can count it -- and not knowing the file's vocabulary is *precisely the
state you are in when you open an unfamiliar file.* Instance 1.4 is the pure case: the probe used the
ASKER's words, the row used its own, and the count was 1 where the truth was a live row.

**`--enumerate` could not have answered 1.1 at all.** The question was *what fields does a leg carry*;
answering it by enumeration requires guessing the field names, which IS the question.

⚠ **AND A FALSE ABSENCE IS THE WORSE FAILURE**, because a zero TERMINATES inquiry while a bad ranking
merely fails to end it. In 1.4 the zero produced a confident STOP and redirected the search. A ranked
miss leaves the reader still looking.

>> **SO THEY ARE SEQUENTIAL, NOT ALTERNATIVES: `--for` to learn the file's SHAPE and VOCABULARY,
   `--enumerate` to census a term ONCE YOU KNOW IT IS THE RIGHT TERM.** Retiring `--for` would remove
   the only mode that works before you know what to ask, and would hand every unfamiliar-file read to
   the instrument that fails silently. <<

### The second half of the question is the better framing, and it SUPERSEDES P1's narrow form

**Yes -- the disclosure belongs in EVERY mode regardless of intent, not in a mode switch.** That is the
correct generalization and it is stronger than what this brief first proposed.

Note what `--for` already does: its **UNREAD LEDGER** ("you have been shown 28 of 1328 lines and 6 of
43 sections") is a coverage denominator, and it is honest. **But COVERAGE is not CLAIM.** It says how
much was not seen; it never says *this is a ranking and cannot support an absence claim.* Those are
two different disclosures and the tool ships only the first.

⛔ **THE GENERAL RULE, which is CLAUDE.md's own value-must-carry-its-claim applied to a tool's
OUTPUT rather than to a data field: EVERY MODE STATES WHAT ITS NUMBER IS EVIDENCE OF.** For
`--enumerate` that is *"N occurrences of THIS PATTERN; a different wording returns a different N."*
For `--for` it is *"a ranking, not a census."* **Neither mode is retired; both start carrying their
claim.**

---

## 4. PROPOSALS -- flagged as PROPOSALS, not findings

**None of this is authorized, dispatched or staffed by this seat** (charter s.3: research PROPOSES on
the build side). Ranked by payoff over cost. The first three are strings and a ratio.

| # | change | cost | closes |
|---|---|---|---|
| P1 | **EVERY MODE STATES WHAT ITS NUMBER IS EVIDENCE OF** (s.3a). `--for`: *a RANKING, not a census; cannot support an absence claim.* `--enumerate`: *N occurrences of THIS PATTERN; a different wording returns a different N.* | two static strings | 1.1, 1.2, 1.4 |
| P2 | Echo the pattern on the RESULT line, not only the header. `ENUMERATE-END` currently drops it | one format string | 1.2, 1.3 |
| P3 | Print the AUTHORITATIVE:DESCRIPTIVE ratio of the salient block, as a NUMBER with no verdict | already computed | 1.1 |
| P4 | WARN when a `--for` question carries multiple interrogatives | small | 1.1 |
| P5 | A `--schema <name>` mode: find every constructor of a named structure, print the union and intersection of their keys, flag disagreement | REAL BUILD, needs a PRD | the s.5 rule |

⭐ **P3 BOOTSTRAPS ITS OWN THRESHOLD, which is why it is worth more than its size.** Two data points
exist: **3 of 18** authoritative on the read that missed, **8 of 18** on a contrast read that landed
(`lib/trading_calendar.py`, 163 lines). **Two points are NOT a band and none is proposed here** --
that would be an unmeasured exact constant, which fails closed looking principled. But printing the
ratio on every run accumulates the base rate in `comp-tool-runs.jsonl` for free: **the fix and the way
to earn its threshold are the same act.**

⚠ **P3's contrast is n=2 and DIRECTIONAL ONLY.** Qualifier density 14.9 per 100 lines on the file
that missed against 3.7 on the file that landed. That promotes "the ranker over-weights commentary on
heavily-annotated files" from asserted cause to **SUPPORTED BY ONE CONTRAST** and no further.

⚠ **P5 IS UNTESTED FOR FEASIBILITY.** comp-read's AST backend was not read to confirm it can
enumerate dict literals by binding. Treat the payoff as real and the cost as UNKNOWN.

---

## 4a. IS THE OUTPUT TOO MUCH TEXT? MEASURED, AND THE ANSWER IS "NO, EXCEPT IN ONE BLOCK"

**Andrew-direct at this terminal, verbatim:** *"also is the text an agent receives from this too much
information?"*

⛔ **A PRIOR OF THIS AUTHOR'S WAS FALSIFIED BY THE MEASUREMENT AND IS RECORDED RATHER THAN QUIETLY
DROPPED.** Before measuring, this seat expected the repeated didactic prose to be the bulk of the
frame. **It is 5 lines.** Diffed across three `--for` outputs on three different files, only 5
non-blank lines are byte-identical in all three. **Almost the entire output varies with the file, so
"the tool repeats itself at every agent" is FALSE.**

```
  --for OUTPUT SIZES, captured and counted (not estimated)

  SUBJECT                    FILE LN   OUTPUT LN   SHAPE LN   SHAPE %   MARKED << / UNMARKED
  .tools/deploy_ledger.py       1328         108         45       41%        6 / 37
  org/XXX.md                     596         162        102       62%        6 / 94
  lib/trading_calendar.py        163          49         13       26%        2 /  9

  fixed text identical across all three: 5 lines
  compression vs reading the file: 12.3x / 3.7x / 3.3x
```

### The verdict has three parts

**(1) NOT too much, for the job it does.** 108 lines to map a 1328-line file is a 12x compression, and
this seat used it exactly that way today: the SHAPE block is what turned a hunt into one precise
second read at `:227-286`. **That is the tool's best feature and it should not be cut.**

**(2) ONE BLOCK IS MISCALIBRATED, AND IT IS `SHAPE`.** It is unbounded by design -- the header says
*"all N, never truncated"* -- and it scales with **SECTION COUNT, not with relevance or file size.**
On `org/XXX.md` it is **62% of the output**, and **94 of its 102 rows are unmarked.**

⭐ **THE COST AND THE VALUE COME APART, WHICH IS THE ACTIONABLE PART.** Output cost tracks SECTION
COUNT; value tracks FILE SIZE. `XXX.md` is the smaller file (596 lines) and produces the LARGER output
(162 lines); `deploy_ledger.py` is more than twice its length and produces 108. **A section-dense file
gets the worst deal, and a section-dense file is exactly where an agent most needs the map.**

**(3) THE FIX IS SMALL BECAUSE THE TOOL ALREADY KNOWS THE ANSWER.** SHAPE already marks
question-relevant rows with `<<`, and the marked count matches the SALIENT set exactly (6/6/2). So the
relevance signal is computed and then discarded at render time.

| P6 | Collapse UNMARKED runs in SHAPE into one counted line (e.g. *"lines 550-660: 8 sections, none scoring above 0.5"*), keeping every marked row verbatim | small | cuts ~60% of the output on section-dense files |

⛔ **THIS PRESERVES "NEVER TRUNCATED" RATHER THAN BREAKING IT.** Nothing is hidden and the denominator
is still printed -- a collapsed run states its own count. The property that matters is *the reader can
see that N sections exist and were considered*, not *N lines were emitted*.

### ⛔ THE SELF-CHECK THIS SECTION OWES, because it cuts against section 4

**Do NOT cut the claim-carrying lines to save space.** The 3-line `CONTRADICTIONS: none detected
(intra-file signature claims only)` block is the tool **stating an absence WITH ITS SCOPE** -- which is
precisely what P1 asks it to do MORE of. **A brief that proposes adding claim disclosures in section 4
and then trims them in section 4a would be arguing both sides.** The finding is not *less text*. It is
**less of the text that does not vary, and none of the text that carries a claim.**

---

## 5. THE RULE THAT SHOULD OUTLIVE THIS BRIEF

⛔ **A SCHEMA QUESTION IS NOT ANSWERED UNTIL EVERY CONSTRUCTOR IS FOUND AND SHOWN TO AGREE.**

A leg carries six fields, and the set is CLOSED -- measured, not inferred. Three constructors agree
(`:245-257`, `:280-285`, `:301-302`), and a `leg\[` census returns 17 references of which **only two
are writes** (`:341` proof, `:342` closed_at), so nothing anywhere adds a key outside them:

```
  id | kind | target | proof_required | proof | closed_at
```

**A read that surfaced only ONE constructor would have produced the same six fields and the same
confidence, one disagreeing constructor away from wrong.** This is the estate's scoped-check law:
*a check scoped to the members cannot see a defect in what the members share.*

**Revised operator order** (the first subsumes the second, which is the correction a peer supplied):

```
  1. ENUMERATE THE ENUMERABLE SET, NOT THE ABSENT TOKEN.
     "What is the complete field list" survives a rename. "Is there a field for X" does not.
  2. EVERY CONSTRUCTOR, AND SHOW THEY AGREE.
  3. PUBLISH THE PATTERN AND THE VINTAGE, NEVER THE CLASS.
  4. CHOOSE THE CONTROL ON THE AXIS THE PROBE CAN FAIL ON.
  5. TREAT THE OUTPUT AS AN INDEX, NOT AN ANSWER.
  6. SPLIT COMPOUND QUESTIONS -- and note the cost INVERTS: the --for frame is ~90 lines per call
     against ~15 for --enumerate, so splitting is CHEAPER in context, not dearer.
```

---

## 6. WHAT IS NOT A TOOL PROBLEM

**Instance 1.2 is entirely operator error and the tool was blameless** -- comp-read printed
`enumerate: 'attempt'` on its own face and this seat transcribed prose over it. Recorded separately so
the proposal list is not judged on a failure it does not own. **A fix list that absorbs operator
failures gets measured against them and loses.**

---

## 7. OWNERSHIP AND ROUTING

**comp-read authorship, last 12 commits:** `3.0.0_SA_CVO~B` 7, `0.8.0_AE_CloudComp` 2,
`3.0.0_SA_CVO~C` 1, `1.0.0_SA_CTO~P` 1, `0.8.0_AE_CloudComp~A` 1. Head @dc944897c5.
**Suggested owner: the CVO lane, CloudComp second.** Research names suggested owners; it does not
staff them.

**Downstream, already in flight and NOT part of this brief:** the eight sites that define "open leg"
in `deploy_ledger.py` (seven predicates plus the renderer at `:211`) belong on
NFRA_OPSEC202609 row **Z-S47** (`3.0.0_SA_CVO~Z`, the CLOSED-direction carrier), beside Z-S42/Z-S44.
The INSTANCE is that project's r2b ledger; **the CLASS is a fabric item on the deploy-ledger contract
and closing NFRA_OPSEC202609 would not close it.**

**Provenance note.** Instances 1.3 and 1.4 were found by `0.0.0_AB_MSTR~Z` against this seat's work,
and 1.2's better half by the same seat against its own. The sentence in s.1.4 is `3.0.0_SA_CVO~Z`'s
formulation. **Recorded because the method rests on it: none of the four was caught by the seat that
made it, and the round trip is what produced the finding.**
