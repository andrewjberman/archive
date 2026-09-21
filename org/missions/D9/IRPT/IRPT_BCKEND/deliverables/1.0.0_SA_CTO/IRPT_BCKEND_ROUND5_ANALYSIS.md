# `IRPT_BCKEND` ROUND 5 -- L10 ROUND ANALYSIS (`1.0.0_SA_CTO`)

**Slug:** `3.0.0_SA_CVO`, msg 98112, off L9 @`49f5a98f5e` and `2.0.0_SA_COO~B`'s L8 hand-off @`82ecb14d32`.
**Date:** 2026-09-19 ~03:2xZ. **Round state as slugged:** channel **247 items, 0 undispositioned, 0 unknown
`adjudicates` targets, 0 GRADUATED without a remediation row, 0 open orders of 61.** 6 judgment PASS, 17 rows
disposed, 16 graduated with a carrier each, 3 dismissed.

## 0. COVERAGE READ -- **NO PRD ADDENDUM IS OWED**

The slug names no outcome that no cell served, and my own read finds none. **Round 6 is a recut.**
⚠ **`FWD-11` remains unreachable by ANY identity** -- `/opal/irpt/opal-principal-roster` reads `ParameterNotFound`
on the CVO's own live call -- but that is a **missing infrastructure act with its own sign-off**, already named in
the never-widen half I signed, not an unserved outcome.

## 1. ⛔ `S77` IS THE FINDING OF THE ROUND, AND ITS OTHER HALF IS **MY OWN DEFECT**

`W3-S42` said the cross-firm fence cannot recognise the two new bucket names *"because `scopes.json`'s
`bucket_provisioned` stays false for both firms."* **At HEAD it is TRUE for both** -- the flip I drafted and
`4.0.0_SA_CRO` landed. ⛔ **AND THE FENCE IS STILL STALE ANYWAY:** regenerating from today's registry produces the
same block **PLUS** `opal-data-cottonwood` under `data/black_diamond/` and `opal-data-inflection` under `data/cot/`.

⭐ **SO THE BLOCKING CONDITION SURVIVES WHILE ITS STATED CAUSE IS FALSE** -- the sharpest shape a row can have, and
neither cell could have seen it because each owned one half.

### THE MECHANISM, WHICH ANSWERS MY OWN `R57-AC2` QUESTION BY MEASUREMENT

`bucket_provisioned` has **FIVE functional readers of 136 occurrences across 43 files** (denominator 38,374 tracked
/ 35,965 readable), and **TWO OF THEM DISAGREE ABOUT WHAT IT MEANS.** Verified on my own instrument at HEAD:
- `infra/aws/terraform/shared-infra/s3-lgic-firm-buckets.tf:96-102` -- *"not managed here"* -- **already re-keyed**
  onto `bucket_managed_by`;
- `lib/opal_naming.py:617` -- `ruled = [g["bucket"] for g in foreign if g.get("bucket_provisioned")]` -- *"real, so
  the cross-firm fence must name it"* -- **still keys on the flag ALONE.**

⛔ **SO ONE FLIP UN-BLOCKED TERRAFORM AND SIMULTANEOUSLY CHANGED THE FENCE GENERATOR'S DESIRED OUTPUT, AND ONLY THE
FIRST WAS ACTED ON.** The split I drafted has **already happened in one of the two places**, and **the ASYMMETRY is
the defect** -- not the field, and not the flip.

### ⛔ MY DEFECT, STATED PLAINLY

My handoff verified the flip against **ONE consumer** -- the Terraform selector, re-derived on two instruments with
a negative control -- and **never asked what ELSE reads the flag.** The reader population is five; I checked one.

⚠ **This is Rule 22's shared-dependency clause, which I have cited at three seats this session:** *"A CHECK SCOPED
TO THE MEMBERS CANNOT SEE A DEFECT IN WHAT THE MEMBERS SHARE... Ask what the members have in COMMON, and check THAT
on its own."* I applied it to the exemption rows' **writers** and never to the flag's **readers.**

### ⭐ THE BAR THIS EARNS -- THE MIRROR OF A RULE THIS ESTATE ALREADY HAS

CLAUDE.md's never-widen line already says: ***"FIRST COUNT THE WRITERS OF THE NAMED PROPERTY: a property with N
writers needs N rules read, and N is a number the half PRINTS."***

⛔ **THE MIRROR IS OWED AND IS NOW STATED: FLIPPING A SHARED FLAG NEEDS ITS *READER* CENSUS, EXACTLY AS WRITING A
SHARED PROPERTY NEEDS ITS WRITER CENSUS -- N readers, N rules read, N printed.** A write asks *who else sets this?*
A flip asks *who else BELIEVES this?* ⭐ **And the flip is the more dangerous of the two, because a write is visible
in a diff while a flip's effect lands in whatever a DIFFERENT file generates from it.**
**COST:** one census of the flag's readers, banded. **NON-APPLICATION:** a value with exactly one reader, which the
same census proves.

**EXPOSURE, NOT INCIDENT** -- and the slug measured it rather than asserting it: the signature over **290 readable
tracked files in the two trees returns 0.** Nothing has used the hole. ⭐ The remedy is therefore **one generator
re-run**, now unblocked -- it moved from a registry edit outside an order's paths to an act inside one.

## 2. `S78` -- **CLAUDE.md CITES TWO `memory/` PATHS AND 2 OF 2 ARE UNRESOLVABLE AS WRITTEN.** MINE

Verified at HEAD, both ways, because the claim is about the constitutional file:
| citation | at HEAD? | in this worktree? | why it fails |
|---|---|---|---|
| `CLAUDE.md:420` -> `memory/feedback_no_shadow_channels_veto_build_correctly_and_port.md` | **NO** | yes | **worktree-only, so ABSENT in every fresh worktree -- which is where WORKERS run** |
| `CLAUDE.md:493` -> `memory/feedback_availability_is_not_authorization_vendor_egress.md` | **NO** | **no** | lives in the user memory directory, **absent from the repo entirely** |

⚠ **NOT A CONTENT CLAIM: both memories exist and their substance is not in question. What fails is the ADDRESS**,
and it fails differently in each case, which is why one fix does not cover both. ⛔ **The worker case is the one
that bites: a worker in a fresh worktree following a NEVER-class citation finds nothing there**, and the two rules
cited are the shadow-pipeline veto and the vendor-egress word -- both NEVER-class.

**RULING: the fix is in the CITATION, never in the rule.** The pointer is re-written to something a reader in a
fresh worktree can resolve, or the line carries its substance inline and drops the path. ⛔ **NO GATE IS PROPOSED
AND NONE SHOULD BE INFERRED** -- the CVO said so explicitly and I am repeating it because a citation-hygiene finding
on a law file is exactly where an agent-made gate would get invented. **The order face that cited a `memory/` path
owes nothing; `W4-S36` is correctly dismissed and the CLASS is what graduated.**

## 3. THE SIX GRADES -- ACCEPTED, AND WHAT EARNED IT

All six accepted. ⭐ **Each carries at least one fact re-measured on an instrument the CVO ran**, and three deserve
naming:

- **`R56-AC2`** -- it read my L4 ruling **at the bytes** and then **verified its load-bearing premise on the code**,
  *"because the whole remedy is an ordering inversion and an inversion aimed at the wrong lines fixes nothing"*:
  `enforce.py` refuses UNPROJECTED at `:283`, tests the empty permitted set at `:291`, with the file's own comment
  at `:276` stating that order deliberately. ⭐ **That the order is DOCUMENTED POLICY is exactly why my
  ENTITLEMENT-CONTRACT-at-L4 classification holds rather than "code defect"** -- the grader confirmed the
  classification by finding the comment, not by accepting my word for it.
- **`R51-AC2`** -- ⭐ **it reported its OWN WRONG DISCRIMINATOR:** a first probe counted modules referencing
  `Enforcer` and returned 2 of 13, *"which would have published a false picture"*, because five entry modules pass
  `id_projection` to a different constructor. **`Enforcer` was the wrong OBJECT.** And it supersedes the record's
  *"0 of 13 modules pass `id_projection`"* -- **7 of 7 `entry.py` modules do**, the other 6 being inner modules that
  structurally cannot carry the property. ⚠ **That is `S32`'s class one project over, same UNDERSTATE direction**,
  and it is the second measured instance of the pinned-record-goes-stale shape in two nights.
- **`R54-AC2`** -- `.gitattributes` at HEAD carries **no general `*.json eol=lf` rule**, so `W4-S38`'s 49-of-147
  CRLF artifact is real. ⭐ **A census that had not said so would have reported a THIRD OF ITS POPULATION as a
  defect.** The file's own comments show this is the **third widening** to the member that bit; the remedy is the
  subtraction Rule 24 asks for, and the owner is the estate's because `infra/aws/lambda/ci/` serves every family.

## 4. A SMALL BAR FROM `R55-AC2`, WORTH ONE LINE

The pin `@1258192be1` is a **BLOB**, and this estate reads `@<hash>` as a **commit-ish** -- so resolving it that way
returns *"exists on disk, but not in `<rev>`"*, **which reads like a MISSING FILE rather than a wrong hash KIND.**
⭐ **The pin is the STRONGER kind and only the notation is ambiguous** -- but it cost the grader a confused lookup.
**BAR: a blob pin is written so its kind is legible (`blob <hash>`), because `@<hash>` is already spoken for.**
COST: one word. NON-APPLICATION: a commit-ish pin, which `@` already means.

## 5. WHAT ROUND 6 CARRIES

1. **The no-source members cell FIRST** (@`457cf494c6`) -- population `W4-S34`/`S35` + `W1-S26`'s two functions +
   the 3 UNRESOLVED, on the measure-then-branch shape.
2. **The `(a)` policy cell** -- the ordering inversion, with its three binding conditions carried verbatim onto the
   face, and `rte-2` re-cut BEHIND it.
3. ⭐ **`S77`'s generator re-run** -- newly unblocked, and **it is now the cheaper remedy than the registry edit it
   replaced.**
4. **`IB-rte-3`'s re-hand** behind Andrew's step 4, its sign-off naming `W3-S45`'s **4 TAINTED resources** as blast
   radius -- and, on this analysis, **also naming the fence generator's output** as a thing the flip already moved.
5. ⛔ **`W3-S44`'s host negative control is UNEXERCISED, NOT PASSED** -- its instance is STOPPED, and a
   simulate-policy substitute cannot close it when the estate's own catalogue records simulate-policy returning
   **FALSE ALLOW**.

**Nothing in this analysis re-opens a graded criterion, moves a cap, or rewrites a proof.**

---

## ADDENDUM -- `ASK 2` RULED: **THE HOST IS NOT STARTED, AND `(d)` RECORDS `UNEXERCISED`, NOT `FAIL`**

`2.0.0_SA_COO~B` (98118) asks whether host `i-02448edb624a7a7cf` -- STOPPED, `W3-S44` -- is started so `IB-rtf-5`'s
arm (d) can close, or whether a host-independent negative control is named; absent either, (d) grades a truthful
FAIL and `W3-S44` stays open.

### 1. ⛔ THE HOST IS NOT STARTED -- NOT BY THIS SEAT AND NOT BY ANY CELL

Three independent reasons, any one sufficient:
1. ⛔ **IT IS SOMEONE ELSE'S RESOURCE AND THE STOP WAS SOMEONE ELSE'S ACT.** `W3-S44` records it plainly: *"NOT this
   worker's act; somebody stopped it."* **An unexplained stop is a SIGNAL, not an obstacle** -- starting a host
   another owner deliberately stopped, without knowing why, is acting on their resource for this project's
   convenience.
2. **The host has another purpose**, so an EC2 state change on it is outside every `<paths>` grant in this project
   and outside this seat's lane.
3. ⚠ **CLAUDE.md reserves STOPPING an EC2 to human confirmation.** Starting is not the same act and I am not reading
   the rule wider than it is written -- **but the reason behind it (an instance's run state is shared, visible and
   billable) applies in both directions**, and a seat that starts what a human stopped has made the confirmation
   meaningless in the direction it was not written for.

### 2. ⛔ `(d)` RECORDS **`UNEXERCISED`**, AND THAT IS THE LOAD-BEARING HALF OF THIS RULING

The ask frames the fallback as *"a truthful FAIL."* ⛔ **A FAIL IS NOT TRUTHFUL HERE AND IS THE WRONG WORD.** FAIL
asserts the control was exercised and did not hold. **Nothing was exercised.** The estate's own catalogued rule:
*a verdict vocabulary with no NOT-EVALUATED value encodes non-evaluation as a verdict.*

⭐ **So (d) reads `UNEXERCISED` / NOT-EVALUATED, with the reason and the owner named.** It does not pass, it does not
fail, and it does not quietly become either on a later read. **`W3-S44` stays open, which is the correct state for a
control nobody has run.**

### 3. **NO SUBSTITUTE IS NAMED BLIND -- BUT ITS SHAPE IS**

⛔ **I am not inventing a host-independent control from a message.** What the host is load-bearing FOR is decided by
the criterion's own text, and that read is a cell input, not a ruling. ⚠ **A substitute chosen without it would be
the "legs that do not inspect the defect's COORDINATE" shape -- a control that passes every time.**

**The shape any substitute must have, and this is binding:** it **EXERCISES THE DENY on the real plane, from a
principal the fence does not admit.** ⛔ **`simulate-principal-policy` is REFUSED** -- the estate's own catalogue
records it returning **FALSE ALLOW**, so it cannot discriminate the thing this control exists to prove.
`2.0.0_SA_COO~B` already ruled it out and is right.

### 4. `ASK 1` -- CONFIRMED

When `WK~1` reports with the packet's blob, **the CTO never-widen half is signed BY BLOB the same tick**, bound to
that hash and not to a version -- as with `IB-rte-2`'s half @`482b2c627e`. **A re-cut packet is a re-signature.**
