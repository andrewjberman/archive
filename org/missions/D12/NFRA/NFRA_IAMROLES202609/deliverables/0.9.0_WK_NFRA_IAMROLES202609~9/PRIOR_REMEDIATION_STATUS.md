# IAM-t-3 -- THE THREE PRIOR REMEDIATION PLANS: landed or not, ON THE ARTIFACT

**Cell:** IAM-t-3 (outcome FWD-6; round-2 analysis "R3-C"). **Worker:** `0.9.0_WK_NFRA_IAMROLES202609~9`.
**Date of every live read below:** 2026-09-10. **Fabric:** site-z.

---

## 0. WHAT THIS DOCUMENT DOES NOT REST ON

No verdict below is drawn from a plan's **directory**, its **status tag**, a **commit message**, or a
**ledger entry**. C-CLOSED-RECORD, in the cell's words: a closed record is a snapshot, not an oracle.
Concretely, and stated because the temptation here is unusually strong:

* Plans 1 and 2 sit in `infra/security/remediation/active/`. `completed/` exists and is **not empty** --
  it holds `moltbot-egress-hardening-2026-02-17.md` and `moltbot-iam-scoping-2026-02-17.md`. The
  2026-02-17 reorganisation therefore **demonstrably did sort work into `completed/`**, which makes
  "still in `active/`" read like a status claim. It is not one, and nothing below uses it.
* Plan 3 carries `<status>complete -- SPRING-CLEAN 2026-08-25 (S2)</status>`. Its own text then says
  *"Closed as a record act, not a work verdict. Prior status: ISSUED -- QUEUED after WS-2b"*, and the
  document also carries `<dispatch_held>true</dispatch_held>`. A reader trusting the tag reads "complete".
  The artifact reads 1 of 3 items landed, and by another project's hand. Not used as evidence either.

### The instruments, named, with their vintages and their limits

| plane | instrument | scope / denominator | vintage |
|---|---|---|---|
| DESIRED | `python .tools/comp-find` run **from this worktree** | repo, `[corpus=all]`, 29409 files content / 31192 files name | HEAD `775e6cf20a30b7af29e0341b48b0c2a1ab6d1195`, branch `wk-NFRA_IAMROLES202609-9`, `/c/tmp/wk-iamroles-9` |
| DESIRED | direct line-range reads of named `.tf` files | per file, cited `file:line @ <commit>` | per citation |
| LIVE | `.tools/aws <service> <read-only verb>` | account `313476888478`, region **`us-east-1`** unless stated | 2026-09-10, this pass |

**THE TREE THIS WAS MEASURED FROM IS CLEAN AND THAT IS LOAD-BEARING.** The battery warned that measuring
the Terraform plane from a dirty tree can show a policy that is in no commit and read it as landed. This
worktree's `git status --porcelain` returned **empty** (zero modified, zero untracked) before every sweep
below, so every DESIRED-plane hit is committed state at `775e6cf20a`. This is *not* the main checkout.

**COVERAGE QUALIFIER on every live read:** region-scoped to `us-east-1`. The two populations where a
second region could have hidden members were measured and are empty:
`aws secretsmanager list-secrets --region us-east-2` -> no output, rc=0;
`aws apigateway get-rest-apis --region us-east-2` -> no output, rc=0.

---

## PLAN 1 -- `infra/security/remediation/active/iam-least-privilege-rollback-plan.md`

**Vintage of the plan:** `6aad42da0dffb72c88371b8dbc40349d15c6c3f7`, 2026-02-17, Andrew Berman
(`git log -1 -- <path>`, run in this worktree). 13331 bytes, 506 lines, present at HEAD.

**What it committed to, in its own artifacts** (not paraphrase -- these are the names the plan itself
types into `aws` commands, and they are what makes it checkable):

1. Phase 1, described by the plan as **"No Risk"** and first in order: create two customer-managed
   policies, `OpalLambdaLeastPrivilege` and `OpalEC2SSMLeastPrivilege` (`:159-168`), plus per-function
   policies via `./create-function-specific-policies.sh` (`:170-171`).
2. Phase 2: dual-attach, stamping each role with tags `IAMMigrationStatus=DualAttached`,
   `IAMMigrationDate`, `OldPolicy`, `NewPolicy` (`:194-200`).
3. Phase 4: detach old, re-stamping `IAMMigrationStatus=NewPolicyOnly` + `OldPolicyRemoved` (`:271-276`).
4. Rollout over eight named roles in four tiers (`:376-405`).

### VERDICT: **NOT-LANDED** @ `775e6cf20a` (DESIRED) and 2026-09-10 (LIVE)

**DESIRED plane.**

* `python .tools/comp-find 'Opal(Lambda|EC2SSM)LeastPrivilege' --all`
  -> `DENOMINATOR: 8 hit(s) across 29409 file(s) scanned in scope [corpus=all]`.
  All 8 are the plan document itself (`iam-least-privilege-rollback-plan.md:160,:166,:186,:421`) or this
  project's own commentary about it. **Zero hits under `infra/aws/terraform/`.**
* `python .tools/comp-find 'IAMMigrationStatus' --all`
  -> `DENOMINATOR: 7 hit(s) across 29409 file(s)`. All 7 are the plan (`:197,:274,:304`) plus commentary.
* `python .tools/comp-find --name '<script>'` for the plan's own three scripts:
  `dual-attach-policies.sh` -> `0 hit(s) across 31192 file(s)`;
  `create-custom-policies.sh` -> `0 hit(s) across 31192 file(s)`;
  `create-function-specific-policies.sh` -> `0 hit(s) across 31192 file(s)`.
  **POSITIVE CONTROL on that instrument:** `--name 'safe-commit.sh'` -> `1 hit(s)`, `[HEAD] .tools/safe-commit.sh`.
  The filename sweep finds a `.sh` that exists, so the three zeros are absences, not blindness.

**LIVE plane.**

* `aws iam list-policies --scope Local --query 'Policies[].PolicyName'` -> **30 customer-managed policies**,
  enumerated in full. Neither `OpalLambdaLeastPrivilege` nor `OpalEC2SSMLeastPrivilege` is among them.
  The plan's **first, self-described zero-risk step** produced nothing that survives.
* The eight named target roles, `aws iam list-role-tags --role-name <r> --query "Tags[?Key=='IAMMigrationStatus']"`:

  | role (plan `:376-405`) | live | `IAMMigrationStatus` |
  |---|---|---|
  | `bd-allocation-checker-lambda-role` | exists | `[]` rc=0 |
  | `docker-builder-temp-role` | **NoSuchEntity** | n/a |
  | `bd-gold-detail-generator-role` | exists | `[]` rc=0 |
  | `trending-image-selector-role` | **NoSuchEntity** | n/a |
  | `bd-exporter-ec2-role` | exists | `[]` rc=0 |
  | `smartx-ingestion-pipeline-role` | **NoSuchEntity** | n/a |
  | `opal-portal-data-proxy-role` | **NoSuchEntity** | n/a |
  | `news-layer3-curation-role` | **NoSuchEntity** | n/a |

  The three survivors carry `Project / Name / System / Environment / ManagedBy` -- a general tagging
  scheme, none of the plan's five migration tags. Five of eight roles no longer exist at all, which is
  retirement, not migration: a migrated role would still exist and would carry `NewPolicyOnly`.

### DENOMINATOR

* **8 of 8** named target roles queried live; **8 of 8** answered (3 tag-read, 5 `NoSuchEntity`). Zero unreachable.
* **2 of 2** named custom policies checked against a **complete** 30-name customer-managed enumeration.
* **0 of the headline "40 policies" individually checked -- because the document does not enumerate them.**
  The plan's Overview (`:4`) says *"Replace 40 overly-permissive IAM policies"*; the document then names
  **8 roles** (`:376-405`) and its own timeline table (`:440-457`) sums to **22 roles** (2+5+10+5). Three
  numbers, one document, no list of forty. The forty is not recoverable from the plan, so no verdict about
  "the forty" is available to anyone from this artifact. Filed as surprise row `NFRA_IAMROLES202609-Z-W9-S2`.
  The verdict above is scoped to what the plan **does** name, and says so.

### NEGATIVE CONTROL -- what I would have seen if the answer were the other way

Had Phase 1 alone run, the two named policies would appear in the `--scope Local` list. That list is not
empty and is not blind to policies of this class: it contains **20 least-privilege-shaped per-firm policies**
(`opal-assets-silver-write-schwab`, `opal-assets-write-orion`, and 18 siblings). So the instrument
demonstrably prints custom least-privilege policies when they exist. Had Phase 2 run, at least one of the
three surviving roles would carry `IAMMigrationStatus=DualAttached`; had Phase 4 run, `OldPolicyRemoved`.
Three independent stamps, three empty reads, one complete policy enumeration. There is no hypothesis under
which the plan landed and all four of those reads look like this.

### CROSS-READING, and its limit

Sibling worker `0.9.0_WK_NFRA_IAMROLES202609~4`'s IAM-s-7 deliverable
(`.../deliverables/0.9.0_WK_NFRA_IAMROLES202609~4/HISTORICAL_COMPLETION.md:52`) reaches **NOT-LANDED
@21d42b3b16** on this same plan. Per Rule 22 that is offered as **agreement, not corroboration**: it used
the same `aws iam` API family (a filtered `list-policies` query and `get-role --query Role.Tags` rather
than my full enumeration and `list-role-tags`), so a fault in that API family would move both readings
together. The genuinely different instrument here is the repo-side `comp-find` sweep, and it agrees.

---

## PLAN 2 -- `infra/security/remediation/active/SOC2-FULL-REMEDIATION-MASTER-PLAN.md`

**Vintage:** `6aad42da0dffb72c88371b8dbc40349d15c6c3f7`, 2026-02-17, Andrew Berman -- **the same commit
that last touched plan 1**. 13127 bytes, 473 lines, present at HEAD.

**What it committed to:** three phases with enumerated sub-items and counts -- Phase 1 EBS encryption
("All 11 volumes encrypted", `:60-63`), Phase 2 IAM least privilege (**this is plan 1**, `:75-129`), and
Phase 3 security hardening in seven numbered limbs (`:135-279`). **Enumerable limb denominator: 9.**

### VERDICT: **PARTIALLY-LANDED** -- 2 limbs landed, 3 not landed, 2 partial, 2 undeterminable within cap

Checked **7 of 9** limbs on the artifact. **2 of 9** (3.5, 3.7) are UNDETERMINABLE within the read cap and
each names its missing instrument below.

**Phase 1 -- EBS volume encryption: LANDED.**
`aws ec2 describe-volumes --query 'Volumes[].[VolumeId,Encrypted]'` -> **32 of 32 `True`**, rc=0.

> **CONFOUNDER, FOUND AND DISCLOSED:** `aws ec2 get-ebs-encryption-by-default` -> `{"EbsEncryptionByDefault": true}`.
> "Everything is encrypted" is therefore **not** discriminating on its own -- it is exactly what an account
> with default encryption looks like whether or not this plan ever ran.
>
> **THE DISCRIMINATOR:** default encryption applies only to **newly created** volumes; it never encrypts an
> existing one. So an unencrypted pre-2026-02-17 volume would have survived it. `describe-volumes --query
> 'Volumes[].[CreateTime,Encrypted]'` shows exactly **one** volume predating the plan (2025-12-22, `True`)
> and then **six volumes created on 2026-02-17 between 17:37:35Z and 18:31:22Z** -- a 54-minute burst on the
> plan's own creation date, which is the signature of the blue-green volume swap the plan describes
> ("Encrypt batch 1 (8 stopped instances) - 3 hours", `:46-51`). Old volumes destroyed, new encrypted ones
> minted, in one window.

**NEGATIVE CONTROL:** had the swap not run, unencrypted volumes created before 2026-02-17 would still be
attached, because nothing in this account can retro-encrypt them. Zero unencrypted volumes exist across a
32-volume enumeration. Denominator: 32 of 32.

**Phase 2 -- IAM least privilege: NOT-LANDED.** This limb *is* plan 1. See above; the evidence is not
repeated. Note that plan 2 assigned this phase 8 of its 10-14 days and the target "Security score jumps to
~85/100" (`:115-120`) -- the single largest limb of the master plan did not run.

**3.1 -- DynamoDB deletion protection (plan: 15 tables): PARTIALLY-LANDED at population grain,
UNDETERMINABLE at member grain.** `aws dynamodb list-tables` -> **37 tables**; `describe-table --query
'Table.DeletionProtectionEnabled'` on each -> **18 `True`, 19 `False`**. Denominator: 37 of 37 described,
zero unreachable. Member grain is unreachable because the plan **names none of its 15 tables** and the
population has since grown to 37; I cannot say which 18 are the plan's.
**NEGATIVE CONTROL:** full landing on a static population reads 37/37 `True`; total non-landing on a
never-protected estate reads 0/37 `True`. The mixed 18/19 is what a partial rollout *or* a grown population
looks like, and those two are not separable without the plan's own 15 names -- which is why the member
verdict is UNDETERMINABLE rather than a guess. **What would settle it:** table `CreationDateTime` from the
same `describe-table` output, partitioning the 37 into pre- and post-2026-02-17 cohorts; if the 15 oldest
unprotected tables are pre-plan, the limb did not land for its own targets.

**3.2 -- CloudFront WAF attachment (plan: 12 distributions): LANDED on today's population.**
`aws cloudfront list-distributions --query 'DistributionList.Items[].[Id,WebACLId]'` -> **2 of 2 attached**:
`EVTSA9VEHNZVH` -> `arn:aws:wafv2:us-east-1:313476888478:global/webacl/opal-cloudfront-protection/a09833c0-...`,
`E1DHJH4Y1W8YC2` -> `.../opal-website-edge-protection/af7ed304-...`. Population drift 12 -> 2; the ten others
no longer exist and cannot be graded. Denominator: 2 of 2 live distributions.
**NEGATIVE CONTROL:** an unattached distribution prints `None` in that column. That output form is
demonstrated on the very same run by limb 3.4 below, where seven stages print `None` for the analogous
field -- so the column is provably capable of rendering an absence, and two ARNs are two attachments.

**3.3 -- EC2 IMDSv2 enforcement (plan: 9 instances): PARTIALLY-LANDED.**
`aws ec2 describe-instances --query 'Reservations[].Instances[].[InstanceId,State.Name,MetadataOptions.HttpTokens]'`
-> **32 instances: 28 `required`, 4 `optional`**. The four still optional:
`i-07ebae29a16e43ed1` (stopped), `i-06376c11d8b3c3443` (stopped), `i-0f3d57a97f14727af` (**running**),
`i-08ee5fb1991430cb9` (stopped). Denominator: 32 of 32.
**NEGATIVE CONTROL:** the field prints both values on one run, so `required` is not a renderer default or a
missing-key artifact; and a fully-landed limb on a grown estate would still be expected to read 32/32 only
if enforcement were continuous -- it reads 28/32, so at minimum enforcement is not held.

**3.4 -- API Gateway access logging (plan: 4 APIs): NOT-LANDED.**
`aws apigateway get-rest-apis` -> 1 REST API (`f61h681z9g opal-portal-api`); `get-stages` -> stages `prod`
and `production`, both `accessLogSettings.destinationArn` = `None`.
`aws apigatewayv2 get-apis` -> 5 HTTP APIs (`opal-portal-data-proxy-api`, `sentiment-query-api`,
`inf-otp-relay-api`, `opal-session-analytics-api`, `trade-submission-api`); `get-stages` on each ->
`AccessLogSettings.DestinationArn` = `None` on all 5.
**Denominator: 7 of 7 stages across 6 of 6 APIs, both API planes, both regions** (us-east-2 REST -> empty, rc=0).
**NEGATIVE CONTROL:** a landed limb prints a CloudWatch log-group ARN in that column. The same `--output text`
renderer printed two full `arn:aws:wafv2:...` values in limb 3.2 on this same pass, so ARNs are not being
swallowed. Seven `None`s are seven absences.

**3.5 -- Lambda environment-variable secrets (plan: 3 functions): UNDETERMINABLE.**
**NOT CHECKED**, deliberately, against the cell's cap: the plan **names none of the three functions** and the
account holds **203 Lambda functions** (`aws lambda list-functions`, client-side count). Scanning every
function's environment against the 91 live secret names is beyond a bounded read here.
**WHAT WOULD SETTLE IT (the missing instrument, named):** one `aws lambda list-functions` pull retaining
`Environment.Variables`, scanned client-side for values matching the 91 `secretsmanager list-secrets` names
or for keys matching `.*(SECRET|KEY|TOKEN|PASSWORD).*`; a hit whose value is a literal rather than a secret
ARN is an unmigrated function. One paginated call plus a local scan -- read-only, and cheap for a cell that
is given it as its subject.

**3.6 -- Secrets Manager auto-rotation (plan: 2 secrets): NOT-LANDED.**
`aws secretsmanager list-secrets --query 'SecretList[].[Name,RotationEnabled]'` -> **91 secrets, 91 of 91
read `None`**. Plus `--region us-east-2` -> empty, rc=0, closing the second-region hole.
Denominator: 91 of 91 in the only region that holds any.
**NEGATIVE CONTROL:** `RotationEnabled` renders `True` where rotation is configured. A uniform absence across
the entire account means there is no "the two rotating secrets are somewhere else" reading available -- the
enumeration *is* the population.

**3.7 -- Remaining items (security groups, Step Functions logging, Andrew's IAM key rotation): UNDETERMINABLE.**
Not checked; three unrelated surfaces, none named specifically enough to grade. **What would settle it:**
`aws stepfunctions list-state-machines` + `describe-state-machine --query loggingConfiguration.level` for the
logging limb; `aws iam list-access-keys --user-name Andrew_Berman --query 'AccessKeyMetadata[].CreateDate'`
against 2026-02-17 for the key limb. Both single read-only calls. **NOT RUN HERE** -- the key-rotation limb
is a credential-plane question that is the OPSEC project's subject, not this cell's, and this cell may not
act there.

### PLAN 2 SUMMARY

| limb | verdict | denominator |
|---|---|---|
| Phase 1 EBS encryption | **LANDED** | 32 of 32 volumes |
| Phase 2 IAM least privilege (= plan 1) | **NOT-LANDED** | 8 of 8 roles, 2 of 2 policies |
| 3.1 DynamoDB deletion protection | **PARTIALLY-LANDED** (member grain UNDETERMINABLE) | 37 of 37 tables |
| 3.2 CloudFront WAF | **LANDED** on today's population | 2 of 2 distributions |
| 3.3 EC2 IMDSv2 | **PARTIALLY-LANDED** | 32 of 32 instances |
| 3.4 API Gateway access logging | **NOT-LANDED** | 7 of 7 stages |
| 3.5 Lambda env-var secrets | **UNDETERMINABLE** | 0 of 203 functions checked |
| 3.6 Secrets auto-rotation | **NOT-LANDED** | 91 of 91 secrets |
| 3.7 Remaining items | **UNDETERMINABLE** | 0 of 3 |

**OVERALL: PARTIALLY-LANDED.** 7 of 9 limbs graded on the artifact. The plan's own headline goal --
"Current Score: 0/100 -> Target Score: 90+/100" (`:6-7`) -- is not measurable from any artifact this cell can
reach, and no score was found anywhere; that number is the plan's own instrument and its absence is not
evidence in either direction. Note the shape: **the phase that landed is the one with no IAM in it.**

---

## PLAN 3 -- `org/projects/task_orders/PORTAL_AUTHHARD.WS6.least-priv-role-split-secret-dewildcard.md`

**Vintage:** `122947867278df5df44fe9faa84c2dd1cd6fd12f`, 2026-08-25, `1.0.0_SA_CTO~X`. 5809 bytes, present at HEAD.
**BOUND OBSERVED:** this file was **read only**. Nothing was written into `PORTAL_AUTHHARD`, nothing re-opened.

**What it committed to:** three numbered deliverable items (`:34-40`). **Denominator: 3 of 3 checked.**

### VERDICT: **PARTIALLY-LANDED** -- 1 of 3 items landed, and it landed under a DIFFERENT project's authority

**Item 1 -- SPLIT `opal-portal-lambda-role`, ISOLATING THE PUBLIC AUTHORIZER FIRST: NOT-LANDED.**

* DESIRED @ `775e6cf20a`: `infra/aws/terraform/portal-auth/iam.tf:198` still reads
  *"This role is shared by 13 Lambda functions across multiple pipelines."*
  `infra/aws/terraform/portfolio-management/rest-authorizer.tf:30` reads
  *"NO NEW IAM GRANT. This function reuses the SHARED opal-portal-lambda-role"* -- an **authorizer being
  added to** the shared role, which is the opposite of the item.
* LIVE 2026-09-10: `aws lambda list-functions` filtered on `Role == arn:aws:iam::313476888478:role/opal-portal-lambda-role`,
  counted client-side -> **12 functions**, out of **203** in the account. Two of the twelve are the
  authorizers: **`opal-portal-authorizer`** and **`opal-portal-rest-authorizer`**.
* LIVE: `aws iam list-role-policies --role-name opal-portal-lambda-role --query 'length(PolicyNames)'` -> **18**
  inline policies, one of which is `SecretsManagerAccess`. So the public authorizer still shares a role that
  reads production secrets -- the exact condition the item existed to end.

**NEGATIVE CONTROL:** a landed split would have minted a dedicated role. `aws iam list-roles --query
'Roles[].RoleName'` -> **229 roles**, of which **zero** contain "author" (case-insensitive, pipe-receiver
filter over the full enumeration; the filter exited 1 = no match). And `opal-portal-authorizer` would have
dropped out of the 12-function list; it is in it. Two independent stamps of the same absence.

**Item 2 -- replace `secret:opal/*` wildcards with explicit per-role allowlists: LANDED, 3 of 3 named roles.**

* DESIRED, `infra/aws/terraform/shared-infra/opal-portal-lambda-role.tf:59` @ `0cf8aed766997b13af1be66722a481dba8222336`
  (2026-07-09, `0.5.0_AE_OpalETL`): *"NARROWED 2026-07-09 (NFRA_TERRAFORM-P2 Phase A). Was `secret:opal/*` in
  BOTH regions."* -- with three exact ARNs at `:79-81` (`opal/auth/jwt-public-key-??????`,
  `opal/external-apis-??????`, `opal/openai/news-trending-??????`).
* DESIRED, `infra/aws/terraform/news-pipeline/iam.tf:63`: same narrowing on `news-ingestion-lambda-role`, two
  exact ARNs at `:76-77`.
* DESIRED, `infra/aws/terraform/yang-pipeline/iam.tf:142`: same on `yang-pipeline-lambda-role` (the one the
  plan itself called "region-scoped-safe").
* DESIRED, `infra/aws/terraform/portal-auth/iam.tf:230-233` @ `a7edcf67228061a71135f437b417474ed3cfe67c`
  (2026-09-03, `0.7.0_AE_CloudOps~X`), on `opalinvest-auth-lambda-role`'s neighbourhood: *"cross-firm-secret-deny.tf:6-10
  describes this role as holding `secret:opal/*`. IT DOES NOT, at 2026-09-03 -- Phase A ... narrowed it to an allowlist."*
* **LIVE, the same object read directly:** `aws iam get-role-policy --role-name opal-portal-lambda-role
  --policy-name SecretsManagerAccess --query 'PolicyDocument.Statement[].Resource'` returns **exactly those
  three ARNs and no wildcard**, rc=0. DESIRED == APPLIED on the live IAM plane.

> **THE FINDING THAT THE STATUS TAG WOULD HAVE HIDDEN:** this work landed on **2026-07-09** under
> **NFRA_TERRAFORM-P2 Phase A** -- six weeks *before* plan 3's own file was last written (2026-08-25), by a
> different seat, under a different project, against a different plan document
> (`infra/security/remediation/secrets-allowlist-narrowing-and-least-privilege-PLAN-20260709.md`, which is a
> fourth plan in the same directory and is not one of this cell's three). Plan 3's `<status>complete</status>`
> would have told a reader "done" and been accidentally right about this one item **for entirely the wrong
> reason**, while being flatly wrong about items 1 and 3. A location, a tag and a completion claim were all
> three uninformative here, in both directions at once.

**NEGATIVE CONTROL:** had the de-wildcarding not landed, `secret:opal/*` would appear as a **Resource value**
in a policy body. `python .tools/comp-find 'secret:opal/\*' infra/aws/terraform/ --all` ->
`DENOMINATOR: 17 hit(s) across 517 file(s)`, and **every one of the 17 is inside a `#` comment** describing
the past state or the deny-belt's original 2026-07 reasoning; none is a live `Resource =` line. The
independent check that this is not a reading error: the **live** `get-role-policy` read has no comments in it
at all and returns the allowlist. Two planes, one answer.

**Item 3 -- `dynamodb:LeadingKeys` conditions on the partner tables: NOT-LANDED.**

* `python .tools/comp-find 'LeadingKeys' --all` -> `DENOMINATOR: 10 hit(s) across 29409 file(s) [corpus=all]`.
  All 10 are prose or config: `docs/architecture/PORTAL_AUTHHARD_PRD.md:45,:163,:168,:212`,
  `docs/briefs/PORTAL_AUTH_HARDENING_BRIEF_20260720.md:67`, `org/projects/PORTAL_AUTHHARD.json:5`, and the task
  order itself (`:5,:13,:39,:60`). **Zero hits under `infra/aws/terraform/`.**

**NEGATIVE CONTROL:** had it landed, at least one `.tf` under `infra/aws/terraform/` would carry the condition
key. That sweep provably reaches Terraform policy bodies: the *same* instrument over the *same* 517-file
Terraform scope returned 17 hits for `secret:opal/*` in item 2. A zero under a scope that just produced 17 is
an absence, not a blind spot.

### PLAN 3 DENOMINATOR

**3 of 3** deliverable items checked; **0 unreachable**. Within item 2, **3 of 3** named wildcard-holding roles
verified in the DESIRED plane and **1 of 3** additionally verified on the LIVE plane
(`opal-portal-lambda-role`); the other two were not live-read, and that is stated rather than implied --
their verdict rests on committed Terraform at a pinned commit plus a third seat's dated in-source statement.
The plan's acceptance list also demands **exercise** (simulate-principal-policy, a broken-Lambda check, a
denied cross-partition read). **None of the five acceptance boxes is ticked in the document and this cell did
not exercise anything** -- establishing status is not exercising. So item 2's grade is APPLIED, not EXERCISED,
and is labelled that way.

---

## SUMMARY

| plan | vintage | verdict | items checked / items named |
|---|---|---|---|
| 1 `iam-least-privilege-rollback-plan.md` | `6aad42da0d` 2026-02-17 | **NOT-LANDED** | 8 of 8 roles, 2 of 2 policies; 0 of a headline "40" the doc never lists |
| 2 `SOC2-FULL-REMEDIATION-MASTER-PLAN.md` | `6aad42da0d` 2026-02-17 | **PARTIALLY-LANDED** | 7 of 9 limbs graded, 2 UNDETERMINABLE |
| 3 `PORTAL_AUTHHARD.WS6...md` | `1229478672` 2026-08-25 | **PARTIALLY-LANDED** | 3 of 3 items; 1 landed, under another project |

### The three UNDETERMINABLE verdicts and what would settle each

1. **Plan 1's "40 policies"** -- settled by nothing in this repo: the document does not enumerate them and no
   list of forty was found. What would settle it is a **February-vintage IAM snapshot**: the plan's own
   `backup-current-iam-state.sh` (`:30-59`) was to write one to S3. `aws s3 ls` over the backup prefix that
   script names is the one instrument that could reconstruct the denominator. If no such backup object exists,
   that is itself the answer -- Phase 0 did not run either, and the forty is unrecoverable for good.
2. **Plan 2 limb 3.1 at member grain** -- `CreationDateTime` from `describe-table`, partitioning today's 37
   tables into pre- and post-2026-02-17.
3. **Plan 2 limb 3.5** -- one `list-functions` pull retaining `Environment.Variables`, scanned client-side
   against the 91 live secret names.

All three are single bounded read-only calls. None was run here because none is this cell's named subject; each
is a cuttable next-round item rather than a shrug.

### What this cell did NOT do (bounds held)

No permission was narrowed, no plan was edited, no document was moved between `active/` and `completed/`, no
status tag was written, no alarm/monitor/schedule/notification was minted, AWS Access Analyzer was not used,
and nothing was written into `PORTAL_AUTHHARD`. Every AWS call was `get-*` / `list-*` / `describe-*`.
Mechanically checked: `git status --porcelain -- infra/security/remediation/
org/projects/task_orders/PORTAL_AUTHHARD.WS6.least-priv-role-split-secret-dewildcard.md infra/aws/terraform/`
-> `0`.

Recording that plan 1 did not land, and that plan 3's role split did not land, is a **status finding**. It is
not a recommendation to do either, and this document makes none (C-TWO-REMEDIES).

### Surprise rows filed from this cell

* `NFRA_IAMROLES202609-Z-W9-S1` -- the cell states plan 3 "carries NO status tag at all"; it carries a
  `<status>` reading `complete`, plus `dispatch_held=true`. OBSERVATION, INERT.
* `NFRA_IAMROLES202609-Z-W9-S2` -- the cell and AC4 state "plan 1 names forty policies"; the document names 8
  roles, its timeline sums to 22, and it lists no forty. OBSERVATION, INERT.
