# LEGACY-READ AUTHORITY -- OPLGTW-LEGACY-READ-01 (NFRA_OPLGTW OG-m-2b, the 49F chain-log classifier)

**Authority:** `1.0.0_SA_CTO~O`, on the ruling of laptop `1.0.0_SA_CTO` (the owner of ADVI_FIRMBKTS and of the
LGIC_ENFORCE gate), msgs 102529, 102531 and 102538, relayed verbatim by `0.0.0_AB_MSTR~Z`. The admitted form is a
NAMING_LEGACY_READS.json entry. The gate's `tf_local` read_context kind landed @7610be987f22887e3d8e08edf123460d8d367e7e
after the laptop CTO read and APPROVED the patch (sha256 757b22255336).
**Precedent:** IRPT-M-LEGACY-READ-01. **Remediation owner of the key:** ADVI_FIRMBKTS (D8). This authority neither
advances nor closes that migration.

## What OPLGTW-LEGACY-READ-01 authorizes

In `infra/aws/terraform/opal-assets/advi_49f_floor.tf`, the EXISTING literal `gold/advi/_logs/chain_` in bucket
`opal-data-49financial` (the key the SSM document `advi-49f-chain-dispatch` already writes chain logs to) may be carried
ONLY as the value of the local `advi_49f_chain_log_prefix`, in a top-level `locals` block. The literal occurs once, and
`local.advi_49f_chain_log_prefix` is referenced exactly 3 times:
1. the existing SSM upload (the write that exists today, with rendered bytes unchanged);
2. the dispatcher role's IAM statement `ReadTheChainLog` (`s3:GetObject` on the prefix, no ListBucket);
3. the dispatcher Lambda's env var `CHAIN_LOG_PREFIX` (read at `lambda_function.py:68`).

## What it does NOT authorize

- Any new writer. A fourth reference changes the count, and the gate refuses it; the laptop CTO named that intended.
- The literal anywhere else, in any other file, or in Python (the Lambda reads the env var and carries no literal).
- Any other bucket, prefix or key.

**Cutoff:** `as_of_cutoff` 2026-10-06 (inclusive, UTC). It covers the commit window. Renewal is a new record, never an
edit of the date.
