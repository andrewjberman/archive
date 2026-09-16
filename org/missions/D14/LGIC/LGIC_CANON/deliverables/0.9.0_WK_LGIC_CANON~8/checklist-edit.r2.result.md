# checklist-edit.r2.result -- LGIC_CANON.CN-o-3-r2 (cell CN-o-3), 0.9.0_WK_LGIC_CANON~8

**Worker:** `0.9.0_WK_LGIC_CANON~8`, an L7 worker subagent of `2.0.0_SA_COO~G`, on task order
`org/missions/D14/LGIC/LGIC_CANON/task-orders/LGIC_CANON.CN-o-3-r2.checklist-edit.md`.
**Worktree:** `.worktrees/wk-lgic-canon-2-8`, branch `wk-lgic-canon-2-8`, based on CLOUD @`7db18a4464`.
**Edited artifact:** `infra/logic/10_ONBOARDING_CHECKLIST.md` @`a6c9652ac2` (the only file this cell writes besides its
rows and this record).
**Written against:** the canon `infra/logic/02_DOCTRINE.md` v1.1 (R22, the pipeline-instance rule `CN-k-2` added), the
ledger `infra/logic/06_CONFORMANCE_LEDGER.md` v1.2 (register entry X8), and the round-1 analysis
`org/missions/D14/LGIC/LGIC_CANON/deliverables/1.0.0_SA_CTO/LGIC_CANON_ROUND1_ANALYSIS.md` @`26ae876d23`, s.2 rulings
A-6, A-7, A-8, A-9, A-10.

---

## 1. WHAT THE EDIT DID, ELEMENT BY ELEMENT

The cell has five elements. The analysis's own CN-o-3 row names them: *"the checklist edit: sovereign inputs named;
Step 6 second block; Step 10's STOP names ADVI_FIRMBKTS; Step 14's STOP names X8; steps 3, 7, 8, 9 take the family |
A-6, A-7, A-8, A-9, A-10"*. All five are built.

### (1) A-9 -- STEPS 3, 7, 8 AND 9 TAKE THE PIPELINE FAMILY AS A GIVEN INPUT

Round 1's review (`CHECKLIST_REVIEW.md`) marked those four JUDGEMENT for one shared cause: *"The canon fixes a
pipeline's homes, formats, compute and name grammar, but not its contents: which directory, which tables, which
partition form, which resources, which function words. The inputs table carries none of them."* R22 now supplies
exactly those contents, so each of the four steps opens with a block that names the FAMILY and reads its contents
from the rule rather than asking the runner to choose:

- **STEP 3** -- the family is handed to the step per vendor; the firm joins it with scope `<LONG>`; part (c)'s
  directory is *the family's*, read rather than named. R22's non-application (a vendor with no family yet) is stated
  as a STOP: that pipeline is R19 work, not onboarding. The step's second free value from the review, the master
  row's free-text `label`, is closed on R3 -- it is the name the vendor's own header gives that master, copied.
- **STEP 7** -- the resource SET is the family's, and each function word is the word the family's corresponding
  resource already carries, so no item description is written here and no verb is chosen here.
- **STEP 8** -- every `<table>` and every bronze `<partition>` form is the family's; the note that `key()` passes
  those two through `_segment` only is kept, because it is the reason the family (not the builder) has to fix them.
- **STEP 9** -- the gold tables, their names, the gold partition form and `<source>` for a combined build are the
  family's; so are the `state` and `code` tiers. The run sets the scope and nothing else.

The INPUTS table gains the family as its own row, so the four steps' input is *given*, not asserted inside a step.

### (2) A-6 -- THE SOVEREIGN INPUTS ARE MARKED WHERE THE INPUTS ARE GIVEN

`## THE INPUTS` gains a `mark` column over three values, defined once above the table:

| mark | meaning | rows |
|---|---|---|
| **SOVEREIGN** | Andrew's word fixes it; no rule, builder or document derives it; a missing one is a STOP, never a default | 5 |
| GIVEN | a document outside this run fixes it (the engagement, a vendor agreement, the canon's family definition) | 4 |
| DERIVED | a builder writes it from another input on the table | (the `<SHORT>` row's second branch) |

Nine input rows, five SOVEREIGN (`<LONG>`, `<SHORT>` where Andrew gives one, the surfaces, the tenant bindings, the
portal paths), four GIVEN, none the person running the checklist decides. The LONG/SHORT row is split in two so that
each carries its own mark. The rule the order states -- an input the run may NOT choose marks itself in the INPUTS
section, not in a step -- is the reason no sovereignty mark was added to any step.

### (3) A-8 -- STEP 10's STOP NAMES `ADVI_FIRMBKTS`

STEP 10 now states A-8 first (*a NEW firm mints no legacy served key*; its platinum is served from the FIRM bucket at
the builder's address; the two tier-first reads are LEGACY SERVED PATHS, a list admitting EXISTING firms only,
`org/missions/D14/LGIC/LGIC_NAMING/deliverables/LEGACY_SERVED_PATHS.json`), then STOPs with an owner: repointing the
edge auth validator and the shared advisor router is `ADVI_FIRMBKTS`'s router work. Row LGIC_CANON-W6-S3 records the
gap; ruling A-8 assigns it. The sequence claim in that paragraph was measured, not recalled:
`org/missions/SEQUENCE.yaml` puts the Platform Logic projects (LGIC_*) in stage 1 and `ADVI_FIRMBKTS` in stage 2, so
no order change follows.

### (4) A-7 -- STEP 14's STOP CITES REGISTER ENTRY X8

STEP 14 was the review's one non-family JUDGEMENT: two prescribed rules conflicted (Step 12 applies only on
`CONFORMANT`; `grade()` reads `opal-partner-<LONG>` OUT-OF-PATTERN) and nothing resolved it. The step now cites X8 and
STOPs on X8's owner. **See s.3 for the verification of that citation against the ledger itself.**

### (5) A-10 -- STEP 6 KEEPS THE TEMPLATE'S SECOND COMMENT BLOCK VERBATIM

STEP 6's replace-all is now SCOPED -- it runs over the HCL body and the header comment (which the next bullet replaces
outright) and never over the second comment block. That block is named by its heading, its path, its line range and
its commit: `THE CROSS-FIRM DENY, MINTED AT CREATION`,
`infra/aws/terraform/shared-infra/s3-49financial.tf:70-98` @`080e1b97c6`, between the public-access block and
`module "opal_name"`. The two false strings a blind replace-all would produce (`:74`'s "IS the bd/49F firm's client
bucket" and `:98`'s citation of a ledger entry that does not exist) are named, so the instruction carries its own
reason.

### ALSO CHANGED, FOR INTRA-FILE COHERENCE

The closing section `WHAT THIS CHECKLIST DOES NOT DO` listed three STOP points by ROW. It now lists five by OWNER --
Andrew (the forms), Andrew (the portal paths), `1.0.0_SA_CTO` (X8's extension), `ADVI_FIRMBKTS` (the tier-first served
keys), and R22's non-application (a vendor with no family) -- because a STOP whose owner is named in the step and not
in the summary reads as blocked on nobody from the summary. The header gains a round-2 provenance block naming this
cell, the five rulings, and the vintage read.

### NOT DONE, DELIBERATELY

No step is marked MECHANICAL or JUDGEMENT. That is cell `CN-o-4`'s, by a worker who did not write this edit; a
checklist that marks itself proves nothing. This file states no mark either.

---

## 2. THE CRITERIA, VERBATIM OUTPUT

Every run: `cd /c/Users/AndrewBerman/Desktop/ajb_workspace/.worktrees/wk-lgic-canon-2-8 && timeout 120 python
org/missions/D14/LGIC/LGIC_CANON/deliverables/2.0.0_SA_COO~G/fixed_inputs/r2/check_canon_r2.py <subcommand>`, at
HEAD `a6c9652ac2` with the edited file committed and `git status --porcelain` clean over `infra/` and `org/missions/`.

```
== o3-family
steps in the checklist, denominator 16
family steps ['3', '7', '8', '9']; steps not naming the family: none
VERDICT: PASS-O3-FAMILY-STEPS-TAKE-INPUT
rc=0
== o3-step10-stop
STEP 10 carries a STOP: True ; the STOP names ADVI_FIRMBKTS: True
VERDICT: PASS-O3-STEP10-STOP-NAMES-OWNER
rc=0
== o3-step14-stop
STEP 14 carries a STOP: True ; the STOP cites register entry X8: True
VERDICT: PASS-O3-STEP14-STOP-CITES-X8
rc=0
== o3-sovereign
the INPUTS section names 9 SOVEREIGN input(s)
an input the run may not choose must say so where the inputs are given, not in a step
VERDICT: PASS-O3-SOVEREIGN-INPUTS-NAMED
rc=0
```

**The negative control is the same four subcommands on the UNEDITED file**, run before any edit at HEAD `7db18a4464`:
`FAIL-O3-FAMILY-STEPS-TAKE-INPUT` (steps not naming the family: `['3', '7', '8', '9']`),
`FAIL-O3-STEP10-STOP-NAMES-OWNER` (STOP True, ADVI_FIRMBKTS False), `FAIL-O3-STEP14-STOP-CITES-X8` (STOP True, X8
False), `FAIL-O3-SOVEREIGN-INPUTS-NAMED` (0 SOVEREIGN). So each of the four discriminates, and each PASS above is a
state this edit produced rather than one the file already had.

`O3-J1` is a judgment criterion: recorded, no verdict, graded at L9 by `3.0.0_SA_CVO`. Its two questions are answered
by s.1 (the four family steps are executable by a runner who is handed the family) and by s.3-s.4 (neither STOP defers
work this cell could have finished).

---

## 3. THE X8 CITATION, VERIFIED AGAINST THE LEDGER -- NOT AGAINST THE CRITERION

The order states the reason plainly, and this section is the answer to it: `o3-step14-stop` reads STEP 14 and tests
that its text contains the strings `STOP` and `X8`. **It never opens the register, so it cannot tell a true citation
from a fabricated one, and its PASS is not evidence that the citation is accurate.** The citation was therefore
verified by reading `infra/logic/06_CONFORMANCE_LEDGER.md` at HEAD. What the entry actually says, and what STEP 14 now
says about it:

| claim in STEP 14 | the ledger at `a6c9652ac2` |
|---|---|
| X8 exists, in section 6 | `## §6. THE EXCEPTION REGISTER (from 02_DOCTRINE.md §4, carried here as the ledger's register)`; X8 is its last row |
| axis A3 | the row's `axis` cell reads `A3` |
| state **GRANTED** | the row's `state` cell reads `**GRANTED**` |
| kind CONDITIONAL | the row's `kind` cell opens `CONDITIONAL -- the ruling states no kind; "forced" holds while the force stands` |
| owner `1.0.0_SA_CTO` | the same cell: `owner: 1.0.0_SA_CTO (A-7's author; the seat that opens an R19 project)` |
| added at ledger v1.1, 2026-09-16, by `4.0.0_SA_CRO`, on ruling A-7 / C-S12 | §9 change log: `**v1.1** -- 2026-09-16, 4.0.0_SA_CRO: register entry **X8** added on 1.0.0_SA_CTO ruling A-7 / C-S12 @26ae876d23` |
| the name reads OUT-OF-PATTERN, canonical `opal-<SHORT>-partner-table` | the row's `departure` cell: `grade(name, 'DYNAMODB_TABLE')` reads **OUT-OF-PATTERN** on all four, canonical forms `opal-{demo,49f,cot,inf}-partner-table`, EXERCISED 2026-09-16 |
| the login path derives the name at runtime; the IAM grant is a wildcard, granted twice on one role | the row's `why` cell, coordinates (1) and (2): `partnerTableName(firmId)` returns `` `opal-partner-${normalized}` ``; `dynamodb:GetItem` on `table/opal-partner-*` TWICE on `opalinvest-auth-lambda-role` |
| a rename is an R19 act under never-widen sign-off, not a hygiene edit | the same cell, and the row's condition: `an R19 project renames the four tables ... AND re-derives partnerTableName() (both copies) AND re-scopes both grants, in ONE act under never-widen sign-off on sign-in` |
| **X8 enumerates exactly four tables and a new firm's is not among them** | the row's `pipeline` cell: `the four partner identity tables opal-partner-{demo,49financial,cottonwood,inflection} (DynamoDB)`; the condition speaks only of `the four names`. §7's register denominator reads 8 entries, X1-X8, GRANTED 6 |

The last row is the one that decides what STEP 14 does. X8 declares a departure for FOUR NAMED TABLES. A fifth firm's
`opal-partner-<LONG>` is outside the entry as written, so on R20 it would be a departure nobody declared -- which is a
violation, not an exception. That is why the step STOPs on X8's owner extending the entry rather than simply pointing
at X8 and applying: pointing at X8 would have been the fabricated-citation version of this edit, and it would have
passed `o3-step14-stop` identically.

---

## 4. WHY NEITHER STOP DEFERS WORK THIS CELL COULD HAVE FINISHED (for O3-J1)

- **STEP 10's STOP** needs two lambda-edge reads repointed at the builder address. That is live serving code in
  `infra/aws/lambda-edge/`, outside this order's `<paths>` (which name the checklist and the channel only), and it is
  `ADVI_FIRMBKTS`'s cell by ruling A-8. This cell could not have finished it, and no cell of LGIC_CANON moves anything
  live (the order's own bound).
- **STEP 14's STOP** needs register entry X8 extended to a fifth table. The register lives in
  `infra/logic/06_CONFORMANCE_LEDGER.md`, also outside this order's `<paths>`; its author is `4.0.0_SA_CRO` in the
  CRO's lane and its owner is `1.0.0_SA_CTO`. A worker extending another seat's R20 entry to cover a table nobody has
  yet asked for would be inventing the acknowledgement R20 exists to require.
- **STEP 3's non-application** (a vendor with no family) is R22's own carve-out, not a deferral: the canon says the
  first pipeline of a new vendor is defined by R19's method. Naming it keeps the family steps honest about the case
  where the input does not exist, rather than letting a runner infer one.

Both STOPs name an OWNER and a CONDITION that lifts them, which is the property A-7 and A-8 ask for: *"so no runner
chooses between two prescribed rules"*, and *"the checklist does not read as blocked on nobody"*.

---

## 5. ROWS FILED

Three, all OBSERVATION / INERT, in
`org/missions/D14/LGIC/LGIC_CANON/surprise-channel/investigations/INVESTIGATION_v1.md` @`a6c9652ac2`:

- **`LGIC_CANON-W8-S2`** -- this order's worker face swaps the A-6 and A-10 labels (item 2 cites A-10 for the
  sovereign inputs, item 5 cites A-6 for Step 6's second block), and item 5 then asks Step 6 to state what item 2
  requires to live in the INPUTS section and nowhere else. Both elements were built to the analysis's own CN-o-3 cell
  row, which is unambiguous whichever way the labels are read. The row also records that the order cites the analysis
  at `org/tier1_exec/1.0.0_SA_CTO/deliverables/LGIC_CANON_ROUND1_ANALYSIS.md@26ae876d23`, where `git show` is fatal;
  `git ls-tree -r --name-only 26ae876d23` finds exactly one carrier, the deliverables path used throughout this file.
  Same commit, different directory -- so this is a stale path, not a missing input, and nothing was blocked.
- **`LGIC_CANON-W8-S3`** -- A-6's clause *"SHORT is DERIVED by `name()` from LONG"* does not hold at HEAD. Nothing in
  `lib/opal_naming.py` derives a short form: `name()` looks it up on the identity row (`:1552`) and `validate()`
  refuses a `scopes.json` row whose `short` is missing or empty (`:279-281`). The INPUTS table therefore states the
  measured form -- SOVEREIGN where Andrew gives one, else DERIVED, typed ONCE into Step 1's row and read from there by
  every later name and generated view.
- **`LGIC_CANON-W8-S4`** -- `check_canon_r2.py o3-sovereign` prints *"the INPUTS section names 9 SOVEREIGN input(s)"*,
  where 9 is `len(re.findall("SOVEREIGN", blob))` -- occurrences of the token anywhere in the section, not inputs
  marked SOVEREIGN, which are 5 of 9 rows. The verdict is sound (presence is all the criterion tests); the evidence
  line's denominator certifies its own sweep and not the set. The fixed input was NOT touched: it is read-only by this
  order's bound, and the count that belongs in the record is stated here instead.

## 6. WHAT THIS RECORD DOES NOT CLAIM

- It does not mark any step MECHANICAL or JUDGEMENT (cell `CN-o-4`).
- It does not grade `O3-J1`; that is `3.0.0_SA_CVO`'s at L9.
- It makes no claim about whether the checklist can now be RUN end to end. It cannot, and the file says so: two STOPs
  stand with named owners, a sovereign input (the portal paths) has no registry carrier, and one step waits on
  `EN-s-1`. FWD-5's first real run is cell C6, which is not cut.
- It moves nothing live. This cell edited one markdown file and appended three rows.
