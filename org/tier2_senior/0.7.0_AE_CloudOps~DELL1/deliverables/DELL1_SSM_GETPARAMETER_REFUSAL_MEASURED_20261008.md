# dell1's deploy refusal, measured by exercise: `ssm:GetParameter` is denied at the ACTION level, not the resource

**Seat:** `0.7.0_AE_CloudOps~DELL1` (dell1 own-box deploy seat)
**Date:** 2026-10-08
**Why this exists:** `ANDREW_DIRECT_20261008_220xZ_ONE_LAPTOP_APPLIER_EXCEPTION_YES.md` addendum placement 2
names this refusal as the one thing the laptop still applies for a Dell, "only until that grant lands, and only
for that refusal." The record states the refusal; it does not carry the measurement. This does.
**Grain of the grant cell depends on which it is**, so it was exercised rather than inherited.

---

## Principal

```
arn:aws:iam::313476888478:user/cloudops-dell1-agent-user   (UserId AIDAUR7FNW6PFHEFTJCVV, acct 313476888478)
```

## The exercised read -- the live primitive, not a simulation

```
.tools/aws ssm get-parameter --name /mdpf/custody_source
rc=254
AccessDeniedException: User: arn:aws:iam::313476888478:user/cloudops-dell1-agent-user is not authorized to
perform: ssm:GetParameter on resource: arn:aws:ssm:us-east-1:313476888478:parameter/mdpf/custody_source
because no identity-based policy allows the ssm:GetParameter action
```

**REFUSAL CONFIRMED.** Note the trailing clause: *no identity-based policy allows the action*. This is a
MISSING ALLOW, not an explicit `Deny`. The remedy is an additive identity-based grant; there is no Deny
statement to remove.

`comp-iam` was not used as the oracle here and must not be cited as one: per `/cloud-ops`, it models
`(action)` and never `(action, resource)`, and it fails GREEN. `simulate-principal-policy` was also not used
as the proof -- it carries four independent false-deny modes and one false-allow mode. The exercised call is
the sound oracle and it is the one that was run.

## Control A -- same action, a resource that does not exist

```
.tools/aws ssm get-parameter --name /mdpf/custody_source_DOES_NOT_EXIST_9999
rc=254
AccessDeniedException ... not authorized to perform: ssm:GetParameter on resource:
arn:aws:ssm:us-east-1:313476888478:parameter/mdpf/custody_source_DOES_NOT_EXIST_9999
because no identity-based policy allows the ssm:GetParameter action
```

**BYTE-IDENTICAL denial class against a parameter nothing has created.** Therefore the denial is
**ACTION-LEVEL, not resource-scoped**: the principal holds `ssm:GetParameter` on NOTHING, so the grant cell is
"add the action", not "widen an existing resource pattern."

This control also pins a rule-22a RETRIEVAL trap live: **`AccessDenied` MASKS `ParameterNotFound`.** The two
are indistinguishable from the caller, so for this principal a failed `get-parameter` can never be read as
evidence about whether a parameter exists.

## Control B -- a different SSM action, same principal, same region

```
.tools/aws ssm describe-parameters        rc=0, auto-paginated, counted client-side
DENOMINATOR: 17 parameter(s) visible
TARGET /mdpf/custody_source PRESENT IN LISTING: True
```

So credentials are live, SSM is reachable, the region is right, and the principal is NOT broadly locked out of
SSM. The gap is exactly one action.

**And it settles the existence question Control A cannot:** `/mdpf/custody_source` **EXISTS** and dell1 can
already SEE it -- it is 1 of the 17. Only reading its VALUE is refused. There is nothing to create.

---

## What the grant cell is

| Field | Value |
|---|---|
| Principal | `arn:aws:iam::313476888478:user/cloudops-dell1-agent-user` |
| Action | `ssm:GetParameter` -- **the whole gap**; the principal holds it on no resource at all |
| Resource (minimum) | `arn:aws:ssm:us-east-1:313476888478:parameter/mdpf/custody_source` |
| Shape | ADDITIVE identity-based Allow. No Deny exists to remove. |
| Blast radius | one action, one parameter, one principal. Rollback = delete the statement. |
| Not needed | parameter creation (it exists); `DescribeParameters` (already held); **any KMS grant -- the parameter is `type = "String"`, NOT `SecureString`** (measured from source, below) |

### READ ONLY -- do not widen this cell to a write

`lambdas.tf:25` is explicit that the parameter's VALUE is operationally controlled: the `bd -> schwab`
co-activation flip is a served-critical cutover done by `aws ssm put-parameter` in a coordinated window under
never-widen + CVO co-sign, with `lifecycle.ignore_changes = [value]` so a later apply does not drift-revert it.
Terraform needs only to READ the parameter. **The cell is `ssm:GetParameter`. It must not carry
`ssm:PutParameter`** -- that would hand this seat a served-critical cutover the record does not grant it.

---

## Both previously-held rows, now CLOSED by measurement

### 1. SecureString / `kms:Decrypt` -- CLOSED, no KMS leg needed

The parameter is Terraform-managed, so its TYPE is readable from source without the denied action:

```
infra/aws/terraform/mdpf-pipeline/lambdas.tf:25  resource "aws_ssm_parameter" "mdpf_custody_source"
  name = "/mdpf/custody_source"
  type = "String"          <-- NOT SecureString
```

So `ssm:GetParameter` alone is sufficient. **No `kms:Decrypt` statement is required.** Read from the build
input rather than from the API I am denied -- the sound route when the instrument you would reach for is the
very thing refused.

### 2. "dell1 cannot plan mdpf-pipeline" -- CLOSED, REPRODUCED, and it is the ONLY refusal

Ran the read-only plan (`terraform plan -input=false -lock=false`; binary resolved on PATH, not the baked
`.tools/terraform.exe`, which does not exist on every device):

```
Plan: 0 to add, 1 to change, 0 to destroy
Error: reading SSM Parameter (/mdpf/custody_source): ... AccessDeniedException ...
  with aws_ssm_parameter.mdpf_custody_source, on lambdas.tf line 25
```

**The record's claim is confirmed on this box, and the plan is right-sized by it:** refresh completed across
every other resource in the module and Terraform produced a full execution plan before failing on this ONE
error. Exactly one refusal is in the way. Granting `ssm:GetParameter` on this one parameter is therefore
expected to let the plan complete -- which is read from the plan's own behavior, not predicted from the
module's shape.

---

## Off-task observation, recorded not acted on

The same plan shows a PENDING IN-PLACE CHANGE unrelated to the refusal:

```
~ aws_s3_object.mdpf_route_bindings   (id: config/mdpf/route_bindings.yaml)
    content-sha256: 98f5e9c5...d923 -> 37eb8451...e21c2
    source_hash:    650f893a...b078 -> f94e8e4c...721d
~ output mdpf_route_bindings_sha256   (same pair)
```

The repo's `route_bindings.yaml` differs from the deployed object. **Not diagnosed and not applied** -- this
seat holds no order on it, and an apply here would move a served config object. Named so it is not lost; it
belongs to whoever owns MDPF route bindings. Whether this is intended-but-unlanded or genuine drift is
UNMEASURED by me.

---

**Claim field:** every value in this file is `measured`. Two rows previously carried `UNMEASURED` and are now
closed above. The one remaining `UNMEASURED` is named inline: the cause of the `route_bindings` delta.

**Nothing was applied.** The only acts were reads: three AWS reads, one read-only `terraform plan`
(`-lock=false`, no state lock taken), and one source read. This seat holds no IAM write and asked for none.
