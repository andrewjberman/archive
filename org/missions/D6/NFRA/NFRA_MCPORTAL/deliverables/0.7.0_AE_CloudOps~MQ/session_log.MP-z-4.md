# Session log -- `0.7.0_AE_CloudOps~MQ` -- NFRA_MCPORTAL.TO-MP-z-4

**Date:** 2026-10-13 (UTC). **Seat:** `0.7.0_AE_CloudOps~MQ`, a fresh MCPORTAL applier lane seated by
AMENDMENT 1 of the order after `0.7.0_AE_CloudOps~MP` read HUNG.
**Cell:** `MP-z-4`, workstream GW round 1, PRD v0.7 FWD-20.
**Branch / tree:** `wk-mp-z-4` in the linked sparse worktree `C:/tmp/mp-mq-z4`, cut from `box/sitez` HEAD
`6fe140d0a8`. The issuer drains it.

---

## What was asked

Grant the gateway instance role `opal-gateway-role` ONE new action -- `dynamodb:Scan` on
`gateway-access-state-table` -- so the FWD-20 breakdown can LIST who holds a profile. Build the `.tf`,
plan it, write the never-widen ASK, get both halves, open the NEVER-2 ledger, apply, read back, close.

## archetype: DEPLOY

## What was done, in order

1. **Startup.** `/watcher` (registered `0.7.0_AE_CloudOps~MQ`, PID 40372, Monitor armed), `/cloud-ops`,
   `org/XXX.md` A.1-E. Identity cross-checked against `org/mcp/liveness.json`: `~MQ` at PID 40372, no
   conflict with the five other live CloudOps lanes. Inbox: the issuer's GO, msg 33613, acked.
2. **Worktree.** Sparse, NO-CONE, from `box/sitez` HEAD. The order's MP-k-2 pattern list did not suffice;
   see the Z-S43 row and the Compiler Tools section.
3. **Built** `infra/aws/terraform/opal-gateway/access_state_principal_scan.tf`: ONE
   `aws_iam_role_policy`, ONE statement, `dynamodb:Scan` on `aws_dynamodb_table.access_state_new.arn`,
   literal name from the builder, header comment in the `mcportal_close_request_write.tf` style.
4. **Planned.** `1 to add, 0 to change, 0 to destroy`, targeted, saved to `.build/z4.tfplan`.
   `comp-iam gaps` run on both corpora with their denominators printed.
5. **ASK** written and committed with the `.tf` at `a667941f52`; ONE message to both signers.
6. **Halves.** `1.0.0_SA_CTO~Z` SIGNED @`d9b228d530` (conditions: own file and own policy name; a future
   index is not covered). `2.0.0_SA_COO~MP` SIGNED @`b12118d890` (conditions: apply the SAVED targeted
   plan through `safe-apply`, re-plan if the gateway Terraform moved; entry and sentinel committed before
   the act). Both conditions met and both measured, not assumed.
7. **Ledger** opened with 2 legs and its sentinel committed at `bb2470d479`, BEFORE the act.
8. **Applied** the saved plan through `safe-apply`, rc=0.
9. **Read back:** AC1 PASS. Both legs closed with proof; close committed at `1c605b70a2` BEFORE the AC
   reads were reported, as the order requires.
10. **AC1 PASS, AC2 PASS** after the close commit.

## What I got wrong, and what it cost

**I tailed my own apply and cut its summary line.** `safe-apply ... apply .build/z4.tfplan` was piped
through `tail -30`, which showed only the module's 28 outputs, so the `Apply complete! Resources: 1
added, 0 changed, 0 destroyed` line is gone and cannot be re-run. It is NOT quoted anywhere and NOT
reconstructed. Cost: the L1 proof rests on two other planes instead -- `terraform state show` reading the
exact one-statement document, and the targeted 0-diff re-plan at `-detailed-exitcode` 0 -- plus AC1's
live IAM read. That is arguably stronger evidence than the line I lost (`NEVER trust a producer's
self-report or rc=0`), but losing it was not a choice, and the fix is one line: never pipe an
irreversible act's stdout through a positional slice.

## Blockers

**None.** MP-z-4 is complete. `MP-z-5` (the gateway release) is STAGED on G-REL3 and waits on the
issuer's separate GO; it is not started.

## Compiler Tools

| tool | invocation | result |
|---|---|---|
| `lib/opal_naming.py` (Rule 30 builder) | `name('gateway', None, 'access-state-principal-scan', 'policy')` | PASS -- returned `gateway-access-state-principal-scan-policy`, compared to the order's literal by equality. First attempt raised `FileNotFoundError: infra/logic/registry/systems.json` because the order's sparse list excludes `infra/logic/`. Also used for `address('sharepoint','transcripts','bronze','market_update','date=X')` to feed the root module's one required variable -- builder output, never typed. |
| `comp-iam gaps` | run twice, two corpora | PARTIAL, and the two runs are the point. Worktree (with the new file): `3 trees (50 .tf files)`, all zeros -- a zero over 50 of 571 files, NOT the estate's. Shared tree at HEAD (without the file): `3 trees (571 .tf files)`, 222 roles, `37 missing / 305 deny-present / 1 coverage-unknown / 3 resource-mismatch across 34 services` -- the pre-existing baseline. The run self-declares `DENY-OVERLAY INCOMPLETE: 7 deny statement(s) unparsed` and 11 NOT-ATTACHED policy blocks, so it cannot answer "is this denied?". Treated as a DESIRED-plane floor; AC1's simulation is the oracle. |
| `comp-iam role opal-gateway-role` | worktree, with the new file | PASS -- `dynamodb:Scan` now reads twice on the role: the pre-existing Scan on `mcportal-grant-changes-table` and the new one on `gateway-access-state-table`. |
| `terraform` (v on PATH; site Z has no `.tools/terraform.exe`) | `fmt -check -write=false`; `init`; `plan -target -out`; `state show`; `plan -detailed-exitcode -target` | PASS. `fmt -check` rc=0 (read-only form: `-check`, never `-diff`, which writes). `init` installed all three providers from the shared tree's plugin cache at exactly the locked versions (aws 5.100.0, archive 2.8.0, external 2.4.2), so the order's step-5 provider STOP did not fire. Targeted plan `1 to add, 0 to change, 0 to destroy`. Post-apply targeted re-plan `No changes`, detailed exit code 0. |
| `.tools/safe-apply.sh` | the apply, and earlier a plan | MIXED, both halves recorded. APPLY rc=0 -- not cited as proof on its own. PLAN rc=2, `no 'apply' subcommand in the arguments`: the wrapper gates `apply` only, by design. That is row Z-S42. The HALTGT checkpoint raised no surface and is NOT cited: a HALTGT pass is not evidence you were not halted, and a `~lane` serial is unhaltable regardless. The pre-apply mail guard actually used is `/cloud-ops` 18a limb (a): `get_delivery_state(0.7.0_AE_CloudOps~MQ)` -> 3 of 3 rows READ, 0 unread, denominator printed. |
| `.tools/deploy_ledger.py` | `open` / `close-leg` x2 / `close` / `list` | PASS. `open` committed the entry and its sentinel itself at `bb2470d479`; `close` did NOT commit, so the close was committed by hand at `1c605b70a2` before any AC read was reported. `list` shows 13 of 13 sentinels scanned and this slug among none of them. |
| `.tools/surprise-row-gate.py` (via safe-commit) | row commit `f10642d375`, shared tree | PASS -- `2 new row(s) of 66 total checked (64 pre-existing, NOT re-graded)`, corpus pass clean against the baseline (`documents=511 rows=12964 failures=4 baseline=4 known=4 new=0`). Appended in the SHARED tree, not the worktree: CLAUDE.md 14b inverts for an append-only shared file. |
| commit-time naming limb (LGIC_ENFORCE DEC-6) | three refusals, then PASS | The NAME graded `NAMING CONFORMANT ... as IAM_POLICY` on the first attempt that reached it. The three refusals before it were all the PLACEMENT step failing closed on files absent from the sparse cone -- `comp-constants.config.yaml`, then `infra/aws/lambda/ci/lambda-source-map.json`, then `infra/aws/terraform/49f-value-parity/49f_value_parity.tf`. None was a verdict about the change. Row Z-S43. |
| `.tools/proof-of-spec-check.py` | on this cell's instance | see the instance's own `compiler_tools` entry. |

## Surprise rows filed

- **`NFRA_MCPORTAL-Z-S42`** (OBSERVATION, INERT) -- the order says "run the plan with safe-apply";
  safe-apply refuses any invocation without the literal word `apply`.
- **`NFRA_MCPORTAL-Z-S43`** (OBSERVATION, INERT) -- the order's MP-k-2 sparse pattern list cannot plan OR
  commit a gateway `.tf`; four fail-closed refusals, each naming one absent path. Carries the measured
  working list and the denominators that say why "add `infra/`" is not the answer.

Both `disarm_owner` `2.0.0_SA_COO~MP`, both committed in the shared tree at `f10642d375`.
