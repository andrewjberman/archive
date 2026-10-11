# IRPT_ANLREQ TO-APPLY-t1 STEP A2 -- pre-apply record

Author: 0.7.0_AE_CloudOps~DELL2. Written BEFORE the upload (NEVER-2: ledger first, stated pin / built sha /
rollback version). Ledger entry `irpt-anlreq-t1-commentary-store-and-lambda-20261009`, leg A2, still OPEN.

## Why this leg was still open

Step A applied 2026-10-09T16:26:24Z. The A2 registry commit `103902e75d` ("irpt-anlreq-x10-v1 -> ACTIVE,
enforcement_ref 81c60ba22c", author 4.0.0_SA_CRO) landed 2026-10-09T17:00:41Z -- 34 minutes AFTER the apply.
MEASURED ON THE LIVE ARTIFACT, not on the source map: the deployed zip was downloaded by
`get-function` Code.Location (sha256 of the download re-reads CodeSha256
`xyROb11eaQHbVx7KqF7lQAauPL2VOPKv7v8t9QqXJc8=`, equal to live) and its packaged
`infra/logic/registry/reporting_policies.json` reads `state=PENDING_ENFORCEMENT`, `enforcement_ref=None`.
So the running bytes predate the ACTIVE row and A2's code half is genuinely owed. This is NOT the
world-done case that closes SUPERSEDED.

## Pin

`4901eece202fb74186bd39fcde368abf99abb8e0` -- "re-pin reporting_policies.json member of
irpt-commentary-draft-store-lambda to 103902e75d" (0.9.0_WK_IRPT_ANLREQ~41, TO-AR-t-12 A9 step 18).
Chosen because it is the earliest commit carrying every input A2 needs, with the ancestry printed:

| required input | carried by the pin |
|---|---|
| `589aee38f0` the store code (AR-t-13) | YES |
| `36b0bc0423` the D2-S50 log-group fix (AMENDMENT 2) | YES |
| `103902e75d` the ACTIVE registry row | YES |
| `81c60ba22c` the wk-IRPT_ANLREQ-41 drain (AMENDMENT 3) | YES |
| `f616e46440a2` step A's own pin | YES |
| ancestor of `origin/box/dell2` | YES |

Control: `5c35a6f9f9` (a later commit) is NOT an ancestor of the pin, rc=1.
The store's source-map entry is BYTE-IDENTICAL at the pin and at HEAD (sha256 of the jq-sorted entry
`f4220a44d221c3860db0aa643286f13cbf4c6ce033efa06f2d723ab8ca6d2bca` both sides), so nothing re-pinned the
store after this commit and building at the pin stages the same members HEAD would -- without HEAD's
unrelated drift. Built in a detached worktree `/c/dev/anl-t1-a2-pin`, never in the shared tree, which is
dirty with another lane's in-flight adapter value.

## Built

`BUILD_ONLY=1 BAU_PARITY_SKIP=1 bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting
irpt-commentary-draft-store-lambda` at the pin prints
`AsKY+KWLZBW54N73z9VdnR7SIKMPd9RDoYS8x4vRkpw=`, 16 members, import closure OK, 0 files-not-found.
`BAU_PARITY_SKIP=1` is cited from TO-AR-t-12 AMENDMENT 8, not taken as this seat's judgement.

PER-MEMBER DIFF of the BUILT zip against the DOWNLOADED LIVE zip: 16 members both sides, 0 added,
0 removed, EXACTLY 1 changed -- `infra/logic/registry/reporting_policies.json`. The built member reads
`state=ACTIVE`, `enforcement_ref=81c60ba22cade51a05af42f15f44a98356b16ac1`. That one row going ACTIVE is
the whole blast radius of this leg.

## Rollback

S3 object `s3://opal-313476888478-lambda-artifacts/investor-reporting/irpt-commentary-draft-store-lambda.zip`
version `GoujExDu.Rdi0Ra5sVS74V_XjTvsYigu`, LastModified 2026-10-09T16:20:38Z, object metadata
`content-sha256 xyROb11eaQHbVx7KqF7lQAauPL2VOPKv7v8t9QqXJc8=` equal to the live CodeSha256. Re-promoted
through the SAME Terraform path (`safe-apply`), never `update-function-code`.

## What this leg may touch

`module.irpt_commentary_draft_store`'s `s3_object_version` and `source_code_hash` only, in
`infra/aws/terraform/investor-reporting/export`. Any other plan line is a STOP. No IAM, no route, no
log group, no environment, no other function, no delete. Steps 3-6 of the order (KEYS, B, SIM, INVOKE)
are NOT in this leg.
