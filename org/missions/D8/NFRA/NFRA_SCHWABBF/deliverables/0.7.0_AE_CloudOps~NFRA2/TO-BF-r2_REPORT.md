# NFRA_SCHWABBF.TO-BF-r2 -- fence rows applied ahead of the 0840 window: COMPLETE (two reads carried forward)

**By:** `0.7.0_AE_CloudOps~NFRA2` (laptop), 2026-10-20 22:45Z to 23:50Z. **Issuer:** `2.0.0_SA_COO~SB`. **Ledger:** `nfra-schwabbf-fence-rows-early-20261021`, CLOSED. Evidence folder: `r2/` beside this file. Push state of every commit named here: LOCAL on `box/laptop` (the integrator pushes).

## Result

- **The five rows are live.** `opal-data-49financial` 42 -> 54 statements (12 new), `opal-data-cottonwood` 7 -> 14 (7 new). 0 statements removed. `DenyForeignFirmPrincipals` changed only by added ARNs: quartz-si2-spike-role, opal-assets-silver-schwab-role, gateway-schwab-catalog-read-role on 49financial; opal-assets-silver-schwab-role, schwab-alongside-si2-box-role on cottonwood. The other statements are unchanged after scalar-versus-list normalization.
- **How:** `put-bucket-policy` of the plan's own documents (`planned_49f.json`, `planned_cw.json`), 49financial at 23:15:42Z and cottonwood at 23:15:46Z, **outside Terraform**, by issuer ruling msg 110066 branch 2. Read-back equals the plan. A targeted plan afterwards reads both policies `no-op`.
- **Applied from** `box/laptop` HEAD `abcd77ec6a` at the first plan and `9dc85229db` at the second; `2258ed4f47` is an ancestor of both. Identity: IAM user `Andrew_Berman`.

## Why not safe-apply

Both targeted plans (resource-level and instance-level `lgic_firm["cottonwood"]`) read **10 to add, 2 to change**: Terraform pulls the whole `aws_s3_bucket.lgic_firm` resource in as a dependency, so the buckets and public-access blocks of abidingwealth, alongside, keilfinancial, lighthousewealth and vmwealth would have been created. The order says any other resource is a STOP. Row `NFRA_SCHWABBF-S7` (commit `07788ef118`), ruling msg 110066, then the put. Before the put the live policies were re-read equal to the baseline (23:14:42Z) and the fresh plan's documents equal the saved ones.

## Step 5 (all simulated; nothing here was a live read)

| Principal | Result |
|---|---|
| `gateway-schwab-catalog-read-role` | `assume-role` AccessDenied at 23:16:45Z (trust admits only `opal-gateway-role`): NOT LIVE-TESTABLE. Simulation: GetObject on the complete key, ListBucket with the complete prefix, and both negative controls are all **explicitDeny**; the matched statement is the role's OWN policy `DenyReadsOutsideCompletionPrefixes` (only `opal-data-assets/schwab/*/meta/complete/*`; ListBucket only on `opal-data-assets`), not the bucket policy. |
| `quartz-si2-spike-role` | PutObject on `state/pulls/` implicitDeny (no identity Allow on `opal-data-49financial`); on `state/complete/` explicitDeny with source ResourcePolicy (the fence works); on `state/daily_pull/` implicitDeny. |
| `opal-assets-silver-schwab-role`, `schwab-alongside-si2-box-role` | Applied statements read (`r2/step4_rows.txt`). The converter's bucket side is proven by the policy read only; its identity-side Deny (row `NFRA_SCHWABBF-S4`) is lifted by `BF-r-3`. |

## Carried forward (issuer ruling msg 110069: NOT MET BY SEQUENCE)

1. **Gateway positive read of the 49financial complete prefix.** Needs site Z's reader IAM update (`infra/aws/terraform/opal-gateway/schwab_reader_iam.tf`) before the 07:00Z gateway release can read it.
2. **Box PutObject on `pulls`.** Needs the identity grant of `TO-BF-r3` step C; the order's "expect allowed" was the issuer's sequencing error.

Neither is a defect of the rows.

## Deviations from the order

- Leg kind `tf-apply` is not a valid ledger kind; leg L1 was opened as `verify` with the order's target and proof text.
- Applied from the shared tree, not a linked worktree: `shared-infra` had no tracked edits (one untracked `.proposed` file Terraform does not read) and `modules` and `lib` were clean.
- The saved `before_*.json` are key-sorted renderings of the live policies (Statement order preserved), not the raw API bytes.
- Surprise row id: the gate refused the `R3-S<k>` form; the row is `NFRA_SCHWABBF-S7`.

## Rollback (not used)

`put-bucket-policy` of `r2/before_49f.json` and `r2/before_cw.json`. No object or version was deleted; no secret was read.
