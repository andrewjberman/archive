# MP-k-2 PRE-ACT CONTROL -- the three checks read BEFORE the grant exists

**Seat:** `0.7.0_AE_CloudOps~MP`
**Read at:** 2026-10-09, after merging `box/sitez` into `wk-mcportal-cp2-k2` (merge commit `864fae2b01`)
**State when read:** NOTHING APPLIED. Plan graded `1 to add, 0 to change, 0 to destroy`; ledger not yet opened;
CTO half not yet at HEAD.

## Why this file exists

A post-act `AC2: 6 of 6` cannot, on its own, distinguish "the grant landed" from "the simulation returns `allowed`
for everything this principal is asked about". `simulate-principal-policy` has one documented FALSE-ALLOW mode
(it matches the ARN against the policy's `Resource` patterns and never asks whether the ARN names anything) and four
false-deny modes. The only reading that discriminates is the SAME six arms run before the grant exists. That is this
file. It is the negative arm; the proof_of_spec instance will carry the positive one.

ABSENT is not EXERCISED-AGAINST: these rows are what the instrument said when the policy genuinely did not exist,
and AC1 below proves it did not.

## AC1 -- the policy document, live (`k2.AC1.sh`)

```
aws: [ERROR]: An error occurred (NoSuchEntity) when calling the GetRolePolicy operation: The role policy with name
gateway-mcportal-close-request-write-policy cannot be found.
get-role-policy rc=254
RESULT: FAIL
```

Read as: the instrument reaches live IAM under this seat's identity, and the policy this cell adds does not exist.
`NoSuchEntity` is a POSITIVE reading of absence here, not a failure to look -- the call resolved, authenticated and
returned a specific entity-not-found for the exact policy name.

## AC2 -- the six-arm simulation (`k2.AC2.sh`), one `--resource-arns` per call, each its own invocation

| arm | action | expect (post-act) | GOT (pre-act) | verdict |
|---|---|---|---|---|
| put request | `s3:PutObject` | `allowed` | `implicitDeny` | MISMATCH -- the one arm the grant flips |
| put list | `s3:PutObject` | `implicitDeny` | `implicitDeny` | OK |
| put result | `s3:PutObject` | `implicitDeny` | `implicitDeny` | OK |
| put activity | `s3:PutObject` | `implicitDeny` | `implicitDeny` | OK |
| delete request | `s3:DeleteObject` | `implicitDeny` | `implicitDeny` | OK |
| get list (CONTROL) | `s3:GetObject` | `allowed` | `allowed` | OK |

```
simulation arms matched 5 of 6
RESULT: FAIL
```

**This is the discriminating reading, and it discriminates in both directions:**

1. The `get list` control returned `allowed`. So the instrument CAN return `allowed` against
   `opal-gateway-role` on this bucket, which means the four `implicitDeny` rows are real refusals and not an
   instrument that denies everything. (That control arm is MP-x-3's read, applied by this seat earlier today and
   still live -- so it also re-proves MP-x-3 is intact and was not disturbed by this cell's build.)
2. Exactly ONE arm mismatched, and it is precisely the arm this grant is for. Nothing else moved. So when the
   post-act run reads 6 of 6, the delta is attributable to this one statement and to nothing else in the estate.
3. Had the pre-act run already read 6 of 6, the grant would have been redundant or the instrument blind, and either
   finding would have STOPPED the act. It did not.

This matches the issuer's own dry-run at base `2851a9190d` ("AC2 FAIL (5 of 6: the put-request arm reads
implicitDeny before the grant; the other five match, the control arm included)"), measured independently here on a
different base after the `box/sitez` merge.

## AC3 -- the ASK, the halves and the ledger (`k2.AC3.sh`)

```
ask=yes; halves citing the ask=1 of 2; entry files at HEAD=0; sentinel at HEAD=no; listed OPEN/HELD=0;
SCAN DENOMINATOR: 16 of 16 sentinel(s) scanned
RESULT: FAIL
```

Read per clause:
- `ask=yes` -- the ASK is at HEAD and cited correctly.
- `halves citing the ask=1 of 2` -- **the one remaining gate.** `2.0.0_SA_COO~MP` is SIGNED against the ASK
  @`77184244cf`. The CTO half is owed by `1.0.0_SA_CTO~Z` per AMENDMENT 3 (the TO's original `1.0.0_SA_CTO~O` was
  retired by Andrew-direct ~07:4xZ); the issuer has asked `~Z` for it.
- `entry files at HEAD=0; sentinel at HEAD=no` -- correct and intended: per the TO the ledger opens AFTER both
  halves, immediately before the act. A ledger opened now would be an entry held open across a wait.
- `SCAN DENOMINATOR: 16 of 16` -- the sentinel scan is complete, not sampled, so `listed OPEN/HELD=0` is a measured
  zero rather than an unread one.

## What happens next, in order

1. `1.0.0_SA_CTO~Z`'s half lands at HEAD of `box/sitez`; merge it in and re-read AC3 for `2 of 2`. A REFUSED half
   STOPS the act and is reported instead.
2. Open the NEVER-2 ledger `nfra-mcportal-cp2-close-request-grant` on this branch, two legs (apply, read-back),
   commit the entry AND its sentinel.
3. Apply through `safe-apply`, targeted to `aws_iam_role_policy.gw_mcportal_close_request_write` only.
4. Re-read AC1 (expect `actions=s3:PutObject resources=1 problems=0`) and AC2 (expect `6 of 6`, the put-request arm
   having flipped and the other five unmoved from the table above).
5. Close both legs with their proof and commit the close BEFORE reporting the AC reads.

If the apply fails mid-act: `aws iam delete-role-policy --role-name opal-gateway-role --policy-name
gateway-mcportal-close-request-write-policy`, close the entry as rolled back, report. No S3 object is written by this
seat at any point -- the simulation is the exercise.
