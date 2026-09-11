# Session log -- `0.9.0_WK_IRPT_BCKEND~3` on `IRPT_BCKEND.TO-IB-s-8`

Worktree `/c/tmp/wk-irpt-1-3`, branch `wk-irpt_bckend-1-3`, cut from `7d7f33569a`. One task order, one slot.

## Order of acts

1. **The bar.** `git rev-parse --abbrev-ref HEAD` -> `wk-irpt_bckend-1-3`; `test -d org && test -d .tools`
   -> `TREE-OK`. The worktree carries every path the face names.
2. **Re-grounded the face's premises against live state, before building anything.**
   - `infra/aws/ec2/bd-49f-auto-login/` -- present (604-line runner, wrapper, package.json, secret-ids.env).
   - `infra/aws/terraform/investor-reporting/ycharts/` -- the IB-s-18 skeleton, `main.tf` only, no resources.
   - `infra/aws/lambda/ycharts-market-data-pull/ycharts_client.py` -- present; it is the ONE carrier of the
     probe route, the 200-and-only-200 predicate, the `concurrent sign in` eviction discriminator and the
     three session cookie names. Everything the library asserts about "what a live seat is" is read from it.
   - `infra/aws/terraform/investor-reporting/core/dynamodb.tf` -- `irpt-jobs` already declares
     `lease_owner`, `lease_expires_at`, `fence_token`. So the lease needed no new table.
   - **The three secrets, by name.** `ycharts/login/credentials` one version AWSCURRENT;
     `ycharts/session/current` **`VersionIdsToStages = null`** -- exists, no version at all, which is the
     Phase-1 read the order asked for and which shaped `getSession`'s contract; `astn/kimi/api-key` one
     version AWSCURRENT.
   - **Two premises did NOT hold** and are filed as rows, not worked around silently:
     `IRPT_BCKEND-W3-S1` (no browser is installed; installing one is egress this order does not authorize)
     and `IRPT_BCKEND-W3-S2` (the HAR packet is absent and the sanitized evidence carries no login flow).
3. **Built the library** `infra/aws/ec2/investor-reporting-ycharts/ycharts_session.js` -- five surfaces,
   four declared rules, every outside edge an injectable port with a lazy default, so the module imports with
   no playwright, no AWS and no network.
4. **Built the offline proof** under `tests/`: loopback replay whose app routes and statuses are DERIVED from
   the sanitized HAR evidence (`fixtures/har_derived_routes.json`, sha256 of its source recorded), a
   Playwright-shaped replay browser, injected secrets and lease ports that can REFUSE, and `netguard.js`.
5. **Planned, opened the ledger, applied, verified, closed, committed the close -- in that order.**
   `plan` -> `9 to add, 0 to change, 0 to destroy` (nothing existing touched).
   `deploy_ledger.py open --slug irpt-bckend-s8` (4 legs) -> sentinel written.
   `safe-apply` -> `Apply complete! Resources: 9 added, 0 changed, 0 destroyed.`
   `describe-instances` -> `stopped`; `plan` -> `No changes.`
   Legs L1-L4 closed with their proofs; entry CLOSED; close committed at `ded9f9741b` **before** the reads
   that grade the act were taken.
6. **Graded.** `S8-AC1` battery -> `IBS8-RUNNER-BUILT`, arms 6 of 6, rc 0. `S8-AC2` plan ->
   `No changes. Your infrastructure matches the configuration.`, rc 0.
7. **Controls.** One mutant (flip `CH-UNEXPECTED.handles_one_time_code` -> the arm-(b) predicate goes
   false), one determinism pair (22 of 23 deciding lines byte-identical; the 23rd differs only in the
   ephemeral loopback port).

## Instruments, and which of them are independent

- `comp-read --enumerate` over the library for one-time-code tokens: **17 hits** -- an independent third read
  agreeing with the battery's own source census denominator of 17.
- `comp-iam service irpt-ycharts-runner` (Phase 1, after the `.tf` existed): the role resolves on the
  DESIRED plane, 7 statements, resources concrete. `comp-iam gaps` (Phase 2): no gap row names this role.
- `comp-adversary compose` on the library: declaration written, `.scratch/adversary_ib_s_8.json`; it reports
  `T11: decomposition neighborhood NOT RESOLVED` because a `.js` source file carries no `<decomp_ref>` --
  that is the tool's honest exclusion, not a finding.
- **Arm (e) carries a positive control** because the replay's request log and the network guard are NOT
  independent in the direction that matters: the log can only see what arrived at the replay.

## Bounds held

No live vendor call. No OTP branch. No monitor, alarm, SNS or SES. No cross-firm reach. No served output
touched. No secret value read, printed, logged or committed. The host is applied STOPPED and was never
started. Every file written is inside this order's `<paths>` grant or this worker's deliverables folder.
`infra/aws/lambda/ci/lambda-source-map.json` is in the grant and is UNTOUCHED: this cell creates no Lambda.
