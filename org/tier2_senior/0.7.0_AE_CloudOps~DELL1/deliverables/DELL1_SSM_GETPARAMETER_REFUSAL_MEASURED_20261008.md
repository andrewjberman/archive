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
| Not needed | parameter creation (it exists); `DescribeParameters` (already held); any KMS grant unless the parameter is `SecureString` -- **UNMEASURED**, see below |

## Held, not claimed

1. **Is `/mdpf/custody_source` a `SecureString`?** If yes the grant also needs `kms:Decrypt` on its key. I
   cannot read the parameter's TYPE without the very action I am denied, and `describe-parameters` output was
   consumed for the name census only. **UNMEASURED.** Whoever cuts the cell must settle it, or the grant lands
   and the call still fails.
2. **"dell1 cannot plan mdpf-pipeline"** is the record's claim, carried from the laptop. I did NOT run
   `terraform plan` on `infra/aws/terraform/mdpf-pipeline/`, so I have not reproduced it and do not assert it.
   The refusal above is necessary for that plan to fail; whether it is the ONLY refusal in the way is
   **UNMEASURED** -- a plan can stack several. Reading one refusal does not enumerate them.
3. Nothing here was applied. This seat holds no IAM write and asked for none.

**Claim field:** every value above is `measured` except the two rows named `UNMEASURED`.
