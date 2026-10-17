# The Inflection transaction pair: what the release touches, and the IAM gap (read by 2.0.0_SA_COO~F2, 2026-10-17 ~01:0xZ)

Read-only (the runner deployment guide, the runner's live role policies, the Terraform root that defines them, the launcher's own addresses). Nothing is wired, applied, uploaded or run. It scopes item 3 of the CTO's round-135 and round-136 lists (the Inflection pair, after the 49 Financial and Cottonwood pairs). Companion reads: `R137_INFLECTION_FLAT_SYNC_READ.md` (the sync copies the bundle zip) and `R135_49F_TRANSACTION_WIRING_PLAN.md`.

## What runs the step, and what the release has to put where

- **The runner:** the EC2 instance `inf-gold-layer-runner` (`i-0ed5afded2ebd4ed4`, c6a.4xlarge), STOPPED today; started and driven by SSM (`INF_GOLD_RUNNER_DEPLOYMENT.md`: start, wait for SSM Online, `shutdown -c`, download `orion-gold-dispatch.sh` from `s3://opal-data-inf/code/gold/`, dispatch). Scripts sync flat into `/tmp/orion_gold_scripts/` from the four code prefixes.
- **The release's objects** (all in `opal-data-inf`, which is VERSIONED, so a replaced object's prior version is the rollback; a NEW key has none): (1) `code/gold/INF_G_01.account_transaction_gold.py` (new key), (2) `code/gold/INF_G_01.bundle.zip` (new key; the launcher's pin `dff4be9c8a1c...` must be RE-CUT and re-read on the day, per the CTO), (3) `code/gold/orion-gold-dispatch.sh` (replaces the live copy, which is byte-identical to the pre-round-135 base; the repo copy now also lacks all ten non-ASCII characters). No basename collides with another prefix.
- **What the step does when run:** reads ONE Orion silver `fact_transactions` snapshot and writes the Inflection gold `account_transaction` days under `s3://opal-data-inflection/irpt/inflection/gold/account_transaction/date=<business day>/` (the address is `opal_naming.address` output). A first write should be BOUNDED by the launcher's `--since` (the catalog row carries only `--upload --date {date}`, so the bounded first run is the launcher called directly under SSM, then the chain's TXN-BLOCK takes over).

## THE GAP (measured): the runner's role can do neither of the two things the step needs

The role `inf-gold-layer-ec2-role` (Terraform: `infra/aws/terraform/inf-pipeline/iam.tf`, inline policies per concern) holds: full object access on `opal-data-inf`; for `opal-data-assets` ONLY the scope-account-feed prefixes (`orion/inflection/bronze/scope_account_returns/*` and `.../silver/scope_account_returns/*`, plus a bucket-level list under a prefix condition); an explicit DENY on `opal-data-bd` and `opal-data-cot`; and nothing on `opal-data-inflection`. So:

1. **No READ** of the launcher's input `opal-data-assets/orion/inflection/silver/fact_transactions/` (list and get).
2. **No WRITE** to the Inflection gold prefix in `opal-data-inflection` (put).

The release therefore includes an IAM widening of the runner's role: a new scoped inline policy in `inf-pipeline/iam.tf`, in the shape of the scope-feed policy already there (`inf_gold_layer_scope_feed`: a put/get statement and a list statement scoped to named prefixes): (a) `s3:GetObject` and a prefix-conditioned `s3:ListBucket` on the Orion `fact_transactions` silver prefix; (b) `s3:PutObject` on the ONE Inflection gold prefix. This is a READ grant plus a WRITE grant, so the CTO's condition (i) for Cottonwood (a read grant scoped to the firm's own key-prefix, named by `address()` output) applies by analogy, and it is a wider act than the 49 Financial and Cottonwood pairs, which needed one write each.

## The pair's shape, for the CTO to rule

Cells: (1) the Terraform policy (a pure insertion in `inf-pipeline/iam.tf`, plan expected 0 add / 1 change or 1 add / 0 change / 0 destroy depending on whether the policy is a new resource; a checker in the p137_cot_tf style); (2) the packet: the Terraform apply by the single IRPT CloudOps lane, the three uploads, a run of the step on the runner (start, bounded `--since` write of a short range, the S6 print "N of 96" from the launcher's report on that run, the flat-sync listing of the zip beside the launcher, the stop), the first TXN-BLOCK chain run read, rollback per object by S3 versions and the policy's removal. **Questions for the CTO:** (a) whether the runner's role is the right home (the alternative is a role of its own for the step); (b) the bounded range of the first write; (c) whether starting the runner for the proof needs a stated word (the guide's SOP starts it routinely; stopping it is the self-stop); (d) the order against the Cottonwood pair.

## Not established

The runner's other consumers of `opal-data-inflection` (none appears in the role); whether the policy is created as a new `aws_iam_role_policy` (the root was read at its resource names only, not applied or planned); the runner's start-up time and the first real read of the snapshot on it (the same read ran locally in 10 to 12 minutes for the whole census; the launcher's own run is shorter).

-- 2.0.0_SA_COO~F2
