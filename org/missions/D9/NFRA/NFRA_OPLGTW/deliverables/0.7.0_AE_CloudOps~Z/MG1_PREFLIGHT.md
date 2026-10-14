# OG-mg-1 Phase A -- operator identity and the IAM preflight, per amendment A1

`0.7.0_AE_CloudOps~Z`, 2026-10-14 ~01:5xZ. **Read-only. No write ran.** Order amended at A1 after
row `NFRA_OPLGTW-Z-S103`: the preflight now names `dynamodb:PutItem` and `dynamodb:UpdateItem`
simulated with the `dynamodb:LeadingKeys` context `POLICY#*`, in place of
`dynamodb:TransactWriteItems`; the before-record reads run under this seat's own read access.

## 1. Operator identity

| read | value |
|---|---|
| calling principal | `arn:aws:iam::313476888478:user/Andrew_Berman` (account 313476888478) |
| operator role | `arn:aws:iam::313476888478:role/opal-gateway-access-admin`, created 2026-09-15T23:32:16Z |
| `sts:AssumeRole` simulated (user -> role) | **allowed** |
| the role ASSUMED for real, not simulated | `arn:aws:sts::313476888478:assumed-role/opal-gateway-access-admin/mg1-phasea-readonly` |

The live assume is recorded because a simulation of `sts:AssumeRole` answers the identity policy
only; the trust policy is a separate gate and an `allowed` simulation can sit beside a failing
assume. Both were read.

## 2. The role's actual policy -- the ground truth the simulations are judged against

Inline policies: `opal-gateway-access-admin-policy`, `gateway-access-admin-ssm-readonly-policy`.
No attached managed policies. The first carries exactly two statements:

| # | Effect | Action | Resource | Condition |
|---|---|---|---|---|
| 0 | Allow | `dynamodb:GetItem` | `table/gateway-access-state-table` | none |
| 1 | Allow | `dynamodb:PutItem`, `dynamodb:UpdateItem` | same table | `ForAllValues:StringLike dynamodb:LeadingKeys = POLICY#*` **and** `Null dynamodb:LeadingKeys = false` |

`Query`, `Scan`, `DeleteItem`, `ConditionCheckItem` and `secretsmanager:*` appear nowhere in it.

## 3. The simulations, one `--resource-arns` per call, isolated

| action | principal | context supplied | decision | reading |
|---|---|---|---|---|
| `dynamodb:GetItem` | role | -- | **allowed** | unconditioned grant |
| `dynamodb:PutItem` | role | `LeadingKeys=POLICY#test` | **allowed** | the write the act needs |
| `dynamodb:PutItem` | role | none | implicitDeny | the CONDITION mode, not a missing grant |
| `dynamodb:UpdateItem` | role | `LeadingKeys=POLICY#test` | **allowed** | |
| `dynamodb:UpdateItem` | role | none | implicitDeny | same mode |
| `dynamodb:DeleteItem` | role | `LeadingKeys=POLICY#test` | implicitDeny | genuinely absent -- and never used |
| `dynamodb:ConditionCheckItem` | role | `LeadingKeys=POLICY#test` | implicitDeny | genuinely absent -- and never used |
| `dynamodb:Query` | role | -- | implicitDeny | genuinely absent |
| `dynamodb:Scan` | role | -- | implicitDeny | genuinely absent |
| `secretsmanager:GetSecretValue` (rosters) | role | -- | implicitDeny | genuinely absent |
| `sts:AssumeRole` (into the role) | user | -- | **allowed** | plus the live assume above |

**No action the act performs is denied. There is no STOP and no widening is requested.**

## 4. Why the retired `TransactWriteItems` row would have manufactured a STOP

`aws accessanalyzer validate-policy`, per action, against the same table ARN:

| action | finding |
|---|---|
| `dynamodb:TransactWriteItems` | **ERROR / INVALID_ACTION** |
| `dynamodb:Query`, `Scan`, `PutItem`, `UpdateItem`, `DeleteItem`, `ConditionCheckItem` | 0 ERROR findings (all real) |

There is no such IAM action: the `TransactWriteItems` **API** authorizes on the underlying item
actions. Simulating a non-existent action returns `implicitDeny` on any principal without a
matching wildcard, which the original preflight would have read as a STOP on the order's central
write.

**Both controls misled, in opposite directions, and only the policy read settled it.** The role
read `implicitDeny` for the bogus action -- indistinguishable from a missing grant. The broad
positive control (`user/Andrew_Berman`) read **allowed** for that same non-existent action, because
an admin wildcard matches any string: the documented false-ALLOW mode. A reader who ran only the
control would have concluded the role was under-granted relative to an admin; a reader who ran only
the role simulation would have filed a BLOCKING row.

## 5. What authorizes the write, read from the writer rather than the preflight

`ops/schwab_entitlement_admin.py` `activate()` (:377-394) builds

```
ops = [profile_put_op(profile_item, base_profile_revision), grant_put_op(grant_item), audit_op]
      + one _deny_put_op per plan.deny_emails alias
```

Every member is a **Put**. The optimistic staleness check rides the Put's own `ConditionExpression`
(a `STALE` base raises `acs.ConditionFailed`), **not** a separate `ConditionCheck` transaction item.
The revoke path states "Never a DeleteItem" (:404). `access_state.py` (:499-521) does define `Put`,
`Delete` and `ConditionCheck` builders and calls `transact_write_items`, but `activate` uses only
the Put builder -- so `DeleteItem` and `ConditionCheckItem` being absent from the role is consistent
with the module's design rather than a gap in it.

Every record written sits in a `POLICY#<tid>#<oid>` partition, which is exactly what statement 1's
`LeadingKeys = POLICY#*` condition admits. **The condition is a real constraint, not a formality:**
the same role could not write a non-POLICY# item in this table even by mistake.

## 6. Three gaps recorded, none blocking

1. **`Query` and `Scan` are absent from the role.** The before-record's strongly consistent scan ran
   under the calling principal, which A1 rules is correct. A successor who assumes the role to
   re-run it will get `AccessDenied`.
2. **`secretsmanager:GetSecretValue` on `gateway/principals/rosters` is absent from the role.** The
   original preflight offered "read host-side or under the operator role"; the role cannot. This
   read also ran under the calling principal, and the values went only to
   `%LOCALAPPDATA%/opal/og-salt/mg1/`, asserted at run time to resolve outside the worktree.
3. **`gateway-access-admin-ssm-readonly-policy`** is a second inline policy on the role and is not
   named in the preflight. Not exercised by this act; noted so the role's surface is not read as
   just the one policy.

## 7. The before-record, and what it means for the two writes

From `MG1_BEFORE.json` -- strongly consistent Scan, `NextToken` followed to exhaustion,
**1510 items scanned, 17 POLICY# partitions, 4 `principal_profile`, 4 `data_entitlement`**:

| role | pk_hash | profile | grant scope keys |
|---|---|---|---|
| andrew | `a18b74486b` | **NONE** | 0 |
| bbg | `3c1d2597c9` | **NONE** | 0 |
| alyssa | `2c61471b14` | active, revision 4, grant_revision 4, kind `restricted` | 7 |

This confirms the order's own reading independently: **both writes CREATE** (profile revision 1 and
grant revision 1 each, since `activate` computes `1 if base is None`), and Alyssa's revision-4
scope is the only v2.2-width grant on record, so it is the template R1 is built from and diffed
against. Roles were resolved as the order specifies -- Andrew from the roster's `master_admin`, the
Bloomberg principal by the Part D oid prefix the order names, Alyssa from her active profile's own
email prefix rather than any hardcoded id.

**DynamoDB's `ItemCount` was not used as the denominator.** It refreshes roughly every six hours and
read 1493 while a consistent scan read 1504, then 1510 minutes later. The scan's own count is the
denominator, and it is printed.

## 8. A constraint on the candidates that the order's step 3 does not state

`prepare()` **refuses** a candidate with no resolvable email: it takes the candidate's own
`email`/`emails`, else the STORED profile's, and with neither it raises `CandidateRejected` -- row
W3-S22, AMENDMENT A1, so that no email-less grant can activate without a deny record. The refusal
happens in `prepare`, before `activate` is ever reached, so nothing is written.

**Both of this order's records are CREATES with no stored profile** (section 7: Andrew and bbg hold
none), so neither has a stored email to fall back on. Therefore **each candidate must itself carry
the email**, or Phase A's own `prepare` call fails and Phase B could never run.

That has a consequence for where identifiers live. The email is an identifier, so it goes in the
candidate files under `X` (`%LOCALAPPDATA%/opal/og-salt/mg1/`) and never into `W`. The ask will
therefore describe each candidate's `emails` field by its PRESENCE and its effect -- one
`email_deny` row put per alias in the same transaction -- and not by value.

Noted here rather than discovered at the `prepare` call, because the natural reading of step 3 ("the
template is the store's own v2.2-width grant") is that identity means tid and oid alone; the writer
requires a third field, and only for the create case.
