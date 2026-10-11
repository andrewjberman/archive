# RETIRE_READBACK -- `lambda-test-role` is GONE (NFRA_IAMROLES202609.TO-IAM-x-4, steps 2-4)

**Cell:** IAM-x-4 (round 7, E3). **Executed by:** `0.7.0_AE_CloudOps~IR`.
**Authority:** `1.0.0_SA_CTO~Z` @`5af6d5e23e`, read in full at its pin beside a positive control, adopting
laptop `1.0.0_SA_CTO`'s YES @`106f60a7c8` and superseding the round-6 "Andrew's word first" line.
**Measured:** 2026-10-11. Detach `12:05:40Z`, delete `12:07:35Z`, read-back immediately after.

---

## 1. THE READ-BACK, BOTH OUTPUTS VERBATIM

**The deleted role:**

```
$ aws iam get-role --role-name lambda-test-role
aws: [ERROR]: An error occurred (NoSuchEntity) when calling the GetRole operation: The role with name lambda-test-role cannot be found.
rc=254
```

**THE POSITIVE CONTROL -- the same call shape, run as its own invocation, on a role that must still exist:**

```
$ aws iam get-role --role-name opal-smartx-lambda-role
{
    "Name": "opal-smartx-lambda-role",
    "Arn": "arn:aws:iam::313476888478:role/opal-smartx-lambda-role",
    "Created": "2025-11-20T14:43:02+00:00"
}
rc=0        (1337 bytes of role JSON returned)
```

> **THE CONTROL IS WHAT MAKES THE `NoSuchEntity` EVIDENCE.** A failed retrieval returns a value: an IAM call
> that could not reach the service, a mistyped role name, or an expired credential would also produce
> `NoSuchEntity` or an error indistinguishable from it. Running the same call against a role that must survive
> is what makes the absence a fact about `lambda-test-role` rather than about the instrument. It was run as a
> SEPARATE invocation, because a control sharing a call with its target is not a control.

**`AC2`'s own invocation reads exactly `1`.**

### 1a. ONE MEASUREMENT CORRECTION, MADE BEFORE IT WAS RECORDED

My first read-back printed `rc=0` for the deleted role, which is wrong and would have been a strange thing to
file beside a `NoSuchEntity` message. The cause is this device's familiar trap: `$?` was taken **after a pipe to
`head`**, so it was `head`'s status, not the AWS call's. Re-measured unpiped, the role reads **`rc=254`** and
the control reads **`rc=0`**. The `NoSuchEntity` text was always the real evidence; the rc is now also correct.

## 2. THE ACTS, IN THE RULING'S ORDER

| step | act | result |
|---|---|---|
| 0 | re-read the five facts live, write the site-Z recreation record | all five matched; **STOP did not fire**; record committed `a3994c4cb7` |
| 1 | open the NEVER-2 entry, rollback leg = the rebuild commands | `iamroles-r7-retire-row7`, 4 legs, opened `12:03Z`, committed |
| 2 | `detach-role-policy` | rc=0 at `12:05:40Z`; attached **1 -> []**, inline `[]` both sides |
| 3 | `delete-role` | rc=0 at `12:07:35Z` |
| 4 | read back `NoSuchEntity` with a positive control | section 1 |

**The rollback leg was closed BEFORE anything was detached**, which is the part that matters: the restore path
existed on this device and in git history before the role stopped existing.

### 2a. WHY THE DETACH LEG'S PROOF IS A COUNT, NOT AN rc

`detach-role-policy` returning rc=0 says the call was accepted. The proof is that
`list-attached-role-policies` read **exactly 1** (`AWSLambdaBasicExecutionRole`) before and **exactly `[]`**
after. It is also self-checking in this cell: `delete-role` **refuses while any policy is attached**, so an
rc=0 that had not actually detached would have surfaced as a refusal on step 3 rather than passing silently.

## 3. WHAT WAS DELETED, AND WHY IT WAS RECOVERABLE

A role created `2026-02-19T16:00:44Z` and **never assumed in its entire existence** (`RoleLastUsed` empty; AWS
has populated last-used since 2019). Trust `lambda.amazonaws.com` only with no `Condition`. One AWS-managed
attachment, zero inline policies, zero tags, no permissions boundary. Nothing named it: the served graph
returned **1 hit across 2892 nodes** -- the role itself -- and a repo census returned **4 hits across 7922
files**, all four being **inventories that LIST the role** (a census instrument, an `NFRA_TERRAFORM_P1` IAM
slice, a resource-explorer dump, a graph parity dump) rather than policy documents granting on or passing it.
That matches the ruling's own account sweep: 301 roles, 78 policies, 0 documents outside the role itself.

**The restore is `round7/retire_row7/RECREATE_lambda-test-role.md` @`a3994c4cb7`** -- two commands, read from
the live role by this device rather than copied from the laptop's record, which is not in this clone.

> **ONE THING THAT WILL NOT COME BACK, stated because the ruling itself turned on it:** a recreated role gets a
> **new `RoleId`** (the deleted one was `AROAUR7FNW6PKHOVBXCS4`). The round-6 analysis reserved this delete for
> Andrew precisely because of that. The ruling lifted the reservation on the ground that nothing pins the old
> principal, and the two censuses above are what that rests on. The ARN is name-derived, so it returns
> identical. **If a future reader finds something that did reference the old `RoleId`, this is the sentence to
> read first.**

## 4. THE GRAPH WILL DISAGREE WITH THE WORLD FOR A WHILE

The served AWS graph still carries an `IAM_ROLE` node for `lambda-test-role`; its stitch source is
`2026-10-11T03:01:08Z`, hours before this delete. I measured that staleness rather than assuming it: the same
graph lists **3** inline policies for `opal-smartx-lambda-role` while a live read returns **1**, because cell
IAM-x-2 deleted the other two at ~07:1xZ today. **So a reader querying the graph for this role will find it
until the next stitch. The live plane is the authority, and section 1 is the live plane.**

## 5. WHAT IS NOT THIS CELL'S

The `GOVERNANCE_DISPOSITION` row is the issuer's, per step 5. This record reports the read-back and nothing
more; it takes no view on whether other RETIRE candidates should follow, because each would need its own five
facts re-read and its own ruling.

**STEPS 2-4 END HERE. One role deleted, recoverable from the record above, and nothing else was touched.**
