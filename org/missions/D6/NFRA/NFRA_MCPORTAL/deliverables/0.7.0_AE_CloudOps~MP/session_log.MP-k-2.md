# MP-k-2 -- the gateway role's one close-request write, applied and proven -- 0.7.0_AE_CloudOps~MP

**archetype:** DEPLOY
**secondary_archetypes:** VALIDATE

**Date:** 2026-10-09
**Task Order:** `NFRA_MCPORTAL.TO-MP-k-2` (workstream CP2, round 1; `<risk>WORLD</risk>`)
**Status:** COMPLETE

---

## Objective

Give `opal-gateway-role` exactly one new permission -- `s3:PutObject` on
`arn:aws:s3:::opal-313476888478-globgrph/fabric/open-calls/v1/box=*/requests/*` -- so the FWD-17 Control Plane page can
write a close-request object, and nothing else. Under a never-widen pair, with the apply gated on both halves.

---

## Compiler Tools

| Tool | Command | Result | Note |
|------|---------|--------|------|
| comp-iam gaps | `comp-iam gaps` (twice) | PARTIAL | First run: all zeros against a **0-service denominator** -- the cell's sparse list excluded the service trees, so that zero was "could not check". Re-run after widening to `infra/`: 36 missing / 52 deny-present / 1 coverage-unknown / 2 resource-mismatch across 30 services, 602 calls verdicted across 105 roles. All estate-wide and pre-existing; no row touches this role's grants or the globgrph `requests/` path |
| comp-iam (self-declared limit) | same run's banner | WARN | `DENY-OVERLAY INCOMPLETE: 7 deny statement(s) unparsed` -- it cannot answer "is this denied?", so it is a floor and AC2's simulation is the oracle |
| lib/opal_naming.py | `name('gateway', None, 'mcportal-close-request-write', 'policy')` | PASS | Returned `gateway-mcportal-close-request-write-policy`; match against the order's literal verified `True`. The name was read from the builder, never typed |
| naming-gate (commit limb) | via `safe-commit.sh` | PASS | `NAMING CONFORMANT ... CONFORMANT as IAM_POLICY / NAMING-GATE: PASS 1 graded`. This is the limb that only RAISEd (G3) on MP-x-3's interpolated name and then refused it at apply |
| terraform | `fmt -check`, `init`, targeted `plan`, targeted re-plan | PASS | fmt rc=0; init rc=0 from the local cache (aws 5.100.0, external 2.4.2); plan `1 to add, 0 to change, 0 to destroy`; post-apply targeted re-plan `No changes` |
| safe-apply | `-chdir=... apply C:/tmp/mp-k2.tfplan` | PASS | rc=0, and NOT cited as the proof -- see Verification |
| safe-apply (plan) | `-chdir=... plan -target=...` | FAIL | rc=2 by design: gates `apply` only. Row Z-S22 |
| deploy_ledger.py | `open` / `close-leg` x2 / `close` / `check` | PASS | Entry opened before the act with its sentinel, both legs closed with proof, entry CLOSED, sentinel removed, `check` shows it absent from the open set (16 of 16 sentinels scanned) |
| proof-of-spec-check.py | on this cell's instance | see instance | recorded in the instance's own `compiler_tools` |

**What worked:** the builder + literal-name route cleared the naming limb at COMMIT time, which is exactly the trap that
stopped MP-x-3 after its ledger was already open. The issuer's AC2 script is well-built: one `--resource-arns` per
call, each its own invocation, and a GetObject positive control inside the sheet.

**What failed:** `safe-apply` cannot run a plan (rc=2, by design -- row Z-S22). `comp-find 'TO-MP-x-4' --files
--limit 20` exceeded the 120 s tool timeout earlier in the session; native `Glob` answered the same question in one
call.

**Gap found:** two, both banked as rows. (1) A `<round>` tag and a gateway RELEASE number are different series in
NFRA_OPLGTW, so a census keyed on `<round>29</round>` returns rows -- a plausible non-empty answer to a question not
asked. (2) `comp-iam gaps` run inside a sparse worktree returns a clean-looking all-zero sheet whose denominator is
`0 services scanned`; the zero and the denominator must be read together or "could not check" reads as "no gaps".

---

## Deployment Sequence

| Step | Action | Result |
|------|--------|--------|
| 1 | Worktree cut from `box/sitez`, no-cone sparse | `C:/tmp/mp-k2`, branch `wk-mcportal-cp2-k2`, base `5db9d4cbab` (first cut was discarded: MSYS resolved `/tmp` to a path containing a space) |
| 2 | Builder read for the policy name | `gateway-mcportal-close-request-write-policy`, match `True` |
| 3 | New `.tf` + comment-only `graph-read.tf` R3 extension | `77184244cf`; non-comment diff of `graph-read.tf` measured EMPTY |
| 4 | `comp-iam gaps`, real denominator | see Compiler Tools |
| 5 | Targeted plan, saved | `1 to add, 0 to change, 0 to destroy` -> `C:/tmp/mp-k2.tfplan` |
| 6 | ASK written and committed | `NEVER_WIDEN_ASK_MP-k-2.md` @ `77184244cf` |
| 7 | ONE message to both half-owners | `1 DELIVERED / 1 QUEUED` -- the CTO half's named owner was retired; see Decisions |
| 8 | Pre-act control banked | `MP-k-2_PRE_ACT_CONTROL.md` @ `1087f48ed1` -- AC1 NoSuchEntity, AC2 **5 of 6**, AC3 1 of 2 halves |
| 9 | NEVER-2 ledger opened + sentinel committed | `1087f48ed1`, slug `nfra-mcportal-cp2-close-request-grant`, 2 legs |
| 10 | THE ACT: `safe-apply` with the SAVED plan | rc=0 |
| 11 | Read-back AC1, AC2 | PASS; AC2 **6 of 6** |
| 12 | Legs closed with proof, entry CLOSED, committed | `542de4b7e8` |
| 13 | AC3 after the close commit | PASS, `2 of 2` halves |

Module drift found at step 11 and left untouched: row Z-S23.

---

## Verification

**rc=0 is not cited as proof anywhere.** The apply's own tail showed only module outputs, so the act was verified
against live state and config on three independent planes:

```
terraform state list | grep -c gw_mcportal_close_request_write   -> 1
terraform state list | grep gw_mcportal
  aws_iam_role_policy.gw_mcportal_close_request_write
  aws_iam_role_policy.gw_mcportal_fabric_read      <- MP-x-3, still present, untouched

k2.AC1.sh  -> actions=s3:PutObject resources=1 problems=0 / RESULT: PASS
              (the same call, pre-act: NoSuchEntity rc=254)

targeted re-plan -> No changes. Your infrastructure matches the configuration.
```

**The discriminating read -- AC2, before and after the same six arms:**

| arm | pre-act | post-act | moved? |
|---|---|---|---|
| put request (`s3:PutObject`, `requests/<id>.json`) | `implicitDeny` | **`allowed`** | YES -- the one arm this grant is for |
| put list (`open_calls.json`) | `implicitDeny` | `implicitDeny` | no |
| put result (`request_results/x.json`) | `implicitDeny` | `implicitDeny` | no |
| put activity (`activity/v1/...`) | `implicitDeny` | `implicitDeny` | no |
| delete request (`s3:DeleteObject`) | `implicitDeny` | `implicitDeny` | no |
| get list (`s3:GetObject`) -- CONTROL | `allowed` | `allowed` | no |
| | **5 of 6** | **6 of 6** | exactly one |

Exactly one arm moved. The GetObject control was `allowed` on both runs, so the five refusals are real refusals and
the post-act sheet is not an all-`implicitDeny` instrument fault -- which is CTO half condition 2, read as stated. The
delta is attributable to this one statement and to nothing else in the estate. A post-act `6 of 6` on its own could
not have established that, which is why the pre-act arm was banked before the act.

No S3 object was written by this seat at any point: the task order's BOUNDS make the simulation the exercise.

---

## Decisions Made

1. **Plan run with terraform directly, not `safe-apply`.** Step 2 directs the plan through `safe-apply`, which gates
   `apply` only and exits 2 before terraform runs, telling the caller to invoke terraform directly. Measured, filed as
   row Z-S22, no override taken. Step 4's apply does go through `safe-apply`.
2. **Sparse pattern list widened beyond the one the order names.** `lib/opal_naming.py` reads
   `infra/logic/registry/*.json`, `comp-iam gaps` needs the service trees for a denominator, and `commit-gate` and the
   owned-paths hook read root-level `comp-constants.config.yaml` and `.owned-paths.yaml`. Mechanical necessity for
   criteria the order itself sets; stated rather than silent.
3. **Did not re-point the never-widen pair myself.** The order named `1.0.0_SA_CTO~O`, retired by Andrew-direct
   ~07:4xZ ("we don't need CTO~O anymore, you just lead the fabric here"). My send to it returned QUEUED -- no reader.
   The record hands OPLGTW and the MCPINDEX addendum to `~Z` by name but says nothing of NFRA_MCPORTAL, so the issuer
   was asked rather than the half re-routed. It answered with AMENDMENT 3: the CTO half is `1.0.0_SA_CTO~Z`.
4. **Read the CTO half whole rather than trusting the issuer's summary of its two conditions.** The summary was
   accurate; reading it also surfaced that the signer's own live check (20 inline policies, none mine; PutObject
   `implicitDeny`) independently matched this seat's pre-act control.
5. **Left the module drift alone and filed it.** `aws_lambda_function.mcportal_grant_writer` and the absent
   `gateway/mail/commassist-bearer` secret are outside this cell's write surface. Row Z-S23.

---

## Files Modified

see commit messages: `77184244cf` (build + ASK), `1087f48ed1` (ledger open + sentinel + pre-act control),
`542de4b7e8` (legs closed, entry CLOSED, sentinel removed). Rows `290e48a54c` (Z-S22) and `761e08adf7` (Z-S23) are in
the SHARED tree, not this branch, per CLAUDE.md 14b's append-only inversion.

---

## Blockers

None at close. The two that occurred during the cell both cleared: the CTO half's named owner was retired (resolved by
the issuer's AMENDMENT 3), and `safe-apply` could not produce the plan (resolved by the wrapper's own documented
route, row Z-S22 accepted INERT by the issuer).

---

## Current State

`gateway-mcportal-close-request-write-policy` is **LIVE** on `opal-gateway-role`, one statement,
`Allow s3:PutObject` on `arn:aws:s3:::opal-313476888478-globgrph/fabric/open-calls/v1/box=*/requests/*`, no condition.
Read live by `k2.AC1.sh`: `actions=s3:PutObject resources=1 problems=0`. MP-x-3's
`gateway-mcportal-fabric-read-policy` is intact beside it and was re-proven by AC2's control arm. All three criteria
PASS. The NEVER-2 entry
`org/critical_paths/change_management/20261009T0935Z_nfra-mcportal-cp2-close-request-grant_deploy_completion.md`
is CLOSED with both legs proven and its sentinel removed; nothing of this cell's is left open.

Rollback is available and unexercised, touching no other grant:
`aws iam delete-role-policy --role-name opal-gateway-role --policy-name gateway-mcportal-close-request-write-policy`.

The grant is a ceiling, not an authority: who may ask to close a call is decided in the gateway's request handler, and
a request closes nothing by itself -- each box's own scan applies it and writes the result
(`open-calls-scan.py:407`, `:453`). The gateway is the sole production writer of `requests/` (census of all 11 write
verbs in that file; its only `requests/` put is inside the self-test).

Branch `wk-mcportal-cp2-k2` at `542de4b7e8` in worktree `C:/tmp/mp-k2`, **NOT drained** -- the issuer drains it. All
commits LOCAL; `box/*` is pushed by an MSTR or `box-sync`, not by this seat.

---

## Next Steps

1. `[2.0.0_SA_COO~MP]` Drain `wk-mcportal-cp2-k2` and re-run the three checks on the merged index as issuer.
2. `[2.0.0_SA_COO~MP]` Disposition rows Z-S22 (accepted INERT already) and Z-S23 (module drift; route the Lambda to
   the grant-writer cell's owner and the absent secret to the gateway mail path's owner).
3. `[0.7.0_AE_CloudOps~MP]` Holds `NFRA_MCPORTAL.TO-MP-x-4`, still `staged` on G-REL: OPLGTW r29 is merged
   @`76ff10095c` but not deployed, so the release base MP-x-4 step 1 reads does not yet exist on the host.
4. `[0.7.0_AE_CloudOps~MP]` `MP-r-2` is staged for this seat on G-REL2 per the GO of 09:32Z.
