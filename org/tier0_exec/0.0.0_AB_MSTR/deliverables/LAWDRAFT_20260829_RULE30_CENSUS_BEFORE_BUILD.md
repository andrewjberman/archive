# LAW DRAFT for Andrew — Rule 30: census before build, and the placement defect that hid the Build Ladder

**Author:** `0.0.0_AB_MSTR~Z` | **Date:** 2026-08-29 | **Status:** ⛔ **DRAFT. NOT LANDED.**
**Drafted on Andrew's word** ("yes draft it", 2026-08-29, at the MSTR~Z terminal), against his own
observation that the reuse rule "doesn't seem to really be getting to the agents ever."

> ⛔ **I CANNOT LAND THIS.** `.owned-paths.yaml:2009` — `CLAUDE.md` is `lane: BASE_EXEC`
> (CTO / COO / CVO / CRO). `0.0.0_AB_MSTR~Z` is not a member. A BASE_EXEC seat lands it, or Andrew
> rules an override. **Verified before drafting, not assumed.**

---

## ⛔ SUPERSESSION NOTICE — READ BEFORE USING §3 EDIT 3

**Andrew ruled a TWO-TIER design after this draft was written** (*"both CTO at PRD level and COO at
TO level should have some kind of prior art check"*), and named `2.0.0_SA_COO~Z` to hold the pen.
**That design landed at `8139364866`** and it answers the design question this draft left open.

>> **`2.0.0_SA_COO~Z`'s DESIGN GOVERNS THE TIERING. THIS DRAFT DOES NOT.** EDIT 3 below is retired
   as a *placement* proposal — it put the census at ONE point (Rule 27 step 0) and the ruled shape
   has TWO. **Do not build against it.** <<

**Why this notice exists rather than a rewrite:** two durable records of one obligation diverge from
minute one. Rewriting EDIT 3 into a second tiering proposal would create exactly that, in a document
whose subject is not duplicating work. **This draft is hereby narrowed to the three things that are
NOT in `8139364866` and are still outstanding:**

```
  STILL MINE, STILL OPEN   §3 EDIT 1  the PLACEMENT defect (ladder in §4, mandatory read is §1-3)
                           §3 EDIT 2  rung 2 names a CLASS (completes the 22-day law call)
                           §1(c)      the SPEED-GOVERNOR carve-out -- a census is not a check
  NOT MINE                 the two-tier design, its corpora, and its criteria -> 8139364866
```
⭐ **And `2.0.0_SA_COO~Z` answered the trap this draft flagged**: the two tiers read **different
corpora** — CTO/PRD over ARTIFACTS (code, infra, graph edges, ratified terms, schemas), COO/TO over
RECORDS OF WORK (open+closed TOs, decomp cells, `.open_findings`, change_management, the registry).
**The second tier is not a smaller first tier, so it is not repetition.** That is the correct
resolution and it is theirs, not mine.

---

## 0. THIS DRAFT RAN ITS OWN RULE FIRST, AND THE CENSUS CHANGED IT

Before writing a new rule I censused whether the estate already had one. **It did, and I would have
duplicated it.**

```
  comp-find 'prior_art'    ->  8 hits / 27,929 files. The only source hit is `prior_artifact`,
                               a SUBSTRING false positive. No such field convention exists.
  comp-find 'reuse census' ->  0 hits / 27,929 files. Genuinely absent.
  comp-find 'BUILD LADDER' ->  264 hits. *** AND THIS ONE FOUND AN OPEN LAW CALL ***
```

**`org/tier1_exec/1.0.0_SA_CTO/deliverables/LAWCALL_BUILD_LADDER_RUNG2_APPLIES_TO_SCHEMA_20260807.md`**
— authored `1.0.0_SA_CTO~D`, co-signed `4.0.0_SA_CRO`, **status PROPOSAL / NOT LANDED, open 22 days.**

⭐ **So the estate had already diagnosed half of this, and I nearly legislated over it.** That is the
exact failure Andrew is describing, and the census is what caught it — which is the argument for the
rule, made by the rule, on itself.

---

## 1. THE DIAGNOSIS — FOUR REASONS, AND THE FIRST IS STRUCTURAL

**(a) THE BUILD LADDER IS IN SECTION 4. THE FILE SAYS "Read sections 1–3 before acting."**
`CLAUDE.md:3` sets the mandatory pre-action read at §1–3. `CLAUDE.md:89` puts the Build Ladder in
§4 (CLAIMS AND SCHEMAS). **An agent obeying the file exactly never reads the ladder during the window
the ladder exists for.** No agent has to be careless for this to fail.

**(b) RULE 21 IS IN THE MANDATORY READ BUT ANSWERS THE WRONG QUESTION.** It sits under "FINDING
THINGS FAST" and specifies *which instrument* to use once you have decided to search. **Nothing names
"I am about to build" as a trigger.** The estate has a search *preference*; it does not have a search
*reflex*.

**(c) ⛔ THE SPEED GOVERNOR ACTIVELY LICENSES SKIPPING IT, AND THIS IS THE WORST ONE.** §2 reads
*"WHEN THE NEXT CHECK WOULD NOT CHANGE WHAT YOU DO, STOP."* An agent that skips the census can cite
that correctly. **The reasoning is broken because a prior-art census IS NOT A CHECK.** A check asks
*"am I right?"*; a census asks *"is this work necessary at all?"* — and it can delete the task
entirely. The asymmetry is total and the file currently argues the wrong way.

**(d) YOU CANNOT GATE AN ABSENCE.** Hooks intercept tool calls. **There is no tool call for
"did not search."** The comp-rail fires when an agent searches WRONG; it is structurally incapable of
firing when an agent searches NOT AT ALL. That is why this has stayed, in the file's own phrase, an
imperative enforced by nobody.

---

## 2. ⛔ AND THE 08-07 LAW CALL PARTIALLY LANDED — IN THE EXACT SHAPE IT WARNED AGAINST

The law call's finding: rung 2 stated its scope as an **ENUMERATION OF TWO** (code, infrastructure),
and the estate's ratified `limitation_class_form` says *"an enumerated list of three silently
authorises deleting a fourth."* Schema was the silently-excluded fourth. `4.0.0_SA_CRO` ran rung 2
**correctly, twice, against code**, then spent three revisions designing an ontology layer whose every
capability was already live on **961 graph edges**.

```
  PROPOSED (08-07)  "(2) The estate already has it — in ANY form it can already exist in."
  WHAT LANDED       "(2) the estate already has it — comp-which for code,
                     comp-estate --layers/--definitions for infra + RATIFIED TERMS"
```

>> ⛔ **THE CLASS FRAMING DID NOT LAND. THE ENUMERATION GREW FROM TWO TO THREE.** The remedy for an
   under-enumeration was applied *by extending the enumeration* — which is precisely the defect the
   law call was written to name, committed in the act of partially adopting it. **A taxonomy, an enum,
   a status vocabulary, a routing table, a naming convention and a HALF-FINISHED INSTANCE OF THE THING
   ITSELF are all still outside the list.** <<

---

## 3. THE THREE EDITS

### EDIT 1 — move THE BUILD LADDER from §4 to §3, unchanged in text

Cut `CLAUDE.md:89-92` and paste it into §3 (FINDING THINGS FAST) directly after rule 21. **No wording
change in this edit.** It removes the structural excuse in §1(a) and costs nothing: §3 is already
mandatory reading, and "find it before you build it" is what §3 is about.

### EDIT 2 — rung 2 names a CLASS (completes the open 08-07 law call)

> **(2) the estate already has it — IN ANY FORM IT CAN ALREADY EXIST IN**, never an enumeration:
> code, infrastructure, schema, taxonomy, vocabulary, convention, **or a half-finished instance of
> the thing itself.** `comp-which`/`comp-find` for code; `comp-estate --layers/--definitions` for
> infra + ratified terms; the open-work surfaces for a partial. **A duplicated SCHEMA is worse than
> duplicated code — code is deleted by whoever notices; a ratified token needs a naming act to
> retire.** `…/LAWCALL_BUILD_LADDER_RUNG2_APPLIES_TO_SCHEMA_20260807.md`.

Attribution: the class framing and the final clause are `1.0.0_SA_CTO~D`'s and `4.0.0_SA_CRO`'s from
08-07. **The only thing I added is "or a half-finished instance of the thing itself."**

### EDIT 3 — ⛔ RETIRED AS A PLACEMENT PROPOSAL. See the SUPERSESSION NOTICE above.

**`8139364866` (`2.0.0_SA_COO~Z`, Andrew-ruled two-tier) governs WHERE the census fires and WHAT
each tier reads.** The text below is kept ONLY for the wording of the speed-governor carve-out and
the three-valued answer (ABSENT / PARTIAL / PRESENT), which whoever lands the CLAUDE.md edit may
lift verbatim. **It is not a competing placement.**

#### Retained wording — the carve-out and the answer set

`30` is free (in-file: 13,14,14a,16,20,21,22,22a,24,27,28,29; annex/cloud-ops hold 4–12,15,17–19,23,25,26).

> 30. **BEFORE BUILDING ANYTHING, CENSUS WHAT THE DIRECTIVE ITSELF NAMES — ON TWO DIFFERENT
>     MECHANISMS, NEVER ONE PLUS A CONFIRMATION.** (1) `comp-find` for the **HISTORICAL** plane —
>     what the corpus has EVER carried; (2) a relevant **SCOPED comp-tool** for **CURRENT STATE**,
>     the same object through an alternate lens. **On each, watch the COVERAGE UNIVERSE —
>     DENOMINATOR, HEAD, TIMESTAMP** — because a comp-tool's answer is scoped to a corpus it will
>     name and you will otherwise not read. The answer is ABSENT (build) · PARTIAL (finish it, do
>     not restart) · PRESENT (use it) — **and you may not assert which without both.**
>     ⛔ **THIS IS NOT A RULE-22 CHECK AND THE SPEED GOVERNOR DOES NOT APPLY** — a check asks *am I
>     right*, a census asks *is this work necessary at all*, and it can DELETE THE TASK.
>     **COST: two calls, seconds. NON-APPLICATION: answering a question, reading, measuring,
>     debugging an existing thing — anything that creates no file, tool, schema, or infrastructure.**

⛔ **THE TWO-MECHANISM FORM IS ANDREW-DIRECT, 2026-08-29 ~04:0xZ, AND IT REPLACED A WEAKER DRAFT —
INCLUDING MINE.** Verbatim:

> *"a better approach is to just use two different mechanisms. use `comp-find` for historical search,
> use a relevant scoped comp-tool to view the same thing from an alternate lens in current state
> (watch denominator/head/timestamp aka nature of coverage universe for comp-tools)"*

**My own wording above originally said "`comp-find` the request's own nouns and PRINT THE
DENOMINATOR" — ONE mechanism.** `2.0.0_SA_COO~Z` had independently written "census the records plane,
then corroborate against an artifact plane," which is **one mechanism plus a confirmation.**
>> ⛔ **BOTH OF US WROTE THE SAME DEFECT AND HIS CORRECTION NAMES IT: A CONFIRMATION RUN TO SETTLE A
   QUESTION THE FIRST MECHANISM ALREADY ANSWERED INHERITS THAT MECHANISM'S FRAME.** A TEMPORAL tool
   and a CURRENT-STATE tool can disagree in ways a follow-up check structurally cannot — which is
   CLAUDE.md Rule 22's own "a second seat's confirmation via the FIRST seat's method is REPETITION"
   applied to tools instead of seats. **Two independent drafters missed it; the sovereign did not.** <<
⭐ **And the coverage-universe clause is the operative half, not a caveat.** `comp-find` prints
`corpus=default` (tracked + untracked-not-ignored) and a scoped comp-tool answers within a corpus of
its own — **a zero from either is scoped to a universe you must read off the output, or the absence
verdict is unfounded.**

**The cost-and-non-application clause is mandatory** per CLAUDE.md's own "Changing this file" rule
(*"A new verification rule STATES ITS COST AND NON-APPLICATION or it does not land"*). It is stated
above rather than left for a reader to infer.

---

## 4. WHAT THIS DOES NOT DO, STATED PLAINLY

⛔ **Prose does not enforce. This draft is three paragraphs of prose and it will decay exactly like
the ladder did** unless one of the following also happens — and CLAUDE.md's own preference is gates
over prose:

1. **A form that cannot be completed without the census.** The estate already has this shape in
   proof-of-spec. A PRD/TO carrying `prior_art: {query, hits, denominator}` is un-fakeable in the way
   "check before you build" is not — **you cannot type a denominator you did not measure.** This is
   the same mechanism the 08-07 law call floated as its option 3, and I think it is the real fix.
2. **A PreToolUse nudge on Write/Edit of a NEW file when the session has made zero `comp-*` calls.**
   This is the one gateable moment: you cannot intercept "did not search", but you CAN intercept
   "creating a file having never searched." A nudge, not a deny — a deny here would be a
   manufactured gate and Rule "DO NOT MANUFACTURE FRICTION" forbids me implementing one uninstructed.

**I have not implemented either.** Both are gate candidates and gates are Andrew's call.

## 5. THE HONEST SELF-INDICTMENT

Tonight `comp-find` put a 4-day-old provenance defect beyond doubt in ONE call, with the DEF-band
line, the denominator, and four historical instances of the same drift — none of which a grep would
have surfaced. **In the same session I wrote `.tools/schedule-check.py` without ever censusing
whether the estate already had a timetable compiler.** I did not consider it. The rule is not failing
to reach junior seats; it did not reach the seat writing this draft, five hours ago.

## 6. ROUTING

```
  LAND IT        a BASE_EXEC seat (1.0.0_SA_CTO / 2.0.0_SA_COO / 3.0.0_SA_CVO / 4.0.0_SA_CRO)
  ALSO CLOSES    LAWCALL_BUILD_LADDER_RUNG2_APPLIES_TO_SCHEMA_20260807.md -- open 22 days,
                 partially landed, its class framing still outstanding
  THREE SURFACES per CLAUDE.md: commit + same-turn MCP broadcast to live seats + push state
                 STATED in the broadcast
  ⚠ CONFLICT     CLAUDE.md is a shared-surface file and CLOUD/SITEZ have ALREADY DIVERGED on it
                 (CLOUD 19,990 B / SITEZ 18,704 B, different sha256, measured 2026-08-29).
                 This edit lands on ONE fabric and becomes an /integrate overlap. Expected, not
                 a defect -- but the resolution should be a UNION, and whoever lands it should
                 say so in the broadcast.
```
