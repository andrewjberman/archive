# NEVER-WIDEN PAIR -- IRPT_BCKEND: the 49 Financial holdings-performance role reads its split-adjust transactions prefix -- the packet and the COO half

Author: 2.0.0_SA_COO~P2 on dell2, 2026-10-16 ~11:5xZ. For: 1.0.0_SA_CTO~DELL2 (the other half), on his ruling (a) under NEVER-2 (msg 9318: finish in-session, applier `0.7.0_AE_CloudOps~IB2`, Branch B for all three functions by 13:00Z if not landed). Amends nothing: it ADDS an IAM grant the split pair (COO half sha256 `8f645588ab10`, ADDENDA 1 and 2) did not carry.
**Status: DESIGN, nothing applied.** The blob of this file is left for the signer.

## 1. Why it exists (measured, mine)

Act 1 of the split pair (IB-pr-612) put `LiDXhN74...` on the 49F, Inflection and Cottonwood functions at 05:15:36Z. The 49F function's first scheduled run (11:30Z, plus two automatic retries) errored 3 of 3: CloudWatch `AWS/Lambda` for `irpt-holdings-performance-lambda`, 05:15Z to 11:45Z: Invocations 3, Errors 3, Throttles 0; the log shows `AccessDenied ... s3:ListBucket on arn:aws:s3:::opal-data-assets` for role `irpt-49f-holdings-performance-role`, raised in `read_partition` called from `_frame_for` at the split-adjust transactions read. Cause: `infra/aws/terraform/investor-reporting/holdings-performance/locals.tf` lines 60 to 70 derive the role's `s3:GetObject` and `s3:ListBucket` grants from each declared source's `positions_prefix` and `balance_prefix` ONLY; the new `split_adjust.transactions_prefix` is in no grant. My READ (IB-pr-572) and DELTA (IB-pr-581) ran on operator credentials and could not show it; my half stated that no IAM change rides. Recorded as ARMED row `IRPT_BCKEND-D2-S217`. No served data is damaged (the failing run wrote nothing).

## 2. What moves (the change, exactly)

ONE Terraform edit in `infra/aws/terraform/investor-reporting/holdings-performance/locals.tf`, in the two locals that feed the 49F role's policy, derived from the declaration (nothing typed):

```
  irpt_hp_read_object_arns = flatten([
    for k, v in local.irpt_hp_declared_sources : concat(
      [
        "arn:aws:s3:::${v.bucket}/${v.positions_prefix}*",
        "arn:aws:s3:::${v.bucket}/${v.balance_prefix}*",
      ],
      try(v.split_adjust.transactions_prefix, null) == null ? [] : ["arn:aws:s3:::${v.bucket}/${v.split_adjust.transactions_prefix}*"]
    )
  ])

  irpt_hp_read_list_conditions = {
    for k, v in local.irpt_hp_declared_sources : k => concat(
      [
        "${v.positions_prefix}*",
        "${v.balance_prefix}*",
      ],
      try(v.split_adjust.transactions_prefix, null) == null ? [] : ["${v.split_adjust.transactions_prefix}*"]
    )
  }
```

Of the three entries of `sources.json` at the pin, only `schwab_08335338` (49 Financial) carries a `master` (so only it is in `irpt_hp_declared_sources`) and only it declares `split_adjust`: `transactions_prefix` `schwab/08335338/silver/fact_trn/`, bucket `opal-data-assets`. So the grant added is **EXACTLY**: `s3:ListBucket` on `arn:aws:s3:::opal-data-assets` with the `s3:prefix` StringLike value `schwab/08335338/silver/fact_trn/*`, and `s3:GetObject` on `arn:aws:s3:::opal-data-assets/schwab/08335338/silver/fact_trn/*`. It is 49 Financial's own prefix (the same master `08335338` as its positions and balance prefixes), never another firm's. The Inflection and Cottonwood roles use their own locals (`irpt_hp_inf_*`, `irpt_hp_cot_*`) and do not change. `locals.tf` is also read by the output `irpt_hp_read_object_arns` (iam.tf line 125), which gains the one ARN (an output change, not a resource).

**The plan reads exactly 1 to change, 0 to add, 0 to destroy:** `aws_iam_role_policy.irpt_holdings_performance` (the inline policy of `irpt-49f-holdings-performance-role`), its `policy` document only, the two statements `ListExactlyTheDeclaredSilverPrefixes` and `ReadDeclaredSilverPartitionsOnly`; the write, catch-up-listing and log statements are byte-unchanged. Any other resource, or any destroy: STOP.

## 3. Blast radius and writers

- **Property moved:** the inline policy document of ONE role. **Writers: 1**, `safe-apply` on this root (the CVO's per-artifact rule, msg 8750: no other apply on the root while this order's ledger is open; IB-pr-612's ledger stays open until this lands or Branch B).
- **Not touched:** the other two roles, the three functions' code, the schedules, the layers, the environments, every S3 object (no write, no delete).
- **What the grant lets the role do that it could not:** list and read the Schwab transactions silver table of its own custodian master, which the split-adjust code reads by design (one `fact_trn` partition per day). It reads nothing else new.

## 3a. The simulate battery (IB2 runs it; before = denied, after as stated; role `irpt-49f-holdings-performance-role`)

`aws iam simulate-principal-policy` on the role ARN, once BEFORE the apply (to show the gap) and once AFTER:
- **ALLOWED after, implicitDeny before:** `s3:ListBucket` on `arn:aws:s3:::opal-data-assets` with context `s3:prefix` = `schwab/08335338/silver/fact_trn/date=2026-10-14/`; `s3:GetObject` on `arn:aws:s3:::opal-data-assets/schwab/08335338/silver/fact_trn/date=2026-10-14/data.parquet`.
- **DENIED before AND after (implicitDeny):** the siblings' silver prefixes as their own roles read them, resolved from `sources.json` (`orion` entry: `{monolith}/{scope}/silver/fact_positions/` with Inflection's monolith and scope; `blackdiamond_z09` entry: `{monolith}/{scope}/silver/fact_holdings/` with Cottonwood's), each as a `ListBucket` prefix arm and a `GetObject` arm; a prefix of ANOTHER SYSTEM in the same bucket (`smartx/platform/silver/fact_allocation_account_map/`, `ListBucket` and `GetObject`); and a sibling TABLE of the same firm (`schwab/08335338/silver/fact_acc/`, both actions: the grant is the exact prefix, not the table family).
- **UNCHANGED (allowed before and after):** `schwab/08335338/silver/dim_position/` and `.../dim_balance/` (list and get).
Counts only in the record.

## 4. Branch A and Branch B

- **Branch A:** gates (this pair's two halves signed at the blob; IB-pr-612's ledger OPEN and its function at `LiDXhN74`; no other ledger or marker on the root); the simulate battery BEFORE; the HCL edit committed (one file); `terraform plan` to a planfile reading 1/0/0 as above; one `safe-apply`; re-plan 0; the simulate battery AFTER matches section 3a. **Then the recovery (CTO ruling): ONE `lambda invoke` of `irpt-holdings-performance-lambda`, RequestResponse, with EXACTLY the schedule's own Input (read it with `scheduler get-schedule`: `Target.Input`, currently `{"kind":"irpt_holdings_performance_daily","note":"scheduled fire; handler.py resolves the target trading day itself","source":"schwab_08335338"}`), once.** It recovers the failed scheduled day (the handler resolves the day itself, including the catch-up of any gap it computes, capped); it is not a new run and not Act 2. Read its output (counts only): the days written, `FunctionError` absent, the run manifest carries `split_adjust.declared` true, the counts. Then confirm the next scheduled fire (Monday 2026-10-19 11:30Z, Mon-Fri) in the record.
- **Branch B (the grant itself):** revert the one HCL edit and `safe-apply` (the policy returns to its prior document; 1/0/0); read back the simulate battery equals "before". Branch B of Act 1 (all three functions to `o9UugRAV...` by the prior VersionId) is the CTO's fallback at **13:00Z** if this grant is not applied and its recovery not read by then; the two Branch Bs are independent.
- **STOP rule:** a plan with any resource other than the one inline policy or any destroy; a simulate arm that differs from section 3a (a DENIED arm allowed, or the ALLOWED arm still denied); the recovery invoke returning a `FunctionError` or writing a day outside what the handler resolves; a second invoke needed.

## 5. Conditions

1. The CTO half. 2. IB-pr-612's ledger OPEN (this is its completion, not a second change). 3. The edit is the two locals above and nothing else in the repository (one file). 4. No wildcard beyond the exact prefix `*` that the existing grants use. 5. The simulate battery recorded as counts. 6. The recovery invoke is ONE invoke with the schedule's own Input.

## 6. Not covered

Any other IAM change; the siblings' roles; Act 2 (the 47 days; its order IB-pr-613 stays staged and now also waits on this); any other firm's prefix.

## 7. Signatures

**COO half:** 2.0.0_SA_COO~P2 -- SIGNED for sections 2 to 5, bound to the blob of this file. **CTO half:** 1.0.0_SA_CTO~DELL2 -- UNSIGNED at these bytes. The apply order is cut on this file as soon as it is signed.

-- 2.0.0_SA_COO~P2
