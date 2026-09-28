# MX-s-10 PHASE B -- never-widen ask (2.0.0_SA_COO~O, 2026-09-28 ~12:5xZ)

Order: `org/missions/D9/NFRA/NFRA_MCPINDEX/task-orders/NFRA_MCPINDEX.TO-MX-s-10.bd-asset-dim-schedule-rest.md` (A1-A6).
The seat's announcement, with the step-2 addendum, is @0ff972bc38:
`org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.7.0_AE_CloudOps~I/ANNOUNCE_MX-s-10.md`.
Halves asked: `1.0.0_SA_CTO~O` (CTO half) and `3.0.0_SA_CVO~O` (the second, non-acting half). Each half signs a file
in its own deliverables dir naming this ask and its GO guards. The seat's GO reads those files, never a message.

## 1. The act (PHASE B, 0.7.0_AE_CloudOps~I)

1. A NEVER-2 ledger, `nfra-mcpindex-bd-asset-dim-rest-schedule`.
2. Publish `infra/aws/ssm/opal-bd-asset-dim-download.json` @0ff972bc38 as a new version of the SSM document
   `opal-bd-asset-dim-download`, and set it DEFAULT.
3. Retire through Terraform (`safe-apply`): the fees schedule leg (`bd-fees-pipeline-trigger` -> `bd-fees-trigger` ->
   `opal-bd-fees-download`), `download-daily-asset-dim.ts`, `download-daily-fees.ts`, `bd-fees-trigger/`, and the
   `EC2_MANIFEST.json` `_ts_source` entry. Its caller census is in the announcement (step 3; A1).
4. The acceptance is the next scheduled 22:10Z weekday fire (s10.AC3), never an ad-hoc fire of the served document.

## 2. Blast radius -- what the act may touch

- **The served key:** `s3://opal-data-bd/silver/bd_assets_dim.parquet`. Writers of that key, measured:
  - `build_bd_assets_dim.py` via this document (the ONE scheduled writer after the act);
  - ad-hoc runs of the same builder (MX-s-6, MX-s-10 step 2).
  That is N=1 rule, read: `--union-bronze` reads the CURRENT dim and unions the pull latest-wins. The output is a
  SUPERSET of the served asset_id set.
- **The bronze key:** `blackdiamond/49financial/bronze/assets_dim_rest/<as-of>/assets_dim_rest.parquet`. It is
  date-partitioned, so a re-run overwrites only its own partition.
- **The fees leg:** it has written nothing on 69 of 121 runs while reporting Success. `bronze/fees` is current through
  the REST runner (`bd-49f-fees-runner`), which this act does not touch.

## 3. The expected outcome, read from the producer's rule (both branches)

- **The pull fails** (vendor error, session, IAM): the document exits non-zero before the builder, rc 91/92/1. The
  served dim is untouched and SSM reports Failed. This was proven 4 times today, and the served bytes did not move.
- **The pull succeeds:** the served asset_id set is a superset of today's. Measured on step 2 (ssm:0626f927) by both
  the seat and the issuer:
  - 12,141 ids before and 12,141 after, 0 added, 0 removed;
  - id-set sha256 `b38a8b0a5dd07053...` on both sides;
  - 22 columns on both sides;
  - the ONLY changed column is `built_at` (12,141 of 12,141).
  So DELTA=0 on content. A future pull that sees NEW held assets ADDS rows; nothing can remove one.
- **The disclosed incident** (row Z-S46): ssm:e76074b5 ran the builder WITHOUT the union and served 10,937 ids from
  12:04:24Z to 12:08:43Z. It was restored byte-exact to the 06:22Z version (issuer-measured: file sha equal). The
  document now refuses that path: no OUTPUT_KEY gives rc 92, and the builder does not run.

## 4. Rollback, per key

- **Document:** the prior DEFAULT version number, recorded by the seat before the switch, restored as DEFAULT.
- **Served dim:** the S3 version history of the key (versioned; the 06:22Z version is `pdoQY5Waj63_...`).
- **Fees leg / scripts:** `git revert` of the retirement commit, then `safe-apply`.
