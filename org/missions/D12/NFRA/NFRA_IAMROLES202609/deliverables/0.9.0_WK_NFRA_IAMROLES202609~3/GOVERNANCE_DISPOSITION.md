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

1. `bd-merge-daily-lambda-role` -- ADOPT. Absent from the fresh 191-role comp-iam parse and from
   every first-party Terraform file in this repo (`comp-find infra/ --all`: only two world-model
   census/inventory JSON hits, no SURFACED or DEF band); an ordinary bd-domain role with 17 already
   Terraform-declared bd- siblings (`bd-processor-lambda-role`, `bd-silver-merge-role`,
   `bd-daily-trigger-lambda-role` and others, per the same comp-iam parse) and nothing in this repo
   distinguishing it as a candidate for exception.
2. `bd-pipeline-task-role` -- ADOPT. Same evidence pattern as #1: absent from the fresh comp-iam
   parse, no SURFACED/DEF source hit, no documented rationale, an ordinary bd- role among many
   already-declared bd- siblings.
3. `codebuild-semantic-clustering-role` -- ADOPT. Manually built via a documented one-off setup
   (`infra/aws/lambda/news_semantic_clustering/CODEBUILD_SETUP.md`, dated 2026-02-17, "Engineer:
   Data Scientist", "What Was Created: 1. IAM Role for CodeBuild -- Role Name:
   codebuild-semantic-clustering-role"). That document records what an engineer built, never a
   decision to exclude it from Terraform, so it does not meet FWD-4's ACCEPT bar for an exemption
   ("says who decided that and why" -- a build log names no such decision). House convention already
   manages CodeBuild roles of this exact shape in Terraform (`opal-drift-producer-codebuild-role`,
   `opal-stitch-produce-codebuild-role`, both present in the fresh comp-iam parse) -- this one is the
   outlier against that convention, not the norm.
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
5. `finbert-ec2-backfill-role` -- ADOPT. Absent from the fresh comp-iam parse and from every
   first-party source file (census/inventory JSON only); an EC2 backfill role with no service-default
   naming pattern and no documented exclusion rationale anywhere in this repo.
6. `lambda-ec2-runtime-monitor-role` -- ADOPT. Same evidence pattern: absent from the fresh
   comp-iam parse, no SURFACED/DEF source hit beyond census JSON, no documented rationale for
   exclusion.
7. `lambda-test-role` -- EXEMPT owner=UNASSIGNED reason=the name itself reads as test/scratch
   residue rather than a serving role, and residue is a DIFFERENT remedy shape than either "add to
   Terraform" or "except it going forward" -- the decision owed is whether this role is still
   exercised at all and, if not, whether it should be retired, which neither this cell nor IAM-s-5
   has usage-telemetry access or the mandate to determine. A named owner must make that call.
8. `opal-data-refresh-lambda-role` -- EXEMPT owner=UNASSIGNED reason=production serving-path role
   (backs the deployed `opal-data-refresh-api` Lambda via a literal `role_arn`,
   `infra/aws/terraform/data-refresh/main.tf:38`) that Terraform already touches through three
   `aws_iam_role_policy` attachments explicitly naming it "the pre-existing
   opal-data-refresh-lambda-role" (`main.tf:53`) but never creates or owns as a resource. IAM-s-5's
   own character note flags an exemption here as "a much heavier claim" than for a background role;
   this worker cannot make that heavier call or name who accepts it. The decision owed is an explicit
   sign-off (adopt via import, or formally except) from a seat holding Terraform-change authority.
9. `opal-smartx-lambda-role` -- ADOPT. Absent from the fresh comp-iam parse and from all Terraform
   source; documented only in a hand-maintained, non-Terraform inventory
   (`infra/aws/manifests/iam/iam-roles.yaml`, "Last Updated: 2026-01-02") and the portal-functions
   manifest (`infra/aws/manifests/lambda/opal-portal-functions.yaml:138,736-737`). An inventory entry
   describes the role; it is not a decision to except it from Terraform, so FWD-4's exemption bar is
   not met.
10. `portal-auth-lambda-role` -- EXEMPT owner=UNASSIGNED reason=production serving-path role per
    IAM-s-5's own character note ("PRODUCTION SURFACES ON THE SERVING PATH ... a much heavier
    claim"), and unlike `opal-data-refresh-lambda-role` this one has ZERO Terraform source touch at
    all (fresh comp-iam parse: absent; `comp-find infra/ --all`: only world-model census/inventory
    JSON and a parity dump, no SURFACED or DEF band). It is NOT the same object as the
    Terraform-declared `opalinvest-auth-lambda-role` (`infra/aws/terraform/portal-auth/iam.tf:16`,
    a distinctly-named sibling created in the same module) -- a genuinely separate, undeclared role
    next to an already-declared one for the same functional area. The heavier stakes IAM-s-5 named
    apply in full; the decision owed is an explicit sign-off from a seat with Terraform-change
    authority on whether to adopt or except, not a call this worker can make.
11. `portfolio-management-lambda-role` -- ADOPT. Absent from the fresh comp-iam parse and from all
    Terraform source (census/inventory JSON only). It is NOT the same object as the
    Terraform-declared `portfolio-export-lambda-role` (`infra/aws/terraform/portfolio-management/
    main.tf:227`, a distinctly-named sibling created in the same module) -- a genuinely separate,
    undeclared role alongside an already-declared one in the same domain, with no documented
    rationale anywhere in this repo for treating it differently.
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
14. `sentiment_query_api-role` -- ADOPT. Absent from the fresh comp-iam parse and from all
    Terraform source (census/inventory JSON only); an ordinary API-serving lambda role with no
    service-default naming pattern and no documented exclusion rationale.
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
16. `workspace-sync-lambda-role` -- ADOPT. Absent from the fresh comp-iam parse and from all
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
