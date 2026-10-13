# NEVER-WIDEN ASK -- NFRA_MCPORTAL.TO-MP-z-4

**Asked by:** `0.7.0_AE_CloudOps~MQ`
**Pair asked:** `1.0.0_SA_CTO~Z` (CTO half) and `2.0.0_SA_COO~MP` (COO half). Both halves are required
before the apply; a refused half STOPS the act.
**Cell:** `MP-z-4`, workstream GW round 1 (PRD v0.7 FWD-20).
**Act:** create ONE new inline IAM role policy on the existing gateway instance role
`opal-gateway-role`, granting ONE action, `dynamodb:Scan`, on ONE resource, the
`gateway-access-state-table` table ARN.
**Risk class:** `WORLD` (the order's own `<risk>` tag). EGRESS CLASS: AWS IAM write on
`opal-gateway-role`, one inline policy, by `safe-apply`.
**Branch / tree:** `wk-mp-z-4`, a linked sparse worktree cut from `box/sitez` HEAD `6fe140d0a8`.

---

## 1. BLAST RADIUS

### 1.1 What the act may touch

| plane | the write set, exactly |
|---|---|
| AWS | ONE new inline role policy `gateway-access-state-principal-scan-policy` on role `opal-gateway-role`. Nothing else is created, changed or destroyed -- the plan reads `1 to add, 0 to change, 0 to destroy` under a `-target` of that one resource. |
| Terraform state | ONE new resource address `aws_iam_role_policy.gw_access_state_principal_scan` in `opal-gateway/tfstate`. No existing address moves. |
| repo | the paths in section 3 of the task order, and no others. |

### 1.2 What it widens, stated plainly

`dynamodb:Scan` **cannot be bound by a key condition** -- `dynamodb:LeadingKeys` is not evaluated for
Scan -- so this grant lets `opal-gateway-role` **ENUMERATE every row of `gateway-access-state-table`**.

That enumeration is the whole of the widening, and it is a **LIST** delta, not a **READ** delta:

- Every item in that table is **already readable one at a time** by this role. Its existing
  `AccessStateStrongRead` statement (`schwab_access_state.tf`, `aws_iam_role_policy.gw_access_state_runtime`)
  grants `dynamodb:GetItem` on the whole table ARN with no condition -- `POLICY#` and `RUNTIME#` alike.
- The `RUNTIME#` items are the role's own writes.
- So the role gains the ability to **discover keys it would otherwise have to already know**. It gains no
  reach over any individual item it could not already fetch.

The handler that consumes it (a separate cell, not this one) Scans with a `pk`/`sk` projection and keeps
only `POLICY#<tid>#<oid>` / `principal_profile` keys. That projection is a property of the handler, not of
this grant: **the grant itself is unprojected**, and any future caller using this role may Scan the whole
table. The pair is signing the unprojected grant, not the handler's narrowing.

### 1.3 Who writes what this Scan will enumerate -- this act adds no writer

Counted from the Terraform at HEAD; **3 writers** of the table, and this act moves none of them:

1. `opal-gateway-role` -- `PutItem`/`UpdateItem`/`DeleteItem` **conditioned on `RUNTIME#*` leading keys only**
   (`schwab_access_state.tf`, `AccessStateRuntimeWritesRuntimeKeysOnly`). Unchanged by this act.
2. `opal-gateway-access-admin` (the operator role, `ops/schwab_entitlement_admin.py`) -- `GetItem`, plus
   `PutItem`/`UpdateItem` on `POLICY#*` leading keys. Its trust policy still refuses the gateway role by ARN
   (`ArnNotEquals aws:PrincipalArn`). Unchanged by this act.
3. `mcportal-grant-writer-role` (the grant-writer Lambda) -- `GetItem`, plus `PutItem`/`UpdateItem` on
   `POLICY#*` leading keys, no `DeleteItem`. Unchanged by this act.

`opal-gateway-role` holds **no `POLICY#` write path before this act and none after it.** This grant is
read-side only.

### 1.4 What it may NEVER touch

The statement is a single `Allow` of a single action on a single resource. It therefore grants, and the pair
is asked to hold it to, **none** of the following:

- **No write of any kind** -- no `PutItem`, `UpdateItem`, `BatchWriteItem`, `PartiQL*`, `ImportTable`,
  `RestoreTable*` or any table-admin action.
- **No `DeleteItem`**, anywhere, on any key prefix.
- **No other table.** `mcportal-grant-changes-table` keeps its own separate, pre-existing grant
  (`mcportal_grant_writer.tf`, `aws_iam_role_policy.gw_read_mcportal_grant_changes`) and is not edited here.
  No third table is named.
- **No index.** No index ARN appears in the statement. The table has no secondary index today, and because
  a DynamoDB index ARN is a distinct resource (`.../table/<name>/index/<idx>`) that this `Resource` list does
  not match, **a future index would not be reachable through this statement** -- adding one would want its
  own grant and its own sign-off.
- **No `Query`.** Only `Scan`.
- **No change to the role's existing grants.** `AccessStateStrongRead` and
  `AccessStateRuntimeWritesRuntimeKeysOnly` are untouched; this is an additive file, not an edit.
- **Nothing outside DynamoDB**, and nothing on any other principal.

### 1.5 ROLLBACK

Per key, the write set is one inline policy, so the rollback is one call:

```
aws iam delete-role-policy --role-name opal-gateway-role \
  --policy-name gateway-access-state-principal-scan-policy
```

or, from `infra/aws/terraform/opal-gateway/`, a targeted destroy of
`aws_iam_role_policy.gw_access_state_principal_scan`.

Either leaves every other gateway grant exactly as it is now, because the grant lives in its **own separate
file** (`access_state_principal_scan.tf`) and is not folded into `schwab_access_state.tf`. Retiring the FWD-20
principal list is deleting that file. **No data is written by this act, so the rollback loses nothing** --
there is no state to restore, only a permission to remove.

---

## 2. THE POLICY DOCUMENT AS PLANNED, AND THE PLAN COUNTS

### 2.1 Plan counts

```
Plan: 1 to add, 0 to change, 0 to destroy.
```

Run from the worktree root, targeted to the one resource:

```
terraform -chdir=infra/aws/terraform/opal-gateway plan -input=false -lock-timeout=180s \
  -var market_update_s3_root=s3://opal-data-transcripts/sharepoint/transcripts/bronze/market_update/ \
  -target=aws_iam_role_policy.gw_access_state_principal_scan \
  -out=.build/z4.tfplan
```

rc=0. Refreshed `aws_dynamodb_table.access_state_new` and `aws_iam_role.gw` only. The saved plan file
`.build/z4.tfplan` is what the apply will consume, so the apply executes exactly these actions.

Two mechanical notes on that invocation, both measured, neither a change of scope:

- **`safe-apply` refuses a `plan`.** The task order says "run the plan with `safe-apply`". Measured:
  `.tools/safe-apply.sh -chdir=... plan -target=...` exits **rc=2** with
  `safe-apply: ERROR -- no 'apply' subcommand in the arguments. ... For 'plan' or any other subcommand call
  the terraform binary directly.` The wrapper gates `apply` only, by design (its own header). The plan was
  therefore run with the terraform binary directly, as the wrapper instructs. **The APPLY will go through
  `safe-apply`**, which is the gated step the rule exists for.
- **`-var market_update_s3_root=...`** is required because the root module declares it with no default and
  Terraform requires every root variable even under `-target`. The value is **builder output, never typed**:
  `lib/opal_naming.py address('sharepoint','transcripts','bronze','market_update','date=X')` =
  `s3://opal-data-transcripts/sharepoint/transcripts/bronze/market_update/date=X`, with the trailing
  `date=X` removed exactly as `variables.tf:5` specifies. It feeds an unrelated, untargeted resource.

### 2.2 The policy document as planned (verbatim from the plan output)

```
# aws_iam_role_policy.gw_access_state_principal_scan will be created
+ resource "aws_iam_role_policy" "gw_access_state_principal_scan" {
    + id          = (known after apply)
    + name        = "gateway-access-state-principal-scan-policy"
    + name_prefix = (known after apply)
    + policy      = jsonencode(
          {
            + Statement = [
                + {
                    + Action   = [
                        + "dynamodb:Scan",
                      ]
                    + Effect   = "Allow"
                    + Resource = [
                        + "arn:aws:dynamodb:us-east-1:313476888478:table/gateway-access-state-table",
                      ]
                    + Sid      = "AccessStatePrincipalScanOnly"
                  },
              ]
            + Version   = "2012-10-17"
          }
      )
    + role        = "opal-gateway-role"
  }
```

One statement. One action. One resource. No `Condition`, no `NotAction`, no `NotResource`, no second
statement, no index ARN.

### 2.3 The name is builder output, not typed

`lib/opal_naming.py name('gateway', None, 'access-state-principal-scan', 'policy')` =
`'gateway-access-state-principal-scan-policy'` -- run in this worktree, and the literal in the `.tf` is that
string byte-for-byte. It is a LITERAL and not a `var.name` interpolation for the reason recorded in
surprise row `NFRA_MCPORTAL-Z-S21`: the commit-time naming limb grades a new resource name's own bytes and
cannot resolve `var.name`. The naming gate did **not** refuse.

### 2.4 Formatting

`terraform fmt -check -write=false access_state_principal_scan.tf` -> **rc=0**, no output. Read-only form
(`-check`, not `-diff`): the file was not rewritten, so nothing but my own lines is in the diff.

---

## 3. THE `comp-iam gaps` LINE

Two runs, because the corpus differs and saying so is the point:

- **Worktree (contains the new file), narrowed corpus:** `scanned 3 trees (50 .tf files)` --
  `Total: 0 missing | 0 deny-present | 0 coverage-unknown | 0 resource-mismatch across 0 service(s)`, rc=0.
  **This number is NOT the estate's.** The sparse cone holds only `infra/aws/terraform/opal-gateway/` and
  `.../modules/`, so 50 of 571 `.tf` files were parsed. A zero over 50 files is a zero over 50 files.
- **Shared tree at `box/sitez` HEAD (does NOT contain the new file), full corpus:**
  `scanned 3 trees (571 .tf files)`, 222 IAM roles parsed (`comp-iam stats`) --
  `Total: 37 missing | 305 deny-present | 1 coverage-unknown | 3 resource-mismatch across 34 service(s)`.
  That is the **pre-existing baseline**, measured without my change; this cell adds nothing to it and
  resolves nothing in it.

`comp-iam role opal-gateway-role`, run in the worktree **with** the new file, shows `dynamodb:Scan` present
twice on the role: the pre-existing Scan on `mcportal-grant-changes-table` and the new one on
`gateway-access-state-table`.

**What comp-iam cannot tell you here, stated rather than swallowed** (its own banner, this run):
11 policy blocks `NOT ATTACHED` (a role ref the parser cannot resolve) and **7 deny statements unparsed**,
so `comp-iam` **cannot answer "is this denied?"**. It also models `(action)` and never `(action, resource)`.
It is a DESIRED-plane floor, not an oracle. **The live plane is read by AC1 after the apply** --
`get-role-policy` on the exact document plus four isolated `simulate-principal-policy` arms, one
`--resource-arns` per call.

---

## 4. THE READ-BACK I WILL RUN (AC1)

`bash org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/2.0.0_SA_COO~MP/fwd20/checks/z4.AC1.sh`, which:

1. `aws iam get-role-policy --role-name opal-gateway-role --policy-name
   gateway-access-state-principal-scan-policy --query PolicyDocument` and asserts the parsed document holds
   **exactly** `actions=dynamodb:Scan resources=1 problems=0` -- every statement `Allow`, no `NotAction` or
   `NotResource`, the action set exactly the one Scan, the resource set exactly the one table ARN.
2. Four `simulate-principal-policy` arms, **one `--resource-arns` per call, each its own invocation**
   (CLAUDE.md Rule 22a):

   | arm | expected |
   |---|---|
   | `dynamodb:Scan` on `gateway-access-state-table` | `allowed` -- the one new read |
   | `dynamodb:Scan` on `mcportal-grant-changes-table` | `allowed` -- pre-existing, unchanged (control) |
   | `dynamodb:Scan` on `opal-users-v2` | `implicitDeny` -- no other table |
   | `dynamodb:GetItem` on `gateway-access-state-table` | `allowed` -- pre-existing strong read (control) |

   PASS needs the exact-document line **and** 4 of 4 arms.

An `allowed` proves the pattern matches the string typed, never that the resource holds anything, so the
allowed arms are read **together with** the refused arm and never on their own. The simulation runs **after**
the resource exists, never as its pre-apply proof.

**I read no table item.** The simulation is the exercise; no `dynamodb:Scan` call is made against the data.

---

## 5. NEVER-2 LEDGER (the order of the act)

1. `.tools/deploy_ledger.py open` with slug `nfra-mcportal-gw-principal-scan-grant`, legs **apply** and
   **read-back**; commit the entry AND its sentinel
   `org/critical_paths/.open_deploys/nfra-mcportal-gw-principal-scan-grant.json`.
2. `.tools/safe-apply.sh -chdir=infra/aws/terraform/opal-gateway apply .build/z4.tfplan` -- the saved,
   targeted plan. Never a bare `terraform apply`.
3. Read back with AC1.
4. Close both legs with their proofs and commit the close **before** reporting the AC reads.

If a leg fails mid-act, roll back with the section 1.5 command, close the entry as rolled back, and report.

---

## 6. WHAT EACH HALF IS BEING ASKED TO SIGN

> `opal-gateway-role` may **LIST** `gateway-access-state-table` -- one `dynamodb:Scan`, unprojected and
> unconditioned, on that one table ARN. It may not write it, delete from it, reach any other table, or reach
> any index. It already reads every item in it by key. No writer of the table changes. The rollback is one
> `delete-role-policy` and loses no data.

Sign as `.../deliverables/1.0.0_SA_CTO~Z/NEVER_WIDEN_HALF_CTO_MP-z-4_<date>.md` and
`.../deliverables/2.0.0_SA_COO~MP/NEVER_WIDEN_HALF_COO_MP-z-4_<date>.md`, each citing this ASK by path
(`org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/0.7.0_AE_CloudOps~MQ/NEVER_WIDEN_ASK_MP-z-4.md`) -- the
AC2 check greps each half for that exact filename. A refused half STOPS the act and is reported as written.
