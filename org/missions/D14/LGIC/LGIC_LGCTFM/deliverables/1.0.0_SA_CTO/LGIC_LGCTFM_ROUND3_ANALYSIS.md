# `LGIC_LGCTFM` ROUND 3 -- L10 ROUND ANALYSIS (`1.0.0_SA_CTO`)

**Slug:** `3.0.0_SA_CVO`, msg 98093, off L9 @`71d0c885fd`. **Date:** 2026-09-19 ~00:5xZ.
**Round state as slugged:** channel 44 items, **0 undispositioned, 0 unknown `adjudicates` targets, 0 GRADUATED
without a remediation row, 0 open orders of 21.** 3 judgment criteria PASS, 7 graduated with a carrier each,
5 dismissed.

## 0. COVERAGE READ -- **NO PRD ADDENDUM IS OWED**

The PRD carries **FWD-1 .. FWD-10** (`endpoint_outcomes`, `:11`). Round 3's cells served the engine-design
requirement and its verification legs; **the slug names no outcome that no cell served**, and my own read of it
finds none. ⭐ **The round-3 design requirement I set (R-81) was the round's subject and it was met**, so the
`/open-calls --adjudicate` PRD-addendum path is NOT entered. Round 4 is a recut, not a re-issue.

⚠ **FWD-4 REMAINS `APPLIED, NOT REALIZED` AND ROUND 3 DOES NOT MOVE IT.** Its DONE WHEN is EXERCISED -- Andrew has
read the list for one subject -- and that has not happened. Nothing in this round is evidence for it, and I am not
counting the round's success toward it. **FWD-6 is likewise untouched** (its ACCEPT names the 49 Financial
migration, which waits on `ADVI_FIRMBKTS`).

## 1. THE THREE JUDGMENT CRITERIA -- ACCEPTED, AND THE REASON IS THE INSTRUMENT, NOT THE VERDICT

I accept `R2R3-AC4`, `E5R3-AC5` and `P2R3-AC4` as PASS. ⭐ **What earns the acceptance is that `3.0.0_SA_CVO` ran
its OWN instruments rather than reading the worker's quotation** -- it imported `lib/lgctfm_render.py` and rendered
all five contracts itself; it exercised **all three branches** of an "empty OR SHORT" criterion instead of the one
the evidence happened to show; and on `P2R3-AC4` it **stated where its own arm was blind** (arm 1 cannot see a bare
list element) and built arm 2 to close that. **A grader that names its own blindness is the only kind whose PASS
carries information.**

⭐ **AND THE `E5R3-AC5` INSTRUMENT DIFFERENCE IS REPORTED CORRECTLY.** Its live census read **13** log groups against
the walk's **9**, and the slug reports *the instrument difference, not the number* -- substring vs word-bounded, the
four extra being the `opal-assets-bd49f-*` names. ⛔ **That is the right move and the opposite of the common one:
a 13-vs-9 disagreement reported as a COUNT would have read as a coverage gap, when it is a tokenizer boundary.**

## 2. ⛔ `S32` -- THE PINNED-PROOF PROBLEM. THE SLUG FOUND THE SAFE POLARITY; **THE DANGEROUS ONE IS THE MIRROR**

**The finding, verified on my own instrument rather than taken from the slug:**
- the worker pinned its proof at `b736ee4fdf` -- **2026-09-18T16:27:12-04:00**
- `2.0.0_SA_COO~G` repaired the checker at `fd02b24c51` -- **2026-09-18T17:09:25-04:00**
- **delta 0:42:13**, the repair strictly after the pin.

So `LT-e-5`'s pinned proof records `E5R3-AC4` as **FAIL** while the arm reads **PASS at HEAD**. Both readings are
correct at their own vintage. **Nothing in the fabric re-grades a pinned proof when a fixed input moves under it**,
and the round's record therefore **understates** the cell.

### ⛔ THE CLASS, AND THE PART THE SLUG DID NOT DRAW

The slug says the class generalises, and it does -- **but it generalises in BOTH directions, and only one of them is
visible here.** This instance is an **UNDERSTATE**: the checker was BROKEN at pin time and REPAIRED after, so the
record is more pessimistic than the world. ⛔ **THE MIRROR IS AN OVERSTATE, AND IT IS THE DANGEROUS ONE: a fixed
input that REGRESSES after a pin leaves a proof reading PASS while the arm now FAILS -- and nothing re-grades that
either.** An understate costs a cell its credit. **An overstate ships a defect with a green proof attached.**

⚠ **AND THE TWO ARE INDISTINGUISHABLE FROM THE PROOF ALONE**, because a pinned proof is a snapshot that carries its
vintage but not its input's vintage. The only instrument that caught this one was **re-running the arm at L9, which
no limb requires** -- so the estate's detection rate for the overstate direction is currently *whatever the CVO
happens to re-run*.

### THE BAR THIS EARNS -- and it is cheaper than the incident that produced it

⛔ **WHEN A FIXED INPUT (a checker, a gate, a schema, a fixture) IS CHANGED MID-ROUND, EVERY PROOF PINNED BEFORE
THAT CHANGE AGAINST THAT INPUT IS `STALE-UNGRADED` UNTIL RE-RUN. THE ROUND ENUMERATES THEM AND PRINTS THE COUNT.**

⭐ **The discriminator is one command and it usually returns zero:** `git log --since=<round cut> -- <fixed-input
path>`. **No commits -> no proof is stale and the bar costs nothing.** Commits -> re-run exactly the arms whose pin
predates them, and record the direction (UNDERSTATE / OVERSTATE / UNCHANGED) per arm.
**COST:** one `git log` per round, plus one re-run per affected arm. **NON-APPLICATION:** a round in which no fixed
input changed -- which the same command proves.

**Disposition:** ⛔ **NO ARTIFACT IS REWRITTEN AND NO PROOF IS RE-CUT.** `3.0.0_SA_CVO` is right that the remedy is
forward-looking. **Round 4's issuance carries the bar above**, and `S32` stays as the record of why.

## 3. THE TWO ROUTED ROWS -- NEITHER ASKS FOR A BUILD, AND I AM NOT ORDERING ONE

### `W1-S24` -- `comp-trigger` has no path that reads a Scheduler schedule's targets (23 of 167 entries)

⛔ **THE DEFECT IS NOT THE MISSING PATH. IT IS THAT THE TOOL DOES NOT DISCLOSE ITS OWN BLINDNESS**, and the proof of
that is in the row: **TWO SEPARATE PARTIES wrote orders on the premise that `--list` carries the targets.** Two
independent parties reaching the same false belief from the same output is a **tool-contract defect**, not two
careless readers.

**RULING: the remedy is a DISCLOSURE LINE IN THE TOOL'S OWN OUTPUT, not a new code path.** The estate already has
the pattern and its counter-example: `comp-iam live` prints its derive time and **both of its unverified halves**,
while its sibling `comp-iam roles` prints `(210 found)` with no vintage and silently omits a role applied two hours
earlier -- *same tool, one path disclosing and one silent* (`IRPT_BCKEND-S73`, cited in Rule 24). **`comp-trigger
--list` is in the silent class and joins the disclosing one.** `23 of 167` is the denominator it must print.
**Owner: the comp-rail surface (`NFRA_COMPRAIL`), not `LGIC_LGCTFM`.** Routed, not absorbed.

### `W1-S25` -- the commit gate's MANIFEST-ADVISORY flags two Cypher strings that ARE routed through `comp-kuzu`

The gate's own output says both *"would block in blocking mode."* ⛔ **THIS IS AN ARMED REGRESSION WITH A KNOWN
TRIGGER: the day the advisory turns blocking, a CONFORMANT caller is refused.** Under Rule 22's negative mirror
this is an **EXPOSURE**, not an incident -- nothing has been refused yet, because the flag is advisory today. ⚠ **But
it is an exposure with a SCHEDULED ARMING, which is the one kind that cannot be left to be rediscovered:** the flip
is someone's future act, and on that day the failure will read as "the new gate broke the build" rather than as a
known false positive filed weeks earlier.

**RULING: the false positive is fixed BEFORE the advisory flips, and the flip is the deadline.** Owner: the commit
gate's surface. ⛔ **Fixing it by exempting the two strings by name is REFUSED** -- an enumerated exemption lapses
silently when a string changes, which is the failure mode CLAUDE.md names on the cross-firm ban list. The classifier
learns that a string routed through `comp-kuzu` is conformant.

## 4. `S21` -- THE ROUTING DECISION THE SLUG PUT TO ME

`opal-data-inf/gold/meta/pipeline-complete.json` last written **2026-09-05**; the **ENABLED**
`mdpf-feeder-accelerator` has therefore not fired in 13 days, **while its backstop schedule hides it.**

**RULING -- WHOSE IT IS:** ⛔ **NOT `LGIC_LGCTFM`'s.** This project found it as a bystander while walking a
subject; nothing in its ENDPOINT covers a feeder's liveness, and absorbing it would make a transform project the
owner of another chain's health. **It belongs to the MDPF feeder chain's owning project**, and it enters there as a
round input, not as a new directive.

**AND THE ROW IS RIGHT TO REFUSE A MONITOR.** CLAUDE.md's standing moratorium forbids building one unless Andrew
asks, and ⭐ **a monitor is the wrong instrument here anyway: the defect is not that nobody watched, it is that A
BACKSTOP CONVERTED A LOUD FAILURE INTO A QUIET SUCCESS.** The accelerator's silence is invisible *because the
backstop schedule produces the same artifact*. **The remedy is that the two producers become distinguishable in
what they write** -- the artifact records which path produced it -- so the primary's silence is readable from the
output the estate already keeps. **That is a producer change, not a watcher**, and it needs no new alarm.

⚠ **I do NOT rule on whether the accelerator's silence is itself a defect** -- 13 days of a backstop carrying the
load may be exactly the design. **That is the owning project's call and it needs the producer's rule read, which I
have not read.** What I rule is the ROUTING and the shape of the remedy class.

## 5. WHAT ROUND 4 CARRIES

1. **The `STALE-UNGRADED` bar** (s.2), with its one-command discriminator and its both-direction polarity.
2. **`W1-S24` and `W1-S25` routed out** with their owners named; neither is round-4 work for this project.
3. **`S21` routed to the MDPF feeder chain's owner**, with "no monitor" restated and the producer-distinguishability
   remedy named.
4. ⛔ **Nothing in this analysis re-opens a graded criterion, moves a cap, or rewrites a proof.**

**PUSH STATE at write time:** the two L9 commits (`71d0c885fd`, `c69d712ebb`) were LOCAL at the slug's own
measurement and are in this seat's HEAD; `0.0.0_AB_MSTR` integrates.

---

## ADDENDUM (2026-09-19 ~02:0xZ) -- `S34`: **MY "usually returns zero" IS WITHDRAWN AS FALSE. 63 of 112.** The bar changes SHAPE rather than price

`3.0.0_SA_CVO` ran the discriminator my analysis NAMED, over the backlog, **before round 4 adopted it**, and measured
the one thing s.2 asserted instead of measuring.

**DENOMINATOR: 163 tracked proof-of-spec instances across `LGIC_LGCTFM`, `LGIC_ENFORCE`, `LGIC_CANON`,
`IRPT_BCKEND`; 112 name a fixed-input checker in their own bytes and are EVALUABLE** (`IRPT_BCKEND` contributes 0
checkers, so its 51 are OUTSIDE the population and are **not** counted as clean -- the honest handling).
**SIGNATURE HITS: 63 of 112.**

⛔ **SO "one command that usually returns zero" IS FALSE ON THIS ESTATE, AND I WITHDRAW IT.** It returns non-zero on
the MAJORITY case. ⚠ **And the consequence is the CVO's sentence, which is the part that matters: *"a bar that fires
on the majority case will either be paid in full every round or quietly skipped -- and the second is how a bar
becomes a convention."*** A skipped bar is worse than an absent one, because the record implies it ran.

### WHY I TAKE NEITHER BRANCH THE ROW OFFERED

**(a) Pay ~63 arm re-runs per round as a known cost.** ⛔ **REFUSED.** It is not the re-runs that are expensive --
each is a command the order already names -- it is that a per-round sweep of 63 is exactly the size that gets
skipped, and the row predicts it.

**(b) Narrow the trigger so it selects only the arms a commit can move.** ⛔ **REFUSED ON THE ROW'S OWN
MEASUREMENT.** It showed a file's history CANNOT decide this: `check_lt_r1.py` across 6 commits goes 61 -> 67
subcommand keys with **0 removed** (additive, cannot change an earlier arm's verdict), **but 3 of those 6 change the
line count WITHOUT changing the key set** -- they edit existing code and could. ⭐ **Any narrowing built on file
history is therefore unsound in the direction that matters**, and a trigger that is cheap because it is wrong is the
worse failure.

### ⭐ THE RULING -- (c): THE PROOF CARRIES ITS INPUT'S VINTAGE, AND STALENESS BECOMES A COMPARISON

⛔ **THE DEFECT IS NOT THE TRIGGER'S PRICE. IT IS THAT A PINNED PROOF CLAIMS A VERDICT WITHOUT CARRYING THE VINTAGE
OF THE INPUT THAT VERDICT DEPENDS ON.** That is `A VALUE MUST CARRY ITS CLAIM`, exactly: *a value must carry its
claim in a field a consumer can reject on; no such field -> you may NOT treat it as measured.*

**So: at pin time, a proof instance records the COMMIT of each fixed input it invoked.** Then
- **staleness is a ONE-LINE COMPARISON, not a sweep** -- the recorded commit against the input's commit at read time;
- **it is computed only when a proof is CONSUMED** (L9 grading, L10 coverage), never for all 112 every round;
- **and it answers the direction question too**, because the two commits are both in hand.

**COST: one field at pin time, one comparison at read time. NON-APPLICATION:** a proof naming no fixed input --
which is `IRPT_BCKEND`'s whole 51 today, and they stay outside the population rather than being counted clean.

⚠ **AND THIS IS A RECORD, NOT A GATE.** `3.0.0_SA_CVO` was right to decline designing a trigger -- *"a trigger is an
enforcement surface and designing one from this seat would be an agent-made gate"* -- and that reasoning binds me
too. **I am adding a FIELD to an artifact the estate already writes, whose consumer is the seat reading the proof.
Nothing refuses anything. No limb is armed.** If a refusing limb is ever wanted, that is Andrew's to ask for.

### WHAT ROUND 4 CARRIES, AMENDED

1. ⛔ **The s.2 bar's TRIGGER is REPLACED by the field above. Round 4 does NOT run a 63-arm sweep.**
2. **Interim, because no proof carries the field yet:** round 4 re-runs an arm **only where its verdict is actually
   relied on** at L9/L10, and records the direction. **Not all 63.**
3. **The bar's DIRECTION and REMEDY are unchanged and were never in question** -- the row says so itself, and both
   polarities (UNDERSTATE / OVERSTATE) still stand, with the OVERSTATE the dangerous one.

### RECORDED AS CREDIT, BECAUSE THREE THINGS HERE ARE RARE

⭐ It **ran a command an analysis merely named**, which is the only way an asserted cost ever gets tested.
⭐ It **reported the narrowing that FAILED** -- the round-match axis subtracted exactly zero -- when reporting only
the successful one would have looked stronger.
⭐ It **corrected its own first pass**, 134 `(instance x checker-COMMIT)` tuples down to 63 pairs, and said which
number means anything. **A seat that publishes its own discarded number is the one whose surviving number I can use.**

---

## ADDENDUM 2 (2026-09-19 ~02:3xZ) -- **MY OWN ROUTING IN s.3 WAS A DEAD LETTER.** `NFRA_COMPRAIL` is a COMPLETE project

s.3 routed `W1-S24` and `W1-S25` with: *"Owner: the comp-rail surface (`NFRA_COMPRAIL`), not `LGIC_LGCTFM`. Routed,
not absorbed."*

⛔ **TWO THINGS WERE WRONG WITH THAT, AND THE FIRST IS THE ONE I WOULD HAVE MISSED FOREVER.**

1. ⛔ **A ROUTING THAT EXISTS ONLY IN MY OWN ANALYSIS IS A NOTE, NOT A ROUTING.** I named an owner in a document
   and sent that document to `2.0.0_SA_COO~G` and `3.0.0_SA_CVO` -- neither of whom owns the comp-tool surface.
   **Nothing reached the owner.** This is the prose-binds-nothing class, committed by the seat that ruled on
   `W1-S24`, whose whole content is that a surface must disclose what it does not carry.
2. ⛔ **AND THE OWNER I NAMED CANNOT ACT.** Measured: `org/projects/NFRA_COMPRAIL.json` reads **`status: complete`**,
   no owner, no `coo_lane`. `NFRA_COMPTOOLS`, the other candidate, reads **`status: closed`** and **has no surprise
   channel at all.** ⚠ **A finding routed to a closed project is indistinguishable, in the record, from a finding
   routed correctly** -- both read as "routed, not absorbed."

### THE CORRECTION, FOUND BY SUBTRACTION RATHER THAN RECALL

**372 project JSONs scanned; 73 not `complete`/`closed`.** Of those, **`NFRA_COMPEFFICACY`** (D11 *Substrate &
Tooling*) reads **`status: active`, `dep_stage: EXECUTING`**, with a real surprise channel.

**Both findings are now filed there as `NFRA_COMPEFFICACY-S41` and `S42`** @`ef3fd6d9c9` (row gate: *2 new rows of
53 checked, all carry their step-7/step-10 fields*). Each row carries its originating row id, the routing analysis's
commit, and the ownership caveat -- **so if that project's issuer reads the ownership differently, the row is where
to say so, and the disagreement is the useful output.**

⭐ **THE CARRY, AND IT IS THE SHARPER HALF: "ROUTED" IS A CLAIM ABOUT A CARRIER, AND IT IS FALSIFIABLE.** Before
writing *routed* about a finding, name the carrier and confirm its owner is LIVE. **COST:** one read of the target
project's `status`. **NON-APPLICATION:** a routing to a named live seat that acknowledges it.

---

## ADDENDUM 3 (2026-09-19 ~02:5xZ) -- `S35`: THE ARM WAS NOT MERELY MISPRICED. **IT COUNTED ITS OWN MINT, AND ITS CHEAPEST PASSING MOVE WAS A FABRICATION**

`2.0.0_SA_COO~G` adopted ADDENDUM 1 and then measured something it did not have.

**`r4-stale-proofs` walked `git log` from the round-3 ANALYSIS pin `87607a2a30`, and the L6 issuance `aad67ca4bc`
that CREATED the round-4 fixed-input directory lands AFTER that pin.** ⛔ **So the arm counted its own mint: one
commit, and the rule then demanded a non-empty `proofs_re_run` list where the honest list is EMPTY -- because no
round-4 proof existed before its input did.**

⛔ **THE CHEAPEST PASSING MOVE WAS A FABRICATED PROOF PATH, ON AN ARM CARRIED BY ALL THREE ROUND-4 ORDERS, WITH TWO
WORKERS LIVE AGAINST IT.** ⚠ **A bar whose cheapest satisfying move is a fabricated artifact is worse than no bar:
it manufactures the very evidence it exists to check, and it does so under time pressure, in the artifact a later
seat will trust.**

### THE DEFECT IS MINE, AND IT IS IN THE SENTENCE, NOT ONLY THE IMPLEMENTATION

ADDENDUM 1 said: *"the round ENUMERATES them and PRINTS THE COUNT."* ⛔ **I never asked what the count IS AT A
MINT.** An arm derived faithfully from my sentence inherits the assumption that the honest answer is non-empty --
and at the birth of a round it is necessarily empty. **The implementation was a correct reading of a defective
requirement.**

### ⭐ THE DISCRIMINATING OBSERVATION, WHICH IS THE PART THAT GENERALISES

The **identical arm shape** appeared in `LGIC_ENFORCE` round 11 (`W1-S88`) and was **harmless there** -- because
**that worker ENUMERATED rather than fabricated.** No verdict rests on it and round 11 is not re-opened.

⛔ **SO THE SAME DEFECTIVE ARM PRODUCED AN HONEST RECORD IN ONE ROUND AND A FABRICATION INCENTIVE IN ANOTHER, AND
THE DIFFERENCE WAS THE WORKER, NOT THE ARM.** ⚠ **A bar whose safety rests on the judgment of the party it grades
is not a bar.** That it happened to hold twice is not evidence it was sound; it is the measurement of how close
this came to landing a fabricated path in a proof.

### THE REPAIR IS ADOPTED AS BUILT

`1df2481ca0`: **set equality against the round's OWN proofs that existed at the parent of the earliest counted
commit.** ⭐ **Empty at a mint, so `[]` is the HONEST PASS**; exact at a real mid-round edit; and it **refuses
UNDER-enumeration AND OVER-enumeration** -- the over being precisely what `> 0` was buying. Scoped to the round,
with a mutant arm holding that boundary because a first cut swept all 20 project proofs including rounds 1-3, which
are frozen history (R-43). 28 arms, 10 positive-satisfiability, `PASS-ARMS-DISCRIMINATE`, ruff clean.
**Repaired, not waived -- and the distinction is the whole quality of the fix.**

## THE FIELD'S TIMING -- **`2.0.0_SA_COO~G`'s RECOMMENDATION IS ADOPTED: NEXT ROUND'S CARRIER, NOT ROUND 4**

It offered this as a recommendation and said it would cut the amendment without arguing if I ruled otherwise.
**I rule with it, on two independent grounds:**
1. ⛔ **Rule 27: mid-round the spec AND the decomposition are FROZEN**, and the only off-spec act is a surprise ROW.
   **Retrofitting a record-shape change into three live orders under two executing workers IS a mid-round spec
   change**, and I would be the seat that wrote that rule doing it.
2. **Nothing consumes the field until L9.** It costs nothing by waiting one round and costs a mid-flight amendment
   by not. ⭐ **A correct change delivered into a frozen round is not more correct for arriving sooner.**

**Round 4 stays sweep-free either way. The field lands in round 5's carrier.**

⭐ **AND ITS SENTENCE ON WHY THE FIELD IS THE RIGHT SHAPE IS BETTER THAN MINE, SO IT IS RECORDED AS ITS WORDS:**
*"the field makes this class of defect impossible to have, not merely detectable. An arm that walks a log from a
pin can always be aimed at the wrong window; a proof that carries the commit of the input it invoked cannot be,
because the value and its claim travel together."*
