# RECREATE `lambda-test-role` -- the SITE-Z recreation record (NFRA_IAMROLES202609.TO-IAM-x-4, step 0)

**Written BEFORE anything was touched**, from this device's own live reads, 2026-10-11 ~11:4xZ.
**Cell:** IAM-x-4 (round 7, E3). **Executed by:** `0.7.0_AE_CloudOps~IR`.
**Authority:** `1.0.0_SA_CTO~Z` @`5af6d5e23e`, adopting laptop `1.0.0_SA_CTO`'s YES @`106f60a7c8`.

> **WHY THIS FILE EXISTS AND WHY IT IS SITE-Z's OWN.** The laptop wrote its own record, and that record **is not
> in this clone**. A rollback that depends on a file this device cannot read is not a rollback. So every value
> below is read from the live role by THIS seat, and the commands below are the whole restore path.

---

## 1. THE REBUILD -- exactly two commands

```bash
aws iam create-role \
  --role-name lambda-test-role \
  --path / \
  --description 'Scoped Lambda role - created 2026-02-19 IAM audit' \
  --max-session-duration 3600 \
  --assume-role-policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"lambda.amazonaws.com"},"Action":"sts:AssumeRole"}]}'

aws iam attach-role-policy \
  --role-name lambda-test-role \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
```

**That is the complete restore.** The role has **0 inline policies**, **0 tags** and **no permissions boundary**,
so nothing else is owed. Run them in that order; `attach-role-policy` fails if the role does not yet exist.

> **TWO FIELDS CANNOT BE REPRODUCED AND DO NOT NEED TO BE.** `RoleId`
> (`AROAUR7FNW6PKHOVBXCS4`) and `CreateDate` (`2026-02-19T16:00:44+00:00`) are AWS-assigned; a recreated role
> gets a new `RoleId`. **That matters only if something referenced the role by `RoleId` rather than by ARN or
> name, and nothing does** -- the account-wide census in section 3 found no reference of any kind. The ARN is
> name-derived (`arn:aws:iam::313476888478:role/lambda-test-role`) and therefore comes back identical.

## 2. THE LIVE STATE, AS READ -- the five facts step 0 re-reads, each matching the cell

| fact the cell asserts | read live at ~11:4xZ | matches |
|---|---|---|
| **1. never assumed** (`RoleLastUsed` null) | `RoleLastUsed` = `{}` -- **empty** | **yes** |
| **2. trust `lambda.amazonaws.com` only** | 1 statement: `Allow` / `{"Service":"lambda.amazonaws.com"}` / `sts:AssumeRole`, **`Condition` absent** | **yes** |
| **3. 1 AWS-managed attachment** | exactly 1: `AWSLambdaBasicExecutionRole` (`arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole`) | **yes** |
| **4. 0 inline policies** | `list-role-policies` -> `[]` | **yes** |
| **5. 0 functions on it / 0 documents naming it** | section 3 | **yes** |

Other fields, for completeness: `Path` `/`, `Description` `Scoped Lambda role - created 2026-02-19 IAM audit`,
`MaxSessionDuration` `3600`, `PermissionsBoundary` **None**, `Tags` **`[]`**.

### 2a. `get-role`'s own output, verbatim

```json
{
  "Path": "/",
  "RoleName": "lambda-test-role",
  "RoleId": "AROAUR7FNW6PKHOVBXCS4",
  "Arn": "arn:aws:iam::313476888478:role/lambda-test-role",
  "CreateDate": "2026-02-19T16:00:44+00:00",
  "Description": "Scoped Lambda role - created 2026-02-19 IAM audit",
  "MaxSessionDuration": 3600,
  "AssumeRolePolicyDocument": {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": { "Service": "lambda.amazonaws.com" },
        "Action": "sts:AssumeRole"
      }
    ]
  },
  "RoleLastUsed": {}
}
```

## 3. FACT 5, AND THE INSTRUMENT CAVEAT THAT GOES WITH IT

**The served AWS graph: exactly ONE hit across 2892 nodes, and it is the role itself.** No `LAMBDA` node, no
`IAM_POLICY` node, nothing else names it.

```
comp-find --corpus aws 'lambda-test-role'  ->  DENOMINATOR: 1 hit(s) across 2892 aws node(s)
  BANDS = node_type: IAM_ROLE=1
POSITIVE CONTROL, same method: 'opal-smartx-lambda-role' -> 4 hits (IAM_ROLE=1, IAM_POLICY=3)
```

> **THE GRAPH IS ABOUT EIGHT HOURS STALE ON IAM POLICY NODES, AND I MEASURED THAT RATHER THAN TRUSTING THE
> VINTAGE LINE.** Its stitch source is `2026-10-11T03:01:08Z`. The positive control above returns **3** inline
> policies for `opal-smartx-lambda-role`, but a **live** `list-role-policies` on that role returns **1**
> (`['opal-smartx-logs']`) -- because cell IAM-x-2 deleted the other two at ~07:1xZ this morning. So the graph
> would not show a reference created after 03:01Z, and fact 5 does not rest on it alone.

**LIVE CORROBORATION, which is the stronger argument:** `RoleLastUsed` is **empty**. AWS has populated
last-used data since 2019, so an empty value means **no principal has ever assumed this role** in its entire
existence since 2026-02-19. A Lambda function configured with an execution role assumes it on its first
invocation; a role never assumed has therefore never backed a function that ran. Combined with zero graph
references of any type, fact 5 holds on two independent planes.

## 4. WHAT THIS RECORD DELIBERATELY DOES NOT CLAIM

- **It does not claim the role is useless.** It claims the role is UNUSED and RECOVERABLE. The decision to
  retire it is `1.0.0_SA_CTO~Z`'s ruling @`5af6d5e23e`, not this seat's, and the ruling is the sign-off on the
  blast radius.
- **It does not depend on the laptop's record**, which is unreadable from this device. If the laptop's record
  and this one ever disagree, this one was read from the live role on the device that performed the delete.
- **It does not assert that a recreated role is byte-identical.** `RoleId` will differ. Section 1 states why
  that is immaterial here and what would have made it material.

**Nothing has been detached or deleted at the time this file is committed. Step 0's STOP did not fire: all five
facts match the cell.**
