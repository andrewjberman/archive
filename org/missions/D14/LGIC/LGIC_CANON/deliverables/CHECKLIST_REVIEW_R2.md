# CN-o-4 -- THE ONBOARDING CHECKLIST'S REVIEW, ROUND 2 (LGIC_CANON)

**Reviewer:** 0.9.0_WK_LGIC_CANON~9, an L7 worker of 2.0.0_SA_COO~G, on task order
`LGIC_CANON.CN-o-4-r2` (PRD `LGIC_CANON_PRD.md` v1.3 @`5b2336a5e4`, decomposition v4 cell `CN-o-4`).
**This reviewer did not write the checklist, and that is read from git, not claimed here:**
`infra/logic/10_ONBOARDING_CHECKLIST.md`'s last commit is @`a6c9652ac2`, author `0.9.0_WK_LGIC_CANON~8`
(cell `CN-o-3`); round 1's review was `0.9.0_WK_LGIC_CANON~7`'s @`894b41f920`. Criterion `O4-AC3`
compares the two authorship lines itself.
**Read at:** branch `wk-lgic-canon-2-10`, based on CLOUD @`d173e700f7`, worktree
`.worktrees/wk-lgic-canon-2-10`. A bare `:n` is a line of the checklist at that vintage; every other
citation carries its path.

## THE TEST -- TWO BARS, BOTH PRINTED

**Bar 1 (the mark).** A step is JUDGEMENT when the person running it must decide something the rules do
not already decide. Round 1's working rule is kept unchanged: a value counts as DECIDED when one of four
things fixes it -- an input in the checklist's inputs table (`:51-61`), a canon rule, a builder's output
or printed line, or a named owner (a STOP, a sign-off, or Andrew). A value whose FORM is fixed but whose
content is not is NOT decided. One undecided value makes a step JUDGEMENT however mechanical the rest is.

**Bar 2 (the account), new this round.** A MECHANICAL step is RUNNABLE TODAY only when all three hold at
the vintage above: (a) the builder the step names EXISTS today; (b) every input it reads has a carrier a
runner can reach today; (c) nothing upstream in the checklist stops before it. Where one fails, the step
is accounted for by a STOP with a NAMED OWNER -- a seat, a project, or Andrew. A MECHANICAL step that is
neither is the failure this bar exists to catch, and it is reported as such rather than smoothed over.

**What I did NOT do:** I did not mark a step to make the cell pass. Round 1's `CN-o-2` marked five steps
JUDGEMENT and failed its own criterion; that was the right act and it is the standard applied here. Every
mark below moved because the ARTIFACT moved, and each move names the bytes that moved it.

## WHAT WAS READ, AND WITH WHICH INSTRUMENTS

- `infra/logic/10_ONBOARDING_CHECKLIST.md` in full (432 lines), after `CN-o-3`.
- `infra/logic/02_DOCTRINE.md` (629 lines) -- R22 read in full at `:459-468`, plus R13, R14, R16, R19,
  R20, R21.
- `infra/logic/06_CONFORMANCE_LEDGER.md` v1.2 -- section 6's register in full, X8's row read at the
  source rather than through the checklist's summary of it, plus the decider note at `:141-146`.
- `org/missions/D14/LGIC/LGIC_CANON/deliverables/CHECKLIST_REVIEW.md` (round 1's, for comparison).

Five instruments were run in this worktree. Round 1's review was a reading pass with one `grade()` call
and one census; these are named so the CVO can see which of my statements are measured and which are read.

1. **Builder-existence sweep** (python, over the checklist's own `built:` lines). Denominator: 16 of 16
   steps carry a `built:` line. 15 name a path and read `built: yes`; **15 of 15 of those paths exist**
   in this worktree. One reads `built: no EN-s-1` (Step 13). This is bar 2 clause (a), measured.
2. **`grade()`, read-only** (`lib/opal_naming.py`, run by this reviewer):
   - `grade("opal-partner-newfirm", "DYNAMODB_TABLE")` -> `('OUT-OF-PATTERN', 'opal-partner-newfirm-table')`
   - `grade("opal-partner-demo", "DYNAMODB_TABLE")` -> `('OUT-OF-PATTERN', 'opal-demo-partner-table')`
   - positive control `grade("gateway-49f-sessions-table", "DYNAMODB_TABLE")` -> `('CONFORMANT', ...)`
   - negative control `grade("opal-data-newfirm", "S3_BUCKET")` -> RAISES `RaiseDefect` *"B2: 'newfirm'
     after opal-data- is no scope key"*, which is the control that proves `newfirm` is NOT a registry
     scope: so the partner-table grade above is the PRE-identity-row read, and the `demo` line beside it
     is the POST-identity-row read. **Both branches read OUT-OF-PATTERN**; only the suggested canonical
     form changes with the row's presence. Step 14's conflict therefore does not depend on run order.
3. **`comp-find 'family' --pathspec infra/logic`**: denominator 32 hits across 20 files (corpus `all`),
   read to both pages. Every hit is prose in `02_DOCTRINE.md`, `10_ONBOARDING_CHECKLIST.md`,
   `08_TENSION_MAP.md`, `ORDER_OF_OPERATIONS.md` or `README.md`. **Zero hits in `infra/logic/registry/`**
   (6 files: exemptions, remediations, resources, scopes, systems, tiers). The FAMILY input has no
   registry carrier; its carrier is the vendor's existing pipeline itself.
4. **X8's enumeration, read at its own row** (`06_CONFORMANCE_LEDGER.md` section 6): X8 names *"the four
   partner identity tables `opal-partner-{demo,49financial,cottonwood,inflection}`"*, state GRANTED, kind
   CONDITIONAL, decider and owner `1.0.0_SA_CTO`, and its condition ends *"until such a project lands the
   four names stand and are NOT violations"*. A fifth firm's table is not in the enumeration and not in
   the condition.
5. **EN-s-1's state, on two instruments** (Step 13's dependency): both
   `LGIC_ENFORCE.TO-EN-s-1.census-run.md` and `...-r2...` read `<status>pending</status>`; independently,
   round 1's proof instance
   `.../0.9.0_WK_LGIC_ENFORCE~7/LGIC_ENFORCE.TO-EN-s-1.census-run.proof_of_spec.json` carries 4 acceptance
   rows of which **2 read FAIL** (S1-AC1, S1-AC2 -- the census stopped on its first RAISE). The cell has
   not closed, by the proof and not only by the status field.

Also read to ground single marks: `infra/aws/terraform/shared-infra/s3-49financial.tf` at `:70-74` and
`:96-98` (the second comment block Step 6 orders kept verbatim -- `:74` does read *"opal-data-49financial
IS the bd/49F"*, which is the sentence a blind replace-all would falsify);
`infra/aws/terraform/shared-infra/cloudtrail-organization-trail.tf` (`local.org_trail_read_logged_buckets`
declared at `:46`, consumed at `:78`).

## THE MARKS

| step | mark | account | why |
|---|---|---|---|
| 1 | MECHANICAL | RUNNABLE | Every field of the identity row is either written out literally (`class`/`tenancy` FIRM, `kind` client, `enabled` true, `bucket_provisioned` false, `aliases` `[]`), derived from `<LONG>`/`<SHORT>`, or an inputs-table row, and the step ends at a printed line, `VALIDATE: OK`, with each `REFUSED` naming the field to correct (`:76-91`); the one fork, a firm Andrew has ruled product-shaped, is declared out of this checklist's scope (`:87-88`), and the sovereign forms are given to the run rather than met inside it (`:53-54`). |
| 2 | MECHANICAL | RUNNABLE | The branch is chosen by whether `validate` prints one named WARN line, and both branches are prescribed to the byte -- append `{"key": "<LONG>", "short": "<SHORT>"}` and re-render, or make no edit because the firm list has moved to the registry -- ending at `VALIDATE: OK` with no warning naming `<LONG>` (`:97-108`); the named builder `org/standards/NAMING_SCHEMA.json` exists. |
| 3 | MECHANICAL | RUNNABLE | Round 1's two free values are now fixed by named sources: the pipeline directory is the FAMILY's and is read rather than named (`:129-135`, R22), and a master row's `label` is *"the name the vendor's own header gives that master, copied, not composed"* under R3 (`:122-126`), so the run types neither; the vendor-with-no-family case exits the checklist into R19 work rather than being decided inside it (`:118-120`), and that branch is the one caveat printed under OBSERVATIONS below. |
| 4 | MECHANICAL | RUNNABLE | One command with no argument to choose, `python lib/opal_naming.py generate --out .`, whose output is one `WROTE` line per file and a `GENERATE:` summary, committed unedited, and whose done-condition is a measured state -- a second `generate` leaves `git status` clean (`:144-160`). |
| 5 | MECHANICAL | RUNNABLE | The edit is one key with an empty list, `"opal-data-<LONG>": []` (`:170-171`); whether a principal is ever added is explicitly not the runner's call -- it needs a `reason` and a never-widen `signoff_ref` from 1.0.0_SA_CTO and 2.0.0_SA_COO, and the step says the runner adds none on their own reading (`:171-175`). |
| 6 | MECHANICAL | RUNNABLE | A copy with an enumerated edit list and "no others", now including the scoped-replace clause that keeps the template's second comment block VERBATIM (`:181-198`) -- I read that block at `s3-49financial.tf:70-98` and the two lines the step cites are the lines it says they are -- plus one named value added to `local.org_trail_read_logged_buckets`, which exists at `cloudtrail-organization-trail.tf:46`, and it closes on a named row flip and a re-run of Step 4 (`:203-211`). |
| 7 | MECHANICAL | RUNNABLE | The resource SET and every function word -- round 1's two undecided values -- are now the family's, inherited not chosen, under R22 read at `02_DOCTRINE.md:459-468` (*"inheriting the family's tables, partition forms, resource set, function words and directory"*), and the step states that FN1's word-choice clauses bind the family's NAMER whose naming has already happened (`:218-223`), leaving `name()` to compose from inputs only. |
| 8 | MECHANICAL | RUNNABLE | `<table>` and `<partition>`, round 1's undecided pair, are read from the vendor family's existing pipeline with `<scope>` set to this firm (`:243-247`, R22), so the property round 1 found missing -- two runs against one family writing one tree -- is now supplied by the rule rather than by `key()`, whose `_segment` the step correctly says does not supply it. |
| 9 | MECHANICAL | RUNNABLE | Which gold tables, their names, the gold partition form and `<source>` for a combined build are all the family's (`:263-266`, R22), and the remaining values are canon defaults with no runner input: the home by R5, parquet by R11, Lambda by R13 with EC2 only on Andrew's deferred threshold, `state` by R21 and the code home by R16 (`:268-276`). |
| 10 | MECHANICAL | STOP: ADVI_FIRMBKTS | The step's own values are fixed (the builder address, kebab-case `.json`, R14's mandatory chain) and it forbids the one hand-typed escape by name -- a new firm mints no legacy served key, the legacy list being a closed membership of existing firms (`:290-294`) -- and it then STOPs, because two live routes read a key `address()` cannot produce (the edge auth validator's `platinum/{firmId}/ownership_map.json` and the shared router's `platinum/advi/{firm}/`), with the repoint assigned to `ADVI_FIRMBKTS` by ruling A-8 and row LGIC_CANON-W6-S3 (`:296-305`). |
| 11 | MECHANICAL | RUNNABLE | One command, one printed verdict: the step is done only on `NAMING-GATE: PASS`, `WARN` counts as a refusal and the step says why (the kill switch `org/mcp/naming-gate.enforce` is absent at this vintage), and each refusal prints the canonical form or builder call that replaces the literal (`:311-320`); the named builder `.tools/naming-gate.py` exists. |
| 12 | MECHANICAL | RUNNABLE | Every act has a printed result and none is a choice: apply only through `safe-apply`, grade each new resource name with `grade(name, type)` until the plan limb of `EN-t-2` lands, apply only when every one reads `CONFORMANT`, one ledger entry opened before and closed after (`:326-335`); `.tools/safe-apply.sh` exists, and the conflict this rule meets is marked on Step 14, the step that prescribes the offending name. |
| 13 | MECHANICAL | RUNNABLE | This is the one step whose builder reads `built: no` (cell `EN-s-1`), and it is runnable today ONLY on its until-then branch, which writes `EN-s-1 open` in the run's record and leans on Steps 11 and 12 to grade every name this run adds; I confirmed the dependency on two instruments -- both EN-s-1 orders read `pending` AND round 1's proof carries 2 FAIL of 4 rows -- so the census arm is genuinely unavailable and the step both says so and names the cell that lands it (`:337-347`). |
| 14 | MECHANICAL | STOP: 1.0.0_SA_CTO (X8); Andrew (portal paths) | The firm id is the identity row's `key`, the users are inputs, and the two values the runner could otherwise invent are stopped on named owners: the partner table's name on `1.0.0_SA_CTO`, X8's decider and owner, because X8 enumerates four tables and a new firm's is not among them (`:360-376`), and the portal page-access list on Andrew, a SOVEREIGN input with no registry carrier (`:379-381`); my own `grade()` run confirms the conflict is live for a NEW firm and not merely for X8's four -- see the next section, which is where this mark is argued. |
| 15 | MECHANICAL | RUNNABLE | Nothing in the step is typed: Step 4 already wrote the routing entries, the shared-bucket check is a read of `FIRM_CONFIG` with a stated pass condition, and the deploy set is a lookup -- every edge function whose source imports `../_shared/firm-config.mjs`, plus the investor-reporting packages that ship `loaders.py` (`:391-403`); the one item it does not cover, the ownership map, it hands back to Step 10's STOP by name rather than leaving it to the runner. |
| 16 | MECHANICAL | STOP: ADVI_FIRMBKTS (inherited from Step 10, cited in this step's own pass condition) | The acts and the pass condition are fixed and measurable -- each surface's dashboard loads with the firm's own data, every platinum request returns HTTP 200 from `opal-data-<LONG>`, and the negative control is another firm's path returning 401 (`:409-414`) -- but bar 2 clause (c) fails: the pass condition cites "(Steps 10 and 15)" and Step 10 STOPs, so no run reaches a served dashboard for a new firm until `ADVI_FIRMBKTS` repoints the two routes, and this step is marked on that fact rather than on its own text, which carries no STOP of its own. |

## THE TALLY

Steps: **16**. MECHANICAL: **16**. JUDGEMENT: **0**.
Of the 16 MECHANICAL: **13 RUNNABLE** (1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 15) and **3 STOPPED with a
named owner** (10 and 16 on `ADVI_FIRMBKTS`; 14 on `1.0.0_SA_CTO`, with a second STOP on Andrew for the
portal paths). No MECHANICAL step is left unaccounted for, which is bar 2's whole question.

**What moved since round 1, and on what.** Round 1 marked five steps JUDGEMENT: 3, 7, 8, 9 and 14.

| step | round 1's undecided value | what decides it now |
|---|---|---|
| STEP 3 | the pipeline directory's existence and name; a master row's free-text `label` | R22 makes the directory the family's, read not named (`:129-135`); R3 makes the label the vendor header's, copied not composed (`:122-126`) |
| STEP 7 | the resource SET; each function word | R22: the firm's pipeline is an INSTANCE of the family, inheriting its resource set and its function words (`02_DOCTRINE.md:459-468`; `:218-223`) |
| STEP 8 | every bronze/silver `<table>`; bronze's `<partition>` | R22: both are the family's, with `<scope>` set to this firm (`:243-247`) |
| STEP 9 | which gold tables and their names; the gold partition form; `<source>` for a combined build | R22, same sentence, extended to `state` and `code` (`:263-266`) |
| STEP 14 | which of two prescribed rules gives way -- Step 12's CONFORMANT-only apply, or the mandated `opal-partner-<LONG>` | neither: the step no longer asks the runner to choose, it STOPs on X8's owner `1.0.0_SA_CTO` (`:360-376`) |

Four of the five moved on ONE canon sentence, R22, which did not exist at round 1 and which names these
four steps explicitly as the reason it was written. That is a single point of dependence and it is stated
here as such: if R22 were withdrawn or narrowed, Steps 3, 7, 8 and 9 return to JUDGEMENT together.

## IS STEP 14's STOP HONEST, OR IS IT DEFERRAL?

This is the mark most worth arguing, so it is argued rather than asserted. **I find the STOP honest**, on
four readings, of which two are my own instruments and two are the source documents.

1. **The conflict is real for a NEW firm, not only for X8's four.** The ledger's X8 row records
   OUT-OF-PATTERN for the four existing tables, EXERCISED 2026-09-16. That says nothing about a fifth. I
   ran `grade()` myself: `grade("opal-partner-newfirm", "DYNAMODB_TABLE")` reads **OUT-OF-PATTERN**, and
   the negative control (`opal-data-newfirm` as an S3 bucket RAISES `B2: 'newfirm' ... is no scope key`)
   shows that read is the pre-identity-row one, while `opal-partner-demo` -- a firm that IS in the
   registry -- also reads OUT-OF-PATTERN. Both branches refuse, so Step 12's apply condition
   (`:330-332`, apply only when every new resource name reads `CONFORMANT`) genuinely blocks Step 14's
   mandated name for any new firm.
2. **X8 does not cover it, read at the register and not through the step.** The entry enumerates
   `opal-partner-{demo,49financial,cottonwood,inflection}`; its condition closes *"until such a project
   lands the four names stand and are NOT violations"*. Four named tables, four standing names. A fifth
   firm's table is outside both the enumeration and the condition, so quoting X8 as cover for it would be
   a declared exception claimed for an object it does not name. **The step does not do that** -- it says
   so in its own words (`:372-373`) and stops.
3. **The act the STOP defers is not available to this cell or to any runner.** Extending X8 is a write to
   `06_CONFORMANCE_LEDGER.md` section 6, whose decider the ledger names as `1.0.0_SA_CTO` under Andrew's
   2026-09-16 ~05:2xZ delegation (`:141-146` of the ledger), and R20 makes every exception
   sovereign-acknowledged (`02_DOCTRINE.md` R20: *"Every exception is sovereign-acknowledged and recorded
   with the schema in section 4"*). A worker or a checklist runner extending the enumeration would be
   declaring an exception it cannot decide. It is also unavailable in a second, simpler way: the
   enumeration lists NAMED tables, and at cut time there is no new firm to name -- the entry can only be
   extended when a specific `<LONG>` exists. So the STOP is not work `CN-o-3` skipped; it is work that
   cannot be done before the run that needs it, by the seat that is running.
4. **The alternatives are both violations, and the step forecloses both.** Renaming the table breaks
   every partner sign-in (X8's two coordinates: `partnerTableName(firmId)` derives the name at runtime in
   two byte-identical carriers, and the auth role holds `dynamodb:GetItem` on `table/opal-partner-*`
   twice), which X8 rules an R19 act under never-widen sign-off. Applying the departure undeclared is
   R20's own violation case. The step names both and takes neither (`:363-376`).

**The cost of the STOP, stated rather than hidden:** it is reached on EVERY first run for EVERY new firm,
so FWD-5's first real run (cell C6) needs a `1.0.0_SA_CTO` act inside the run's window, not before it.
That is a sequencing fact for whoever cuts C6, and it is not a defect in the step. The same is true of
Step 10's STOP, which the checklist already routes to `ADVI_FIRMBKTS` and which `org/missions/SEQUENCE.yaml`
already orders after LGIC (`:304-305`).

## OBSERVATIONS THAT DO NOT CHANGE A MARK

1. **Step 16's STOP is inherited, not written.** Steps 10 and 14 carry the word STOP in their own text;
   Step 16 does not, and a reader of Step 16 alone would take it for runnable. I marked it STOPPED because
   its pass condition cites Steps 10 and 15 and Step 10 STOPs. The checklist's closing section lists five
   STOP points and does not say Step 16 inherits one (`:422-432`).
2. **One of the five listed STOP owners is a METHOD, not a seat.** The closing section claims *"Each STOP
   point names an OWNER, so none of them is blocked on nobody"*, then lists the vendor-with-no-family case
   as *"R22's non-application: that pipeline is R19 work, not onboarding"* (`:430`). R19 is a rule naming a
   method, not a person or a seat. Four of five list a seat, a project or Andrew; this one does not, so
   the claim overstates by one item. It does not change Step 3's mark, because that branch leaves the
   checklist rather than stalling inside it -- but if a run ever takes it, nobody is named to answer.
3. **The FAMILY input has no registry carrier.** Measured: 32 of 32 `family` hits under `infra/logic` are
   prose; none is in `infra/logic/registry/`. So the GIVEN input rests on the vendor's existing pipeline
   code and S3 trees, and where a family's existing firms run divergent trees -- the ledger records
   `_legacy` bronze/silver pairs and a JSON-under-silver format move inside the blackdiamond family -- WHICH
   tree is the family is settled by whoever hands the input over, not by anything the checklist or the
   canon names. That is consistent with the inputs table's own definition of GIVEN (*"a document outside
   this run fixes it"*, `:47-48`), and it is the reason Steps 3, 7, 8 and 9 read RUNNABLE rather than
   self-contained.
4. **The canon's own header count is stale.** `02_DOCTRINE.md`'s title line still reads v1.0 and section 0
   still reads `RULES CARRYING ALL THREE PARTS: 21 of 21`, while the file now carries **22 rule blocks**
   (R22 inserted after R13) and its change log's last row reads v1.1. R22 itself carries all three parts,
   so nothing in my marks depends on the count. Filed as surprise row `LGIC_CANON-W9-S1`; it belongs to
   `CN-k-2`'s artifact, not to this one.

## WHAT THIS REVIEW DOES NOT DO

- It does not edit the checklist, the canon or the ledger -- none is in this order's `<paths>`.
- It does not grade `CN-o-3`'s own criteria, and it does not re-run them.
- It does not rule on whether X8 SHOULD be extended, whether the partner tables should be renamed, or
  when `ADVI_FIRMBKTS` should run. Those belong to `1.0.0_SA_CTO` and to that project.
- `O4-J1` -- whether these marks are this reviewer's own reading, and whether each RUNNABLE is a claim a
  runner could act on today -- is graded at L9 by `3.0.0_SA_CVO`. It is not graded here.
