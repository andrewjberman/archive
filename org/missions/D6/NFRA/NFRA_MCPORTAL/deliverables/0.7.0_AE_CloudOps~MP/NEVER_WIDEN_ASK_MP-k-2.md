# NEVER-WIDEN ASK -- NFRA_MCPORTAL MP-k-2: the gateway role's one write, close requests only

**Asked by:** `0.7.0_AE_CloudOps~MP`
**Task order:** `org/missions/D6/NFRA/NFRA_MCPORTAL/task-orders/NFRA_MCPORTAL.TO-MP-k-2.close-request-write-grant.md`
**Halves owed:** `1.0.0_SA_CTO~O` (CTO half) and `2.0.0_SA_COO~MP` (COO half). Both are owed against THIS file.
**Ruling this implements:** `1.0.0_SA_CTO~O` msg 32404 on Q3 -- "NFRA_MCPORTAL builds ONLY the gateway side ... writing
close-request objects, on one PutObject grant scoped to `requests/` (never-widen, C10, this project's pair)".
**Worktree / branch / base:** `C:/tmp/mp-k2` / `wk-mcportal-cp2-k2` / `box/sitez` @ `5db9d4cbabf33ac5298e2c6a956cfc8ec2c90abb`
**State at the time of asking:** NOTHING IS APPLIED. The plan is graded and saved; the apply waits on both halves.

---

## 1. BLAST RADIUS -- the one action and the one resource pattern

One `aws_iam_role_policy` is ADDED to the existing role `opal-gateway-role`
(`aws_iam_role.gw`, `infra/aws/terraform/opal-gateway/main.tf:151`). It carries ONE statement:

| element | value |
|---|---|
| Effect | `Allow` |
| Action | `s3:PutObject` -- exactly one, no second action |
| Resource | `arn:aws:s3:::opal-313476888478-globgrph/fabric/open-calls/v1/box=*/requests/*` -- exactly one pattern |
| Sid | `McportalCloseRequestWriteOnly` |
| Condition | none |

Policy name `gateway-mcportal-close-request-write-policy`, a LITERAL. It is builder output, not typed:
`lib/opal_naming.py name('gateway', None, 'mcportal-close-request-write', 'policy')` was run in this worktree and
returned that exact string (match verified True). An interpolated name is refused by the apply-time naming limb --
that is surprise row `NFRA_MCPORTAL-Z-S21` from MP-x-3, and the literal form is the amendment that cleared it.

New file, nothing folded into an existing grant:
`infra/aws/terraform/opal-gateway/mcportal_close_request_write.tf`. The only other edit is COMMENTS in
`graph-read.tf`, extending the R3 carve-out sentence to name this one write and cite msg 32404. Measured: the
non-comment diff of `graph-read.tf` is EMPTY (every `+`/`-` line in it begins with `#`).

## 2. WHAT THE ACT MAY TOUCH

Request objects under any box's `requests/` prefix of the globgrph bucket -- i.e.
`fabric/open-calls/v1/box=<any>/requests/<id>.json`. `box=*` is deliberate and is the ruling's scope: the MC portal
page serves every box's open calls, so Andrew's close request may be addressed to any box. The grant admits creating
and overwriting such objects and nothing more.

**Writers of that prefix after this act: 1 (printed, as NEVER-1 requires).** Measured in `.tools/open-calls-scan.py`,
the only other participant in this prefix:
- it READS `requests/` -- `xa._list_keys(req_prefix(device))` at `:407`;
- it WRITES `request_results/` -- `xa._put(res_key(device, rid), ...)` at `:453`;
- its one `_put` into `req_prefix` is at `:711`, inside the `ocscan_selftest_` block (tempdir fixtures, `fake_close`,
  `rec(...)` assertions), so it is not a production writer.
All 11 write verbs in that file were enumerated and each one's target key read; the denominator is printed, not
sampled. So the gateway becomes the SOLE production writer of `requests/`, and there is no second rule to read and no
write collision. The scan's own contract agrees: "The request is never deleted; its RESULT object ... marks it done"
(`:400-402`).

## 3. WHAT THE ACT MAY NEVER TOUCH

| never | why it is out |
|---|---|
| `fabric/open-calls/v1/box=*/open_calls.json` -- the LIST itself | not matched by the pattern. Decomposition C11: the page never edits a list; the box's own scan applies the request through the box's writer |
| `fabric/open-calls/v1/box=*/request_results/*` | a SIBLING of `requests/`, not a child -- not matched. The result is the box's to write, not the page's |
| `fabric/open-calls/v1/box=*/scan.json`, `open_deploys.json`, `mode.json` | not matched -- all are siblings of `requests/` |
| `fabric/activity/v1/*` -- the activity store | not matched; the role's grant there stays READ-only (MP-x-3) |
| `s3:DeleteObject` and every multipart, ACL or tagging action | not in `Action`. There is no delete anywhere |
| `warehouse/*`, `projection/*`, any other prefix of this bucket | not matched. R3's remaining text stands |
| any other bucket; any bucket-admin action | not matched; no `s3:*`, no `Resource: "*"` |
| the role's existing grants | untouched. `mcportal_fabric_read.tf` (MP-x-3 read), `mcportal_grant_writer.tf`, `graph-read.tf`'s secret read and `gw_golive` are not edited. No resource line moves anywhere |
| the gateway itself | not redeployed. No Terraform resource other than the one addition. No ALB, host, role-trust or secret change |

No KMS grant is involved: the bucket is SSE-S3 (AES256) and carries no bucket policy, so the identity grant alone
admits the write.

## 4. THE PLAN, AND THE POLICY DOCUMENT AS PLANNED

Targeted plan, run from the worktree root against `infra/aws/terraform/opal-gateway`:

```
Plan: 1 to add, 0 to change, 0 to destroy.
```

That is exactly the count the task order requires; anything else was to STOP the act.

```
  # aws_iam_role_policy.gw_mcportal_close_request_write will be created
  + resource "aws_iam_role_policy" "gw_mcportal_close_request_write" {
      + id          = (known after apply)
      + name        = "gateway-mcportal-close-request-write-policy"
      + name_prefix = (known after apply)
      + policy      = jsonencode(
            {
              + Statement = [
                  + {
                      + Action   = [
                          + "s3:PutObject",
                        ]
                      + Effect   = "Allow"
                      + Resource = [
                          + "arn:aws:s3:::opal-313476888478-globgrph/fabric/open-calls/v1/box=*/requests/*",
                        ]
                      + Sid      = "McportalCloseRequestWriteOnly"
                    },
                ]
              + Version   = "2012-10-17"
            }
        )
      + role        = "opal-gateway-role"
    }
```

Saved plan: `C:/tmp/mp-k2.tfplan`. Terraform v1.15.8, resolved on PATH -- site Z has no `.tools/terraform.exe`, so the
binary is resolved and not assumed. `terraform fmt -check` on the new file: rc=0. `terraform init` installed
`hashicorp/aws v5.100.0` and `hashicorp/external v2.4.2` from the local cache, rc=0, so the task order's step-5
provider stop does not fire.

**Plan-vs-apply note.** The task order's step 2 directs the plan to be run with `safe-apply`. That is not satisfiable:
`safe-apply` gates the `apply` subcommand ONLY and exits 2 before terraform is invoked at all, telling the caller to
run the terraform binary directly -- measured, rc=2, and documented in the wrapper's own header (`:19-21`). The plan
above was therefore produced with the resolved terraform binary, which is the wrapper's own instruction. Filed as
surprise row `NFRA_MCPORTAL-Z-S22` (OBSERVATION / INERT) @ `290e48a54c`; no override was taken and none is needed.
**Step 4's apply does go through `safe-apply`,** because that invocation carries the `apply` subcommand.

## 5. `comp-iam gaps`

```
Total: 36 missing | 52 deny-present | 1 coverage-unknown | 2 resource-mismatch  across 30 service(s)
  RESOURCE PLANE: 602 call(s) verdicted across 105 mapped role(s); 412 UNRESOLVABLE-RESOURCE, 121 GRANTED,
                  48 GRANTED-BROAD, 19 UNGRANTED, 2 GRANTED-ACTION / UNGRANTED-RESOURCE
```

Read this as a FLOOR, with its denominator and its holes stated:

- **Those are estate-wide standing figures, not this cell's.** None of the 36 missing or 2 resource-mismatch rows
  concerns `opal-gateway-role` or the globgrph `requests/` path. The 26 lines mentioning `PutObject`/`globgrph` are
  other services (`astn-wsjft-orchestrator-role`, `etfs-reports-orchestrator-role`, `news-semantic-clustering`,
  `opal-pm-*`, `opal-portfolio-pickle-parser`, `semantic-trending-topics-portal-publisher`). The 56 lines naming
  `opal-gateway` are all `UNMAPPED-METHOD` raised from TEST files
  (`infra/aws/ec2/opal-gateway/tests/...`) -- a parser limitation, pre-existing, and not a grant gap.
- **A grant ADDITION cannot create a missing-permission gap**, so no before/after diff of this figure is informative
  for this cell.
- **The first run of this command in this worktree returned all zeros against a 0-service denominator**, because the
  cell's sparse pattern list excluded the service trees. That zero was "could not check", not "no gaps". The checkout
  was widened to `infra/` and the command re-run to obtain the real denominator above. The widening is a departure
  from the pattern list the order names (`.tools/`, `org/`, `lib/`,
  `infra/aws/terraform/opal-gateway/`) and was needed for two mechanical reasons: `lib/opal_naming.py` reads
  `infra/logic/registry/*.json`, and `comp-iam gaps` needs the service trees to have a denominator at all.
- **comp-iam is necessary, not sufficient, and it fails GREEN**: it models `(action)`, not `(action, resource)`. Its
  own banner on this run also declared `DENY-OVERLAY INCOMPLETE: 7 deny statement(s) unparsed`, so it cannot answer
  "is this denied?" at all. **AC2's simulation is the oracle for this act**, not this figure.

## 6. ROLLBACK, PER RESOURCE

One resource, so one rollback. Either form, from the worktree:

```
aws iam delete-role-policy --role-name opal-gateway-role \
  --policy-name gateway-mcportal-close-request-write-policy
```

or a targeted destroy of `aws_iam_role_policy.gw_mcportal_close_request_write` in
`infra/aws/terraform/opal-gateway`.

The rollback is clean by construction: the grant lives alone in its own file, so removing it touches no other gateway
grant, and in particular does not disturb MP-x-3's read, which outlives it. Nothing else in the module moves, and no S3
object is created or deleted by either the act or its rollback -- this act writes IAM only. Reverting leaves the role
exactly as it is at the moment of signing.

Ledger: `nfra-mcportal-cp2-close-request-grant`, opened on this branch before the act with two legs (apply,
read-back) and its sentinel committed, per NEVER-2. If a leg fails mid-act the named command above runs at once and the
entry closes as rolled back.

## 7. THE READ-BACK I WILL RUN

Both checks are the issuer's, read-only to me, at
`org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/2.0.0_SA_COO~MP/cp2/checks/`.

**AC1 -- the policy document, live (`k2.AC1.sh`).** `aws iam get-role-policy --role-name opal-gateway-role
--policy-name gateway-mcportal-close-request-write-policy`, then a parse that collects every statement's actions and
resources and FAILS on any non-`Allow` effect, any `NotAction`/`NotResource`, any action other than `s3:PutObject`, or
any resource other than the single pattern. Expect `actions=s3:PutObject resources=1 problems=0`.

**AC2 -- the exercise, by simulation (`k2.AC2.sh`), 6 arms, each its own invocation with ONE `--resource-arns`.**

| arm | action | key | expect |
|---|---|---|---|
| put request | `s3:PutObject` | `open-calls/v1/box=sitez/requests/<id>.json` | `allowed` |
| put list | `s3:PutObject` | `open-calls/v1/box=sitez/open_calls.json` | `implicitDeny` |
| put result | `s3:PutObject` | `open-calls/v1/box=sitez/request_results/x.json` | `implicitDeny` |
| put activity | `s3:PutObject` | `activity/v1/dt=2026-10-09/box=sitez/x.json` | `implicitDeny` |
| delete request | `s3:DeleteObject` | `open-calls/v1/box=sitez/requests/<id>.json` | `implicitDeny` |
| get list (CONTROL) | `s3:GetObject` | `open-calls/v1/box=sitez/open_calls.json` | `allowed` |

6 of 6 must match. The four refused arms are the adversary reads this cell's `<preflight>` relies on in place of
`comp-adversary`. The shape satisfies Rule 22a: one ARN per call (two in one call flip the held one to
`implicitDeny`), each call a separate invocation, and the `get list` arm is a positive control proving the simulation
can return `allowed` against this principal at all -- so an all-`implicitDeny` sheet would be read as the instrument,
not the world. The grant carries no `Condition`, so no `--context-entries` is needed; the conditioned statement in the
estate is MP-x-3's `ListBucket`, which this act does not touch.

**What an `allowed` here does and does not prove.** It proves the policy PATTERN matches the string typed. It does not
prove the key exists -- simulate-principal-policy returns `allowed` for a resource nothing has created. That is why the
allowed arm is read only together with the four refused arms, and why no S3 object is written by me: the task order's
BOUNDS make the simulation the exercise, and this seat writes no object under the new grant.

**AC3** reads this ASK and both halves at HEAD of `box/sitez`, and requires the ledger entry present with its sentinel
removed and nothing left OPEN or HELD.

---

## WHAT EACH HALF IS BEING ASKED TO SIGN

That the blast radius in sections 1-3 is the whole of it: **one action, `s3:PutObject`, on one pattern,
`arn:aws:s3:::opal-313476888478-globgrph/fabric/open-calls/v1/box=*/requests/*`, added to `opal-gateway-role` as a
separate removable file, with the rollback in section 6 and the read-back in section 7.** Nothing in the list, the
results, the activity store, any other prefix, any other bucket, or any delete.

A refused half STOPS the act and is reported. Until both halves are at HEAD, nothing is applied.
