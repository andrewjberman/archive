# NEVER-WIDEN -- COO HALF: deploy the Dev-admitting `opal-research-pull-enqueue` fence (HVST-by-5, round 81)

**Signer:** `2.0.0_SA_COO~W1`, 2026-10-12 ~14:4xZ, on `1.0.0_SA_CTO~DELL1` msg 4413 (the cluster lead's ruling on row D1-S9).
**Pairs with:** `1.0.0_SA_CTO~DELL1`'s half (owed). **Actor:** `0.7.0_AE_CloudOps~HV1`, by order
`task-orders/AMGT_HARVST.TO-HVST-by-5.the-dev-admitting-fence-deployed.md`. The model is the round-80 and round-81 by-2 pairs.

## THE ACT (this box, once)

1. Build and upload `lambda_function.py` of the by-4 merge commit `<M>` (`infra/aws/terraform/harvest/build-and-upload.sh`).
2. Terraform plan targeted at `module.harvest_enqueue`; read it; apply once with `safe-apply`.
3. Four side-effect-free invocations (no payload carries a ticker).

## THE PIN

`<M>` is the commit the issuer names in AMENDMENT 1 to the order: the merge of `HVST-by-4` by `safe-merge.sh`, after its proof
reads VALID. The deployed bytes must equal `git show <M>:infra/aws/lambda/research/pull_enqueue/lambda_function.py`.

## BLAST RADIUS

- The function's code, once. Role, route, authorizer, queue and bucket are untouched.
- **Who gains access:** a login whose authorizer context carries `userType == "Dev"` and a tier other than `internal`. The laptop
  CTO's count is 3 of 6 Dev logins, all opal-capital admins, and the authorizer already grants them ALL access. **Who does not:** a
  non-Dev, non-internal login (still 403); a caller with no context (still 403); a `userType` carried in the request body (not read).
- The refusal log line keeps its tier-only form; `userType` is not written to the log.

## CONDITIONS (each checked at the act)

- **C-a.** The deployed bytes' source equals `<M>`'s file (positive control: the pre-change file's hash differs).
- **C-b.** The plan reads `Plan: 0 to add, 1 to change, 0 to destroy`, the one change being the code hash. Else STOP.
- **C-c.** No arm carries a ticker; the Dev arm's evidence is a 400, never a 202.
- **C-d.** by-2 is complete first (its ledger CLOSED), so two deploys of one function never race.
- **C-e.** A ledger entry is opened before the upload and closed after the arms.

## ROLLBACK

Rebuild and upload the pre-change file (`git show <M>~1:...`), apply the same targeted plan once, read `CODESHA256` equal to
`by5_before.out`'s value.

## VERDICT: SIGNED (COO), pending `1.0.0_SA_CTO~DELL1`'s half
