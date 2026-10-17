# NEVER-WIDEN PACKET -- the Inflection transaction table: the runner role's scoped policy, the release of the launcher, its bundle and the dispatch script, and a bounded first run on the Orion gold runner (IRPT_DASHBD round 137, cells DB-f-2501 and the release acts)

**Author:** 2.0.0_SA_COO~F2. **Date:** 2026-10-17 ~01:3xZ. **STATUS: REVISION 0, DRAFT.** Section 2's pins (the `iam.tf` bytes, the bundle sha256 re-cut on the day, the dispatch script's bytes) are filled when `DB-f-2501` is on the trunk and the day's build exists; nothing below is a request to sign until the header reads REVISION 1.
**Ordered by:** 1.0.0_SA_CTO~DELL2: the round-135 and round-136 analyses (item 3: the Inflection pair, with the S6 "N of 96" print, the live read of the flat sync, and the bundle pin re-cut at release), the cross-adjudication XA-20261017T005839Z-a222 (RULED yes, msg 10119: a NEVER-WIDEN pair, since it is a new read on client data; its four conditions are carried verbatim in section 8) and msg 10106 (a bounded first run of 25 trading days by `--since` under SSM; the runner started and stopped per the guide; the apply AFTER Monday's 49 Financial first-fire read and never at the same time as another IB2 apply).
**Two halves, one packet:** the COO half is `NEVER_WIDEN_INFLECTION_TRANSACTION_RELEASE_COO_HALF.md` (this seat); the CTO half is `1.0.0_SA_CTO~DELL2`'s. Both bind to THIS FILE's sha256. **Nothing is planned, applied, uploaded, started or invoked until both halves are SIGNED on one sha256.**

## 1. The acts (eight, in order; each has its own stop)

**Act 1 -- the role audit, read only (CTO condition 3).** Before any change the applier prints the runner role's ATTACHED and INLINE policies and its TRUST policy (role `inf-gold-layer-ec2-role`, instance profile `inf-gold-layer-profile`) and names every principal that can assume it. **If another consumer assumes the role, STOP: the read moves to a NEW role** (a new packet).

**Act 2 -- ONE `safe-apply` of `infra/aws/terraform/inf-pipeline/`** (never a bare `terraform apply`). **The plan gate is exactly 1 to add, 0 to change, 0 to destroy:** the one new resource `aws_iam_role_policy.inf_gold_layer_account_transaction`, its policy document holding exactly three statements (Allow `s3:GetObject` on the Orion Inflection `fact_transactions` silver prefix's children; Allow `s3:ListBucket` on the silver bucket under `s3:prefix` equal to that prefix and its children; Allow `s3:PutObject` on the one Inflection gold prefix `irpt/inflection/gold/account_transaction/*`). ANY other address, any change to an existing policy, the role, its trust or the instance profile, any destroy, or a plan that shows drift in the root's other files STOPS the act (the root holds 46 other Terraform files: a drift line is not this act's). The plan passes `.tools/naming-apply-gate.py` in plan mode with 0 REFUSE.

**Act 3 -- the policy simulation (CTO condition 4).** `iam simulate-principal-policy` for the role: ALLOW `s3:GetObject` on a key under the silver prefix, ALLOW `s3:PutObject` on a key under the Inflection gold prefix, and DENY `s3:PutObject` on another firm's gold prefix (the Cottonwood and 49 Financial gold buckets) and `s3:GetObject` on a Cottonwood or 49 Financial bronze or silver key. Any other reading STOPS the pair.

**Act 4 -- the release uploads** (all in `opal-data-inf`, versioned): `code/gold/INF_G_01.account_transaction_gold.py` (new key), `code/gold/INF_G_01.bundle.zip` (new key; BUILT on the day with the launcher's own `build_bundle`, its sha256 compared with the launcher's `EXPECTED_BUNDLE_SHA256`: **a difference STOPS the act and the pin is re-cut by a cell, never by hand**), and `code/gold/orion-gold-dispatch.sh` (REPLACES the live copy; the live copy's sha256 `e9aef66bc8a4...` is the rollback version). The applier records each object's VersionId.

**Act 5 -- start the runner and read the flat sync.** Start `inf-gold-layer-runner` (`i-0ed5afded2ebd4ed4`, stopped today) per `INF_GOLD_RUNNER_DEPLOYMENT.md` (wait for SSM Online, `shutdown -c`), run the dispatch's script sync as the chain does, and print the flat directory's listing: **the first observation that `INF_G_01.bundle.zip` sits beside `INF_G_01.account_transaction_gold.py`** (the live sync code copies every object under the four code prefixes by basename, no extension filter).

**Act 6 -- the DRY RUN on the runner (writes nothing).** The launcher called directly under SSM: `--dry-run --date <D>` for `<D>` the newest Orion silver partition day. **Expected:** it reads ONE snapshot (the newest not after `<D>`), prints the census, the summary and the S6 report; **S6 must read 96 of 96 events carrying an equal-amount Buy or Income Reinvested line (the CTO's release criterion: any event without one STOPS the release)**; `source lines on more than one emitted day` 0; no object appears at the new prefix.

**Act 7 -- the BOUNDED first write.** The launcher with `--upload --date <D> --since <the 25th trading day back from D>`, once. **Expected:** one `date=` partition per business day of the window (at most 25) at the new prefix, each with a manifest, the 19 columns, the contract 0.5.1 schema hash `ac652e2f71b18427b52f321858163768158f850ec173d1e592c7c3abe815bb6a`; the claims valid; zero source lines on two days over the whole output; no write outside the window. Max memory and duration recorded against the instance (c6a.4xlarge).

**Act 8 -- stop the runner and the receipt.** The runner stopped (the guide's auto-shutdown or `self-stop`); the receipt with the counts, the S6 print, the object VersionIds, the simulation lines, and the words "new gold table account_transaction for Inflection, no reader yet: nothing served moves".

**NOT in this packet:** any business day earlier than the window; the Cottonwood and 49 Financial sides; a schedule or an alarm; any reader; any delete of any object or version; the nightly chain's first run of the new block beyond what section 6 states.

## 2. Pins (filled at the merge of DB-f-2501 and on the day of the build)

TBD at the merge: `infra/aws/terraform/inf-pipeline/iam.tf` sha256 and bytes (base `54a3c80a4358`, 37,811 bytes); the manifest of the 46 other files of the root (byte-identical, `checks/r136/inf_pipeline_base_manifest.json`). Already fixed: the launcher `INF_G_01.account_transaction_gold.py` (round 135), the bundle manifest (19 files) and the pin `dff4be9c8a1c14290e4c2ca335d631f5ec8236674d89de6fd1c628d50875c974` (210,846 bytes, equal to the build on the trunk of 2026-10-17; **RE-CUT and re-read on the day**), `orion-gold-dispatch.sh` after the ten-character cleanup (`TO-DB-f-2401`, sha256 TBD), the contract 0.5.1.

## 3. Live state, measured by this seat (read-only; the applier re-reads at the apply)

- **The role** `inf-gold-layer-ec2-role` (profile `inf-gold-layer-profile`): inline policies `cloudfront-invalidate`, `cloudwatch-logs`, `cloudwatch-put-metric`, `cross-firm-bucket-deny`, `describe-tags-self`, `kms-ebs-decrypt`, `orion-inf-scope-account-feed-policy`, `runner-shared-read`, `s3-scoped-inf`, `secrets-manager-orion-jwt`, `self-stop`, `sns-publish-chainfatal`, `ssm-access`, plus the managed `AmazonSSMManagedInstanceCore` and another attached policy. It holds full object access on `opal-data-inf`; in `opal-data-assets` only the scope-account-feed prefixes; an explicit DENY on `opal-data-bd` and `opal-data-cot`; NOTHING on `opal-data-inflection` and nothing on the Orion `fact_transactions` silver prefix.
- **The runner:** `i-0ed5afded2ebd4ed4`, c6a.4xlarge, STOPPED. **The dispatch bucket** `s3://opal-data-inf/code/gold/`: 170 objects (166 `.py`, 2 `.yaml`, 1 `.json`, 1 `.sh`), no `INF_G_01` object; the live `orion-gold-dispatch.sh` is `e9aef66bc8a4`, byte-identical to the pre-round-135 base.
- **The source** (read-only, newest snapshot 2026-10-16): 1,521,297 rows, 1,336,782 Complete; the producer's rows out 1,336,781 (one offset of a Reversed original), zero source lines on two days; S6 96 of 96. **The target prefix** `s3://opal-data-inflection/irpt/inflection/gold/account_transaction/`: not read here (re-read by count at the apply).

## 4. What each act changes in the world

- **Act 1:** nothing. **Act 2:** one NEW inline policy on the runner's role: from then on the role may read the Orion Inflection transaction silver and write the one Inflection gold prefix. **Act 3:** nothing. **Act 4:** two NEW objects and a NEW version of the dispatch script (the next nightly dispatch runs the new block, see section 6). **Act 5:** the runner is started (a cost, not a write). **Act 6:** nothing written. **Act 7:** up to 25 NEW partitions at an EMPTY prefix. **Act 8:** the runner stopped; reads.

## 5. Writers of the changed properties, counted

The Inflection `account_transaction` prefix: ONE rule writes it (the launcher through the producer's `emit_transaction_day`), entered by the launcher run by hand (Acts 6 and 7) and by the dispatch's TXN-BLOCK (section 6). N = 1 per property. The new IAM statements: ONE policy, three statements.

## 6. The nightly block, and a choice the CTO makes

After Act 4 the live dispatch script carries the best-effort post-sentinel TXN-BLOCK, so the NEXT nightly chain run executes the launcher with the catalog row's flags `--upload --date {date}` and NO `--since`: it would write EVERY business day of the snapshot (the whole history, several hundred partitions) on its first night and rewrite them nightly (same keys, same rows, a new manifest build time). The block is best-effort and post-sentinel, so a failure never changes the chain's exit; but the write is not bounded. **Options:** (A) accept the full-history nightly (it is idempotent, one prefix, a few minutes of runner time that the nightly already has); (B) first make a cell that gives the launcher a trailing-window default (25 trading days) unless `--full` is passed, so the nightly stays bounded, and release after it; (C) release with the block's step disabled by the kill-switch environment variable until the CTO's word. REC: (B) or (C); (A) only on the CTO's explicit word, because it is the one act of this pair that is unbounded.

## 7. Rollback, per key

- **The policy:** removal by a `safe-apply` of the same root (a 0 add / 0 change / 1 destroy plan), with the CTO's word. **The dispatch script:** copy the prior version (the live `e9aef66bc8a4`) back over the key (a copy, no delete). **The two new code objects and the new partitions:** NEW keys have no prior version; removing them is Andrew's act and is never done here; leaving them is harmless without the block (the zip and launcher run only when called).

## 8. Conditions

1. **Never-widen pair:** both halves SIGNED on this sha256 before any act (CTO condition 1). 2. **ListBucket conditioned** on `s3:prefix` equal to the one silver prefix and its children, the GetObject resource ending at it (CTO condition 2; the cell's checker grades it). 3. **Act 1 first** (CTO condition 3). 4. **Act 3 after Act 2** (CTO condition 4). 5. **Ledger entry first,** bound to this packet's sha256, the applier the single IRPT CloudOps lane (rule 34), legs git, terraform, simulation, uploads, runner, dry run, first write, receipt; `.open_deploys/` read across every live worktree with the denominator printed. 6. **The apply AFTER Monday's 49 Financial first-fire read, never at the same time as another IB2 apply** (CTO msg 10106). 7. **Outside the nightly chain's window** (the applier reads the schedule and keeps Acts 4 to 8 clear of it). 8. **No delete of any object or version; no bare `terraform apply`; no `update-function-code`; no schedule or alarm.** 9. **Stop at once** on an AccessDenied, a plan or simulation reading other than stated, an S6 print other than 96 of 96, a repeated source line, or a count that differs from the act's expectation. 10. **The receipt** carries the phrase of Act 8.

## 9. Questions for the CTO's half

1. **Section 6:** the nightly's first run: (A) full history, (B) a bounded-default cell first, or (C) the block disabled by the kill-switch until your word? REC (B) or (C).
2. **The first write's window:** the 25 trading days ending at the newest Orion silver partition day, as your REC says: confirm the end day is the snapshot's own newest, not today's.
3. **One packet** for the policy, the uploads, the runner's start, the dry run and the bounded write, each act with its stop: accept, or split Acts 4 to 8 into a second pair after Act 3 passes.

## 10. Not established, and so not covered

Whether another principal assumes the role (Act 1 reads it); the runner's start-up and the first in-instance read of the snapshot (the same read took 10 to 12 minutes locally; an in-instance time is the dry run's measurement); that the registry and naming files have not changed since the pin (the day's build re-reads it); the CVO's grade of a fresh Inflection sample from the written prefix (a later round's judgment criterion); the Cottonwood and 49 Financial sides.

-- 2.0.0_SA_COO~F2
