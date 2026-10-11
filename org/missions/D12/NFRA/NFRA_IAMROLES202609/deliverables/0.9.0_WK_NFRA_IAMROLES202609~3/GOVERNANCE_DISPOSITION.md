# NFRA_IAMROLES202609 -- IAM-s-6: GOVERNANCE DISPOSITION of the undeclared roles

Cell: `IAM-s-6`. Serves outcome `FWD-4`. THIS IS THE GOVERNANCE HALF ONLY -- for each member of
IAM-s-5's set, the question answered is whether this role belongs in code at all, never a question
about how widely it is granted. Bound `C-TWO-REMEDIES` (D6) is honoured throughout: nothing below
touches the scope of any grant in either direction, and no permissions finding is read as a
governance answer -- that is `IAM-s-1`'s remedy, and it does not move with this one.

## INPUT SET AND ITS VINTAGE

The set dispositioned below is exactly the 16 members `IAM-s-5` established, unchanged: its
deliverable (`DECLARED_VS_LIVE.md` in this same folder, committed `52c82c7537`) measured
`comp-find '.' --corpus aws IAM_ROLE --all` at vintage 2026-09-10 05:57:16 UTC -- DENOMINATOR
219 hit(s) across 219 aws node(s) scanned, DRIFT (scanned) DECLARED=203 LIVE-no-DECLARED=16
(203 + 16 = 219) -- and then diffed that 16 by NAME against the L5 lane's own enumerated list
(2026-09-10 03:31:02 UTC), finding all 16 SAME (no arrival, no departure). IAM-s-5 found no member
moved off 16, so this cell disposes of the 16 named members as found, nothing more and nothing
fewer.

## METHOD -- how each disposition was reached

Per the bound's own warning ("a role you cannot find in Terraform via comp-iam is a role to look
for BY NAME before you class it as an exception"), each of the 16 was checked two ways, not
inherited from the L5 lane's character notes:

1. `.tools/comp-iam roles` (Terraform-source parser) re-run fresh this cell, at
   `2026-09-10T08:48:35Z` -- `.tools/comp-iam stats` at that same run: "IAM roles parsed: 191"
   (191, not the 195 the L5-lane preflight cited -- a live-plane count that does not hold across
   re-measurement; see the filed surprise row. This cell does not depend on the aggregate count,
   only on a NAME-LEVEL check against the fresh 191-role list). Each of the 16 names was grepped
   against that fresh role list exactly.
2. `.tools/comp-find "<role-name>" infra/ --all` (repo-source search, `--corpus all`, this cell's
   own re-run) for a first-party Terraform hit (`SURFACED`/`DEF` band), distinguishing an actual
   `resource "aws_iam_role"` declaration from a mention in a world-model census JSON or a
   hand-maintained inventory doc (neither of which is Terraform and neither of which decides
   anything).

Where step 1 or 2 found the role genuinely declared -- an `aws_iam_role` resource block naming it
exists in this repo's Terraform, cited by path -- the disposition is `DECLARED`: a fact, never a
recommendation. Where neither step found a declaration AND no documented rationale for exclusion
names a decision-maker, this worker -- who holds no send tool and cannot obtain a sign-off -- did
not invent an owner and did not quietly mark the line `DECLARED` to manufacture a fact that is not
there. That member's disposition is `ADOPT`: a recommendation that it be brought into Terraform, not
an accomplished fact and not yet a `DECLARED` state. Where neither step found a declaration AND a
real, unresolved decision (a service-default origin, a production-serving-path stake, or a residue
question) is owed to a named owner, the disposition is `EXEMPT owner=UNASSIGNED reason=<what is
owed and why>` -- unchanged from round 1, with the reason named per row below. Three different
shapes resulted from that split, matching the cell's own warning that one disposition would not fit
all sixteen:

- Members with **no service-default character, no serving-path criticality, and no documented
  exclusion rationale**, and for which neither check found an `aws_iam_role` resource block, are
  dispositioned `ADOPT` -- a recommendation, not a fact, that they be brought into code, absent any
  reason to except them and consistent with already-declared siblings of the same shape elsewhere in
  this estate's Terraform. FWD-4's ordinary default state is what these members are recommended
  toward, not what they presently are.
- One member sharing that same no-service-default, no-serving-path shape (`seeking-alpha-scraper-role`,
  row 13) is in fact ALREADY declared -- a real `aws_iam_role` resource block exists and is cited
  directly -- and carries `DECLARED`, not `ADOPT`: the ordinary default state FWD-4 asks for, already
  met, not still owed.
- Members that are **plausibly AWS service-default, sit on a production serving path, or read as
  residue** carry a real, unresolved decision that only a named owner can make (adopt or except).
  For those, the disposition is `EXEMPT owner=UNASSIGNED reason=<what is owed and why>`, per the
  bound's own instruction, and a surprise row is filed naming each class.

## DISPOSITION TABLE -- 16 of 16

1. `bd-merge-daily-lambda-role` -- DECLARED (round 6: `infra/aws/terraform/bd-pipeline/zz_adopt_family_a.tf`, TO-IAM-w-2 @beeb07f26c). Prior token: ADOPT owner=0.7.0_AE_CloudOps~Z reason=the adopting act (a
   `resource "aws_iam_role"` block for this name in `infra/aws/terraform/`) sits in a lane that
   exists and is busy, and NO seat in it has accepted this row -- a measured search, not an
   assumption; THE OWNER FINDING below carries its four planes and their denominators.
   Absent from the fresh 191-role comp-iam parse and from
   every first-party Terraform file in this repo (`comp-find infra/ --all`: only two world-model
   census/inventory JSON hits, no SURFACED or DEF band); an ordinary bd-domain role with 17 already
   Terraform-declared bd- siblings (`bd-processor-lambda-role`, `bd-silver-merge-role`,
   `bd-daily-trigger-lambda-role` and others, per the same comp-iam parse) and nothing in this repo
   distinguishing it as a candidate for exception.
   ACCEPTED 2026-10-09 by `0.7.0_AE_CloudOps~Z`: Live 2026-10-09: lambda trust, 1 inline `bd-merge-daily-policy`, 0
   consumers of 233 functions, RoleLastUsed EMPTY. Home `infra/aws/terraform/bd-pipeline/`, which already declares two
   roles from the same 2026-02-19 batch. Never used is NOT my reason to retire it: `news-pipeline/iam.tf:256,303`
   declares two roles it annotates `orphaned`, so this estate's pattern is to declare. I accept custody of the role
   AND of the adoption decision; I do NOT accept the apply, which is a separate WORLD act under its own never-widen
   pair, and any declaration must leave `inline_policy` and `managed_policy_arns` ABSENT (both are Optional+Computed
   and become authoritative when set). Full reasoning: deliverables/0.7.0_AE_CloudOps~Z/ACCEPTANCE_ROWS_TEN.md;
   families and order of application: ADOPTION_PLAN_TEN.md.
2. `bd-pipeline-task-role` -- DECLARED (round 6: `infra/aws/terraform/bd-pipeline/zz_adopt_family_a.tf`, TO-IAM-w-2 @beeb07f26c). Prior token: ADOPT owner=0.7.0_AE_CloudOps~Z reason=the adopting act (a
   `resource "aws_iam_role"` block for this name in `infra/aws/terraform/`) sits in a lane that
   exists and is busy, and NO seat in it has accepted this row -- a measured search, not an
   assumption; THE OWNER FINDING below carries its four planes and their denominators.
   Same evidence pattern as #1: absent from the fresh comp-iam
   parse, no SURFACED/DEF source hit, no documented rationale, an ordinary bd- role among many
   already-declared bd- siblings.
   ACCEPTED 2026-10-09 by `0.7.0_AE_CloudOps~Z`: Live 2026-10-09: `ecs-tasks.amazonaws.com` trust -- the only
   non-Lambda trust of my ten -- 1 inline `BDPipelineTaskPolicy`, RoleLastUsed 2026-02-02. Its 0 Lambda consumers is
   EXPECTED and is not evidence of disuse: the Lambda map cannot see an ECS task role. Home
   `infra/aws/terraform/bd-pipeline/`. CONDITION: its pair must state the assume_role_policy principal explicitly, the
   one field a copy-paste from a sibling Lambda role gets silently wrong. I accept custody of the role AND of the
   adoption decision; I do NOT accept the apply, which is a separate WORLD act under its own never-widen pair, and any
   declaration must leave `inline_policy` and `managed_policy_arns` ABSENT (both are Optional+Computed and become
   authoritative when set). Full reasoning: deliverables/0.7.0_AE_CloudOps~Z/ACCEPTANCE_ROWS_TEN.md; families and
   order of application: ADOPTION_PLAN_TEN.md.
3. `codebuild-semantic-clustering-role` -- DECLARED (round 6: `infra/aws/terraform/news-pipeline/zz_adopt_row3.tf`, TO-IAM-w-3 @fc8da02312). Prior token: ADOPT owner=0.7.0_AE_CloudOps~Z reason=the adopting act (a
   `resource "aws_iam_role"` block for this name in `infra/aws/terraform/`) sits in a lane that
   exists and is busy, and NO seat in it has accepted this row -- a measured search, not an
   assumption; THE OWNER FINDING below carries its four planes and their denominators.
   The closest thing to a named human anywhere in this row's record is a job title in a build log
   (`CODEBUILD_SETUP.md:3`, "Engineer: Data Scientist"), which is neither a seat nor an acceptance.
   Manually built via a documented one-off setup
   (`infra/aws/lambda/news_semantic_clustering/CODEBUILD_SETUP.md`, dated 2026-02-17, "Engineer:
   Data Scientist", "What Was Created: 1. IAM Role for CodeBuild -- Role Name:
   codebuild-semantic-clustering-role"). That document records what an engineer built, never a
   decision to exclude it from Terraform, so it does not meet FWD-4's ACCEPT bar for an exemption
   ("says who decided that and why" -- a build log names no such decision). House convention already
   manages CodeBuild roles of this exact shape in Terraform (`opal-drift-producer-codebuild-role`,
   `opal-stitch-produce-codebuild-role`, both present in the fresh comp-iam parse) -- this one is the
   outlier against that convention, not the norm.
   ACCEPTED 2026-10-09 by `0.7.0_AE_CloudOps~Z`: Live 2026-10-09: `codebuild.amazonaws.com` trust, 1 inline
   `CodeBuildSemanticClusteringPolicy`, RoleLastUsed 2026-09-11 -- live infrastructure, not a leftover. OPEN CALL I do
   not close: its home is a BUILD-plane question, and the module owning the semantic/news RUNTIME is not automatically
   the module that should own a CodeBuild project's role; I would not let a pair land it in `news-pipeline/` because
   the names rhyme. I accept custody of the role AND of the adoption decision; I do NOT accept the apply, which is a
   separate WORLD act under its own never-widen pair, and any declaration must leave `inline_policy` and
   `managed_policy_arns` ABSENT (both are Optional+Computed and become authoritative when set). Full reasoning:
   deliverables/0.7.0_AE_CloudOps~Z/ACCEPTANCE_ROWS_TEN.md; families and order of application: ADOPTION_PLAN_TEN.md.
4. `ecsTaskExecutionRole` -- EXEMPT owner=1.0.0_SA_CTO~Z reason=AWS-managed service role, minted by a
   console or service action (the literal conventional name AWS's own ECS quick-create
   task-execution-role wizard assigns), correctly outside our Terraform -- CLASS RULING, see CLASS
   RULINGS below; ruling recorded at
   `task-orders/NFRA_IAMROLES202609.TO-IAM-r-4.record-the-service-default-class-ruling.md` and
   `ledger/ROUND_ANALYSIS.round1.md` §4. Absent from the fresh 191-role comp-iam parse and from every
   first-party source file in this repo (only world-model census/inventory JSON mentions it), no
   change from round 1's research. Membership in the not-in-Terraform set is INHERITED from round 1's
   classification, carried forward unchanged by `IAM-r-1` -- `IAM-r-3`'s own per-member
   re-confirmation was not present in this worker's tree at write time; see CLASS RULINGS,
   MEMBERSHIP NOTE below.
5. `finbert-ec2-backfill-role` -- DEFER owner=0.7.0_AE_CloudOps~Z reason=completed one-shot backfill; retirement is a WORLD act no one has asked for (CTO, ROUND_ANALYSIS.round5.md @f77e32d7c3; revisited only if a finbert backfill recurs) -- the earlier ADOPT recommendation rested on: the adopting act (a
   `resource "aws_iam_role"` block for this name in `infra/aws/terraform/`) sits in a lane that
   exists and is busy, and NO seat in it has accepted this row -- a measured search, not an
   assumption; THE OWNER FINDING below carries its four planes and their denominators.
   Absent from the fresh comp-iam parse and from every
   first-party source file (census/inventory JSON only); an EC2 backfill role with no service-default
   naming pattern and no documented exclusion rationale anywhere in this repo.
   ACCEPTED 2026-10-09 by `0.7.0_AE_CloudOps~Z`: Live 2026-10-09: `ec2.amazonaws.com` trust, 1 inline
   `DynamoDBAccessPolicy`, created 14:23Z and last used 15:20Z on 2025-12-15 in us-east-2 and never since -- its whole
   lifetime is about one hour, the signature of a one-shot backfill. I propose NO custody home deliberately: adopting
   a role whose job is finished is the wrong act and retiring it is a WORLD decision nobody has asked for. The
   decision owed is adopt-or-retire, and the evidence that settles it sits with the workload's owner. I accept custody
   of the role AND of the adoption decision; I do NOT accept the apply, which is a separate WORLD act under its own
   never-widen pair, and any declaration must leave `inline_policy` and `managed_policy_arns` ABSENT (both are
   Optional+Computed and become authoritative when set). Full reasoning:
   deliverables/0.7.0_AE_CloudOps~Z/ACCEPTANCE_ROWS_TEN.md; families and order of application: ADOPTION_PLAN_TEN.md.
6. `lambda-ec2-runtime-monitor-role` -- ADOPT owner=0.7.0_AE_CloudOps~Z reason=the adopting act (a
   `resource "aws_iam_role"` block for this name in `infra/aws/terraform/`) sits in a lane that
   exists and is busy, and NO seat in it has accepted this row -- a measured search, not an
   assumption; THE OWNER FINDING below carries its four planes and their denominators.
   Same evidence pattern: absent from the fresh
   comp-iam parse, no SURFACED/DEF source hit beyond census JSON, no documented rationale for
   exclusion.
   ACCEPTED 2026-10-09 by `0.7.0_AE_CloudOps~Z`: Live 2026-10-09: lambda trust, 1 inline `EC2RuntimeMonitorPolicy` +
   `AWSLambdaBasicExecutionRole`, consumer `ec2-runtime-monitor`, RoleLastUsed 2026-10-09T09:51:30Z -- FIFTEEN MINUTES
   before I read it. This is a RUNNING PRODUCTION ROLE and the acceptance says so loudly, because the error this row
   invites is treating an undeclared role as a dormant one. OPEN CALL: its home -- a cross-cutting operational
   function no module obviously owns; `shared-infra/iam_legacy.tf` is the honest candidate but 'legacy' argues against
   putting live infrastructure there. I accept custody of the role AND of the adoption decision; I do NOT accept the
   apply, which is a separate WORLD act under its own never-widen pair, and any declaration must leave `inline_policy`
   and `managed_policy_arns` ABSENT (both are Optional+Computed and become authoritative when set). Full reasoning:
   deliverables/0.7.0_AE_CloudOps~Z/ACCEPTANCE_ROWS_TEN.md; families and order of application: ADOPTION_PLAN_TEN.md.
7. `lambda-test-role` -- RETIRE owner=0.7.0_AE_CloudOps~Z reason=three planes agree that nothing declares
   it and nothing uses it -- 0 Terraform hits across 415 tracked `.tf` files (IAM-r-3's per-member
   verdict list), 1 of 2382 live nodes with no consumer node pointing at it, and no LastUsedDate
   inside AWS's 400-day tracking window -- so the honest answer is that this role should not
   exist, which is neither "add it to Terraform" nor "keep it outside Terraform". A named owner
   decides and performs the act; NOTHING WAS DELETED BY THIS RECORD. AMENDED BY IAM-r-6: round 1
   wrote this row with the exemption value because the schema had nowhere else to put the answer,
   and it named the decision owed as "whether this role is still exercised at all and, if not,
   whether it should be retired" -- that is the question the evidence now settles. See THE
   RETIREMENT VALUE section below for the three planes, the positive control, the falsifier and
   the four-postulate record. OWNER AMENDED BY `IAM-t-1` from `UNASSIGNED`: the owner search ran
   and returned empty for this row too, and this row alone needs one thing the other eleven do
   not -- its terminal act deletes a live IAM object, which this estate reserves for human
   confirmation (CLAUDE.md, Agent Autonomy: "Human confirmation ONLY for: recursive deletion,
   destructive git, dropping tables/S3 deletes, stopping EC2, anything unrecoverable"), so no
   agent seat can be its terminal owner alone. Nothing was minted, scheduled or deleted by
   recording that. See THE OWNER FINDING below.
   ACCEPTED 2026-10-09 by `0.7.0_AE_CloudOps~Z`: Live 2026-10-09: lambda trust, ZERO inline, only
   `AWSLambdaBasicExecutionRole`, 0 consumers, RoleLastUsed EMPTY, created 2026-02-19T16:00:44 in a nine-role scripted
   batch. I accept RETIRE as the right disposition -- the only retirement among my ten -- because it grants nothing
   beyond CloudWatch Logs, its generic name identifies no workload, and it has never been used; rows 11 and 14 fail
   that test on every count. I do NOT accept the delete itself: the four proofs it needs (including an ABSENT negative
   control against a role known to be in use) and its rollback are in ADOPTION_PLAN_TEN.md Family F, and it is a WORLD
   act needing its own order and pair.
8. `opal-data-refresh-lambda-role` -- EXEMPT owner=0.7.0_AE_CloudOps~Z reason=production serving-path role
   (backs the deployed `opal-data-refresh-api` Lambda via a literal `role_arn`,
   `infra/aws/terraform/data-refresh/main.tf:38`) that Terraform already touches through five
   `aws_iam_role_policy` attachments explicitly naming it "the pre-existing
   opal-data-refresh-lambda-role" (`main.tf:53`) but never creates or owns as a resource. THE
   COUNT IS FIVE, CORRECTED FROM THREE BY `IAM-t-1` AND RE-READ AT SOURCE rather than inherited:
   `data-refresh/main.tf:58`, `:80`, `:99`, `:138` and `data-refresh/qa-scratch-instance.tf:36`,
   each carrying `role = "opal-data-refresh-lambda-role"` two lines below its
   `resource "aws_iam_role_policy"` line. Five is the tree-wide figure of record
   (`ledger/ROUND_ANALYSIS.round2.md` section 8; row `Z-W5-S2`); substance is unaffected at any
   count and no disposition moves. IAM-s-5's
   own character note flags an exemption here as "a much heavier claim" than for a background role;
   this worker cannot make that heavier call or name who accepts it. The decision owed is an explicit
   sign-off (adopt via import, or formally except) from a seat holding Terraform-change authority.
   OWNER AMENDED BY `IAM-t-1` from `UNASSIGNED`: the owner search ran and returned empty here too.
   The decision owed is unchanged, and the adopting TEXT for this role is already written and inert
   at `infra/aws/terraform/data-refresh/zz_adoption_candidate.tf.proposed:29-30` (`IAM-r-5`) -- so
   what is missing on this row is not the work, it is a seat that has accepted it. See THE OWNER
   FINDING below.
   ACCEPTED 2026-10-09 by `0.7.0_AE_CloudOps~Z`: I take custody of this role AND of the adoption
   decision for it, on evidence re-measured live today rather than inherited -- all THREE Lambdas in
   the data-refresh root (`opal-data-refresh-api`, `opal-data-refresh-api-qa-scratch`,
   `portal-time-machine`) assume this role, and all FIVE of its live inline policies are declared in
   this module, so this module is its custody home; I deployed through it today under
   `NFRA_OPLGTW.TO-OG-da-1` and the role was unchanged by both applies. WHAT I DO NOT ACCEPT BY THIS
   COMMIT: the apply. Moving the inert text into a live `.tf` is a separate WORLD act under its own
   never-widen pair, and I would not apply it as written until that pair names ADOPTION_PLAN section
   7's two non-travelling items -- the state key it lands in and the provider `default_tags` it
   inherits. CITATION NOTE: the count of five is confirmed against the live role (5 inline, 1 attached
   managed), but this row's LINE cites have aged -- the five are now `main.tf:60`, `:82`, `:101`,
   `:140` and `qa-scratch-instance.tf:53`, and 17 lines of that last shift are MINE, from the OG-da-1
   qa-scratch pin at `99c3b4c1b1`. The substance is unaffected at any line number.
9. `opal-smartx-lambda-role` -- DECLARED (round 6: `infra/aws/terraform/smartx-pipeline/zz_adopt_family_b.tf`, TO-IAM-w-1 @af790901d5). Prior token: ADOPT owner=0.7.0_AE_CloudOps~Z reason=the adopting act (a
   `resource "aws_iam_role"` block for this name in `infra/aws/terraform/`) sits in a lane that
   exists and is busy, and NO seat in it has accepted this row -- a measured search, not an
   assumption; THE OWNER FINDING below carries its four planes and their denominators.
   It is the ONE of the twelve that appears in this estate's hand-maintained IAM inventory, and that
   file's only owner statement is at FILE grain (`infra/aws/manifests/iam/iam-roles.yaml:3`,
   `# Owner: Andrew Berman`, `Last Updated: 2026-01-02`, `total_roles: 8`) -- not a row-grain
   acceptance, and round 2's own table records that nothing is owed by Andrew.
   Absent from the fresh comp-iam parse and from all Terraform
   source; documented only in a hand-maintained, non-Terraform inventory
   (`infra/aws/manifests/iam/iam-roles.yaml`, "Last Updated: 2026-01-02") and the portal-functions
   manifest (`infra/aws/manifests/lambda/opal-portal-functions.yaml:138,736-737`). An inventory entry
   describes the role; it is not a decision to except it from Terraform, so FWD-4's exemption bar is
   not met.
   ACCEPTED 2026-10-09 by `0.7.0_AE_CloudOps~Z`: Live 2026-10-09: lambda trust, THREE inline (`opal-smartx-logs`,
   `opal-smartx-s3-access`, `opal-smartx-secrets`), RoleLastUsed 2025-12-30. The cleanest adoption of my ten: every
   policy names the pipeline and `infra/aws/terraform/smartx-pipeline/` exists (15 .tf files, verified). Three inline
   policies is the most of any role here, so this is where a 'completed' block costs most. I accept custody of the
   role AND of the adoption decision; I do NOT accept the apply, which is a separate WORLD act under its own
   never-widen pair, and any declaration must leave `inline_policy` and `managed_policy_arns` ABSENT (both are
   Optional+Computed and become authoritative when set). Full reasoning:
   deliverables/0.7.0_AE_CloudOps~Z/ACCEPTANCE_ROWS_TEN.md; families and order of application: ADOPTION_PLAN_TEN.md.
10. `portal-auth-lambda-role` -- EXEMPT owner=0.7.0_AE_CloudOps~Z reason=production serving-path role per
    IAM-s-5's own character note ("PRODUCTION SURFACES ON THE SERVING PATH ... a much heavier
    claim"), and unlike `opal-data-refresh-lambda-role` this one has ZERO Terraform source touch at
    all (fresh comp-iam parse: absent; `comp-find infra/ --all`: only world-model census/inventory
    JSON and a parity dump, no SURFACED or DEF band). It is NOT the same object as the
    Terraform-declared `opalinvest-auth-lambda-role` (`infra/aws/terraform/portal-auth/iam.tf:16`,
    a distinctly-named sibling created in the same module) -- a genuinely separate, undeclared role
    next to an already-declared one for the same functional area. The heavier stakes IAM-s-5 named
    apply in full; the decision owed is an explicit sign-off from a seat with Terraform-change
    authority on whether to adopt or except, not a call this worker can make. OWNER AMENDED BY
    `IAM-t-1` from `UNASSIGNED`: the owner search ran and returned empty here too, and this row's
    adopting text is likewise already written and inert, in the same file
    (`infra/aws/terraform/data-refresh/zz_adoption_candidate.tf.proposed:66-67`, `IAM-r-5`, whose
    own row `Z-W6-S1` records that this module is the wrong custody home for it). See THE OWNER
    FINDING below.
    ACCEPTED 2026-10-09 by `0.7.0_AE_CloudOps~Z`: I take custody of this role AND of the adoption
    decision for it -- portal-auth is a surface this seat owns -- and I re-measured it live today: 1
    inline policy (`jwt-public-key-secret`), 1 attached managed policy
    (`AWSLambdaBasicExecutionRole`), `RoleLastUsed` EMPTY, created 2026-02-19T16:00:39Z, max session
    3600, description "Scoped Lambda role - created 2026-02-19 IAM audit" -- every value matching the
    inert text. WHAT I DO NOT ACCEPT BY THIS COMMIT: the apply, and separately the PLACEMENT. This
    module is the wrong custody home by row `Z-W6-S1`'s own finding; that open call is NOT settled
    here, because accepting custody of a role is not a decision about which module declares it. I also
    accept NO narrowing on the back of the zero-usage reading: `C-TWO-REMEDIES` binds, and a role that
    has never been used is not evidence that a permission is unneeded.
11. `portfolio-management-lambda-role` -- DECLARED (round 6: `infra/aws/terraform/portfolio-management/zz_adopt_family_e.tf`, TO-IAM-w-3 @fc8da02312). Prior token: ADOPT owner=0.7.0_AE_CloudOps~Z reason=the adopting act (a
    `resource "aws_iam_role"` block for this name in `infra/aws/terraform/`) sits in a lane that
    exists and is busy, and NO seat in it has accepted this row -- a measured search, not an
    assumption; THE OWNER FINDING below carries its four planes and their denominators.
    Absent from the fresh comp-iam parse and from all
    Terraform source (census/inventory JSON only). It is NOT the same object as the
    Terraform-declared `portfolio-export-lambda-role` (`infra/aws/terraform/portfolio-management/
    main.tf:227`, a distinctly-named sibling created in the same module) -- a genuinely separate,
    undeclared role alongside an already-declared one in the same domain, with no documented
    rationale anywhere in this repo for treating it differently.
    ACCEPTED 2026-10-09 by `0.7.0_AE_CloudOps~Z`: Live 2026-10-09: lambda trust, 1 inline `portfolio-s3-dynamodb` +
    `AWSLambdaBasicExecutionRole`, 0 consumers, RoleLastUsed EMPTY, created 2026-02-19T16:00:38 with the batch
    description. The best-precedented row of my ten: six of its nine batch siblings are already declared in their own
    domain modules, and its home `infra/aws/terraform/portfolio-management/` exists and declares the distinctly-named
    sibling `portfolio-export-lambda-role`, which I verified by printing the bytes at main.tf:226-227 rather than
    trusting this row's citation. I accept custody of the role AND of the adoption decision; I do NOT accept the
    apply, which is a separate WORLD act under its own never-widen pair, and any declaration must leave
    `inline_policy` and `managed_policy_arns` ABSENT (both are Optional+Computed and become authoritative when set).
    Full reasoning: deliverables/0.7.0_AE_CloudOps~Z/ACCEPTANCE_ROWS_TEN.md; families and order of application:
    ADOPTION_PLAN_TEN.md.
12. `rds-monitoring-role` -- EXEMPT owner=1.0.0_SA_CTO~Z reason=AWS-managed service role, minted by a
    console or service action (the literal name AWS's own RDS Enhanced Monitoring console flow offers
    when no role is specified), correctly outside our Terraform -- CLASS RULING, see CLASS RULINGS
    below; ruling recorded at
    `task-orders/NFRA_IAMROLES202609.TO-IAM-r-4.record-the-service-default-class-ruling.md` and
    `ledger/ROUND_ANALYSIS.round1.md` §4. Absent from the fresh comp-iam parse and from all
    first-party Terraform source, no change from round 1's research. Same class as
    `ecsTaskExecutionRole` and `vpc-flow-logs-role`; membership is INHERITED from round 1's
    classification, not independently re-confirmed by `IAM-r-3` in this worker's tree -- see CLASS
    RULINGS, MEMBERSHIP NOTE below.
13. `seeking-alpha-scraper-role` -- DECLARED. This one is factually already declared:
    `resource "aws_iam_role" "seeking_alpha_role" { name = "seeking-alpha-scraper-role" ... }` at
    `infra/aws/terraform/seeking-alpha/main.tf:240-241`, and this cell's fresh `comp-iam roles`
    re-run lists it directly by that exact name with `tf_resource: seeking_alpha_role`, `source:
    infra/aws/terraform/seeking-alpha/main.tf`. The DECLARED-vs-LIVE drift instrument's
    `LIVE-no-DECLARED` classification for this specific member does not match ground truth in
    Terraform source at this cell's own re-measurement; see the filed surprise row -- this is not a
    governance finding about the role, it is an instrument discrepancy the governance disposition
    corrects for.
14. `sentiment_query_api-role` -- ADOPT owner=0.7.0_AE_CloudOps~Z reason=the adopting act (a
    `resource "aws_iam_role"` block for this name in `infra/aws/terraform/`) sits in a lane that
    exists and is busy, and NO seat in it has accepted this row -- a measured search, not an
    assumption; THE OWNER FINDING below carries its four planes and their denominators.
    Absent from the fresh comp-iam parse and from all
    Terraform source (census/inventory JSON only); an ordinary API-serving lambda role with no
    service-default naming pattern and no documented exclusion rationale.
    ACCEPTED 2026-10-09 by `0.7.0_AE_CloudOps~Z`: Live 2026-10-09: lambda trust, 1 inline `DynamoDBAccess` +
    `AWSLambdaBasicExecutionRole`, consumer `sentiment_query_api`, RoleLastUsed 2026-01-02, both consumer and last use
    in US-EAST-2. A live consumer-bearing role, adopted LAST of the adoptions with row 6. CONDITION: its pair must
    carry the REGION -- a declaration that silently assumes us-east-1 would adopt a role whose workload lives
    elsewhere. I accept custody of the role AND of the adoption decision; I do NOT accept the apply, which is a
    separate WORLD act under its own never-widen pair, and any declaration must leave `inline_policy` and
    `managed_policy_arns` ABSENT (both are Optional+Computed and become authoritative when set). Full reasoning:
    deliverables/0.7.0_AE_CloudOps~Z/ACCEPTANCE_ROWS_TEN.md; families and order of application: ADOPTION_PLAN_TEN.md.
15. `vpc-flow-logs-role` -- EXEMPT owner=1.0.0_SA_CTO~Z reason=AWS-managed service role, minted by a
    console or service action (the literal name AWS's own VPC Flow Logs console setup offers when no
    role is specified), correctly outside our Terraform -- CLASS RULING, see CLASS RULINGS below;
    ruling recorded at
    `task-orders/NFRA_IAMROLES202609.TO-IAM-r-4.record-the-service-default-class-ruling.md` and
    `ledger/ROUND_ANALYSIS.round1.md` §4. Absent from the fresh comp-iam parse and from all
    first-party Terraform source, no change from round 1's research. Same class as the other two
    service-default candidates; membership is INHERITED from round 1's classification, not
    independently re-confirmed by `IAM-r-3` in this worker's tree -- see CLASS RULINGS, MEMBERSHIP
    NOTE below.
16. `workspace-sync-lambda-role` -- DEFER owner=0.7.0_AE_CloudOps~Z reason=no consumer since 2025-12-30; no domain module (CTO, ROUND_ANALYSIS.round5.md @f77e32d7c3; adoption opens only if a module comes to own the function) -- the earlier ADOPT recommendation rested on: the adopting act (a
    `resource "aws_iam_role"` block for this name in `infra/aws/terraform/`) sits in a lane that
    exists and is busy, and NO seat in it has accepted this row -- a measured search, not an
    assumption; THE OWNER FINDING below carries its four planes and their denominators.
    Absent from the fresh comp-iam parse and from all
    Terraform source (census/inventory JSON only); an ordinary sync-lambda role with no
    service-default naming pattern and no documented exclusion rationale.

**Coverage: 16 of 16 members carry a disposition token above -- 1 `DECLARED` (a fact: an
`aws_iam_role` resource block exists, cited by path), 9 `ADOPT` (a recommendation: not yet declared,
should be brought into code), 6 `EXEMPT owner=... reason=...` rows (owner and reason recorded on
each of those 6 disposition-table lines). Read plainly: ONE of sixteen roles is presently declared
in this repo's Terraform. Nine are recommended for adoption and remain undeclared until a later act
(not this one) brings them in. Six carry an open governance decision this worker could not
authorize. No `ADOPT` row is an accomplished fact, and no `DECLARED` row is a recommendation still
owed.**

**AMENDED BY `IAM-r-6` (2026-09-10) -- one row and one count.** Row 7 (`lambda-test-role`) now
carries `RETIRE`, the fourth value, so the arithmetic above reads 1 `DECLARED` + 9 `ADOPT` + 5
exemption rows + 1 `RETIRE` = 16. The paragraph above is left exactly as its author wrote it, at
its own vintage; this line is the amendment, and the value it names is defined in THE RETIREMENT
VALUE section below.

**AMENDED BY `IAM-t-1` (2026-09-10) -- TWELVE OWNER FIELDS AND ONE STALE COUNT; NO DISPOSITION
MOVED.** The nine `ADOPT` rows gained an `owner=` and a `reason=`, which they had never carried at
all; rows 7, 8 and 10 moved from `owner=UNASSIGNED` to `owner=NO-ACCEPTING-SEAT`, a value THE OWNER
FINDING section below defines and evidences; and row 8's attachment count is corrected from three to
five, re-read at source. The arithmetic above is UNCHANGED -- 1 `DECLARED` + 9 `ADOPT` + 5 exemption
rows + 1 `RETIRE` = 16 -- because no disposition token moved and no research was re-opened. What
moved is the owner field, which is the half of `FWD-4`'s bar ("in code, or a named owner and a
reason") that nine of sixteen rows could not be measured against, because a census of
`owner=UNASSIGNED` cannot see a row that carries no owner field at all.

**AMENDED BY `IAM-w-4` (2026-10-09; arithmetic re-cut by the issuer `2.0.0_SA_COO~ZI` 2026-10-10) -- TWO
TOKENS MOVED, NO OWNER MOVED.** Rows 5 (`finbert-ec2-backfill-role`) and 16 (`workspace-sync-lambda-role`)
moved from `ADOPT` to `DEFER` on the CTO's home ruling (`ledger/ROUND_ANALYSIS.round5.md` @`f77e32d7c3`,
lines 22-23), landed as carrier @`6c9703007c`. So the arithmetic above now reads 1 `DECLARED` + 7 `ADOPT`
+ 5 exemption rows + 1 `RETIRE` + 2 `DEFER` = 16, re-counted from the table's first lines. `DEFER` and its
reopen-condition discipline are defined in `deliverables/0.7.0_AE_CloudOps~IR/round6/DEFER_ROWS_5_16.md`
@`4dff2b348a`. Both rows keep `owner=0.7.0_AE_CloudOps~Z`, so owner coverage stays `rows=16 unowned=0`.
The paragraphs above stay as their authors wrote them, at their own vintage.

**AMENDED BY THE ROUND-6 DRAIN BATCH REPAIR (issuer `2.0.0_SA_COO~ZI`, 2026-10-11, ROUND_ANALYSIS.round6.md @`2f49aa235b`) -- FIVE
TOKENS MOVED, NO OWNER MOVED.** Rows 1, 2, 3, 9 and 11 were adopted into Terraform in round 6 and now read `DECLARED`, each
citing its file and completing order. The arithmetic now reads 6 `DECLARED` + 2 `ADOPT` (rows 6, 14) + 5 exemption rows + 1
`RETIRE` + 2 `DEFER` = 16, re-counted from the table's first lines. Each prior token is kept beside the new one, so
the row's history stays readable.

## CLASS RULINGS

One ruling disposes of a class rather than one role at a time, stated here once so a reader sees
disposition-table rows 4, 12 and 15 (`ecsTaskExecutionRole`, `rds-monitoring-role`,
`vpc-flow-logs-role`) sharing ONE decision rather than three coincidental exemptions.

**RULING -- AWS-MANAGED SERVICE-DEFAULT ROLES.** Decider: `1.0.0_SA_CTO~Z`, ruled as ARCHITECTURE.
AWS-managed service roles -- a role minted by a console quick-create wizard or another AWS service
action, never by this estate's own Terraform, carrying AWS's own conventional literal name for that
service's default role -- stay OUTSIDE this repo's Terraform, deliberately. That placement is the
correct, settled state for a member of this class, not a gap awaiting adoption and not a per-role
decision awaiting a named exemption owner. Reason: a role of this shape is provisioned and owned by
the AWS service itself at the moment a console/service action creates the resource it attaches to
(an ECS task launch, RDS Enhanced Monitoring, VPC Flow Logs); bringing it under this estate's
Terraform management would fight the issuing service's own lifecycle rather than describe
infrastructure this estate built. This cell RECORDS the ruling; it does not re-derive or re-litigate
it -- round 1 read a per-role-owner requirement for these three as heavier than the outcome demands,
and that reading is corrected here, not re-opened.

**RULING'S RECORD (pointer).** Stated as GIVEN in
`task-orders/NFRA_IAMROLES202609.TO-IAM-r-4.record-the-service-default-class-ruling.md` (this cell's
own issuance, which quotes the ruling and names the decider); traced to
`ledger/ROUND_ANALYSIS.round1.md` §4 ("THE POPULATION DEFECT") and §6 ("R2-C -- the three governance
decisions"), the round-1 analysis `1.0.0_SA_CTO~Z` wrote, which this cell's issuance cites as its
authority chain together with the round-2 decomposition's `IAM-r-4` row
(`../../decompositions/NFRA_IAMROLES202609_DECOMP_R2.md`).

**CLASS BOUNDARY -- which future roles this ruling covers.** A role falls in this class when (a) it
is absent from this repo's Terraform source under a name-level `comp-iam`/`comp-find infra/ --all`
check, AND (b) its name is AWS's own literal conventional name for a specific service's
auto-created default role (the ECS quick-create task-execution-role, RDS Enhanced Monitoring's
console-offered role, VPC Flow Logs' console-offered role, and roles of that identical shape minted
by other AWS services the same way), AND (c) nothing in this repo's Terraform creates or manages it
as a resource. A role failing any one of the three -- present in Terraform, custom-named rather than
AWS's own conventional default name, or created by THIS estate's own automation rather than an AWS
console/service wizard -- is a DIFFERENT member and this ruling does not reach it: it does not cover
`opal-data-refresh-lambda-role` or `portal-auth-lambda-role` (production serving-path roles, a
different remedy shape, owned elsewhere in this round), nor `lambda-test-role` (residue, a different
remedy shape, owned elsewhere in this round), nor any of the nine `ADOPT` members above (no
service-default naming pattern, no plausible console/service-minted origin).

**MEMBERSHIP NOTE (dependency on `IAM-r-3`).** This cell disposes the three members as members of the
not-in-Terraform set on round 1's classification, carried forward unchanged through `IAM-r-1`.
`IAM-r-3` -- the cell that re-confirms true membership per member, against a Terraform resource-block
read rather than a name match -- was still in flight on the measurement chain as this cell was
worked, and no `IAM-r-3` deliverable or verdict list was present anywhere in this worker's tree at
write time (checked by name across the whole repo). Membership for these three is therefore
INHERITED from round 1, not independently re-confirmed by this cell. This same round has already
shown the class this ruling exempts can carry a false positive elsewhere in the same sixteen
(`seeking-alpha-scraper-role`, row 13 above, corrected from `LIVE-no-DECLARED` to `DECLARED`) -- if
`IAM-r-3` later finds any of these three is in fact already declared, that member's row is a second
instance of that identical defect and needs re-disposing to `DECLARED`, not this ruling re-litigated;
the ruling itself would be unaffected, since it governs the CLASS, not any one member's true
membership in it.

## RULE 24 FOUR-POSTULATE RECORD FOR THE REPLACEMENT VOCABULARY (this cell, IAM-r-1)

The prior single token carried two intents -- a measured fact for some rows, a recommendation for
others -- graded FAIL at L9 on exactly that ground (rule 24(iii)). Its replacement, `DECLARED` /
`ADOPT` / the third (exempt) value, is itself a schema and rule 24 binds it. The four postulates,
checked against this document as it now reads:

- **MECE over a declared domain**: the declared domain is the 16 members `IAM-s-5` measured (see
  INPUT SET AND ITS VINTAGE above -- unchanged, not re-measured by this cell). Every one of the 16
  rows in the DISPOSITION TABLE carries exactly one of the three values -- 1 `DECLARED` + 9 `ADOPT` +
  6 exempt = 16, matching the coverage line above. No row carries zero values or two, and the domain
  is closed at 16 because `IAM-r-3` (not this cell) owns any change to that membership.
- **SAME GRAIN**: each value is a property of ONE member (one IAM role name), never of the set as a
  whole and never of a sub-population as a unit. `DECLARED` and `ADOPT` are both resolved at the
  member level by the same two-step method (the fresh `comp-iam roles` name check plus the
  `comp-find infra/ --all` first-party-source check, see METHOD above); the exempt value likewise
  names one member's individually-reasoned owner and reason, never a class-wide default.
- **INTENT COHERENCE**: one axis, one intent. This axis answers exactly one question per member --
  "does an `aws_iam_role` resource block naming this member exist in this repo's Terraform, right
  now" -- `DECLARED` answers yes (a fact, resource block cited), `ADOPT` answers no with no
  documented exclusion (a recommendation, not yet true), and the exempt value answers no with a real
  unresolved decision owed to a named owner (deliberately outside Terraform pending that decision).
  It never answers whether a member's *permissions* are correctly scoped -- that is `IAM-s-1`'s axis
  and does not move with this one (SCOPE HELD, bound D6, below).
- **STATE COHERENCE** (which values one remedy does NOT move): bringing one `ADOPT` member into
  Terraform (a future `IAM-r-3`/`IAM-r-5` act, not performed here) moves ONLY that member's row from
  `ADOPT` to `DECLARED` -- it touches no exempt row and no other `ADOPT` row. Assigning a named
  owner to one exempt row (the `EXEMPT owner=UNASSIGNED reason=<what is owed and why>` pattern used
  per row in the DISPOSITION TABLE above) resolves ONLY that member's open decision -- it touches no
  `DECLARED` row and no `ADOPT` row, and it does not itself change which of the three values that
  row carries; only its `owner=` field moves from `UNASSIGNED` to a name. Neither remedy changes any
  member's permission grant, in either direction (C-TWO-REMEDIES, bound D6, held throughout this
  document and unchanged by this cell).

## THE RETIREMENT VALUE -- IAM-r-6's EXTENSION OF THE DISPOSITION VOCABULARY

Round 1's schema was binary and round 2's split (`DECLARED` / `ADOPT` / the exemption value) is
ternary; neither could express the honest answer for one member. This section adds the value FIRST
and disposes the member SECOND, in that order, because doing it the other way round is how the
round-1 defect happened. It extends the record above; it re-opens nothing in it. Exactly one
disposition-table row changed (row 7) and the coverage arithmetic beneath the table is amended to
match; rows 1-6 and 8-16, the class ruling, and the IAM-r-1 four-postulate record are untouched.

### THE FOURTH VALUE, STATED

`RETIRE owner=<seat|UNASSIGNED> reason=<why this role should not exist, and on what evidence>`

It answers "should this role exist at all?" with NO. It is a RECOMMENDATION and never an
accomplished fact -- the same grade as `ADOPT`, the opposite direction. The role still exists in AWS
after this document says `RETIRE`; a named owner decides and performs the act. It carries the same
`owner=` / `reason=` discipline the exemption value carries, so the regression bar that has run
across all three document cells reads a fourth value the same way it reads the third.

**RECORDING A RETIREMENT IS NOT PERFORMING ONE.** No role was deleted by this cell, no AWS call was
made that changed anything, and no Terraform was modified. `infra/aws/terraform/` was a READ surface
for this cell and every citation below is a read.

### WHY THIS IS NOT A RELABELLING OF THE VALUE BESIDE IT

The discriminator is a question a reader can put to any row, and the four values answer it
differently -- **after the remedy this row names is performed, does the role still exist?**

| value | remedy the row names | role exists afterwards? |
|---|---|---|
| `DECLARED` | none owed; Terraform already declares it | yes |
| `ADOPT` | bring it into Terraform | yes |
| exemption value | ratify that it stays outside Terraform, with an owner | yes |
| `RETIRE` | delete it | **no** |

"Deliberately kept outside our Terraform, and it stays" and "this should not exist at all" are two
intents. Forcing the second into the first is the identical one-axis-two-intents defect L9 graded in
round 1, on a different axis -- so the value is added beside the exemption value rather than
overloaded onto it.

### BUILD-LADDER CHECK -- does the estate already carry this?

Before minting a token, the ladder asks whether the estate already has one.

- **A ratified lifecycle enum exists and is NOT reused.** `comp-estate --definitions Lifecycle_Stage`
  (SYSTEM_DEFINITIONS v3.25) ratifies `EMERGING/ACTIVE/WINDING_DOWN/DISSOLVING/DISSOLVED` plus an
  `UNASSERTED` sentinel, home `org/modules/graph/NFRA_ONTOLOGY_RULE_BANK.yaml#dynamic_rails.D3_contract_obligation.lifecycle.stage`.
  It is refused here on its own canon's grounds: it is asserted at C3.ii VERTICAL grain about a whole
  semantic vertical's position in life, and its definition retains the deciding counterexample -- "a
  vertical can be winding down while every artifact in it is PERMANENT-shaped; both true, neither
  implying the other (Rule 24(ii), two grains never share one axis)". An IAM role is not a vertical.
  Borrowing that enum would put two grains on one axis, which is the thing it exists to prevent.
- **The TOKEN is already bound in this estate to exactly this sense, on a different domain, and that
  is why it is the token chosen.** `comp-tool-health` emits a verdict in `{KEEP, FIX, PROMOTE,
  RETIRE}` where `RETIRE` means "dead" (`org/modules/graph/comp_tool_health.py:5`, `:23`). This cell
  mints no new word; it reuses the estate's existing word for "this should not continue to exist" on
  a new domain, which is the cheapest rung of the ladder that works.
- **Retirement doctrine already exists and it binds the FUTURE act, not this record.** The rulings
  ledger carries "07-29 teardown doctrine: unit of retirement is the WRITE ... preserve before
  deleting" (`infra/system/ontology/worldmodel/20_rulings/RULINGS_LEDGER.jsonl`). Read onto a role:
  name the unit and confirm no live consumer before any deletion. This document names the unit (one
  role) and records the consumer search below; it authorizes nothing.

### WORD-BOUNDARY TOKEN CENSUS -- rule 24's proposal bar

Three corpora, each with its denominator printed beside its number.

**Corpus A -- the document IAM-r-1's split produced** (this file at `b1fececea1`, 350 lines, whole
file, before this cell's edit):

```
comp-read GOVERNANCE_DISPOSITION.md --enumerate <word-boundary alternation, all four tokens>
  ENUMERATE: 57 hit(s) across 350 lines / 20 section(s) scanned
    whole-value matches: 7   |   substring matches: 50
    BANDS (sum to 57):  HEADING 1 | FENCE 0 | PROSE 56

per-token occurrences, word-boundary and case-SENSITIVE, same 350-line denominator:
  DECLARED                        23
  ADOPT                           24
  EXEMPT owner=... reason=...     10   (6 table rows + 4 prose definitions)
  RETIRE                           0   -- and RETIRED 0, RETIREMENT 0
```

The literal alternation is recorded verbatim in this cell's proof-of-spec instance rather than here,
for a reason worth one line: **this document's own regression bar forbids writing the exemption
token on any line that does not also carry its owner and its reason**, and a raw census pattern is a
line like any other. The bar is mechanical and it does not know what a quoted command is -- so the
pattern lives where the bar does not run, and the token appears here only in its canonical written
form, which is what the bar was built to enforce.

The new token collides with nothing in the corpus it joins: zero prior occurrences as a token.

**THE CASE QUALIFIER, and it is why that census is stated case-sensitively.** The same file already
carried THREE lowercase retire-family words in ordinary prose before this cell touched it --
`retire` 1, `retired` 1, `retirement` 1 (lines 106, 291, 349 of the pre-edit file) -- every one of
them describing a decision that was owed, none of them a disposition token. A case-INSENSITIVE,
unanchored count of the same string therefore read **3** at this cell's cut, not 0. Surfaced as
`NFRA_IAMROLES202609-Z-W5-S1`.

**Corpus B -- the project tree.** `comp-find '\bRETIRE\b' org/missions/D12/NFRA/NFRA_IAMROLES202609
--all` -> `2 hit(s) across 53 file(s) scanned in scope`, both inside this cell's own task order (its
definition line and its AC1 invocation). No other deliverable, row, or ruling in this project binds
the token.

**Corpus C -- the estate.** `comp-find '\bRETIRE\b' --all --files` -> `7634 hit(s) across 29366
file(s) scanned`, bands `DEF=1 SURFACED=7116 CONFIG=88 TEST=12 DOC=417`. **READ THE DENOMINATOR
BEFORE THE NUMBER: that mass is a mention, not a vocabulary.** The SURFACED bulk is fund names in
ticker-override maps (`'AMERICAN FUNDS 2030 TRGT DATE RETIRE A'`,
`data/cot/scripts/gold/lib/ticker_overrides.py:61`), which is a substring of prose and binds nothing.
The single DEF-band hit is the tool-health verdict enum cited above. So exactly ONE prior
value-sense binding exists estate-wide, and it agrees with this one.

### RULE 24 FOUR-POSTULATE RECORD FOR THE EXTENDED VOCABULARY (this cell, IAM-r-6)

- **MECE over a declared domain**: the domain is unchanged -- the same 16 members `IAM-s-5`
  measured and `IAM-r-3` re-confirmed per member. Every row carries exactly one of FOUR values:
  1 `DECLARED` + 9 `ADOPT` + 5 exempt + 1 `RETIRE` = 16. No row carries zero values or two. The
  hunt for an uncovered member is the next section and it is not decorative: it found ONE state the
  ternary could not express (retirement, 1 member) and ONE state that must NOT become a value
  (policy-attached-but-undeclared), with the measurement that decides each. **The domain's own
  boundary, stated so a later reader does not mistake its silence:** this axis is declared over
  roles that are LIVE and not declared. A role declared in Terraform but ABSENT from the live plane
  -- the mirror-image drift -- is not in this domain and gets no value here; widening the domain to
  it means running the hunt again.
- **SAME GRAIN**: `RETIRE` is a property of ONE role name, decided on that member's own evidence,
  exactly like the three values beside it. It is never asserted over the set, over a class, or over
  a sub-population as a unit -- and unlike the class ruling above, which disposes three members by
  one shared decision, this value's single member is reasoned individually.
- **INTENT COHERENCE**: one axis, one intent -- **what is this role's correct END STATE in this
  estate?** The four values order on one line: should not exist (`RETIRE`) / should exist outside
  our Terraform, deliberately, with an owner (the exemption value) / should exist inside it and is
  not there yet (`ADOPT`) / is inside it already (`DECLARED`). None of the four answers how widely
  the role grants, which is `IAM-s-1`'s axis and does not move with this one (SCOPE HELD, bound D6).
  **THE HONEST OBJECTION, STATED AND ANSWERED:** existence and placement can be read as two
  questions, and if they are, this record is wrong. They are one axis here because placement is only
  meaningful for a role that should exist -- `RETIRE` is that axis's zero, not a second axis. The
  test that keeps them one: every value answers "where should this role live", and "nowhere" is an
  answer to that question, not a different question. If any member ever needed a placement value AND
  an existence value at the same time, that would be two axes; no member of this domain does.
- **STATE COHERENCE** (which values one remedy does NOT move):
  - Deleting a `RETIRE` member -- a future act by a seat with that lane, not performed here --
    removes that member from the domain entirely (16 becomes 15). It moves no other row and it turns
    no `ADOPT` row into `DECLARED`.
  - **The mass remedy this project is otherwise pointed at -- bringing undeclared roles into
    Terraform -- DOES NOT MOVE A `RETIRE` ROW, and that is the whole point of the value.** Importing
    residue into Terraform would commit the estate to managing a thing that should not exist. That
    cost is exactly what the binary vocabulary hid, and naming it is what the fourth value buys.
  - Assigning a named owner on a `RETIRE` row moves only its `owner=` field, exactly as on an
    exemption row; it does not change which value the row carries.
  - If the evidence turns out to be wrong and the member is in use, its row moves to `ADOPT` or to
    the exemption value -- one value at a time, never two at once.
  - No remedy on this axis changes any role's grants in either direction (C-TWO-REMEDIES, bound D6).

### THE UNCOVERED-MEMBER HUNT -- the second state this round found, and why it gets no value

The round-2 cut measured a state its own vocabulary could not express: for
`opal-data-refresh-lambda-role`, the estate **manages policies on a role it does not own**. The hunt
below re-grounds that measurement, then asks the question rule 24 actually asks -- what is the
POPULATION of that state -- and the answer is what decides it.

**Re-grounded, not inherited** (`comp-find 'opal-data-refresh-lambda-role' infra/aws/terraform
--all` -> `9 hit(s) across 516 file(s) scanned in scope`):

- **FIVE** `aws_iam_role_policy` blocks attach to the role by literal name, each read at source:
  `data-refresh/main.tf:59-60` (`data_refresh_sscn_s3`), `:81-82` (`data_refresh_cloudfront_read`),
  `:100-101` (`data_refresh_time_machine_invoke`), `:139-140`
  (`portal_time_machine_invoke_downstream`), and `data-refresh/qa-scratch-instance.tf:36-38`
  (`data_refresh_qa_scratch_access`). Three `role_arn` strings (`main.tf:38`, `:124`,
  `qa-scratch-instance.tf:19`) and one comment (`main.tf:53`, "inline policy attached to the
  pre-existing opal-data-refresh-lambda-role") make up the remaining four hits.
- **ZERO** role declarations: `comp-find 'resource "aws_iam_role"' infra/aws/terraform/data-refresh
  --all` -> `0 hit(s) across 4 file(s) scanned in scope`, a measured zero over a named denominator.
- The count is FIVE, not the four the cut carried and not the three round 1's row 8 carried.
  Surfaced as `NFRA_IAMROLES202609-Z-W5-S2`; it changes no disposition.

**THE HUNT DID NOT STOP AT THE MEMBER.** `comp-find 'role += +"[a-z]' infra/aws/terraform --all` ->
`21 hit(s) across 516 file(s) scanned in scope`, carrying SIX distinct role names attached by
literal string rather than by resource reference. **FIVE OF THE SIX ARE THEMSELVES DECLARED IN THIS
TERRAFORM**, each inside a `resource "aws_iam_role"` block read at source:

| role attached by literal name | declared in this Terraform? |
|---|---|
| `lambda-execution-role` | YES -- `shared-infra/lambda-execution-role.tf:47-48` |
| `opal-portal-lambda-role` | YES -- `shared-infra/opal-portal-lambda-role.tf:36-37` |
| `opalinvest-auth-lambda-role` | YES -- `portal-auth/iam.tf:16` |
| `bd-exporter-ec2-role` | YES -- `bd-pipeline/iam.tf:340-341` |
| `partners-lambda-role` | YES -- `partners-api/iam.tf:9-10` |
| `opal-data-refresh-lambda-role` | NO -- zero declarations anywhere in the tree |

**DECISION: THE POLICY-ATTACHED STATE GETS NO VALUE, AND THE MEASUREMENT IS WHY.** Five of the six
members carrying it are `DECLARED`. A value naming it would therefore classify five declared roles
and one undeclared role identically -- it is not mutually exclusive with the values already on this
axis, so it fails postulate (i), and it answers a different question (how a module REFERENCES a
role: by resource reference or by literal name) wearing this axis's clothes, so it fails postulate
(iii). It is also a description of a CURRENT state, where every value on this axis is an END state.
A fourth value nobody needs is its own defect; a fifth would be the same defect with better
manners.

**AND THE STATE STILL GOES SOMEWHERE, because "no value" is not "no record".** It belongs on the
membership axis `IAM-r-3` owns, as a qualifier on the member -- and it is already there:
`MEMBERSHIP_PER_MEMBER.md` records `opal-data-refresh-lambda-role` as NOT-IN-TF with 9 reference
hits and ZERO declarations, citing every line. Its END-state question is unchanged by this cell and
still open on row 8: adopt by import, or formally except with a named owner. That row is untouched.

### THE MEMBER -- lambda-test-role

**MEMBERSHIP FIRST, because this round has already misfiled one member.** `IAM-r-3`'s per-member
verdict list rules `lambda-test-role` **NOT-IN-TF -- 0 hits** across the 415 tracked `.tf` files, on
a Terraform resource-block read rather than a name match
(`deliverables/0.9.0_WK_NFRA_IAMROLES202609~6/MEMBERSHIP_PER_MEMBER.md`, rows 7 and the summary
table). Read and confirmed by this cell before disposing. It is genuinely in the undeclared set;
it is not a second `seeking-alpha-scraper-role`.

**THE EVIDENCE, ON THREE PLANES, AND IT IS A FLOOR RATHER THAN A WARRANT.**

1. **Terraform plane** -- 0 hits, `IAM-r-3` above. The same cell used this member as its own
   instrument's negative control.
2. **Live plane, this cell's own read** -- `comp-find 'lambda-test-role' --corpus aws --all`,
   vintage 2026-09-10 12:24:50 UTC, manifest `aebbd9cef8c4`: `DENOMINATOR: 1 hit(s) across 2382 aws
   node(s) scanned`, `BANDS = node_type: IAM_ROLE=1`. The role exists (`drift=LIVE-no-DECLARED`,
   props `{"attached_managed": ["AWSLambdaBasicExecutionRole"...`) and **nothing else in the live
   estate points at it**: no LAMBDA node carries it, no inline policy hangs off it.
   **POSITIVE CONTROL, so that a true silence and a blind instrument cannot read alike:** the
   identical command on `opal-data-refresh-lambda-role`, same corpus, same vintage, same 2382-node
   denominator returns `9 hit(s)`, `BANDS = IAM_POLICY=5 IAM_ROLE=1 LAMBDA=3` -- three LAMBDA nodes
   (`opal-data-refresh-api`, `opal-data-refresh-api-qa-scratch`, `portal-time-machine`) each
   carrying `"role": "opal-data-refresh-lambda-role"` in its own props. The instrument DOES surface
   consumers where consumers exist. For `lambda-test-role` there are none.
3. **Usage plane** -- `.tools/comp-iam investigate-candidates --role lambda-test-role`:
   `INVESTIGATE-CANDIDATE -- UNKNOWN (1 role(s)) -- no LastUsedDate recorded`, "NOT accessed in the
   400-day IAM tracking window. This does NOT mean never used; it may predate the window, or the
   role may genuinely never have been used -- both render identically and this tool cannot
   distinguish them." **The tool's own refusal travels with its output rather than being filed off:
   "THIS SURFACE IS A FLOOR, NEVER A DELETION WARRANT ... It licenses no action beyond
   investigation."** This is precisely the unused-versus-unobservable separation `IAM-s-3`'s
   coverage vocabulary exists to keep, and the value below is written to respect it: a
   recommendation with an owner, not an act.

**A DIFFERENT SEAT, A DIFFERENT INSTRUMENT, AN EARLIER VINTAGE.** The CVO/AE hand-audit of
2026-06-03 reached the same reading from the other direction: "NEW FLAG from AE: `lambda-test-role`
live in prod = scrutinize (likely leftover ...)"
(`docs/briefs/cmpaws-cvo-handaudit-pass1-20260603.md:140`), carried at `:178` to the security
tracker as "lambda-test-role flagged scrutinize". **The remainder of that parenthesis is a
permissions-axis claim and this cell does not carry it** (C-TWO-REMEDIES): only the governance half
-- likely leftover -- is read here, and the reader is pointed at the line rather than handed the
other half second-hand.

**THE DISPOSITION** is row 7 of the table above: `RETIRE owner=UNASSIGNED reason=...`. `IAM-s-6`
wrote that row naming exactly this decision as owed and stating it had no usage telemetry to settle
it; this cell settled it on the three planes above and the vocabulary now has somewhere to put the
answer.

**WHAT WOULD FALSIFY IT, named because the residue reading began as a reading of a name.** A
consumer that does not appear as a live node: a principal assuming the role out of band, a human or
a CI job using it interactively, or a use older than AWS's 400-day tracking window. Any one of those
turns row 7 into `ADOPT` or into an exemption with an owner, and the finding becomes that the
residue reading was wrong -- which would be a good outcome for this cell, not a failed one. None of
the three was found on any of the three planes; none was ruled out by a positive observation either,
and that asymmetry is exactly why the row carries a decision owner and a recommendation rather than
an act.

### WHAT THIS CELL DID NOT DO

No role was deleted and no AWS object changed. No Terraform was created, modified or imported --
`infra/aws/terraform/` was read-only here and every citation above is a read. No alert, alarm,
monitor, schedule or notification was minted (`G-21` remains ARMED and untouched). No permissions
judgment was made about any of the sixteen in either direction, and no earlier cell's research was
re-opened, re-derived or reworded: rows 1-6 and 8-16, the class ruling, the membership note and the
`IAM-r-1` four-postulate record all stand as their authors left them.

### SURPRISE ROWS FILED BY THIS CELL

Filed in `../../surprise-channel/investigations/INVESTIGATION_v1.md`:

- `NFRA_IAMROLES202609-Z-W5-S1` -- this cell's own AC1 asserts the retirement token measured 0 in
  this document at the cut; its case-insensitive, unanchored invocation measured 3, because the file
  already carried lowercase `retire`/`retired`/`retirement` in prose. The criterion passes on text
  that predates the cell, so the discriminating measurement is the case-sensitive word-boundary
  census above (0 before, nonzero after).
- `NFRA_IAMROLES202609-Z-W5-S2` -- the round-2 cut's battery states FOUR `aws_iam_role_policy`
  blocks attaching to `opal-data-refresh-lambda-role` by name; this cell measured FIVE, the fifth in
  `data-refresh/qa-scratch-instance.tf:36-38`. The zero-declarations half of the cut's claim
  reproduced exactly, and no disposition moves either way.

## THE OWNER FINDING -- `IAM-t-1`: TWELVE ROWS CARRY NO SEAT, AND THAT IS A MEASUREMENT

`FWD-4` asks that each member be in code, or carry a named owner and a reason. Twelve rows were
short of that: nine `ADOPT` rows with no owner field at all, and three rows whose owner field read
`UNASSIGNED`. This section is what this cell did about the twelve, and it is a FINDING rather than
an assignment: whether the owners exist inside this fabric was measured, and the measurement is
below with its denominators. This section EXTENDS the record above; it re-opens nothing in it, moves
no disposition token, and touches no grant on any of the sixteen.

### THE OWNER VALUE, STATED

`owner=NO-ACCEPTING-SEAT reason=<what the search established, and how>`

It records A COMPLETED SEARCH WITH AN EMPTY RESULT: a lane able to perform this row's act exists in
this estate's own record, no seat in that lane has accepted this row, and an L7 cell has no channel
by which one could accept. **IT IS NOT A NAME AND MUST NEVER BE READ AS ONE.** It commits nobody,
and that is deliberate -- writing a serial for a seat that has not accepted would forge a commitment
on another agent's behalf, which is the one thing this cell was forbidden to do however reasonable
the guess.

### WHY IT IS NOT `UNASSIGNED`, WHICH THIS DOCUMENT ALREADY CARRIED

| owner value | what a reader may conclude | what moves it |
|---|---|---|
| a seat serial | that seat accepted this row, in writing | the seat performs the act |
| `UNASSIGNED` | a decision is owed; **whether anyone ever looked is unknown** | putting the question |
| `NO-ACCEPTING-SEAT` | the question WAS put, by search; here is the denominator | an acceptance |

The two sentinels are not interchangeable and the difference is the whole point of the value. Rows
7, 8 and 10 carried `UNASSIGNED` because at their vintage no owner search had been run -- their
author said so in terms ("this worker cannot make that heavier call or name who accepts it"). This
cell ran a search that covers those three rows as well as the nine, so leaving them at `UNASSIGNED`
would now UNDERSTATE what is known: it would read as an unasked question when the question has been
asked and answered.

### BUILD LADDER -- does the estate already carry a sentinel that says this?

Checked before minting, because a new token nobody needs is its own defect. Three candidates exist
and all three name a DIFFERENT fact:

- `UNASSIGNED` -- this document's own sentinel, 12 occurrences at this cell's cut, 3 of them on
  member rows. It means the slot is empty. It cannot distinguish "nobody has looked" from "we
  looked and found nobody", and that distinction is this cell's entire finding.
- `UNASSERTED` -- the `Lifecycle_Stage` sentinel cited in THE RETIREMENT VALUE above. It means the
  property was never asserted at all: again an absence of a statement, not a result.
- `NONE-STATED` -- `ledger/ROUND_ANALYSIS.round2.md` section 2's reading of the nine `ADOPT` rows.
  It names an absent FIELD, which is the condition this cell is repairing rather than a value it
  could adopt.

**TOKEN CENSUS, three corpora, each with its denominator printed.** Corpus A, this document
pre-edit: `NO-ACCEPTING-SEAT` 0, `ACCEPTING` 0, `UNASSIGNED` 12. Corpus B, the project tree,
`comp-find 'NO-ACCEPTING-SEAT' org/missions/D12/NFRA/NFRA_IAMROLES202609 --all` -> `0 hit(s) across
63 file(s) scanned in scope`. Corpus C, the estate, `comp-find 'NO-ACCEPTING-SEAT' --all` -> `3
hit(s) across 29409 file(s) scanned`, and **all three are this cell's own search telemetry**
(`org/mcp/comp-tool-runs.jsonl:7`, `org/mcp/comp-which-rail.log:7` -- the rail logs into the corpus
it searches, so a probe finds its own footprint). Read past the footprint, the token collides with
nothing anywhere in this estate.

### THE SEARCH -- FOUR PLANES, EACH WITH ITS DENOMINATOR

**1. CAPABILITY: is there a lane that can perform these acts at all? YES.** `.owned-paths.yaml`
binds `infra/aws/**` to lane `CLOUD_OPS_OR_ETL` (`:1845-1847`, "AWS infra (Terraform, IAM, Lambda)
-- AE 0.5/0.6/0.6.1/0.7 only"), and that lane enumerates 11 permitted agents (`:342-353`) -- the AE
families plus one gate-constrained sweep executor. `.tools/owned-paths-validate.py:278-287` then
admits any tilde-suffixed spawn of an enumerated base serial, so the lane is wider than its
enumeration reads. **The act these twelve rows name is inside a lane, and the lane is not empty.**

**2. ACTIVITY: is that lane alive on this fabric? YES -- it is the busiest family in the estate.**
Repo-wide over the last 14 days: **935 commits by 41 distinct AE serials**, out of **5,785 commits
by 120 distinct authors** in the same window. On `infra/aws/terraform/` itself, all history: **1,486
commits by 74 distinct authors**, led by `0.7.0_AE_CloudOps` with 533. The hands that write this
estate's Terraform are identifiable, numerous and working today.

**3. THIS PROJECT'S RECORD: has any of them been here? NO -- zero, against a printed denominator.**
`git log` over `org/missions/D12/NFRA/NFRA_IAMROLES202609/`: **65 commits, 10 distinct authors** --
`2.0.0_SA_COO~ZI` 26, `3.0.0_SA_CVO~Z` 11, `2.0.0_SA_COO` 8, `1.0.0_SA_CTO~Z` 5, and this project's
six worker slots. **Not one commit by any member of the adopting lane.** A `comp-find` for any AE
serial across the project returns `6 hit(s) across 63 file(s) scanned`, and all six are citations or
git vintages -- two blame lines in `IAM-s-7`'s historical-completion deliverable, two path citations
to a SIBLING project's deliverable folder, two of the same in the channel. **None is an acceptance,
a tasking or a reply.**

**4. ACCEPTANCE: is there an acceptance anywhere for these twelve? NO -- and the instrument can see
one when it exists.** POSITIVE CONTROL, run so that a true absence and a blind search cannot read
alike: `comp-find 'accepted' org/missions/D12/NFRA/NFRA_IAMROLES202609 --all` -> `9 hit(s) across 63
file(s) scanned`, and one of the nine IS the acceptance this document already rests on --
`ledger/ROUND_ANALYSIS.round2.md:237-238`, "three rows already name `1.0.0_SA_CTO~Z`, and that seat
accepted those three". **A search that surfaces an acceptance for three rows and none for twelve is
a measured absence, not a broken matcher.**

**A FIFTH PLACE AN OWNER MIGHT HAVE BEEN WRITTEN, checked because a governance owner need not be an
agent.** The estate's hand-maintained IAM inventory (`infra/aws/manifests/iam/iam-roles.yaml`,
`Last Updated: 2026-01-02`, `total_roles: 8`) carries exactly ONE owner statement and it is at FILE
grain: `# Owner: Andrew Berman` (`:3`). Against the twelve rows it covers exactly one
(`opal-smartx-lambda-role`, 3 hits) and none of the other eleven. A file-grain human attribution on
an 8-role inventory eight months stale is not a row-grain acceptance for a 16-role population, and
round 2's own "what is owed" table records that **nothing is owed by Andrew** and that this
escalation is raised by the recut when a cell finds it -- so what the search found is recorded here
and is NOT converted into an owner field.

**AND THE HALF NO SEARCH CAN IMPROVE.** An L7 worker holds no send tool and cannot be messaged. The
twelve rows therefore could not have been closed from inside this cell at any depth of effort: the
result is not a shallow search, it is a structural one.

### WHAT THIS FINDING DOES NOT SAY

- **It does not say that no seat could own these rows.** The opposite is measured: the lane exists
  and is busy. What is missing is an ASK and an ACCEPTANCE, and neither is an L7 act.
- **It names no candidate seat on any row, and authorship is not acceptance.**
  `0.7.0_AE_CloudOps` has 533 commits on `infra/aws/terraform/` and has never appeared in this
  project's record; converting that into `owner=0.7.0_AE_CloudOps` would be exactly the forged
  commitment this cell was forbidden to write, and it would be forged against the most plausible
  candidate, which is the version that would survive review.
- **It says nothing about any member's permissions, in either direction** (`C-TWO-REMEDIES`, bound
  D6). Governance placement and grant scope are two remedies that do not move together.
- **Nothing was minted that will fire.** No alert, alarm, monitor, schedule or notification was
  created by this cell; `G-21` stays ARMED and untouched. No Terraform was modified: every citation
  above is a read.

### WHAT CLOSES EACH ROW -- so the value is a stop on a route, not a resting place

- **The nine `ADOPT` rows:** one seat with the `CLOUD_OPS_OR_ETL` lane accepts, in writing, and that
  row's owner becomes its serial. Rows 4, 12 and 15 are the precedent already in this document: a
  recorded decision with a decider, and the rows carry the decider's name.
- **Rows 8 and 10:** the same, and for these two the work is already done and waiting. The adopting
  text exists, committed and inert, at
  `infra/aws/terraform/data-refresh/zz_adoption_candidate.tf.proposed` -- `resource "aws_iam_role"
  "opal_data_refresh_lambda_role"` at `:29-30` and `resource "aws_iam_role" "portal_auth_lambda_role"`
  at `:66-67`, authored by `IAM-r-5` with a recorded plan. **THE TEXT IS NOT THE BLOCKER ON THESE
  TWO ROWS; THE ACCEPTANCE IS** -- which is the single most useful thing a reader can take from this
  section.
- **Row 7:** an owner for the retirement, plus one requirement the other eleven do not carry -- its
  terminal act deletes a live IAM object, which this estate reserves for human confirmation. Reading
  that pre-existing constitutional stop is not building a gate and none was built.
- **The escalation, raised HERE and not before.** `ledger/ROUND_ANALYSIS.round2.md` section 9 states
  that a finding of this shape is raised when a cell finds it. This cell found it: **twelve of
  sixteen rows need a seat in the `CLOUD_OPS_OR_ETL` lane to be ASKED, the ask is an ISSUANCE, and
  an issuance is `2.0.0_SA_COO~ZI`'s act rather than a worker's.** Filed as
  `NFRA_IAMROLES202609-Z-W7-S1` in `../../surprise-channel/investigations/INVESTIGATION_v1.md`.

### RULE 24 FOUR-POSTULATE RECORD FOR THE OWNER FIELD (this cell, `IAM-t-1`)

The owner field is a value set with two sentinels and an open set of serials, so rule 24 binds it.

- **MECE over a declared domain.** The domain is the **15 member rows with an act still owed** --
  the sixteen minus the one `DECLARED` row, which owes nothing and therefore carries no owner field
  and needs none. Every one of the 15 now carries exactly one owner value: **3 a seat serial, 12
  `NO-ACCEPTING-SEAT`, 0 `UNASSIGNED`**. THE HUNT FOR AN UNCOVERED MEMBER, and it found one state
  worth naming: a row whose act belongs to NO lane at all -- nobody in this estate could perform it
  even after accepting. Eleven of the twelve acts are repo writes inside `CLOUD_OPS_OR_ETL`, so that
  state is empty for them. **Row 7 is the near miss and is stated rather than smoothed:** its repo
  half sits in that lane, but its terminal half is an AWS-plane deletion no repo lane governs and a
  human confirmation gates. It still takes `NO-ACCEPTING-SEAT` -- no seat has accepted it either --
  and its reason names the extra requirement, because a value that hid it would be the round-1
  defect again in a new place.
- **SAME GRAIN.** The owner value is a property of ONE member row: who has accepted THE ACT THAT ROW
  NAMES. It is asserted twelve times because a search returned empty twelve times. **The honest
  qualifier, since one search covers twelve rows:** the rows' acts are not identical -- nine
  adoptions, two sign-offs, one retirement -- and the search's per-row result was the same for a
  per-row reason each time, which is why each row's `reason=` names its own act rather than pointing
  at a class the way rows 4, 12 and 15 point at the class ruling.
- **INTENT COHERENCE.** One axis, one intent: **WHO HAS ACCEPTED THE ACT THIS ROW NAMES?** A serial
  answers "this seat, in writing"; `NO-ACCEPTING-SEAT` answers "nobody, measured"; `UNASSIGNED`
  answers "not asked". The field never says whether the act is a good idea -- that is the
  disposition token beside it, a separate axis with its own four-postulate record above -- and never
  says how widely the role grants, which is `IAM-s-1`'s axis and does not move with this one.
- **STATE COHERENCE (which values one remedy does NOT move).** An acceptance moves ONE row's owner
  field from `NO-ACCEPTING-SEAT` to a serial and touches nothing else: not that row's disposition
  token, not another row's owner, not any grant. PERFORMING the act afterwards moves the DISPOSITION
  (`ADOPT` -> `DECLARED`) and leaves the owner field standing as the record of who did it -- the two
  fields move on different events, which is why they are two fields. A row that goes back to
  `UNASSIGNED` is a regression, not a state: once a search has run, its result is a fact about the
  fabric at a vintage and a later reader is owed the vintage, not the empty slot.

## WHY ONE DISPOSITION DID NOT FIT ALL SIXTEEN (measured, not inherited)

The cell text predicted three sub-populations and this cell's own re-measurement (not the L5 lane's
say-so) confirms the split, with one correction and one addition the re-measurement itself
surfaced:

- The three predicted AWS-service-default names (`ecsTaskExecutionRole`, `rds-monitoring-role`,
  `vpc-flow-logs-role`) hold up under a name-level Terraform search: none appears in Terraform
  source at all, consistent with (but not proof of) console/service auto-creation.
- The two predicted production-serving-path names (`portal-auth-lambda-role`,
  `opal-data-refresh-lambda-role`) hold up, and the re-measurement adds texture the character notes
  did not carry: one of the two (`opal-data-refresh-lambda-role`) is at least *touched* by Terraform
  (policy attachments against a role Terraform calls "pre-existing"), while the other
  (`portal-auth-lambda-role`) has no Terraform touch whatsoever and sits directly beside a
  similarly-named but functionally distinct declared sibling (`opalinvest-auth-lambda-role`) --
  a near-miss a hasty reader could mistake for the same role. They are not; both were checked by
  literal Terraform resource name, not by family resemblance.
- `lambda-test-role` "reads as residue" exactly as flagged, and the re-measurement found nothing
  to promote that past a plausible reading into a fact -- it is dispositioned as its own class,
  needing a retirement-or-formalize decision rather than either template.
- **The correction:** `seeking-alpha-scraper-role`, carried forward by IAM-s-5 as SAME across all
  measured vintages, is in fact already declared in Terraform. Disposing of "the undeclared set" at
  face value would have manufactured an exemption need where none exists -- exactly the failure mode
  the bound warned against, just on the `comp-find --corpus aws` drift plane rather than the
  `comp-iam` parser plane the bound named. Filed as a surprise row rather than silently corrected,
  because it changes what "the settled 16" means for any other reader of that number.
- **The addition:** `portfolio-management-lambda-role` and `portal-auth-lambda-role` each sit beside
  a distinctly-named Terraform-declared sibling in the same module (`portfolio-export-lambda-role`,
  `opalinvest-auth-lambda-role`). Neither character note anticipated this specific shape (a look-alike
  declared cousin, not a match); it does not change either disposition, but it is the kind of detail
  a name-only lookup can miss and a bound-mandated by-name check catches.

## THE CLASS RE-ARMS ON ONBOARDING (brief F9, carried forward)

Every disposition above closes the INSTANCE: these 16 named members, at IAM-s-5's vintage, each now
carry a governance token. It does not close the CLASS. Brief F9's distinction holds exactly as
stated in the battery findings: a new Lambda stood up by console click, a new EC2 instance given an
inline role, or a new CodeBuild project set up the way
`codebuild-semantic-clustering-role` was (a documented manual build, no Terraform) mints a fresh
live-but-undeclared role tomorrow by the identical mechanism that produced these 16, and disposing
of today's 16 does not touch that mechanism at all. This cell does not build a monitor, alert, or
scheduled check for it (`G-21` is ARMED and stays out of scope here) -- the re-arming on onboarding
is stated as a fact this deliverable carries forward, not remediated by it and not this cell's
failure to remediate.

## SCOPE HELD (C-TWO-REMEDIES, bound D6)

Nothing above assesses whether any member's permissions are appropriately scoped, and nothing above
recommends adding, tightening, or adjusting any grant on any of the 16 -- that judgment belongs to
`IAM-s-1` and is a different remedy that does not move together with this one. A role's governance
placement (in code, or a recorded and owned exception) says nothing about whether its permissions
are right-sized, and this deliverable does not conflate the two in either direction. No Terraform
was modified, created, deleted, or edited to produce this deliverable; every `ADOPT` token above is
a recommendation for a later act by a seat with that lane, never an act performed here, and every
`DECLARED` token above reports a fact already true in Terraform, not an act performed by this
deliverable.

## SURPRISE ROWS FILED

Six of the sixteen dispositions above name a decision this worker cannot authorize (no send tool, no
sign-off capability), plus one instrument discrepancy this cell's own re-measurement surfaced.
Filed in `../../surprise-channel/investigations/INVESTIGATION_v1.md`:

- `NFRA_IAMROLES202609-Z-W3-S2` -- the `comp-find --corpus aws` DECLARED-vs-LIVE drift instrument
  misclassifies `seeking-alpha-scraper-role` as `LIVE-no-DECLARED` despite a genuine, name-matching
  `resource "aws_iam_role"` declaration in Terraform source, corroborated by `comp-iam`'s own parse;
  plus a same-day `comp-iam` role-count drift (195 cited in the L5-lane preflight vs. 191 on this
  cell's fresh re-run) that this cell's disposition does not depend on but that a later aggregate-count
  reader would need to know about.
- `NFRA_IAMROLES202609-Z-W3-S3` -- three members (`ecsTaskExecutionRole`, `rds-monitoring-role`,
  `vpc-flow-logs-role`) are plausible AWS service-default roles this worker cannot confirm the origin
  of or sign an exemption for; dispositioned exempt, owner=UNASSIGNED, with the decision named.
- `NFRA_IAMROLES202609-Z-W3-S4` -- two members (`portal-auth-lambda-role`,
  `opal-data-refresh-lambda-role`) are production serving-path roles where IAM-s-5's own character
  note names an exemption as a heavier claim; this worker cannot make that heavier call, dispositioned
  exempt, owner=UNASSIGNED, with the decision named.
- `NFRA_IAMROLES202609-Z-W3-S5` -- `lambda-test-role` reads as residue, a different remedy shape
  (retire vs. formalize) than the other two classes; dispositioned exempt, owner=UNASSIGNED, with
  the decision named.
    ACCEPTED 2026-10-09 by `0.7.0_AE_CloudOps~Z`: Live 2026-10-09: lambda trust, 1 inline
    `workspace-sync-permissions`, 0 consumers, RoleLastUsed 2025-12-30. HONEST LIMIT: this is the row with the least
    distinguishing evidence of my ten -- a named policy and a named role, nine months idle, no consumer and no obvious
    module -- so I accept custody WITHOUT asserting a home, and I would want the workload's owner named in its pair
    before a declaration lands anywhere. I accept custody of the role AND of the adoption decision; I do NOT accept
    the apply, which is a separate WORLD act under its own never-widen pair, and any declaration must leave
    `inline_policy` and `managed_policy_arns` ABSENT (both are Optional+Computed and become authoritative when set).
    Full reasoning: deliverables/0.7.0_AE_CloudOps~Z/ACCEPTANCE_ROWS_TEN.md; families and order of application:
    ADOPTION_PLAN_TEN.md.
