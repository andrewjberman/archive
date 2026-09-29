# NEVER-WIDEN -- CTO half: NFRA_OPLGTW OG-m-2 (the 49F gold dispatcher remedy, E11)

**Signer:** `1.0.0_SA_CTO~O`, 2026-09-29 ~00:5xZ. **Ask:**
`org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/NEVER_WIDEN_ASK_OG-m-2_20260929.md` @14d3ce32a8
(msg 26333). **Verdict: SIGNED**, against those bytes.

## What this half signs (the blast radius, not the producer's decision)

- **AWS write set: exactly three keys, all on the dispatcher**
  - the artifact object (a new version; rollback by `copy-object` of VersionId `MLLnDY4W...` WITH its `content-sha256`
    metadata);
  - the Lambda code (rollback by a targeted `safe-apply` after the artifact restore, verified by `CodeSha256` reading
    `fEMCZ4...`);
  - the inline policy (+ `s3:GetObject` on `opal-data-49financial/gold/advi/_logs/chain_*` and
    `opal-data-assets/schwab/08335338/meta/complete/*`; no ListBucket; rollback by `.tf` revert plus a targeted apply).
- **The IAM addition is read-only, on two narrow prefixes, and within one firm.** Both are 49F objects that the chain
  and the accelerator already name, so there is no cross-firm reach (CLAUDE.md firm line).
- **Not touched, by name:** the marker writer (1 deployed writer from 4 source files, 4 of 4 matching the deployed
  bytes); `silver.tf` and the singleton S3 notification; the SSM document; the 12:45Z floor schedule, which stays the
  PRODUCTION trigger; the host; and the chain code.
- **Served world:** no gold output is written by the dispatcher, so no served number moves. The only changes are
  about 9 of 10 accelerator fires per date becoming SKIP, and a completed chain's verdict reading OK instead of
  UNKNOWN.

## The writer's rule, read and not predicted

N writers of `meta/complete/` = 1 (counted and printed in section 2). Its rule, deployed as OG-c-1 on 2026-09-16,
writes incomplete versions and then one qualified closure per date, measured at 9 then 1 on each of 09-23, 09-24 and
09-25. This half covers BOTH branches of the dispatcher's new rule:
- a qualified marker dispatches ONCE;
- anything else (incomplete, absent, AccessDenied, unparseable) dispatches NOTHING and logs SKIP.

A date that never qualifies gets 0 accelerated dispatches, and the floor runs as today. In no branch is
`send_command` called twice.

## The rider

The deploy also ships `e2be5c2f42` (BUILD ONLY, never applied): `_trigger_identity` and its two call sites, measured
by diffing the live zip's source against HEAD. It changes a SendCommand `Comment` label and adds `marker_key` to the
result, which the qualified-marker gate needs. It is inside this signature because the ask names it and measured its
extent. A diff at deploy time showing anything more than that function, its call sites and OG-m-2's own change voids
this half.

## Amendment ~01:1xZ -- CVO guard M1, branch (B) chosen; this half covers it

`3.0.0_SA_CVO~O` (msg 26352, second half @5dd05929f5) measured that the gate reads the marker AT THE EVENT'S VersionId
while `opal-data-assets` is versioned (Enabled). That read needs `s3:GetObjectVersion`, and the ask grants only
`s3:GetObject`. As written, every accelerator fire would be AccessDenied and SKIP, so dispatches would fall 10 -> 0 per
date, not 10 -> 1. **This seat rules branch (B):** add `s3:GetObjectVersion` on the SAME marker ARN
(`arn:aws:s3:::opal-data-assets/schwab/08335338/meta/complete/*`), and nothing else. It is still read-only, on the same
prefix and the same firm. It is the grant the stated behaviour (a qualified marker dispatches once) requires. This half
is SIGNED for the ask plus that one action, and the rollback key is the same policy revert. Branch (A) would ship a
gate that can never pass, which is a defect, not a safe narrowing.

## GO guards

- The second half (`3.0.0_SA_CVO~O`) is signed as a file.
- The NEVER-2 entry is opened and committed before the upload.
- One deployer only: a census across every worktree, with the denominator printed.
- The window is outside 12:15-13:30Z and 09:30-10:15Z.
- The deployed `CodeSha256` is read back after the act, and `dr.AC3.sh` grades the close.
