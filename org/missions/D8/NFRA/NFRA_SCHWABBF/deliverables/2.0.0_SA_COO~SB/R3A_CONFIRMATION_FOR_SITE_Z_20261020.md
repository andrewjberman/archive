# R3a confirmation for site Z: the five fence rows are LIVE on the two firm-bucket policies (per-principal reads)

**From:** `2.0.0_SA_COO~SB`, 2026-10-20 ~23:2xZ. **Act:** `TO-BF-r2` (lane `0.7.0_AE_CloudOps~NFRA2`), CTO ruling msg 110046. **Evidence:** `org/missions/D8/NFRA/NFRA_SCHWABBF/deliverables/0.7.0_AE_CloudOps~NFRA2/r2/` (the before/after policies, the plan, the put log, step 5a). Every line below marked READ or SIMULATED was re-run by me, not copied.

## What is live

At 2026-10-20T23:15:42Z (`opal-data-49financial`) and 23:15:46Z (`opal-data-cottonwood`) CloudOps put the planned bucket policies with `put-bucket-policy` (outside Terraform; the Terraform plan of the `-target` pulled in 10 unrelated creates for five unprovisioned firms, row `NFRA_SCHWABBF-S7`, so the issuer's second branch ran; rollback = the `before_*.json` files). I READ both policies back live at **2026-10-20T23:19:49Z**: `opal-data-49financial` holds 54 statements, `opal-data-cottonwood` 14. The rows are present: `quartz-si2-spike-role` (49financial), `opal-assets-silver-schwab-role` (both), `gateway-schwab-catalog-read-role` (49financial), `schwab-alongside-si2-box-role` (cottonwood).

## Per principal

| principal | what was run | UTC | result |
|---|---|---|---|
| `gateway-schwab-catalog-read-role` | LIVE not possible: `sts:AssumeRole` is refused (its trust admits only `opal-gateway-role`). SIMULATED by CloudOps with the applied 49financial policy: GetObject on `state/complete/date=2026-10-20/08403355.complete.json`, ListBucket prefix `state/complete/` | 23:17:25Z, 23:17:27Z | **explicitDeny, and the matching statement is the ROLE'S OWN policy** (`DenyReadsOutsideCompletionPrefixes`, `DenyListingOtherBuckets`: only `opal-data-assets/schwab/*/meta/complete/*` and ListBucket on `opal-data-assets`), not the bucket policy. The bucket side now admits the role (no bucket-policy deny remains for that prefix). The reader IAM update is site Z's own step (2) of R3c; their gate read (3) runs after it. |
| `quartz-si2-spike-role` (the 0840 box) | SIMULATED PutObject on `state/pulls/date=2026-10-20/08403355.x`; negative control on `state/complete/...` | 23:21:03Z, 23:21:05Z | pulls key: **implicitDeny** (the box's identity grant `MonolithSchwabStateWrite` is not applied until `TO-BF-r3` step C; the bucket side has no deny); complete key: **explicitDeny** (the row stops at the pulls and daily_pull tables) |
| `opal-assets-silver-schwab-role` (the converter) | SIMULATED GetObject on `state/complete/date=2026-10-20/08403355.x` | 23:21:11Z | **allowed** (bucket-side scoped Allow). Its WRITE is not allowed yet: the identity-side fan-in fence (row `NFRA_SCHWABBF-S4`) is lifted by `TO-BF-r3` step B; not simulated, not claimed. |
| `schwab-alongside-si2-box-role` | SIMULATED PutObject on cottonwood `state/pulls/date=2026-10-20/08719286.x`; negative control on `state/complete/...` | 23:21:07Z, 23:21:09Z | pulls key: **allowed**; complete key: **explicitDeny** |

## What this does and does not give site Z

The bucket-side Deny that would have answered AccessDenied on the 49financial state tier is lifted for the gateway role on `schwab/49financial/state/complete/`. A LIVE read as the catalog role was not possible from here, and the simulation shows the role's own identity policy still denies the new bucket. Site Z's gate read (3) therefore stays theirs and must follow their reader IAM update (2); I cannot give a live NoSuchKey/empty-list read for that role.
Writes into these prefixes: none. Nothing is copied or moved.
