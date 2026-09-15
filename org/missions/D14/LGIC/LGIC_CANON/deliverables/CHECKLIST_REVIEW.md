# CN-o-2 -- THE ONBOARDING CHECKLIST'S REVIEW (LGIC_CANON round 1)

**Reviewer:** 0.9.0_WK_LGIC_CANON~7, an L7 worker of 2.0.0_SA_COO~G, on task order LGIC_CANON.TO-CN-o-2 (PRD
`LGIC_CANON_PRD.md` v1.3 DEC-6, cell candidate C5). **This reviewer did not write the checklist.**
`infra/logic/10_ONBOARDING_CHECKLIST.md` was written by 0.9.0_WK_LGIC_CANON~6 (cell CN-o-1, last commit @05d5131e5e).
**Read at:** CLOUD @c08fd0c0eb (branch `wk-lgic-canon-1-7c`). Every citation below is `path:line` at that commit. A
bare `:n` is a line of the checklist.

**The test applied** is the order's own: *"A step is JUDGEMENT when the person running it must decide something the
rules do not already decide."* In practice, a value a step asks for counts as decided when one of these fixes it:

- an input in the checklist's inputs table (`:32-42`);
- a canon rule;
- a builder's output, or a printed line;
- a named owner: a STOP, a sign-off, or Andrew.

A value whose FORM is fixed but whose content is not (a case, a grammar slot) is not decided. One undecided value
makes a step JUDGEMENT, however mechanical the rest of it is.

**What was read.**
- The three reads the order names: the checklist in full (341 lines); `infra/logic/02_DOCTRINE.md` v1.0 in full (576
  lines); and the CONTRACTS table of `org/missions/D14/LGIC/LGIC_ENFORCE/prd/LGIC_ENFORCE_PRD.md`.
- Files the steps point to, read only to ground a mark:
  - `infra/logic/registry/scopes.json`: the `inflection`, `cottonwood` and `08242234` rows;
  - `infra/logic/registry/systems.json`: its `_about` and its 17 rows;
  - `infra/logic/registry/tiers.json`: `homes`;
  - `lib/opal_naming.py`: `_segment`, `key` and `address` (`:1269-1315`);
  - `infra/aws/terraform/shared-infra/s3-49financial.tf`, in full;
  - `infra/aws/users/ONBOARDING.md`: sections 2 and 5;
  - `infra/aws/terraform/partner-firms/demo.tf`;
  - `org/standards/NAMING_SCHEMA.json`: `changelog`.
- Two instruments were run:
  - one read-only `grade()` call (Step 14);
  - one `comp-find` census of `opal-partner`: 61 hits across 502 files in `infra/logic`, `org/standards` and
    `org/missions/D14/LGIC` (corpus `all`).

## THE MARKS

STEP 1: MECHANICAL -- Every field of the identity row has a value the step or the inputs table fixes. `key`, `long` and `bucket` come from `<LONG>` and `short` from `<SHORT>`. `class`/`tenancy` FIRM, `tenant.kind` client, `enabled` true, `bucket_provisioned` false and `aliases` [] are written out (:53-61). The display name, email domain, surfaces and bindings are inputs (:36-39). The field set is the one the `cottonwood` and `inflection` rows carry (infra/logic/registry/scopes.json). Class FIRM is R5's ruled default for client-confidential data together with R7 (02_DOCTRINE.md:317-320, :341-342). The only fork, a firm Andrew has ruled product-shaped, is a STOP (:63-65). The step is done at a printed line, `VALIDATE: OK` (:67-68). One tension is already settled by the step, so the runner does not settle it: canon section 6 says "A scope not on the table returns to him" (02_DOCTRINE.md:536-538), and the step applies R5's default, stopping only where Andrew has ruled the firm product-shaped.
STEP 2: MECHANICAL -- The branch depends on whether `validate` prints one named WARN line (:74-76). On that branch the appended object is `{"key": "<LONG>", "short": "<SHORT>"}`, both inputs. Two named render commands follow, and `--check` must exit 0 (:77-81). The other branch makes no edit (:82-83). The step is done at a printed state, `VALIDATE: OK` with no warning naming `<LONG>` (:85). The version bump takes the next number in the schema's changelog (org/standards/NAMING_SCHEMA.json `changelog`, last entry v1.8). "In that project's lane" names where the edit is committed. It leaves the runner no choice of value.
STEP 3: JUDGEMENT -- Part (c) applies "If the firm's pipelines get a source directory of their own", and it records that directory "under the name the pipeline's author gave it" (:98-103). Neither whether one exists nor its name is an input; the inputs table, which lists what is "given to the run, never chosen by the person running it", does not carry them (:32-42). No rule decides them: R16's non-application puts the git source tree outside the canon (02_DOCTRINE.md:454), and the step names no owner and no STOP. So whoever builds the firm's pipelines invents both. Part (a) also leaves one free value. A master row is filled "the same way" as `08242234`, and that row carries a free-text `label` ("49F Schwab SmartX", infra/logic/registry/scopes.json) that no input or rule supplies. Part (b) and the rest of (a) are fixed by the inputs. Not counted: the new-vendor `systems.json` row (:105-106), whose fields that file's `_about` defines. A vendor no directive names takes the owner "inferred" reading that seven vendor rows already carry, with its claim marked inferred.
STEP 4: MECHANICAL -- One command, with no argument for the runner to choose: `python lib/opal_naming.py generate --out .` (:112). It prints a `WROTE <path>` line per file and a `GENERATE:` summary, and every written file is committed unedited (:112-116). Done is a measured state: running `generate` again leaves `git status` clean (:127-128). Every value it writes comes from the registry rows Steps 1 to 3 wrote.
STEP 5: MECHANICAL -- The edit is fixed: the key `"opal-data-<LONG>"` with an empty list (:138-139). Whether a principal is admitted is not the runner's call. Admission needs a `reason` and a `signoff_ref`, the never-widen sign-off by 1.0.0_SA_CTO and 2.0.0_SA_COO, and "The person running the checklist adds no principal on their own reading" (:139-142). Which principals need a request is a lookup: those serving Step 15's routes whose names do not carry `<SHORT>` (:142-143). The fence itself is generated (the fence patterns row of the LGIC_ENFORCE CONTRACTS table).
STEP 6: MECHANICAL -- The step is a copy with enumerated edits "and no others" (:149-157), plus one named value added to one named list (:162-164). It is applied through safe-apply from a checkout holding a named commit, with a ledger entry, and ends with a named row flip and a re-run of Step 4 (:166-170). The template's policy has no firm-specific logic beyond the `fence_patterns["49financial"]` key and its own bucket references. Its principal lists are the generated `fence_patterns` and `fence_exemption_arns` (infra/aws/terraform/shared-infra/s3-49financial.tf:103-130), so the copy needs no firm-specific choice. The template's comment block at :70-98 is not its header, so the prescribed replace-all keeps it and rewrites it into false text for the new firm: :74 would read "opal-data-<LONG> IS the bd/49F firm's client bucket", and :98 would name a ledger entry that does not exist. That is a defect in the copied comments, and it asks the runner to decide nothing.
STEP 7: JUDGEMENT -- `name()` composes the name mechanically, and three of its inputs are decided: the system by SY1 (02_DOCTRINE.md:221), the scope `<LONG>` (an input), and the kind by node type (02_DOCTRINE.md:227-246). Two things are not decided. The first is the resource set, "every role, function, queue, topic, alarm, table, schedule and rule the firm's pipelines need" (:176-177), which no input or rule supplies. The second is each function word. The canon says FN1's word-choice clauses "bind the NAMER, who has the item's description" (02_DOCTRINE.md:216), and the verbs it names (publish, fetch, read, build, download) are examples, not a closed list. This run is handed no item descriptions (:32-42), so the runner writes each description and picks each word. The table qualifier inherits the table names Steps 8 and 9 leave open.
STEP 8: JUDGEMENT -- The home is decided (infra/logic/registry/tiers.json `homes.FIRM`: bronze and silver in `opal-data-assets`), and so are scope, source and silver's form: `date=YYYY-MM-DD`, event-triggered (R10; :194-199). Not decided: the `<table>` of every bronze and silver location, and bronze's `<partition>`. No input names them (:32-42). The canon fixes only a table's case, snake_case (02_DOCTRINE.md:179). N1 offers three partition forms without choosing one for bronze (02_DOCTRINE.md:183-186), while R9 says bronze keeps "compact `YYYYMMDD`" (02_DOCTRINE.md:364-365). `key()` checks source, scope and tier against the registry and schema, but it passes table and partition through `_segment` only: non-empty ASCII with no `/` (lib/opal_naming.py:1269-1272, :1287-1300). So two runners could write two different bronze and silver trees for one firm, and both would pass every gate the checklist names.
STEP 9: JUDGEMENT -- Decided: the gold home `opal-data-<LONG>` (R5), the format, parquet (R11), the compute, Lambda, with EC2 only on Andrew's deferred threshold (R13), and the `state` and `code` tiers (:208-216). Not decided: (1) which gold tables the firm gets, and their `<table>` names, which no input names (:32-42) and whose case alone the canon fixes (02_DOCTRINE.md:179); (2) the gold `<partition>` form, since R11's "dated/timestamped-in-title parquets ... each day we just add a row" (02_DOCTRINE.md:385-386) fits both N1's `date=YYYY-MM-DD` and its named-leaf form (02_DOCTRINE.md:183-185); (3) for a combined build, `<source>`, which is the product or subsystem "that owns the combination" (02_DOCTRINE.md:221), and no row this step names records which product owns which combination. As in Step 8, `address()` accepts any of these choices (lib/opal_naming.py:1303-1315).
STEP 10: MECHANICAL -- The home `opal-data-<LONG>` (R6), the JSON format written by a publisher that reads gold (R12), and the case of a new file (kebab-case `.json`, N1) are fixed (:224-228). The served keys are the ones the firm's surfaces' routes already request, which Step 16 grades request by request, so each key's `<table>` and `<leaf>` belong to the route, not to the runner. Where a route reads a key `address()` cannot produce, the step STOPs and names the owner in row LGIC_CANON-W6-S3 (:230-236). Unlike Steps 8 and 9, the platinum names are fixed by a consumer outside the pipeline. At this vintage the step ends at that STOP for the two reads it names.
STEP 11: MECHANICAL -- One command, `bash .tools/safe-commit.sh`. The verdict is a printed summary line: the step is done only on `NAMING-GATE: PASS`, and `WARN` counts as a refusal (:242-247). Each refusal prints its replacement, a canonical form or a builder call (:248-249). A `NAMING RAISE` is fixed at its registry or schema row (:250). A departure kept on purpose is Andrew's to acknowledge under R20 (:251; 02_DOCTRINE.md:484-492).
STEP 12: MECHANICAL -- On its own text every act has a printed result: apply only through safe-apply; grade each new resource name in the plan with `grade(name, type)`; apply only when every one reads `CONFORMANT`; open and close a ledger entry (:257-266). The conflict this rule meets in Step 14 is marked on Step 14, the step that prescribes the name.
STEP 13: MECHANICAL -- The branch depends on a measured state: whether cell `EN-s-1` has closed. Its two task orders are named (:272-274). Each branch is prescribed. Once it closes, run the named census command, and fix any row carrying `<LONG>` or `<SHORT>` that does not read `CONFORMANT` at its name or registry row. Until then, write `EN-s-1 open` in the run's record (:275-278).
STEP 14: JUDGEMENT -- The step prescribes the partner table `opal-partner-<LONG>` and says to "Apply it as Step 12 says" (:287-289). Step 12 applies only when every new resource's name reads `CONFORMANT` (:261-263). `grade()` reads that name OUT-OF-PATTERN: `grade("opal-partner-demo", "DYNAMODB_TABLE")` returned `('OUT-OF-PATTERN', 'opal-demo-partner-table')`, and `opal-partner-49financial` returned `('OUT-OF-PATTERN', 'opal-49f-partner-table')` (lib/opal_naming.py, run by this reviewer). With a different instrument, both LGIC_NAMING human graders read the second name the same way (org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/n6-grader-a.tsv:16, n6-grader-b.tsv:16). The canonical name is not a way out, because the auth handler builds the table name as `opal-partner-{firmId}`, and portal-auth's IAM grant covers `opal-partner-*` (infra/aws/users/ONBOARDING.md:187-199). No register entry declares the departure: the census of `opal-partner` has no hit in `infra/logic/06_CONFORMANCE_LEDGER.md`, `infra/logic/registry/` or `org/standards/`. The step names no STOP and no owner for the conflict, so the runner must decide which of two prescribed rules gives way. One option is an R20 departure for Andrew to acknowledge (:24-26); the other is renaming, which breaks sign-in. The step's other acts are fixed: the firm id is the row's `key`; the users are inputs; and the portal paths are Andrew's, or a STOP (:290-294; row LGIC_CANON-W6-S2 records only that these acts have no builder).
STEP 15: MECHANICAL -- Nothing is typed (:304). The shared-bucket check is a read of `FIRM_CONFIG` with a stated pass condition (:306-308). The functions to rebuild are found by lookup: every edge function whose source imports `../_shared/firm-config.mjs`, and the investor-reporting packages that ship `loaders.py` (:311-313). Each is applied as Step 12 says, and the ownership map belongs to Step 10's STOP (:315-316).
STEP 16: MECHANICAL -- The acts are fixed: the Step 14 admin signs in and opens each surface the row sets `true`. The pass condition is measurable: every platinum request returns HTTP 200 from `opal-data-<LONG>`. So is the negative control: another firm's path returns 401 (:322-325). The record's home is named (:325-327). Nothing is left to the runner's reading. At this vintage the step cannot pass until Step 10's STOP is answered.

## TALLY

Steps: 16. MECHANICAL: 11 (Steps 1, 2, 4, 5, 6, 10, 11, 12, 13, 15, 16). JUDGEMENT: 5 (Steps 3, 7, 8, 9, 14). The
cell's acceptance is zero JUDGEMENT marks, so this review does not meet it, and the order stays open on `O2-AC2`.

## WHAT THE FIVE HAVE IN COMMON

- **Steps 3, 7, 8 and 9 all come from one cause.** The checklist makes building the firm's pipelines part of
  onboarding. The canon fixes a pipeline's homes, formats, compute and name grammar, but not its contents: which
  directory, which tables, which partition form, which resources, which function words. The inputs table carries
  none of them. Step 10 escapes the cause because a served route outside the pipeline fixes its keys.
- **Step 14 is a separate cause:** two prescribed rules conflict, and the conflict was measured with `grade()` and
  the census above. Step 14's mandated name, forced by the auth handler, fails Step 12's apply condition, and nothing
  in the checklist resolves it.
- **What would move the marks is for the checklist's author and the canon to decide, not this review.** An input
  that fixes the pipeline's contents (for example, "the firm runs the vendor's existing pipeline with scope
  `<LONG>`, under the tables and resources it already names for the firms it serves") would change the first four.
  A declared R20 entry for the partner-table name, or a STOP naming its owner, would change Step 14.

## WHAT THIS REVIEW DOES NOT DO

- It does not edit the checklist, which is outside this order's grant, and it does not re-run CN-o-1's criteria.
- It does not say whether the canon ought to decide table names, or which rule should give way in Step 14. Those are
  calls for CN-k-1, the checklist's owner and 1.0.0_SA_CTO.
- `O2-J1`, whether every reason above holds, is graded at L9 by 3.0.0_SA_CVO.
