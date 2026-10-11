# PLAN_SURVEY -- Family C (rows 6 and 14), NFRA_IAMROLES202609.TO-IAM-x-1 PHASE A

**Cell:** IAM-x-1 (round 7, FWD-4 enrichment; the round-6 analysis calls this E1)
**Executed by:** `0.7.0_AE_CloudOps~IR` -- **owner of record:** `0.7.0_AE_CloudOps~Z`
**Authority:** `ROUND_ANALYSIS.round6.md` @`2f49aa235b` E1; `ADOPTION_PLAN_TEN.md` @`59112aafed` Family C;
**GO for PHASE A = the round-7 issuance** @`8b61ddf94f` (msg 33180)
**Issuer:** `2.0.0_SA_COO~ZI` -- **risk:** WORLD -- **PHASE A APPLIED NOTHING AND WROTE NOTHING TO AWS.**
**Measured:** 2026-10-11, worktree `C:/tmp/iam-w1b`, branch `wk-iamroles-r7-x1` @`5ce0a636f4`,
Terraform v1.15.8, provider `hashicorp/aws v5.100.0`.

---

## 0. HEADLINE -- THREE THINGS THIS SURVEY FOUND, none of them this cell's doing

1. **`shared-infra` (row 6's ruled home) CANNOT INIT OR PLAN AT ALL.** A deliberate fail-closed
   `one()` guard in `s3-lgic-firm-buckets.tf:197` has tripped. So row 6's `PLAN:` line is recorded
   BLOCKED with its cause, exactly as `bd-pipeline` was in round 6. Section 4.
2. **The homing rule for row 14 has no answer as written.** The cell says to home it "from where its
   consumers are declared"; its consumer Lambda, this role, its log group and its API Gateway route are
   **all undeclared**. A fallback ground is proposed, labelled thin, and left to the issuer. Section 3.
3. **`market-overview` (row 14's PROPOSED home) is NOT at zero drift** -- its negative control reads
   `4 to add`, and the adds would **recreate a deleted S3 bucket** and its three sub-resources. That is
   materially worse than round 6's `smartx-pipeline` drift and it makes `-target` load-bearing, not
   belt-and-braces. Section 5.

Row 6's own naming verdict is CLEAN (`NO-SYSTEM-ASKED`, no override owed). Row 14's is not. Section 6.

## 1. THE FIVE REQUIRED LINES, PER MODULE

```
PLAN: infra/aws/terraform/shared-infra: BLOCKED -- the module cannot init or plan at HEAD. `terraform init` and `plan` both exit with "Error: Invalid function argument ... while calling one(list) ... must be a list, set, or tuple value with either zero or one elements" at s3-lgic-firm-buckets.tf line 197 (NOT in this cell's file). See section 4.
DEFAULT_TAGS: infra/aws/terraform/shared-infra: ['Environment', 'ManagedBy', 'Project', 'System']
AUTH_KEY_COLLISION: infra/aws/terraform/shared-infra:   *** KEY COLLISION: ['Project', 'System'] are BOTH default_tags keys AND authorization keys.
STATE_KEY: infra/aws/terraform/shared-infra: shared-infra/tfstate
NAMING: infra/aws/terraform/shared-infra: NAMING NO-SYSTEM-ASKED .../zz_adopt_family_c_row6.tf:60 lambda-ec2-runtime-monitor-role -> lambda-ec2-runtime-monitor-role -- "NO-SYSTEM-ASKED as IAM_ROLE: no system is asked of this kind of name" (and the same at :111); counts-as PASS, no override owed

PLAN: infra/aws/terraform/market-overview: Plan: 1 to import, 0 to add, 1 to change, 0 to destroy.
DEFAULT_TAGS: infra/aws/terraform/market-overview: ['Environment', 'ManagedBy', 'Project', 'System']
AUTH_KEY_COLLISION: infra/aws/terraform/market-overview:   *** KEY COLLISION: ['Project', 'System'] are BOTH default_tags keys AND authorization keys.
STATE_KEY: infra/aws/terraform/market-overview: market-overview/tfstate
NAMING: infra/aws/terraform/market-overview: NAMING-PLACE: REFUSE 1 -- "the unplaceable-name list grew in infra/aws/terraform/market-overview: 3 HOLE line(s) now, 2 at HEAD. New: HOLE IAM_ROLE sentiment_query_api-role -> R1.f: 'sentiment' is in no vocabulary; no registry row resolves it ... Owed: a vocabulary row or an event_rules.json row for the word or token the grader names (infra/logic/registry/) -- from 4.0.0_SA_CRO"; plus NAMING RAISE-EXISTING at :69 (WARN, the literal is already carried at HEAD so the copy mints nothing)
```

Both `STATE_KEY`s read from each module's own `backend "s3"` block, bucket
`opal-313476888478-terraform-state`, region `us-east-1`. Both `DEFAULT_TAGS` sets are four keys; the
VALUES differ -- `System = SharedInfra` versus `System = MarketOverview`. Both `AUTH_KEY_COLLISION`
lines are `comp-tagauthz`'s verbatim, including leading spaces.

> **A NOTE ON `shared-infra`'s PROVIDERS that the `DEFAULT_TAGS` line above does not carry.** This
> module declares **TWO** aws providers: the default one with those four keys, and an **ALIASED** one,
> `untagged`, which sets **no `default_tags` at all**. Row 6's declaration names no provider, so it
> takes the default and therefore the four tags. This is the first module in the adoption program with
> an aliased untagged provider, and a reader who checks only "the provider block" could read four tags
> for a resource that would in fact get none. The pair should bind the plan's own `tags_all` delta, not
> the provider block -- and for row 6 that delta is currently unobtainable (section 4).

## 2. THE TWO ROLES' LIVE STATE

Read at 2026-10-11 at write time. **Both roles have ZERO tags, NO description, and -- unusually for this
program -- BOTH carry an attached managed policy.**

| attribute | `lambda-ec2-runtime-monitor-role` (row 6) | `sentiment_query_api-role` (row 14) |
|---|---|---|
| tags | **0** | **0** |
| path | `/` | `/` |
| description | **ABSENT** | **ABSENT** |
| max_session_duration | `3600` | `3600` |
| assume_role_policy principal | `lambda.amazonaws.com` | `lambda.amazonaws.com` |
| inline policies | 1 -- `EC2RuntimeMonitorPolicy` | 1 -- `DynamoDBAccess` |
| **attached managed policies** | **1 -- `AWSLambdaBasicExecutionRole`** | **1 -- `AWSLambdaBasicExecutionRole`** |
| permissions boundary | none | none |
| created | `2026-02-06T15:50:31Z` | `2025-11-24T20:33:48Z` |
| RoleLastUsed | **`2026-10-11T04:36:29Z`, us-east-1 -- IN USE, minutes before this write** | `2026-01-02T17:29:32Z`, **us-east-2** |

**THE OMISSION RULE PROTECTS A MANAGED ATTACHMENT ON BOTH ROLES.** Round 6's row 11 was the first such
case; here both of them are. Setting `managed_policy_arns` -- **even to `[]`, which reads like "no
opinion"** -- makes it authoritative and detaches `AWSLambdaBasicExecutionRole`, the grant that gives
each role its CloudWatch Logs access. Both declarations omit it, and `description` too, since neither
live role has one.

**ROW 6 IS ACTIVELY RUNNING.** `RoleLastUsed` read `2026-10-11T04:36:29Z` -- minutes before this file
was written. Its trust principal is therefore not a theoretical stop condition: a wrong principal
changes WHO MAY ASSUME a role something is assuming right now, and the plan SUMMARY would still read as
one import. The principal was read live and carried, never copied from a sibling.

**OBSERVATION on row 14, recorded and not acted on:** its last use was in **us-east-2**, while its
consumer Lambda, log group and API route all live in **us-east-1** (served graph, vintage 2026-10-11
04:06:44Z). An IAM role is global, so a us-east-2 assumption is not itself a defect, and this cell
moves custody only. It is here because a reader homing this role by REGION would reach a different
answer than one homing it by CONSUMER.

## 3. ROW 14'S HOME -- the rule the cell gives has no answer, and this is the fallback

**THE RULE AS WRITTEN:** "the module YOU name in the survey, from where its consumers are declared."

**ITS CONSUMERS ARE DECLARED NOWHERE. Measured on two independent planes:**

| plane | reading |
|---|---|
| served AWS graph (`comp-find --corpus aws`, vintage 2026-10-11 04:06:44Z, 2894 nodes) | 5 hits for `sentiment_query_api`: the LAMBDA, this IAM_ROLE, its LOG_GROUP and its API_ROUTE all read **`drift=LIVE-no-DECLARED`**; only the inline IAM_POLICY reads DECLARED |
| repo content census over `infra/aws/terraform` (836 files scanned) | **8 hits in 2 files, both TEST fixtures** under `nfra-ctlpln-identity/tests/`. **ZERO `.tf` declarations.** |

A wider census (7897 files) finds it 44 times -- in the Lambda source map, `manifests/`, and
`nfra_terraform_p1` gap-analysis JSONs. All of those RECORD it; none DECLARES it.

**THE FALLBACK GROUND, and it is thin.** With no declared consumer, the next available signal is the
role's FAMILY. `infra/aws/manifests/lambda/opal-portal-functions.yaml` puts `sentiment_query_api` in the
`portal_api` group with exactly two siblings:

```
    portal_api:
      - opal-portal-data-proxy
      - opal-smartx-query
      - sentiment_query_api
```

Of those two siblings, **exactly one is declared in Terraform**: `opal-portal-data-proxy`, as
`resource "aws_lambda_function" "portal_data_proxy"` in `market-overview/lambdas.tf:89-90`.
`opal-smartx-query` is declared nowhere. So `market-overview` is the only module reachable by evidence.

**THE ALTERNATIVE I REJECTED, with its reason.** `shared-infra/apigateway-portal/` fronts the portal
API and is where an API-route home would sit. It is rejected because its own file says the integration
is not managed there: `integrations.tf:41` reads
`# NOTE: integration s7ntfz4 (opal-portal-data-proxy) NOT TF-managed.` Homing a role in a module that
explicitly disclaims managing its consumer's integration would be worse than thin.

> **DECLARATION-VS-REFERENCE, because this is where the answer could easily have been wrong.** A content
> census for the two siblings returns 14 files across the terraform tree, and most are API-Gateway
> integrations that NAME a Lambda rather than declare it. The distinction is carried by the lines
> PRECEDING the literal -- the `resource "aws_lambda_function"` block header -- which a content grade
> does not show. I read those preceding lines deliberately (an audited `# rail-checked:` grep, since
> comp-find grades content but cannot show a block header) and that is what separated the one real
> declaration from thirteen references.

**MY RECOMMENDATION, and its weight.** Propose `market-overview`; treat it as THIN. Two facts argue
against it and belong in the issuer's decision: (a) the module is **not at zero drift** -- it wants to
recreate a deleted S3 bucket (section 5); and (b) homing row 14 there is what grows that module's
unplaceable-name count and produces its naming REFUSE (section 6), so the home choice determines which
module takes that ratchet hit. **The module is the issuer's call. The cell already says PHASE B waits on
an amendment that admits it, and nothing here presumes that amendment.**

## 4. WHY `shared-infra` CANNOT PLAN -- a fail-closed guard that tripped, measured with two controls

`terraform init` AND `plan` both fail in `shared-infra` before producing anything:

```
Error: Invalid function argument
  on s3-lgic-firm-buckets.tf line 197, in locals:
 197:   lgic_crm_scope  = one([for k, s in local.lgic_managed_firm_buckets : s if length(lookup(s, "masters", [])) > 0])
    | while calling one(list)
    | local.lgic_managed_firm_buckets is object with 2 attributes
Invalid value for "list" parameter: must be a list, set, or tuple value with either zero or one elements.
```

**TWO CONTROLS, because two different things could produce this reading:**

1. **NEGATIVE** -- with `zz_adopt_family_c_row6.tf` MOVED OUT and nothing else changed, `init` emits the
   **same 1 Error at the same line**. This cell's file is not implicated.
2. **CHECKOUT** -- the same error reproduces in the **SHARED tree's full checkout**, not only in my
   sparse worktree. So the finding is about the repository, not my working copy. (This control exists
   because in round 6 an earlier sparse cone genuinely did produce a module-level error of its own.)

**THIS IS NOT AN OVERSIGHT. THE GUARD IS DOING EXACTLY WHAT ITS AUTHOR WROTE IT TO DO**, and the file
says so in a comment above the line:

> "the firm row is selected from the registry data this file already reads, as the ONE managed FIRM row
> that carries masters ... today exactly the firm whose bucket these statements land on; **one() fails
> the plan closed if that ever stops being a single row.**"

So the premise "exactly one managed FIRM row carries `masters`" has become false, and `one()` failed
closed as designed. What is missing is a DISPOSITION now that the premise is false -- not a bug fix.

**THE CAUSE, measured from the registry rather than inferred.** `local.lgic_managed_firm_buckets` selects
`class == "FIRM"` rows whose bucket this file manages. Of `infra/logic/registry/scopes.json`'s 14 scope
rows, 4 are FIRM-class and **2 are in that managed set**:

| FIRM row | `bucket_managed_by` | in managed set | `masters` |
|---|---|---|---|
| 49financial | `''` (provisioned) | **no** | `["08242234","08335338"]` |
| inflection | `s3-lgic-firm-buckets.tf` | **yes** | `["4698"]` |
| cottonwood | `s3-lgic-firm-buckets.tf` | **yes** | `["z09"]` |
| demo | `''` (provisioned) | no | none |

**Both members of the managed set now carry `masters`, so `one()` receives 2.**

> **THE TRAP, and it would catch a reader going fast:** THREE firm rows carry `masters`, and the most
> prominent of them -- `49financial`, with two master accounts -- is **NOT in the managed set at all**.
> Counting "firms with masters" gives 3 and names the wrong culprit. The membership rule, not the
> `masters` field, is what selects.

**WHEN IT TIPPED, measured at both pins rather than from commit dates:**

| at | managed rows with `masters` | `one()` receives | verdict |
|---|---|---|---|
| `8e58736597` (2026-10-07, the commit that WROTE the `one()` selector) | `['cottonwood']` | 1 | **PASSES** |
| `5f962296ae` (2026-10-09) | `['inflection','cottonwood']` | 2 | **FAILS CLOSED** |

So the guard was correct for two days and `5f962296ae` tipped it --
`registry(IRPT_DASHBD, 0.9.0_WK_IRPT_DASHBD~52): MASTER 4698 -> inflection / orion in scopes.json`.

**WHO OWNS IT, and it is not this lane.** The guard belongs to `ADVI_COTBKF` cell CB-d-4
(`8e58736597`, worker `0.9.0_WK_ADVI_COTBKF~15`); the registry row that tipped it belongs to
`IRPT_DASHBD` (`5f962296ae`, worker `0.9.0_WK_IRPT_DASHBD~52`); and `scopes.json` itself is the CRO's
carrier (`de56cfd02f` is `4.0.0_SA_CRO`'s, and the naming gate attributes registry rows "from
`4.0.0_SA_CRO`"). All three workers are unmessageable; their COOs own the routing. **Cross-project, and
not an AE's to adjudicate.**

**I PROPOSE NO FIX, deliberately.** The candidates differ in MEANING, not in syntax: widening `one()` to
`[0]`/`sort(...)` silently PICKS one firm's bucket for a CRM prefix that currently names
`commonwealth/${long}/bronze/crm/` -- i.e. it would quietly scope a restricted CRM policy to one of two
firms. Which firm (or whether the policy should now be per-firm `for_each`) is a client-data scoping
decision belonging to the owners above, and `NEVER` bars referencing another firm's data from a pipeline
tree. Filed as a surprise row.

**WHAT IT BLOCKS, precisely:** row 6's `PLAN:` line, and therefore the never-widen pair for row 6's
PHASE B. It does **not** block row 6's declaration, its live reads, its naming verdict (section 6), its
`DEFAULT_TAGS`, `STATE_KEY` or `AUTH_KEY_COLLISION`, all of which are delivered above.

## 5. WHAT IS MINE AND WHAT IS NOT -- and `market-overview` is NOT at zero drift

**NEGATIVE CONTROL, `market-overview`,** with `zz_adopt_family_c_row14.tf` moved out:

```
Plan: 4 to add, 0 to change, 0 to destroy.
  # aws_s3_bucket.market_data_v2 has been deleted
  # aws_s3_bucket.market_data_v2 will be created
  # aws_s3_bucket_public_access_block.market_data_v2 will be created
  # aws_s3_bucket_server_side_encryption_configuration.market_data_v2 will be created
  # aws_s3_bucket_versioning.market_data_v2 will be created
```

**An S3 bucket this module manages has been DELETED out of band, and an unscoped apply here would
RECREATE it plus its three sub-resources.** That is a heavier pre-existing drift than round 6's
`smartx-pipeline` (three in-place Lambda version bumps, row `Z-S21`): a bucket creation is a new
world object, and `market_data_v2` is a DATA bucket. **So `-target` scoping in PHASE B is load-bearing
here, not belt-and-braces as it was in round 6's clean modules.** Not this cell's to repair, and
recorded so a scoped pass cannot hide it. Filed as a surprise row.

**THE ROW-14 PLAN, GRADED PER ATTRIBUTE** from `show -json` on the saved plan -- never from the summary,
which at `1 import / 0 add / 1 change / 0 destroy` is exactly what a trust-policy rewrite would print:

| graded property | measured |
|---|---|
| `resource_changes` total | 1 |
| non-no-op | 1 -- `aws_iam_role.sentiment_query_api_role`, `['update']`, importing `sentiment_query_api-role` |
| attributes that differ | **1** (`tags_all`) |
| `tags_all` delta | `{}` -> `Environment=Production, ManagedBy=Terraform, Project=OpalPortal, System=MarketOverview` (4 keys) |
| `assume_role_policy` / `inline_policy` / `description` | unchanged |
| **`managed_policy_arns`** | **unchanged** -- `["arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"]` identical before and after |
| destroys | 0 |

Row 6's equivalent grading is **unobtainable** until section 4's blocker clears.

## 6. THE NAMING DRY-GRADE -- run WITHOUT committing, per row Z-S35

Graded with `python .tools/naming-gate.py --diff <staged diff>`, which is the safe probe row `Z-S35`
asked for and the cell now mandates. **The two names came out completely differently.**

> **AND THE FIRST ATTEMPT AT THIS PROBE WAS ITSELF A VACUOUS PASS, which is worth recording.** I first
> staged with `git add -N` (intent-to-add) and took `git diff --cached`; that produced a **0-byte, 0-path
> diff**, and the gate duly reported `NAMING-GATE: PASS 0 graded`. A pass over an empty denominator.
> My redirect had also succeeded, so the `||` fallback in my own command never fired -- the zero was my
> instrument, not the world. Re-staged properly (`git add`), confirmed the diff at **12007 bytes / 2
> files / 7 added lines carrying a role name** BEFORE reading the verdict, and only then graded.

```
ROW 6  -- shared-infra/zz_adopt_family_c_row6.tf:60 and :111
  NAMING NO-SYSTEM-ASKED  lambda-ec2-runtime-monitor-role -> lambda-ec2-runtime-monitor-role
  why: "NO-SYSTEM-ASKED as IAM_ROLE: no system is asked of this kind of name"
  => counts-as PASS. The canonical form EQUALS the live name. NO override is owed, and PHASE B needs
     neither a placement override nor an R20 entry for this name. The cleanest naming result of the
     whole adoption program.

ROW 14 -- market-overview/zz_adopt_family_c_row14.tf, TWO rows:
  NAMING REFUSE  <hole-count-ratchet>  (counts under NAMING-PLACE: REFUSE 1)
  why: "the unplaceable-name list grew in infra/aws/terraform/market-overview: 3 HOLE line(s) now,
        2 at HEAD. New: HOLE IAM_ROLE sentiment_query_api-role -> R1.f: 'sentiment' is in no
        vocabulary; no registry row resolves it [...:68] Owed: a vocabulary row or an
        event_rules.json row for the word or token the grader names (infra/logic/registry/)
        -- from 4.0.0_SA_CRO"
  NAMING RAISE-EXISTING  at :69  -> (pre-LGIC key; conformance via its migration project, Rule 30)
  why: "RAISE as IAM_ROLE: ... 'sentiment' is in no vocabulary ...; the same literal is already
        carried at HEAD in infra/aws/nfra_terraform_p1/consolidated_gaps.json, so this copy mints
        nothing: WARN"

NAMING-PLACE: REFUSE 1      NAMING-GATE: REFUSE 4 graded      rc=1
```

**READING THE ROW-14 REFUSAL PRECISELY, because its limb determines PHASE B's route.** It is the
**hole-count ratchet**, which counts as `PLACE-REFUSE` -- so it IS on the limb the audited placement
override reaches, unlike round 6's `bd` carrier refusal (`Z-S34`), which was not and needed an R20
entry. **But the remedy the gate itself names is cleaner than an override:** a vocabulary or
`event_rules.json` row under `infra/logic/registry/` for the token `sentiment`, attributed **from
`4.0.0_SA_CRO`**. That is one registry row, owned by the CRO, and it would retire the HOLE rather than
paper over it.

Note also that the **ratchet is MODULE-SCOPED** -- it fires because *this module's* unplaceable count
grew from 2 to 3. So the homing decision in section 3 determines which module takes the hit, which is a
further reason the home is the issuer's call.

**I did not commit, and I did not override anything.** The cell says to write a refusal in the survey
and STOP before any import if it is on a limb the override cannot reach; this one can be reached, and
PHASE B is not mine to start regardless.

## 7. STATE OF THE WRITE SURFACE AT THE END OF PHASE A

- `infra/aws/terraform/shared-infra/zz_adopt_family_c_row6.tf.proposed` -- committed, **inert**.
- `.../deliverables/0.7.0_AE_CloudOps~IR/round7/zz_adopt_family_c_row14.tf.draft` -- committed, **a
  draft in the deliverables directory**, because row 14's module is not in this order's `<paths>` until
  the issuer amends it in. It is not in any module.
- Both carry one `aws_iam_role` + one `import` block, with `inline_policy`, `managed_policy_arns` and
  `description` all ABSENT. AC1's shape over both files reads **0**.
- **Labels fully namespaced and the collision question measured:** `lambda_ec2_runtime_monitor_role` and
  `sentiment_query_api_role` match **0** of the 270 `aws_iam_role` declarations across 836 files
  scanned under `infra/aws/terraform`.
- **Neither role is declared in Terraform at the cut**, consistent with the issuance's own preflight.
- Both `.tf` copies -- `shared-infra/zz_adopt_family_c_row6.tf` and
  `market-overview/zz_adopt_family_c_row14.tf` -- are **REMOVED**. They existed only for the plan runs
  and the naming dry-grade, and neither is committed. `market-overview/.terraform.lock.hcl`, which
  `init` touched, is restored rather than committed: it is not in this order's `<paths>`.
- No deploy-ledger entry opened. PHASE B opens `iamroles-r7-family-c-<module>`, one per module, first.
- **Nothing applied. No tag, policy, trust relationship, role, bucket or Lambda touched.**

## 8. WHAT PHASE B INHERITS

1. **Row 6 waits on the `shared-infra` blocker** (section 4), which is cross-project and whose remedy is
   a client-data scoping decision, not a syntax fix. Until the module plans there is no plan for its
   pair to sign.
2. **Row 14 waits on TWO things:** the amendment that admits its module (the cell says so), and the home
   decision itself, which section 3 shows the given rule cannot settle.
3. **Row 6's name needs nothing** -- `NO-SYSTEM-ASKED`, no override, no registry row. **Row 14's name
   needs one registry row from `4.0.0_SA_CRO`** for the token `sentiment`, or failing that the audited
   placement override, which its limb does admit.
4. **`-target` is load-bearing in `market-overview`**, which wants to recreate a deleted S3 bucket and
   its three sub-resources. An unscoped apply there is NOT a tagging act.
5. **Row 6's trust is a live stop condition.** The role was assumed minutes before this survey was
   written; verify its principal LIVE after any apply, not from terraform's output.
6. **The omission rule guards a managed attachment on BOTH roles.** After each apply,
   `list-attached-role-policies` must still read 1 and name `AWSLambdaBasicExecutionRole`.

**PHASE A ends here, per the order's step 3.**
