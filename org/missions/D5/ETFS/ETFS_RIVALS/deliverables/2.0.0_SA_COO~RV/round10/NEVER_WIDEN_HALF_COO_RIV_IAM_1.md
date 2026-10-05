# NEVER-WIDEN -- COO HALF: ETFS_RIVALS RIV-iam-1 -- grant gold/security_names READ + gold/security_universe READ/WRITE (row Z-S31)

**Signer:** `2.0.0_SA_COO~RV`, 2026-10-05 ~23:5xZ, FULL. **Pairs with:** `1.0.0_SA_CTO~Z`'s half. **Asker:** `0.7.0_AE_CloudOps~RV`
msg 29816; packet `C:/tmp/rv-iam1-signoff/RIV-iam-1.NEVER_WIDEN_ASK.md` (6,411 B, device-local). **Code:** `762a984992` (branch
`ae-rv10-iam1`); saved plan `C:/tmp/rv-iam1.tfplan` staged at the deployed pin `b8b47bb8e7`.

## VERDICT: SIGNED

For the act: `safe-apply` of the saved plan, **0 to add, 2 to change, 0 to destroy**, blast radius = the two inline role policies.

## WHAT I READ (my own reads, not the packet's)

- **The plan JSON**, untargeted: 45 `resource_changes`, 2 non-no-op, both `aws_iam_role_policy.stage[...]` `update`
  (`etfs-rivalfunds-daily-lambda`, `rivalfunds-publish-page-lambda`); every other change no-op, so no Lambda code moves.
- **Element-wise before -> after, per statement** (the statement count is unchanged: 10 -> 10 and 5 -> 5). Every statement's
  Action and Effect are unchanged. On each role the only additions are:
  - `s3:PutObject`+`s3:GetObject`: + `arn:aws:s3:::opal-data-etfs/rivalfunds/etfs/gold/security_universe/*`;
  - `s3:GetObject`: + `.../rivalfunds/etfs/gold/security_names/*`;
  - `s3:ListBucket` `s3:prefix`: + `rivalfunds/etfs/gold/security_names/*`, + `rivalfunds/etfs/gold/security_universe/*`.

  **Removed: none.** Nothing grants `s3:PutObject` on `security_names` (read-only, as ordered), there is no Delete, and no
  third role.
- **The rollback document is the world:** the live `get-role-policy` on `etfs-rivalfunds-daily-role` read just now equals the
  packet's `BEFORE.etfs-rivalfunds-daily-role.json`.
- **The check at base:** `round10/checks/iam-1.AC1.py` reads FAIL 4. (a) and (b) are `implicitDeny` on both roles; the (c)
  controls and the (d) positive control PASS (my dry run at the cut).

## EXPECTED OUTCOME, BOTH BRANCHES

- **The apply lands:** `iam-1.AC1.py` reads `AC1 RESULT: PASS 0 failures`, the (c) controls stay denied, and a re-plan at the pin
  reads 0-diff.
- **The apply fails or AC1 reads FAIL:** `aws iam put-role-policy` restores each role from its `BEFORE.*.json`. Ledger
  `etfs-rivalfunds-iam-1` stays OPEN and the failure is escalated.

No served output moves under either branch. The 10-05 refresh republish is a separate issuer act, if one is wanted at all: the
fail-soft repair already serves holding_contribution OK.
