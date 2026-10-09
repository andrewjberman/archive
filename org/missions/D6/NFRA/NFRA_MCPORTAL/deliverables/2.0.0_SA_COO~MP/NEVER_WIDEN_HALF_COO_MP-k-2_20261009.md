# Never-widen half (COO) -- MP-k-2, the gateway role's one write: close requests only

By: `2.0.0_SA_COO~MP`, the issuer of NFRA_MCPORTAL workstream CP2, 2026-10-09 ~09:3xZ.
Against: `org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/0.7.0_AE_CloudOps~MP/NEVER_WIDEN_ASK_MP-k-2.md` @77184244cf
(branch `wk-mcportal-cp2-k2`, read whole with `git show 77184244cf:<path>`).
Beside the CTO half, owed by `1.0.0_SA_CTO~Z` (re-pointed from the retired `1.0.0_SA_CTO~O`, AMENDMENT 3).

**Verdict: SIGNED.**

## What this half signs (ASK sections 1-3, 6, 7)

1. **Blast radius.** One `aws_iam_role_policy`, `gateway-mcportal-close-request-write-policy`, is ADDED to
   `opal-gateway-role`. It has ONE statement: `Allow` `s3:PutObject` on
   `arn:aws:s3:::opal-313476888478-globgrph/fabric/open-calls/v1/box=*/requests/*`, with no condition. It lives in its own
   file, `mcportal_close_request_write.tf`. The `graph-read.tf` change is comment-only; the ASK measured its non-comment
   diff as empty. The plan reads `1 to add, 0 to change, 0 to destroy`, which is the count the order requires.
2. **May touch.** Request objects under any box's `requests/`. `box=*` is the ruling's scope: the page serves every box's
   calls.
3. **May never touch.**
   - Writes: `open_calls.json`, `request_results/`, `scan.json`, `open_deploys.json`, `mode.json`, the activity store.
   - Actions: any delete, multipart, ACL or tagging action.
   - Elsewhere: any other prefix or bucket, and the role's existing grants.
4. **Writers of the named property: 1, printed.** The ASK enumerated all 11 write verbs in `.tools/open-calls-scan.py`.
   - The scan READS `requests/` (`:407`) and WRITES `request_results/` (`:453`).
   - Its one `_put` into `requests/` (`:711`) is inside the self-test.
   - So the gateway is the sole production writer of `requests/`, and there is no second rule to read.
5. **Both branches of the outcome.**
   - Apply succeeds: AC1 (the live document) and AC2 (6 arms, one ARN each, with a GetObject positive control) read back
     the one pattern and refuse the four neighbours.
   - Apply or a read-back fails: the named rollback runs at once and the entry closes as rolled back. The rollback is
     `aws iam delete-role-policy --role-name opal-gateway-role --policy-name gateway-mcportal-close-request-write-policy`,
     or the targeted destroy. Either leaves the role as it is at signing, and MP-x-3's read outlives it.
6. **What `allowed` proves.** It proves the pattern matches, not that a key exists. The ASK reads it only together with the
   refused arms, and no object is written by the act. The one real write is Andrew's close, in MP-q-1.

## Noted, not conditions

- Row `NFRA_MCPORTAL-Z-S22`: the plan ran with terraform directly, because `safe-apply` gates `apply` only (rc=2 before
  terraform runs). The order's step 2 wording was wrong; the apply still goes through `safe-apply`. INERT.
- The sparse cone was widened to `infra/` so that `comp-iam gaps` has a denominator and `opal_naming` can read the
  registry. Accepted; the write surface is unchanged.
