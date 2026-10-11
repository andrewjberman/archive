# NARROW_SURVEY -- NFRA_IAMROLES202609.TO-IAM-x-2 PHASE A (the dead grants)

**Cell:** IAM-x-2 (round 7, FWD-4 enrichment; round-6 analysis E2)
**Executed by:** `0.7.0_AE_CloudOps~IR` -- **owner of record:** `0.7.0_AE_CloudOps~Z`
**Authority:** `ROUND_ANALYSIS.round6.md` @`2f49aa235b` E2; GO = the round-7 issuance @`8b61ddf94f`;
third target added by **A2-r7** @`0ac7a5b35c`.
**Issuer:** `2.0.0_SA_COO~ZI` -- **risk:** WORLD -- **PHASE A APPLIED NOTHING AND WROTE NOTHING TO AWS.**
**Measured:** 2026-10-11, worktree `C:/tmp/iam-w1b`, branch `wk-iamroles-r7-x2` @`cac9184c7d`,
Terraform v1.15.8, provider `hashicorp/aws v5.100.0`.

---

## 0. HEADLINE -- THE CELL'S OWN RULE REMOVES LESS THAN THE SURFACED HAZARD, AND THE REASONS DIFFER PER TARGET

The RULE OF REMOVAL is: *a statement is removed only if EVERY resource it names is read live as
non-existent.* Applied honestly to four policies, it yields:

| # | policy (module) | statements | verdict under the rule | squatting hazard? |
|---|---|---|---|---|
| 1 | `opal-smartx-s3-access` (smartx-pipeline) | 1 | **DELETE** -- the sole statement is wholly dead | **YES -- real** |
| 2 | `opal-smartx-secrets` (smartx-pipeline) | 1 | **DELETE** -- the sole statement is dead | **NO** |
| 3 | `CodeBuildSemanticClusteringPolicy` (news-pipeline) | 4 | **ZERO REMOVALS** -- see section 3 | **YES -- and unreachable** |
| 4 | `DynamoDBAccess` (market-overview, A2-r7) | 1 | removable, but see section 4 | **NO** |

**Two findings follow, and both are the issuer's to rule, not this seat's:**

- **Target 3 is where the hazard actually lives, and the rule cannot touch it.** Its one dead ARN shares
  a statement with a live one, so the statement stays.
- **Targets 2 and 4 are removable by the rule but carry NO squatting hazard at all**, because the cell's
  stated WHY is specific to S3's GLOBAL namespace and neither of those ARNs is global. Both are
  additionally *wrong-region*, not deleted: the resource exists in us-east-1.

So the set the rule removes and the set that poses the stated risk **overlap in only one of four targets**.

## 1. THE REQUIRED LINES

```
REMOVED: arn:aws:s3:::opal-data-smartx LIVE-READ: (404) Not Found
REMOVED: arn:aws:s3:::opal-data-smartx/* LIVE-READ: (404) Not Found -- key pattern on the same absent bucket
REMOVED: arn:aws:s3:::opal-code-smartx LIVE-READ: (404) Not Found
REMOVED: arn:aws:s3:::opal-code-smartx/* LIVE-READ: (404) Not Found -- key pattern on the same absent bucket
REMOVED: arn:aws:secretsmanager:us-east-2:313476888478:secret:opal/smartx/config-* LIVE-READ: ResourceNotFoundException
REMOVED: arn:aws:dynamodb:us-east-2:313476888478:table/opal-news-articles LIVE-READ: ResourceNotFoundException
CONTROL: arn:aws:s3:::opal-data-news-v2 FOUND
CONTROL: arn:aws:secretsmanager:us-east-1:313476888478:secret:opal/smartx/config-IKCzE6 FOUND
CONTROL: arn:aws:dynamodb:us-east-1:313476888478:table/opal-news-articles FOUND
CONTROL: arn:aws:lambda:us-east-1:313476888478:function:news-semantic-clustering FOUND
VERDICT: opal-smartx-s3-access (smartx-pipeline): DELETE
VERDICT: opal-smartx-secrets (smartx-pipeline): DELETE
VERDICT: CodeBuildSemanticClusteringPolicy (news-pipeline): NO-CHANGE -- zero statements qualify under the rule
VERDICT: DynamoDBAccess (market-overview): DELETE-BY-RULE, BUT REFERRED -- wrong-region, no squatting hazard, removal destroys the role's only data grant
```

> **`NO-CHANGE` and `DELETE-BY-RULE, BUT REFERRED` are not among the two verdicts the cell offers
> (NARROW | DELETE).** They are reported rather than forced into the binary, because forcing target 3
> into NARROW would claim a removal the rule does not license, and forcing target 4 into a bare DELETE
> would hide that the rule and the rationale disagree there.

**EVERY DEAD READ HAS A LIVE CONTROL ON THE SAME CALL**, because a failed retrieval returns a value:
`head-bucket` dead x3 against `head-bucket` FOUND once; `describe-secret` dead in us-east-2 against
`describe-secret` FOUND in us-east-1; `describe-table` dead in us-east-2 against `describe-table` FOUND in
us-east-1. **And each regional absence was corroborated by a denominator, not just a point read:**
`list-secrets --region us-east-2` returns **0 secrets**; `list-tables --region us-east-2` returns
**0 tables**. A wildcard ARN (`...config-*`) cannot be settled by one `describe`; the empty enumeration is
what makes it an absence.

## 2. TARGETS 1 AND 2 -- `opal-smartx-lambda-role`, both DELETE, for different reasons

**Target 1, `opal-smartx-s3-access`:** one statement, `s3:GetObject`+`s3:ListBucket` over four resources
that are two buckets and their key patterns. **Both buckets read 404.** Every resource dead -> the
statement goes -> the policy has no other statement -> **DELETE the policy.**

**THIS IS THE ONE TARGET WHERE THE CELL'S STATED HAZARD IS REAL.** An S3 bucket name is GLOBAL: while this
Allow exists, anyone who creates `opal-data-smartx` or `opal-code-smartx` in any account receives
`GetObject`/`ListBucket` from this role. Closing it is a genuine narrowing.

**Target 2, `opal-smartx-secrets`:** one statement, `secretsmanager:GetSecretValue` on
`arn:aws:secretsmanager:us-east-2:...:secret:opal/smartx/config-*`. Dead in its own region, and us-east-2
holds **0 secrets at all**. Removable -> **DELETE the policy.**

**BUT THE DIAGNOSIS IS WRONG-REGION, NOT DELETED.** The positive control found the secret alive in
**us-east-1** (`...config-IKCzE6`). So this grant never worked as written; it is not the residue of a
deleted secret. **And a Secrets Manager ARN is scoped to one account and one region -- no third party can
create that name in our us-east-2 -- so there is NO squatting hazard to close.** Removing it is tidiness,
not risk reduction, and if anything ever needed this role to read that secret the correct act is a
REPOINT, not a delete.

**Both policies sit on a role Z-S24 established is an ORPHAN no Lambda assumes** (served graph LAMBDA=0
against a positive control reading LAMBDA=1; `RoleLastUsed` 2025-12-30). So nothing is using either grant,
which is why DELETE is safe here even though target 2's rationale is weak.

## 3. TARGET 3 -- ZERO REMOVALS, AND THE HAZARD IS THE ONE THE RULE CANNOT REACH

`CodeBuildSemanticClusteringPolicy` on `codebuild-semantic-clustering-role` (news-pipeline), **4
statements**, read live:

| Sid | resources | live | removable? |
|---|---|---|---|
| `CloudWatchLogs` | `log-group:/aws/codebuild/*` | wildcard, names no single object | no |
| `ECRAccess` | `*` | wildcard | no |
| `LambdaUpdate` | `function:news-semantic-clustering` | **FOUND** | no |
| `S3Access` | `opal-data-news-v2/*` **FOUND**, `codebuild-semantic-clustering-artifacts/*` **404** | mixed | **NO** |

**The only dead ARN in this policy shares statement `S3Access` with a LIVE bucket.** The rule removes a
statement only if EVERY resource it names is dead, so `S3Access` stays, and **this policy yields zero
removals.** Verdict `NO-CHANGE`.

**AND THIS IS EXACTLY WHERE THE STATED HAZARD BITES.**
`codebuild-semantic-clustering-artifacts` is an S3 bucket -- a GLOBAL name -- and the live
`s3:GetObject`/`s3:PutObject` Allow on `.../*` means whoever creates that bucket name gets read AND WRITE
from a role that is **in active use** (`RoleLastUsed` 2026-09-11) and that can also
`lambda:UpdateFunctionCode` on a live function. So the cell's own WHY applies most sharply to the one
target its rule cannot act on.

**WHAT I AM NOT DOING, and why.** Narrowing a Resource LIST inside a live statement is a different act
from removing a dead statement: it edits a grant that is partly in use, and the cell's rule, BOUNDS and
pair language are all written around whole statements ("Every other statement stays byte-identical").
Proposing it here as my own decision would widen the cell. **Referred to the issuer with the evidence,
and a row filed.** If the issuer wants it, the mechanical shape is a one-element edit to `S3Access`'s
`Resource` list, which the as-live declaration in `zz_narrow_z_s32.tf.proposed` makes a two-line diff.

## 4. TARGET 4 (A2-r7) -- removable by the rule, and referred anyway

`DynamoDBAccess` on `sentiment_query_api-role` (market-overview), one statement,
`dynamodb:Query`/`GetItem`/`Scan` on `arn:aws:dynamodb:us-east-2:...:table/opal-news-articles`.
us-east-2 read: **ResourceNotFoundException**, and us-east-2 holds **0 tables**. So by the rule: removable,
whole policy, DELETE.

**THREE REASONS IT IS REFERRED RATHER THAN PROPOSED FOR DELETION:**

1. **The table EXISTS in us-east-1** (positive control, same call: FOUND; `list-tables` us-east-1 shows
   `opal-news-articles` among 46). So this is a WRONG-REGION ARN, not a dead resource -- the same shape as
   target 2.
2. **No squatting hazard.** A DynamoDB table ARN is scoped to one account and one region. Nobody else can
   create `opal-news-articles` in our us-east-2. The cell's S3-global WHY does not transfer.
3. **It is this role's ONLY data grant.** The role's other policy is the AWS-managed
   `AWSLambdaBasicExecutionRole` (logs). Its consumer Lambda `sentiment_query_api` is LIVE and fronted by
   a live API Gateway route, and the role's last use was `2026-01-02` **in us-east-2**. So the picture is a
   deployment that once ran in us-east-2 against a table that now lives in us-east-1: the grant is
   already broken in practice, and **deleting it makes that permanent instead of repairing it.**

**DELETE vs REPOINT (us-east-2 -> us-east-1) is a product decision** about whether that API is meant to
work, and it belongs to the issuer and the module's owner, not to an IAM-hygiene cell. Row filed.

## 5. THE AS-LIVE DECLARATIONS, AND THE PLAN THAT PROVES THEM

Each target policy is declared as its own `aws_iam_role_policy` with an `import` block, **as live**. The
role blocks are untouched and still set neither `inline_policy` nor `managed_policy_arns` (the omission
rule); an inline policy is managed only as its own resource.

```
PLAN: infra/aws/terraform/smartx-pipeline: Plan: 2 to import, 0 to add, 0 to change, 0 to destroy.
PLAN: infra/aws/terraform/news-pipeline:  Plan: 1 to import, 0 to add, 0 to change, 0 to destroy.
PLAN: infra/aws/terraform/market-overview: Plan: 1 to import, 0 to add, 0 to change, 0 to destroy.
```

**`0 to change` IS THE PROOF, and it is the whole point of PHASE A here:** it says each declaration matches
the live policy document exactly. A single character wrong in a policy JSON and Terraform plans a change.

> **That zero was obtained on the first attempt for a reason worth recording: the documents are GENERATED
> from `aws iam get-role-policy` output, never retyped.** A hand-typed policy document is precisely how an
> "as-live" declaration ends up planning a change nobody asked for. (A side trap met on the way: native
> Python cannot exec `.tools/aws`, which is a shell script -- `OSError [WinError 193] not a valid Win32
> application`. The documents were dumped to files by bash and the generator only reads them.)

**THE NARROWINGS AND THE PLANS THEY WOULD PRODUCE:**

- Targets 1 and 2 are DELETEs, so there is no narrowed document to diff -- the whole resource goes. Per the
  cell's instruction, the Terraform-native route is **import, then remove, as two applies under one
  ledger**: apply 1 imports the policy (the plan above, `0 to change`), then the declaration and its
  `import` block are deleted from the `.tf` and apply 2 plans `0 to add, 0 to change, 1 to destroy` for
  that address. The removal is a Terraform destroy of the `aws_iam_role_policy`, which is a
  `DeleteRolePolicy` -- not a role change, and not an `inline_policy` edit.
- Target 3 produces **no narrowing and no plan delta** under the rule.
- Target 4's narrowing, if ruled, is the same import-then-remove shape as 1 and 2.

## 6. THE NAMING DRY-GRADE -- and a NAME COLLISION the gate found that nothing else would have

Run with `python .tools/naming-gate.py --diff <staged diff>`, **without committing** (row Z-S35).

**FIRST RUN WAS VACUOUS, A THIRD DISTINCT WAY.** Staging the `.tf.proposed` files gave
`DENOMINATOR: 3 path(s)` and `NAMING-GATE: PASS 0 graded` -- and the **COVERAGE line is the tell**:

```
.tf.proposed run:  COVERAGE: 3 path(s) in the declaration domain the gate COULD NOT SEE
                             (extension outside its graded set); 0 seen        -> PASS is vacuous
.tf run:           COVERAGE: 0 path(s) ... could not see; 3 seen               -> real grading
```

**The gate counts a `.tf.proposed` path in its DENOMINATOR but does not grade that extension.** So the
dry-grade must be run on the `.tf` form. That is the third vacuity mode this project has hit, after the
empty `git add -N` diff (x-1 PHASE A) and the pure-rename diff with no added lines (x-1 PHASE B) -- and in
all three the sound habit was the same: print the diff's path/line counts and read COVERAGE *before* the
verdict.

**THE REAL VERDICT: `NAMING-GATE: REFUSE 1` over 8 graded rows (rc=1).** Seven are
`EXISTING, touched, and OUT-OF-PATTERN ... WARN`, each additionally confirmed by the gate against the live
plane as `RUNNING-LIVE ... EXISTING, not minted by this diff` (estate vintage 2026-10-11 06:13:25Z). One is
a refusal:

```
NAMING REFUSE infra/aws/terraform/smartx-pipeline:0 <hole-count-ratchet>
  the unplaceable-name list grew in smartx-pipeline: 2 HOLE line(s) now, 0 at HEAD.
  HOLE IAM_POLICY smartx-s3-access      -> also given to opal-smartx-s3-access at zz_narrow_z_s23.tf:30
  HOLE IAM_POLICY opal-smartx-s3-access -> also given to smartx-s3-access at iam.tf:36
  both canonicalise to: smartx-s3-access-policy
  Owed: one of the two names ... agree it with the owner of the older name -- from the creator
```

**MEASURED: this is a CANON collision, not a world conflict.**

| name | live on role | declared at |
|---|---|---|
| `smartx-s3-access` | **`smartx-ingestion-lambda-role`** | `smartx-pipeline/iam.tf:36` (`aws_iam_role_policy.ingestion_s3`) |
| `opal-smartx-s3-access` | **`opal-smartx-lambda-role`** | this cell's `zz_narrow_z_s23.tf:30` |

**Two different live policies, on two different roles, both real.** AWS requires an inline policy name to
be unique only *within a role*, so there is no conflict in the world -- but both names canonicalise to
`smartx-s3-access-policy`, and the canon cannot represent two same-purpose inline policies on two
different roles in one module.

**AND THE REMEDY THE GATE ASKS FOR IS ONE THIS CELL IS FORBIDDEN TO PERFORM.** Renaming a live inline
policy is a delete-and-create -- a permission move -- which x-2's BOUNDS prohibit outright ("Nothing is
added; no trust and no tag changes"; C-TWO-REMEDIES). And the older of the two names belongs to a resource
that is **not this cell's target at all**. So: referred, with the row. The refusal is on the
hole-count-ratchet limb, which the audited placement override does reach, but an override here would paper
over a canon gap rather than resolve it.

## 7. STATE OF THE WRITE SURFACE AT THE END OF PHASE A

- `infra/aws/terraform/smartx-pipeline/zz_narrow_z_s23.tf.proposed` -- committed, inert (2 policies).
- `infra/aws/terraform/news-pipeline/zz_narrow_z_s32.tf.proposed` -- committed, inert.
- `infra/aws/terraform/market-overview/zz_narrow_row14.tf.proposed` -- committed, inert.
- All three `.tf` copies used for the plans and the dry-grade are **REMOVED** and none is committed.
- No deploy-ledger entry opened. PHASE B opens `iamroles-r7-narrow-<module>`, one per module, first.
- **Nothing applied. No policy, statement, role, trust or tag touched in AWS.**

## 8. WHAT PHASE B INHERITS

1. **Three rulings are owed before any apply:** target 3 (narrow a Resource list inside a live statement,
   or accept the hazard), target 4 (delete vs repoint), and the `smartx-s3-access` canon collision.
2. **AC2 expects 3 `POST-APPLY-PLAN` lines and AC3 `closed=3`** -- one per module. On the rule as written,
   news-pipeline would have nothing to apply, so a third line could only exist if target 3 is ruled.
3. **The import-then-remove route is two applies per DELETE, under ONE ledger entry per module.**
4. **In market-overview the apply serialises behind row 14's adoption** (now landed, `526332353c`), and
   that module still wants to recreate a deleted S3 bucket -- `-target` remains load-bearing there.
5. **smartx-pipeline still carries the three Z-S21 Lambda drifts**, so `-target` is required there too.

**PHASE A ends here, per the order's step 3.**
