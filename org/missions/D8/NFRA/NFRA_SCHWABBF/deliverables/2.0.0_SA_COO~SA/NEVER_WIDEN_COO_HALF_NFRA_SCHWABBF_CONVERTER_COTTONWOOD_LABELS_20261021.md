# NFRA_SCHWABBF -- the shared silver converter learns the four Cottonwood masters (build, upload, apply) and the Cottonwood events are redriven: never-widen pair, COO half

**Issuer:** `2.0.0_SA_COO~SA` (laptop), 2026-10-21 ~18:3xZ. **Halves:** COO = this file (SIGNED below); CTO = `org/tier1_exec/1.0.0_SA_CTO/deliverables/NEVER_WIDEN_CTO_HALF_NFRA_SCHWABBF_CONVERTER_COTTONWOOD_LABELS_20261021.md` (OWED).
**Pin:** `4724bc6017f` on `box/laptop` (LOCAL; the merge of cell `AL-k-5`, which contains the merge `be55cb3071f` of `AL-c-4`). **Order:** `task-orders/NFRA_SCHWABBF.TO-AL-r7.converter-cottonwood-deploy-and-redrive.md`.
**Why:** the first Cottonwood bronze files (305 objects, four masters, landed 2026-10-21 by the Alongside box) fire the converter `opal-assets-silver-schwab`; it raises `ManifestError: master '08719286' has no basis label` and the events retry to the dead-letter queue (`opal-assets-silver-dlq`, depth 42 and rising at 17:1xZ). Andrew-direct ~14:5xZ: "Ok great, let's get these backfilled." and ~17:0xZ: "a, yes. this needs to go through the same full bronze/silver process that the other masters go through".

## 1. The act and what it touches

1. Build the converter artifact from the pin and upload it to `s3://opal-313476888478-lambda-artifacts/opal-assets/opal-assets-silver-schwab.zip` (one S3 key, versioned; the previous version is the rollback).
2. `-target` apply of the schwab converter Lambda in `infra/aws/terraform/opal-assets`: an in-place update of ONE function (code hash and `OPAL_BUILD_COMMIT` `27acf60210` to `be55cb3071`).
3. Redrive: re-invoke the converter for the Cottonwood events held in the dead-letter queue, one message at a time, and delete a message only after its invocation was accepted.

| what | changes |
|---|---|
| the shared converter function | its CODE, by two constants (`BASIS_LABEL`, `DECLARED_SCHWAB_MASTERS`) gaining four keys; the existing three entries and all logic are byte-identical (the diff of the two files is +11 lines, -1 line). It serves the 49F masters too (the 0840 drain): their conversion is unchanged. |
| silver and state objects | NEW objects for the four Cottonwood masters under `schwab/cottonwood/silver/` and `.../state/` (the converter's own writes, already granted by `BF-g-5` / `BF-i-4` and fenced by `BF-h-5`). |
| the dead-letter queue | Cottonwood messages leave it after a successful re-invocation; the 49F-master messages (if any) are left untouched. |

**Does not touch:** reserved concurrency (2), the event rules, the converter's IAM or fence, any bronze key, the 49F masters' silver, the puller, the Alongside box.

## 2. Writers of the property (counted at signing; N printed)

- Writers of the converter artifact key: 2 seats in this project (`~SB`'s B3a earlier today, and this order); serialized by the window below. N = 2, never concurrent.
- Writers of the schwab converter Lambda's code: the Terraform apply (CloudOps). N = 1 at a time.
- Writers of `schwab/cottonwood/silver/`: the converter alone.

## 3. Expected outcome (both branches)

- **Branch A:** the build-only hash equals the upload's `Metadata.content-sha256`; the targeted plan reads exactly one resource updated in place (the schwab function: code and `OPAL_BUILD_COMMIT`), plus `aws_lambda_permission.silver_s3_invoke["schwab"]` only if the plan lists it unchanged; after the apply `get-function-configuration` shows `OPAL_BUILD_COMMIT = be55cb3071`; one redriven Cottonwood event converts (silver objects and a state manifest exist for its key) with no new `ManifestError`.
- **Branch B:** any other resource in the plan, a hash mismatch, a converter error on an existing master's key, or a redriven event that errors. Stop; do not apply (or do not redrive further); report. If the apply already ran, roll back (below).

## 4. Blast radius and rollback

- Blast radius: one shared Lambda's code (a constants-only change) and the Cottonwood silver/state objects it then writes. An in-flight invocation of the 0840 drain finishes on the code it started with; the next use the new code, which is identical for their master.
- **Rollback (same window):** re-point the artifact to the previous S3 version (the order saves its VersionId before the upload) by copying that version back as the current object, and re-apply the previous pin `27acf60210` (revert the `silver.tf` entry in the pinned worktree for the apply only, or the previous commit's text); Cottonwood events then fail as they do today (queued to the DLQ), nothing is lost. Written silver objects for Cottonwood stay (new keys, inert).

## 5. Conditions of this half

1. **Window:** not while `2.0.0_SA_COO~SB`'s 0840 bronze drain, her R5 (puller upload) or her R8 run (her msg 110155); start only after she tells me R8 closed, and finish before the 21:45Z pull fires (and not across the 12:15Z sweep). No window given by her = no start.
2. Apply only from the pinned worktree at `4724bc6017f`, saved plan, `safe-apply`, `-target` to the addresses the plan names, never an untargeted apply (the root holds other seats' pending changes).
3. Redrive paced at most one invocation per 2 seconds; stop on any converter `Errors` for an existing master or if the queue's oldest event age passes 2 hours (the CTO's ruling, msg 110130).
4. No rule is enabled; no backfill step starts in this order.

## COO half -- SIGNED

`2.0.0_SA_COO~SA`, 2026-10-21, for the blast radius in section 1, both branches in section 3, the rollback in section 4 and conditions 1-4, on the pin `4724bc6017f`.

## CTO half -- OWED (`1.0.0_SA_CTO`)
