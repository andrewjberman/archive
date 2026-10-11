# Never-widen half (COO) -- OG-mu-1, the gateway's `.pptx` market_update writer and its one PutObject grant

By: `2.0.0_SA_COO~O` (issuer), 2026-10-11 ~18:2xZ.
Against: `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~55/NEVER_WIDEN_ASK_OG-mu-1.md`, drained @f769ef6103
(Phase A; mu1.AC1 and mu1.AC2 PASS, instance VALID).

## SIGNED, with three conditions

What this seat read at signing:
- **One statement.** `s3:PutObject` only, on `opal-data-transcripts/sharepoint/transcripts/bronze/market_update/*`,
  derived from a required, validated variable. No typed literal. It is a separate inline policy, so it can be removed
  alone.
- **Two writers, one key rule.** N = 2 (intake `place()` and the gateway tool), both naming `deck_<sha16>.pptx` under
  `date=<UTC>`. The same bytes on the same date are refused by the conditional put.
- **Order of acts.** The grant first, then the release, with rollback per act. The cross-day duplicate is a named
  residual.

1. **The ask's decisions are accepted as written:** the diff, the statement, both branches, writers N, the order of
   acts, rollback and the residual.
2. **Condition A, the grant act.** It is cut as its own applier order, under its own ledger. The plan is
   `-target=aws_iam_role_policy.market_update_gateway_put` (and its pure-name module), fed
   `-var market_update_s3_root=<address() output>`, and reads exactly that add at rc=0 before the apply. The targeted
   re-plan afterwards reads 0/0/0 at rc=0. It runs from a box/sitez-HEAD worktree, never a release root (row Z-S81).
3. **Condition B, cross-cell (the required variable).** The variable is on trunk since @f769ef6103, so EVERY plan or apply
   of the `opal-gateway` root from now on must pass the `-var` from `address()`. That includes OG-gw-1's apply and any
   later whole-root read. The issuer's release-cut template carries this clause. A plan that fails on a missing variable
   is a cut defect, never a reason to add a default.
4. **Condition C, the release.** The `.pptx` code ships only in a gateway release cut on the live ref after the grant's
   ledger closes. That release's own pair names the `ADVI_MARKET_UPDATE_S3_ROOT` `.env` key (52 -> 53 class) and the
   registered tool's `quarter` behaviour for `.pptx` (row Z-W55-S2).

## Not covered

Any Get, List or Delete; any other prefix or bucket; deleting written objects (a deliberate act outside this pair).

-- 2.0.0_SA_COO~O
