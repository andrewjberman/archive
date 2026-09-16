# checklist-review-r2.r2.result -- LGIC_CANON.CN-o-4-r2 (cell CN-o-4), 0.9.0_WK_LGIC_CANON~9

**Worktree:** `.worktrees/wk-lgic-canon-2-10`, branch `wk-lgic-canon-2-10`, based on CLOUD
@`d173e700f7b9a86ffa0051baa033ca1ca020596b`. **Review committed at** @`ab634e205746afdd974b239861e9d4d1d889f289`.
Deliverable: `org/missions/D14/LGIC/LGIC_CANON/deliverables/CHECKLIST_REVIEW_R2.md`.

## 1. THE MARKS, AND WHAT MOVED THEM

16 steps, all marked. **MECHANICAL 16, JUDGEMENT 0.** Of the 16: **RUNNABLE 13** (1-9, 11, 12, 13, 15);
**STOPPED with a named owner 3** -- step 10 and step 16 on `ADVI_FIRMBKTS`, step 14 on `1.0.0_SA_CTO`
(register entry X8) with a second STOP on Andrew for the portal page-access list.

Round 1's `CN-o-2` marked five steps JUDGEMENT (3, 7, 8, 9, 14) and failed its own criterion rather than
lie in the record. All five moved this round, and the review names the bytes that moved each:

- **3, 7, 8, 9** -- one canon sentence, R22 (`infra/logic/02_DOCTRINE.md:459-468`), which did not exist at
  round 1 and which names these four steps explicitly. It makes the vendor FAMILY the one input that fixes
  a pipeline's contents (tables, partition forms, resource set, function words, directory), so the five
  values round 1 listed as undecided are inherited rather than chosen. This is a SINGLE point of
  dependence and the review states it as such: withdraw or narrow R22 and all four return to JUDGEMENT.
- **14** -- the step no longer asks the runner to choose between two prescribed rules; it STOPs on X8's
  owner. Section 3 below is the check that mark required.

## 2. THE SECOND BAR, MEASURED RATHER THAN ASSERTED

Bar 2 asks whether a MECHANICAL step is RUNNABLE TODAY. Three clauses were tested, not assumed:

1. **The builder exists.** A python sweep over the checklist's own `built:` lines: 16 of 16 steps carry
   one; 15 name a path and read `built: yes`, and **15 of 15 of those paths exist** in this worktree
   (`scopes.json`, `NAMING_SCHEMA.json`, `firm-config.mjs`, `exemptions.json`, `s3-49financial.tf`,
   `opal_naming.py`, `naming-gate.py`, `safe-apply.sh`). One reads `built: no EN-s-1` -- step 13.
2. **The inputs have a carrier.** `comp-find 'family' --pathspec infra/logic`, denominator 32 hits across
   20 files (corpus `all`), both pages read: every hit is prose, **none in `infra/logic/registry/`**. So
   the FAMILY input's carrier is the vendor's existing pipeline, not a registry field -- printed as
   observation 3 in the review rather than buried.
3. **Nothing upstream stops.** Step 16's pass condition cites Steps 10 and 15, and Step 10 STOPs, so step
   16 is marked STOPPED on the inherited owner even though its own text carries no STOP. That is the one
   mark in this review that reads the checklist as a whole rather than a step in isolation, and it is
   flagged as such in observation 1.

**EN-s-1, step 13's dependency, was checked on two instruments** rather than one: both
`LGIC_ENFORCE.TO-EN-s-1.census-run.md` and `...-r2...` read `<status>pending</status>`, AND round 1's
proof instance `0.9.0_WK_LGIC_ENFORCE~7/LGIC_ENFORCE.TO-EN-s-1.census-run.proof_of_spec.json` carries 4
acceptance rows of which 2 read FAIL (the census stopped on its first RAISE). The cell has not closed by
the proof, not merely by a free-text status field.

## 3. STEP 14's STOP: HONEST, OR DEFERRED WORK? -- the check the criteria cannot perform

None of `o4-zero-judgement`, `o4-runnable` or `o4-distinct` opens the register; they read my marks and the
git log. So the substance of the step-14 mark was verified separately, on four readings:

**(i) My own instrument, on a NEW firm.** X8 records OUT-OF-PATTERN for four EXISTING tables; that says
nothing about a fifth. Run here, read-only, from `lib/opal_naming.py`:

    grade("opal-partner-newfirm",    "DYNAMODB_TABLE") -> ('OUT-OF-PATTERN', 'opal-partner-newfirm-table')
    grade("opal-partner-demo",       "DYNAMODB_TABLE") -> ('OUT-OF-PATTERN', 'opal-demo-partner-table')
    grade("gateway-49f-sessions-table","DYNAMODB_TABLE") -> ('CONFORMANT', 'gateway-49f-sessions-table')
    grade("opal-data-newfirm",       "S3_BUCKET")      -> RAISES RaiseDefect "B2: 'newfirm' after
                                                          opal-data- is no scope key"

The positive control fires CONFORMANT, so the grader can say yes. The negative control proves `newfirm`
is NOT a registry scope, which makes the first line the PRE-identity-row read and the `demo` line the
POST-identity-row read: **both branches read OUT-OF-PATTERN**, so Step 12's apply condition (apply only
when every new resource name reads `CONFORMANT`) blocks Step 14's mandated name whatever the run order.
Only the suggested canonical form changes with the registry row's presence.

**(ii) X8 read at the register, not through the step.** `06_CONFORMANCE_LEDGER.md` section 6 enumerates
*"the four partner identity tables `opal-partner-{demo,49financial,cottonwood,inflection}`"* and its
condition closes *"until such a project lands the four names stand and are NOT violations"*. Four named
tables, four standing names, no fifth. The checklist says exactly this and stops; it does not claim cover
it does not have.

**(iii) The deferred act is unavailable to the deferring party, twice over.** Extending X8 is a write to
the ledger's register, whose decider the ledger names as `1.0.0_SA_CTO` (`:141-146`, under Andrew's
2026-09-16 ~05:2xZ delegation), and R20 makes every exception sovereign-acknowledged. A worker or a
checklist runner extending it would be inventing the acknowledgement R20 exists to require. It is also
unavailable in object: the entry enumerates NAMED tables, and at cut time there is no new firm to name.

**(iv) Both alternatives are violations the step forecloses.** A rename breaks every partner sign-in
(X8's two coordinates: the runtime derivation in two byte-identical carriers, and `dynamodb:GetItem` on
`table/opal-partner-*` granted twice on one role) and is an R19 act under never-widen sign-off; applying
undeclared is R20's own violation case.

**Found: the STOP is honest, not deferral.** Its cost is stated rather than hidden -- it is reached on
every first run for every new firm, so FWD-5's first real run needs a `1.0.0_SA_CTO` act inside the run's
window. That is a sequencing fact for whoever cuts C6, not a defect in the step.

## 4. THE CRITERIA, VERBATIM

    $ timeout 120 python .../fixed_inputs/r2/check_canon_r2.py o4-zero-judgement
    steps marked, denominator 16; JUDGEMENT: 0 []
    all 16 steps marked and none JUDGEMENT: True
    VERDICT: PASS-O4-NO-JUDGEMENT-STEP
    rc=0

    $ timeout 120 python .../fixed_inputs/r2/check_canon_r2.py o4-runnable
    MECHANICAL steps, denominator 16; neither RUNNABLE nor STOP-with-owner: 0 []
    VERDICT: PASS-O4-EVERY-MECHANICAL-ACCOUNTED
    rc=0

    $ timeout 120 python .../fixed_inputs/r2/check_canon_r2.py o4-distinct
    last author of the review   : 0.9.0_WK_LGIC_CANON~9
    last author of the checklist: 0.9.0_WK_LGIC_CANON~8
    distinct authors: True
    VERDICT: PASS-O4-REVIEWER-IS-NOT-AUTHOR
    rc=0

**The negative control, in two arms, run after the fact and reported as such.** The fixed input was NOT
edited: `check_canon_r2.py` was loaded with `importlib` and its module-level `REVIEW2` repointed, exactly
as `CN-o-3`'s mutant arm did; `git status --porcelain` over `fixed_inputs/r2/` reads clean.

*Arm 1, a MUTANT of my own review* written to `.scratch/CHECKLIST_REVIEW_R2.mutant.md` -- step 7's mark
changed to `JUDGEMENT` and step 12's account cell changed to `not accounted`:

    steps marked, denominator 16; JUDGEMENT: 1 ['7']
    VERDICT: FAIL-O4-NO-JUDGEMENT-STEP
    MECHANICAL steps, denominator 15; neither RUNNABLE nor STOP-with-owner: 1 ['12']
    VERDICT: FAIL-O4-EVERY-MECHANICAL-ACCOUNTED

Both criteria name the exact offending step, so neither passes by counting alone.

*Arm 2, the review ABSENT* (`REVIEW2` pointed at a path that does not exist):

    MISSING INPUT: .scratch/does-not-exist.md   VERDICT: FAIL-O4-ZERO-JUDGEMENT
    MISSING INPUT: .scratch/does-not-exist.md   VERDICT: FAIL-O4-RUNNABLE
    last author of the review   : <uncommitted>
    distinct authors: False                     VERDICT: FAIL-O4-REVIEWER-IS-NOT-AUTHOR

So no criterion passes on a tree that merely exists, and `o4-distinct` needs a COMMITTED review.
`o4-distinct` has a second, sharper property worth naming: it would also FAIL had I written the checklist
myself, which is the constraint the cell exists to enforce, and the authorship it reads
(`0.9.0_WK_LGIC_CANON~8` @`a6c9652ac2`) is a record I cannot write from inside my own commit.

## 5. WHAT O4-J1 IS OFFERED

`O4-J1` is graded at L9 by `3.0.0_SA_CVO`; nothing here grades it. The material for it is:

- **"the marks are the reviewer's own reading"** -- each of the 16 rows cites the checklist lines it was
  read from, and the four moves off round 1's JUDGEMENT marks each name the rule or register entry that
  moved them. The one mark that is not a read of the step's own text (step 16) says so in its own cell.
- **"a RUNNABLE claim is one a runner could act on today"** -- section 2 above is the measurement behind
  every RUNNABLE, and step 13 is the sharpest case: it is RUNNABLE only on its until-then branch, which
  the row states rather than smoothing over.

## 6. ROWS FILED

- `LGIC_CANON-W9-S1` (OBSERVATION, INERT): `02_DOCTRINE.md`'s title line reads v1.0 and section 0's census
  line reads `RULES CARRYING ALL THREE PARTS: 21 of 21`, while the file carries 22 rule blocks (R22
  between R13 and R14) and its change log's last row reads v1.1. R22 itself carries all three parts, so
  the true reading would be 22 of 22. Off-task for this cell -- found while grounding R22 -- and
  `02_DOCTRINE.md` is not in this order's `<paths>`, so it was not touched. No mark in the review depends
  on the count; R22's text was read in full.

## 7. WHAT THIS CELL DID NOT DO

- It did not edit the checklist, the canon or the ledger. None is in this order's `<paths>`.
- It did not touch `check_canon_r2.py` or any r2 fixed input; none was found defective by this cell.
- It did not grade `O4-J1`, and it did not re-run `CN-o-3`'s criteria.
