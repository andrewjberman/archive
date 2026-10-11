# Never-widen half (COO) -- OG-gw-1, rebuild `mcportal-grant-writer` from the live gateway release

By: `2.0.0_SA_COO~O` (issuer), 2026-10-11 ~18:5xZ.
Against: `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~56/NEVER_WIDEN_ASK_OG-gw-1.md`, drained @975fb09fca
(Phase A; gw1.AC1 and gw1.AC2 PASS, instance VALID).

## SIGNED section 6 (the one apply), with three conditions

What this seat read at signing:
- The zip carries `data_entitlement.py` and the contract byte-equal to live `c3af8687e4`. The contract-staging test
  passes.
- The targeted plan reads `0 to add, 1 to change, 0 to destroy` at rc=0. The one change is the function's
  `source_code_hash`.
- 7 of 11 members are identical and 4 move (data_entitlement, schwab_entitlement_admin, the contract, config). They move
  from the old pins `adc979b13b`/`db92656c72` to the live release.

1. **Condition A, the apply.** It is cut as its own applier order under its own ledger. A FRESH targeted plan at the act
   (`-target=aws_lambda_function.mcportal_grant_writer`) runs from a box/sitez-HEAD worktree and reads the same single
   row at rc=0 before the apply. The re-plan afterwards reads 0/0/0. It passes `-var market_update_s3_root=<address()
   output>`, required on that root since @f769ef6103 (OG-mu-1 half, condition B). Through `safe-apply` only.
2. **Condition B, the read-back (replaces section 5's owner-session grant write).** A grant written through Andrew's
   session is an Andrew act, so it is not part of this pair. The mechanical read-back needs no session and writes
   nothing:
   - (i) the live function's `CodeSha256` equals the built zip's hash;
   - (ii) the DEPLOYED package (`get-function` Code.Location) parses
     `{"mode":"rolling_complete_window","calendar_months":13}` with its own `parse_scope` and accepts it. Before the
     apply, the prior package refuses it, as row W42-S1 measured; that is the negative control.

   The first real 13-month grant Andrew writes is the organic confirmation and is not a gate here.
3. **Condition C, rollback.** Redeploy the prior `code_sha256` (`ZyYCPPyP5CV53eZP+UJHIgAjq834J4OsvePgmS6k8rI=`) through
   the same Terraform path. No grant is written by the act, so nothing else is undone.

## Not covered

Any grant write, revoke or principal change; any other resource in the `opal-gateway` root.

-- 2.0.0_SA_COO~O
