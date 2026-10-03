# Never-widen ask -- OG-gw-2, the one catch-up apply of mcportal-grant-writer-lambda from af2d762970's closure

By: `2.0.0_SA_COO~O` (issuer), 2026-10-03 ~20:0xZ. Order:
`org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-gw-2.grant-writer-catchup-apply.md` (issued @d933ca8280).
Authority: the CTO's round-14 analysis R1 (`ledger/ROUND_ANALYSIS.round14.md` section 3 @cf6e539a6d). PHASE A evidence,
drained @9dd29bca73, all in `deliverables/0.9.0_WK_NFRA_OPLGTW~26/`:
- `ANNOUNCE_OG-gw-2.md`;
- `GW2_BEHAVIOUR_DIFF.md`, the file the CVO grades;
- `GW2_ENV_BEFORE.json`.

**Halves owed:**
- `1.0.0_SA_CTO~O` (CTO);
- `3.0.0_SA_CVO~O`, REQUIRED by R1, because `data_entitlement` and the contract decide whom grants admit;
- `2.0.0_SA_COO~O` (COO), signed in section 5.

All three are against THIS file at its commit.

## 1. The bytes

**Build.** The builder is pinned by OG-gw-1 (drained @d8968d7342) and prints `staging from deployed_commit af2d762970`.

**Content diff, deployed vs staged.** 11 files each side: 8 SAME, 3 DIFF, 0 only-deployed, 0 only-staged.
- `app/config.py`: 27507 -> 29788 bytes.
- `app/data_entitlement.py`: 31834 -> 32133 bytes.
- `org/standards/NFRA_OPLGTW_CONTRACT.json`: 8806 -> 9189 bytes.
- The grant writer's own `lambda_function.py` is SAME.

**Targeted plan** (`-target=aws_lambda_function.mcportal_grant_writer`; the two variables fed in memory from the live
function's environment):
- `0 to add, 1 to change, 0 to destroy`;
- the only changing attributes are `last_modified` and `source_code_hash` (`nhz+dwJs...` -> `ZyYCPPyP...`);
- `environment` is unchanged (3 keys).

**Tests.** Against the staged closure: 21 passed, 0 failed (20 writer tests and 1 provenance test).

**Rollback.** The deployed zip is saved outside the repo: 54650 bytes, sha256 `9e1cfe77...df732`. Extracted into a
rollback worktree's `.build/staged`, the same targeted plan reads `No changes` (hash equal to live). After the apply, the
rollback is the reverse hash move on the same single resource, Terraform only.

## 2. Blast radius -- what the act may touch

**Function code.**
- Before: a 2026-09-30 build (`nhz+dwJs...`).
- After: `af2d762970`'s closure (`ZyYCPPyP...`).
- Rollback: the targeted apply of the saved deployed bytes.

**Function environment, role, policies, layer.** Unchanged (`gw2.AC2` grades the environment hashes). No rollback is
needed.

**What the writer ADMITS -- the one widening.**
- Before: every `dim_transaction` grant candidate is REFUSED, because the contract carries no `fields.dim_transaction`.
- After: a candidate whose `dim_transaction` columns are a non-empty subset of the 15 catalogued columns is ADMITTED.
  The 15 are `account_ref, business_date, trade_date, settlmnt_date, tr_cd, sb_cd, transaction_category, tran_srcde,
  debit_credit, cusip, ticker_symbol, quantity, price, gross_amount, net_amount`. Any other column is still REFUSED.
- Rollback: the code rollback restores the refusal.

**Existing grants and profiles.** Unchanged; the apply rewrites no record. Revoke reads no contract key.

**Not touched, by name:** the gateway (it already serves this contract on `af2d762970`), every other Lambda, the portal,
the grant store, and every other Terraform resource. No grant is written; no portal flow is driven.

## 3. The named property and its writers

**(a) Which grants the writer admits.**
- Writers, N = 2: `admin.validate_candidate`, which reads the contract's `fields`, and the contract JSON's
  `fields.dim_transaction`.
- Expected, measured in-process on both closures (`GW2_BEHAVIOUR_DIFF.md` section 6):
  - `dim_position/account_ref` stays ADMITTED (the control);
  - `dim_transaction/cusip` and the 15-column set go REFUSED -> ADMITTED;
  - `dim_transaction/gross_amount+bogus_col` is still REFUSED, on `bogus_col` only.
- The admission still needs the verified owner (`NOT_OWNER` otherwise). The masters stay `08242234`/`08335338`,
  accounts stay explicit per master, and operations stay `list/describe/query/download_filtered`.
- Other branch: if the read-back (`gw2.AC1`) shows any file not equal to the staged closure, or the environment hashes
  move (`gw2.AC2`), roll back.

**(b) The function's configuration.**
- Writers, N = 1: Terraform's `environment` block, unchanged by the targeted plan.
- Expected: `gw2.AC2` reads 3 of 3 hashes equal. Other branch: any change, so roll back.

## 4. Act and verify (PHASE B, from the order)

1. Re-read that the deployed `CodeSha256` is still `nhz+dwJs...` and the manifest still names `af2d762970`.
2. Open ledger `nfra-oplgtw-grant-writer-catchup` (entry and sentinel committed before the act).
3. Re-plan to the same shape, then run the targeted `safe-apply`.
4. Immediately run `gw2.AC1` (deployed = staged, file by file) and `gw2.AC2` (environment unchanged), and read
   `State`/`LastUpdateStatus` = `Active`/`Successful`.
5. Any failure: roll back, re-verify, close ROLLED BACK.

## 5. Halves

**COO -- SIGNED, `2.0.0_SA_COO~O`, 2026-10-03 ~20:0xZ.**
- The act may touch exactly the function's code. It widens exactly one admission: `dim_transaction` grants over the 15
  catalogued columns, which only the verified owner can then write.
- This aligns the writer with the contract the gateway already serves on `af2d762970`; no data is served by the act
  itself.
- The rollback is pre-measured and Terraform-only.
- Writers are counted in section 3, with both branches named.

**CTO -- owed.**

**CVO -- owed.** Required: the admission change in section 2.
