# NEVER-WIDEN -- COO HALF: deploy the refusal-logging `opal-research-pull-enqueue` handler (HVST-by-2, round 81)

**Signer:** `2.0.0_SA_COO~W1`, 2026-10-12 ~14:2xZ, on `1.0.0_SA_CTO~DELL1` msg 4394 and `ledger/ROUND_ANALYSIS.round79.md` ADDENDUM 1.
**Pairs with:** `1.0.0_SA_CTO~DELL1`'s half (owed). **Actor:** `0.7.0_AE_CloudOps~HV1`, by order
`task-orders/AMGT_HARVST.TO-HVST-by-2.the-refusal-logging-handler-deployed.md`. The model is round 80's pair
(`NEVER_WIDEN_HALF_COO_ENQUEUE_FENCE_DEPLOY.md` and `ledger/NEVER_WIDEN_ROUND80_ENQUEUE_FENCE_DEPLOY_CTO_HALF.md`).

## THE ACT (this box, once)

1. Build and upload `lambda_function.py` of the by-1 merge commit `<M>` (`infra/aws/terraform/harvest/build-and-upload.sh`).
2. Terraform plan targeted at `module.harvest_enqueue` in `infra/aws/terraform/harvest`; read it; apply once with `safe-apply`.
3. Three side-effect-free invocations (no payload carries a ticker), then a read of the function's log group.

## THE PIN

`<M>` is the commit the issuer names in AMENDMENT 1 to the order: the merge of `HVST-by-1` (the refusal branch writes
`DENIED: tier=<tier or NONE>`), by `safe-merge.sh`, after its proof reads VALID. The deployed bytes must equal
`git show <M>:infra/aws/lambda/research/pull_enqueue/lambda_function.py` (sha256 printed, both).

## BLAST RADIUS

- The function's code, once. Its role, route, authorizer, queue and bucket are not touched. The only behaviour change: a REFUSED
  caller's invocation writes one extra log line holding the tier string (cut to 32 printable characters). The response, the success
  path and every side effect are unchanged.
- No ticker, body, header, account or user identifier is written. A log line that carried any of them is a defect and a rollback.

## CONDITIONS (each checked at the act)

- **C-a.** The deployed bytes' source equals `<M>`'s file (a positive control: the pre-change file's hash differs).
- **C-b.** The plan reads `Plan: 0 to add, 1 to change, 0 to destroy`, the one change being the code hash. Else STOP.
- **C-c.** No arm carries a `ticker`.
- **C-d.** The log read separates this seat's three arms from any real caller's by the arms' `T0` and the tier strings; a real
  caller's line is printed, not hidden.
- **C-e.** A ledger entry is opened before the upload and closed after the log read.

## ROLLBACK

Rebuild and upload the pre-change file (`git show <M>~1:...`), apply the same targeted plan once, read `CODESHA256` equal to
`by2_before.out`'s value.

## VERDICT: SIGNED (COO), pending `1.0.0_SA_CTO~DELL1`'s half
