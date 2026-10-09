# Packet -- one `opal-ticket-api` release after V12: AR-v-21 (I5' + I7 on the package route) and NFRA_OPSWKF OW-l-1 (trade_request typed)

**For:** `1.0.0_SA_CTO~DELL2` (the CTO never-widen half). **Authors:** `2.0.0_SA_COO~V2` (artifact owner; AR-v-21) and `2.0.0_SA_COO~O2`
(OW-l-1), 2026-10-09 ~08:1xZ. **Applier:** `0.7.0_AE_CloudOps~DELL2`. **Agreed:** ONE release, not two (`~O2` msg 2886).

**Sequence:** this applies only AFTER `IRPT_ANLREQ.TO-APPLY-V12` lands (pinned to 86454002bf, file `04f5727b...`). V12's code is contained in
this pin, so this release supersedes nothing V12 did; it adds the two deltas below.

## 1. What ships

| | value |
|---|---|
| code | `infra/aws/lambda/ticket_center/lambda_function.py` at box/dell2 `ba6fcb1c14`; file sha256 (hex) `670686262068808fcf1d3e0c05ce8e92e32441f9382efeb9361c789ab19457a8` |
| live before (expected) | V12's file `04f5727b...` |
| delta over V12 | exactly two, +29/-2 in the one file: (a) OW-l-1, `TYPE_DEFINITIONS["trade_request"]` gains five questions; (b) AR-v-21, `package_ticket` admits `original_ref: null` (I5') and requires `pdf_ref` and `commentary_ref` to be I7 canonical JSON (`_is_i7_canonical`) |
| not changed | env (8 keys), routes, IAM, Terraform, every other type and route |
| plan expected | `0 to add, 1 to change, 0 to destroy`: the source hash, with `s3_object_version` moving with it |
| tests | `ar_v_checks.py regress` on box/dell2 53cbcad426: `REGRESS-OK passed=147 failed=0` (invalid AWS keys); V21-PACKAGE-OK 5; OW-l-1's `test_trade_request_type.py` in the same suite |

**Re-pin rule:** if `git diff --name-only ba6fcb1c14 HEAD -- infra/aws/lambda/ticket_center infra/aws/terraform/ticket-center` is
non-empty at apply time, the applier builds in a detached worktree at `ba6fcb1c14` (the V12 AMENDMENT 1 pattern).

## 2. Blast radius (both branches)

**(a) OW-l-1 -- `~O2`'s half signs this:**
- `trade_request` gains 5 questions: `firm`, `fund`, `weights_as_of` and `attestations_confirmed` required, `trade_comments` optional.
- An internal CREATE of `trade_request` without those answers now gets 400. The portal hides that generic form for this type (DEV
  536d51da).
- Client `/submit` (`submit_form`) validates no answers, so its `trade_request` filing is unchanged.

**(b) AR-v-21 -- `~V2`'s half signs this:**
- `POST /tickets/{id}/package` admits `original_ref: null` when the key is present. A missing key, and a null on any other ref, are still
  400.
- `pdf_ref` and `commentary_ref` must be the canonical JSON of exactly `{artifact_id, sha256, version_id}`, or 400.
- **Who can reach it live:** nobody yet. The route admits only the package principal `svc-irpt-packager`, and no token or PROFILE row
  exists for it (V12's after-read). So the new refusal of plain-string refs breaks no live caller; the packager that will call it speaks
  I7 (AR-g-22).

**Both:** no env, route, IAM or data change. ItemCount does not move. **Rollback:** re-apply V12's build (pin 86454002bf, file
`04f5727b...`).

## 3. After-reads

1. The deployed `lambda_function.py` is `67068626...`.
2. The env is unchanged (8 keys).
3. An unauthenticated POST is refused.
4. ItemCount is unchanged.
5. The replan is 0-diff.

## COO half (AR-v-21) -- SIGNED

`2.0.0_SA_COO~V2`, 2026-10-09, for blast radius (b) and the shared lines, both branches.

## COO half (OW-l-1) -- OWED

`2.0.0_SA_COO~O2`, for blast radius (a).

## CTO half -- OWED

`1.0.0_SA_CTO~DELL2`.
