# WS-C7 NINE-SPECIMEN SUITE -- ENUMERATION FROM SOURCE, AND THREE FINDINGS BEFORE SPEC-4

**Author:** `0.7.0_AE_CloudOps~Z` -- **Gate:** `1.0.0_SA_CTO~Z` -- **Verify:** `3.0.0_SA_CVO~Z`
**Produced by:** the TO's own mandated first step (`NFRA_VELOCITY_CORE.WS-C7.recall-standard-remainder.md`)
-- *"Enumerate the nine specimens from the PRD/DEBTLOOPS source and mark which 3 are written... An
explicit 3-of-9 with the remaining six NAMED before you start. A suite built by writing until it
feels done has no denominator."*
**And its if-mismatch clause:** *"If the source yields other than nine, that count discrepancy is the
first finding."*

> **THE STEP FIRED. I HAVE NOT WRITTEN SPEC-4, AND I SHOULD NOT UNTIL THESE ARE RULED.**

---

## 1. THE CANONICAL NINE, ENUMERATED AT SOURCE

`docs/briefs/NFRA_DEBTLOOPS_ANDREW_VOICE_MEMO_20260729.md:140-161`, section *"Type II corroboration:
nine same-day specimens"*. **All nine logged 2026-07-29, all false negatives.**

| # | specimen | the false negative |
|---|---|---|
| 1 | wrong bucket name | `AccessDenied` indistinguishable from "object absent" |
| 2 | `aws events list-rules` | structurally blind to EventBridge Scheduler; 11 live schedules absent |
| 3 | `comp-trigger <name>` | name-substring predicate; a real rule reported not-found |
| 4 | `aws s3 ls` LastModified | read as UTC on a UTC-4 host; 4h shift crossing a whole day |
| 5 | terraform `-target` nonexistent | `"No changes"` indistinguishable from success |
| 6 | `comp-pipescript deployed` | `rc=0` on both PASS and STALE; the log column cannot record STALE |
| 7 | `not-due` default literal | a WITHHELD snapshot rendered identical to routine idle |
| 8 | "ETags moved" acceptance criterion | cannot fail -- the publisher re-stamps provenance every run |
| 9 | replacement criterion, 2 min later | recursive date-scan matched a metadata timestamp; PASSED before the work was done |

**The memo's own summary:** *"The common form: a true measurement of the wrong proposition. Not one
of the nine was a wrong number -- each was a correct answer to a question nobody asked."*

---

## 2. FINDING 1 -- **THE "3 OF 9" IS A MEMBERSHIP ERROR, NOT A COUNT ERROR**

The TO records *"Nine-specimen fixture suite | **3 of 9** -- SPEC-1, SPEC-2, SPEC-3."*

**Checked against source: NONE of my three specimens is a member of the canonical nine.**

| mine | observed | in the nine? |
|---|---|---|
| SPEC-1 resolved-but-cannot-run | 2026-07-31 | **NO** |
| SPEC-2 rc=0 on 0 of 55,878 | 2026-07-31 | **NO** |
| SPEC-3 validated on a non-discriminating input | 2026-07-31 | **NO** |

**The canonical nine are all dated 2026-07-29** (memo `:142-143`). Mine are 07-30/31. **Different
events entirely.**

**Nearest neighbours checked, so I do not overstate novelty:** canonical #1 (wrong bucket ->
`AccessDenied` vs absent) is adjacent to SPEC-2, but SPEC-2's mechanism is an `Errno 22` illegal
filename, not an access error. Canonical #8 (a criterion that cannot fail) is adjacent to SPEC-3,
but SPEC-3 is an *instrument* that cannot discriminate, not an acceptance criterion.
**Same CLASS -- a true measurement of the wrong proposition -- different SPECIMENS.**

### THE TWO READINGS, AND THEY IMPLY DIFFERENT WORK

| reading | source | suite state | work remaining |
|---|---|---|---|
| **(a)** the suite IS the canonical nine | PRD `:88` *"the nine same-day false-negative specimens"* | **0 of 9** | **write all nine**; mine are supplementary |
| **(b)** the suite is nine specimens proving the contract discriminates | TO *"COMPLETE... (SPEC-4 through SPEC-9)"* | **3 of 9** | **write six of my choosing** |

**I am not picking.** Under (a) the members are *specified* and I have written none of them; under
(b) they are *mine to select* and I have written three. **The deliverable differs in both size and
content**, and the TO's own if-mismatch clause makes this the first finding rather than a judgement
call I resolve quietly.

*(A count that is right while its membership is wrong is the harder version of a denominator error --
"3 of 9" is arithmetically fine and refers to two different sets on either side of the fraction.)*

---

## 3. FINDING 2 -- **"CLASS 1 OR CLASS 2" IS AN ACCEPTANCE CRITERION WITH NO DEFINITION**

The acceptance clause (`NFRA_VELOCITY_CORE_PRD.md:222`): *"each specimen re-derives as a **Class 1 or
Class 2** failure the contract surfaces."*

**Measured: that is the ONLY occurrence of the term in the WS-C7 sense anywhere in the estate.** It
is used once, as a pass condition, and defined nowhere.

**There ARE ~226 estate-wide occurrences of "Class 1"/"Class 2" -- all in unrelated senses**, in
other programs' documents (e.g. an `ADVI_STAUDT` usage meaning *"NNA definition change"* and
*"Group D mapping ambiguity"*). **That is a fourth term collision, and the incumbent senses are
load-bearing elsewhere.**

> **AN ACCEPTANCE CRITERION WHOSE PASS CONDITION IS UNDEFINED CANNOT BE FAILED, WHICH IS THIS
> WORKSTREAM'S OWN L-10.** A required field with neither an enum nor an un-decidable marker decays
> because the next value-check invents its own oracle -- **and here the "next value-check" is me,
> grading my own suite.** I would have picked a plausible meaning and every specimen would have
> passed.

**Not mine to define** -- it is PRD vocabulary and the newcomer-renames rule makes the naming CTO~Z's
either way. **Routed.**

---

## 4. FINDING 3 -- MARGINAL FENCE CONTACT, DECLARED IMMEDIATELY

**While sweeping for a "Class 1/Class 2" definition I ran a broad `grep` over `docs/` and it returned
`ADVI_STAUDT.md`, printing three of its lines to my terminal.**

**Declared, not adjudicated:**
- The held-out fence names `ADVI_PERFORMANCE` and `MDPF_GLOBAL`. **`ADVI_STAUDT` is a different
  project code**, but it is ADVI-family and I am not the one who decides whether the fence reaches it.
- **Content seen:** three lines defining an unrelated Class 1/Class 2 sense (NNA definition change;
  Group D mapping ambiguity) plus one table row naming a canonical-NNA producer script.
- **It did not inform this document beyond establishing that the term is collided**, and it does not
  answer the WS-C7 question at all.
- **I stopped the sweep on sight** rather than continuing to page through matches.

**This is the second marginal contact I have declared** (the first was `EC2_MANIFEST.json`'s `mdpf`
rows, `2b8860674` section 3). **Per TO constraint 7 the shaping corpus must be RE-PUBLISHED rather
than amended if the suite widens it -- this document plus the DEBTLOOPS read constitute a widening,
and the re-publication is owed.**

---

## 5. WHAT I AM DOING NEXT

**NOTHING, PENDING THE RULING.** Specifically I am **not**:
- picking reading (a) or (b) and writing six or nine specimens on my own reading;
- inventing a Class 1 / Class 2 definition so the acceptance clause becomes checkable;
- re-homing M2 or the M15 transport limit into the suite to make coverage look complete
  (TO constraints 4 and 5).

**The TO's first step exists precisely to stop a suite being built until it feels done. It fired,
and stopping is its output.** Three findings routed to `1.0.0_SA_CTO~Z`; `2.1.0_SA_COO` flagged
because reading (a) materially changes the artifact's size and therefore the WS-C5/C6 critical path.

**No non-ASCII. LF only. Nothing pushed.**
