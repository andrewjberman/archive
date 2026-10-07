# REPORT -- MDPF_HEALGAP.TO-HG-d2, the Rebalancer runner's second attempt is wired

**Seat:** `0.7.0_AE_CloudOps~F` (laptop). **Order:** `MDPF_HEALGAP.TO-HG-d2` @dff3c744f1, issuer `2.0.0_SA_COO~G1`
(dell1). **Risk:** WORLD. **Outcome: both criteria PASS; the ledger is CLOSED with nothing stranded.**

The order's REPORT section asks for the ledger entry path, the plan's change lines, the apply output tail, both
checks' output, commits and push state. In that order.

## Ledger entry

`org/critical_paths/change_management/20261007T1621Z_mdpf-healgap-hg-t2-reattempt-apply-20261007_deploy_completion.md`
-- opened at deploy START with 5 legs and an 8h window, CLOSED with all 5 proven and the
`.open_deploys` sentinel removed.

## Act 0 -- the SKIP probe (CTO half @a79f7ea1b7 condition 1)

One `RequestResponse` invoke of `cot-rebalancer-runner` with `{"mode":"pull"}`, 2026-10-07T16:15:36Z, RequestId
`6fe29f10-fadc-4f05-9070-95b68cc7f072`, StatusCode 200, no `FunctionError`.

- Response: `{"verdict": "SKIP-IDEMPOTENT", "as_of": "2026-10-07"}`
- Log (decoded `LogResult`): `cot-rebalancer-runner invoked 2026-10-07T16:15:36Z firm=cottonwood
  bucket=opal-data-assets date=2026-10-07`, then the same verdict. Duration 94.43 ms, Init 553.41 ms.
- Bronze `blackdiamond/cottonwood/bronze/rebalancer_{models,accounts,model_detail}/2026-10-07/`:
  **BEFORE 1/5/91 = 97, AFTER 1/5/91 = 97.** Newest `model_detail` key still `LastModified 2026-10-07T06:00:56Z`.
- Stamp `meta/2026-10-07-complete.json` unchanged at 11,679 B @ `06:00:58Z` -- a pull would have rewritten it.

No Black Diamond call was made. **Branch A is proven on the live plane**, which the CTO half recorded as the one
thing that had never run live. One invoke was spent: an earlier attempt exited rc=255 at CLI argument parsing
(`aws-cli/1.44.44` has no `--cli-binary-format`) and made no API call.

## The plan's change lines (act 2)

`CHECKPOINT_DISABLE=1 terraform -chdir=infra/aws/terraform/opal-assets plan -no-color -input=false
-target=aws_cloudwatch_event_target.cot_rebalancer_reattempt -target=aws_lambda_permission.cot_rebalancer_reattempt`

**`Plan: 2 to add, 0 to change, 0 to destroy.`** -- and no other resource line.

1. `aws_cloudwatch_event_target.cot_rebalancer_reattempt` will be created: `rule = "cot-bronze-complete"`,
   `target_id = "cot-rebalancer-runner-reattempt"`,
   `arn = "arn:aws:lambda:us-east-1:313476888478:function:cot-rebalancer-runner"`,
   `input = jsonencode({ mode = "pull" })`, `event_bus_name = "default"`, `force_destroy = false`.
2. `aws_lambda_permission.cot_rebalancer_reattempt` will be created: `action = "lambda:InvokeFunction"`,
   `function_name = "cot-rebalancer-runner"`, `principal = "events.amazonaws.com"`,
   `source_arn = "arn:aws:events:us-east-1:313476888478:rule/cot-bronze-complete"`,
   `statement_id = "AllowEventBridgeInvokeReattempt"`.

Only the expected `-target` warning and the no-`-out` note followed. `MSYS_NO_PATHCONV` was never set.

## The apply output tail (act 3) -- and what it does NOT say

`.tools/safe-apply.sh -chdir=infra/aws/terraform/opal-assets apply -no-color -input=false -auto-approve` with the
same two `-target`s, 16:47:12Z to 16:47:53Z.

**The captured stdout tail ended inside the root's outputs block and cut off the resource-count line, so that line
was never read and is quoted nowhere in this report, the ledger or the proof instance.** An unread line is not
evidence. The result is measured instead by two independent live reads:

- a targeted re-plan returns `No changes. Your infrastructure matches the configuration.`
- `terraform state list` carries both `aws_cloudwatch_event_target.cot_rebalancer_reattempt` and
  `aws_lambda_permission.cot_rebalancer_reattempt`.

**No HALTGT pass is cited.** `safe-apply` ran and its checkpoint did not block, but per ADHC_HALTGT / LD-0267 that
gate reads only unread files directly under `inbox/<serial>/`, so this seat's live inbox Monitor moves every
message before the gate can see it, and a `~lane` seat is unhaltable regardless. The gate cannot witness this
seat, so its silence is recorded as uninformative.

## Both checks' output (act 4's reads, run after the ledger-close commit as the order directs)

- **HG1-d2-AC1** -- `WIRED-OK target=cot-rebalancer-runner-reattempt input=pull
  other_targets=CotSilverOnBronzeComplete policy_sid=AllowEventBridgeInvokeReattempt` (rc=0).
  Base arm measured by this seat at ~16:09Z before the apply:
  `WIRED-BAD runner targets on cot-bronze-complete=0 (want 1); all=['CotSilverOnBronzeComplete']` -- identical to
  the base the order and both halves state from dell1 at ~14:1xZ.
- **HG1-d2-AC2** -- `UNCHANGED-OK code=HG-t-1 build retry=2 age=21600
  on_success=opal-assets-silver-blackdiamond daily=cron(0 6 * * ? *) input=pull` (rc=0). It also passes at the
  base, so it is a control: all of the discrimination sits in AC1.

Both were run twice, before and after the ledger-close commit, byte-identical.

## `record-terraform-deploy.sh` -- RAN and REFUSED by design

rc=2, nothing written: `basis : plan hgd2.tfplan (0 applied aws_lambda_function address(es))`, `stamped 0 of 15
rows under opal-assets: (none)`, `ERROR: resolved deployment set is EMPTY or unparseable -- REFUSING.` This apply
moves no Lambda code, so Deployment Rule 4's parity loop has nothing to close, and HG-d1 already closed it for
this function. Forcing the recorder with `--function cot-rebalancer-runner` would have overwritten a correct row
with this apply's timestamp; that was refused as a widening. Row owed -- see
`SURPRISE_ROWS_OWED_FROM_TO_HG_D2_20261007.md`, rows 1 and 2.

## The tree this ran in

`/c/tmp/wk-healgap-d2`, branch `wk-healgap-d2`, HEAD `8798e5f484` = `origin/CLOUD`, per `0.0.0_AB_MSTR`'s answer
relayed in msg 106398 and CLAUDE.md 14b: the shared laptop tree was 419 commits behind origin and is not being
merged while seats work in it. The applied `.tf` bytes are sha256
`0105df425f85c088d9b32d7ef8260f27d74ef71d2788821c338e85d2d032922a`, **identical to the ratified blob at the GO
commit `dff3c744f1`**. `terraform` v1.15.8 resolved on PATH; `.tools/terraform.exe` does not exist on this
device, exactly the case cloud-ops warns about. `init` reused the shared provider cache and downloaded nothing.

## Proof of spec

`org/missions/D8/MDPF/MDPF_HEALGAP/deliverables/0.7.0_AE_CloudOps~F/MDPF_HEALGAP.TO-HG-d2.apply-reattempt-target.proof_of_spec.json`
-- `VALID (rc=0)`, violations 0, acceptance rows 2, coverage 2/2, alignment ENFORCE clean on every limb
(`alignment-forward-1` 2/2, `alignment-forward-2` 1/1, `alignment-backward` 1/1, `invocation-alignment` 2/2
matching, 0 diverging).

## Commits and push state

| commit | what | push state |
|---|---|---|
| `1ad97815f3` | ledger OPENED + leg L1 (the act-0 probe), 2 files, exact pathspec | on origin (`0.0.0_AB_MSTR` confirmed it in `origin/CLOUD efc2e63467`, msg 106420) |
| `a536d4b391` | ledger CLOSED, all 5 legs, sentinel removed, 2 files, exact pathspec | LOCAL on shared `CLOUD` at the time of writing -- re-measure with `git ls-remote` |
| this commit | the proof instance, this report, the owed rows, and the `<status>` flip | LOCAL on branch `wk-healgap-d2`, awaiting `0.0.0_AB_MSTR`'s drain |

Both ledger commits used an exact two-path pathspec. `0.7.0_AE_CloudOps~S`'s concurrent `secclass-e65` entry and
sentinel were modified in the same shared working tree by that seat's own work and were deliberately kept out of
both commits -- the shared-surface hazard row `MDPF_HEALGAP-S6` names exactly this.

## What this order did NOT do

FWD-1 is **not** graded REALIZED here. This order wires the second attempt; the induced-failure exercise that
demonstrates it is `MDPF_HEALGAP.TO-HG-d3` (GO, relayed in msg 106443). AC3 of both halves -- the next normal
day's ~11:32Z fire read as `SKIP-IDEMPOTENT` with no new bronze key -- belongs to the issuer on 2026-10-08; the
act-0 probe is the same behaviour proven by direct invocation, and is not offered as AC3. No refill of past dates
(FWD-3, Andrew's ACT 2 answer was no).

-- `0.7.0_AE_CloudOps~F`, 2026-10-07
