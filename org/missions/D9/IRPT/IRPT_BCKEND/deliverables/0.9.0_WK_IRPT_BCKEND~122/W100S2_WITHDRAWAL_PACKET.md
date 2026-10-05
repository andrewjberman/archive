# W100-S2 withdrawal packet -- the 49F perfrp account leaf (IRPT_BCKEND.TO-IB-pr-319)

Worker 0.9.0_WK_IRPT_BCKEND~122, read 2026-10-04, AWS reads only. Ordered by CTO batch 251 (@8ea5889048, msg 105089): withdraw the leaf, keep the portal's call.

**Versioning:** Enabled on `s3://opal-data-portal-v2` (get_bucket_versioning).

**Every perfrp key under platinum/advi/ (denominator 4 perfrp keys of 19 objects listed, all firms; all under 49financial/):**

| key | ETag | size | last modified |
|---|---|---|---|
| perfrp_book_advisor.json | bca9bfb3310e0047acd261aa66ae3597 | 15000091 | 2026-09-01T07:27:05+00:00 |
| perfrp_gainloss_account.json | a820d1636b494069329401ad8ae5d035 | 11896644 | 2026-09-01T03:17:03+00:00 |
| perfrp_gainloss_relationship.json | 9f4a7757384f60e155caf3023655449f | 7419826 | 2026-09-01T03:16:43+00:00 |
| perfrp_performance_account.json | 9873b72ef5da73fc0399d2905d4f7821 | 1923593 | 2026-09-01T03:16:07+00:00 |

Writer of all four: `data/assets/scripts/gold/runners_49f/d_publisher_port.py` registry rows (159-160, 168-169, 171-172, 188-189), serve root :62; IAM write grant `infra/aws/terraform/opal-assets/advi_49f_publisher.tf:70`.

**2025-01-10 measurement:** `perfrp_performance_account.json` does NOT contain the literal date (0 hits; dates present: 2024-07-08, 2024-07-09, 2026-08-31, 2026-09-01). It holds window returns only; its SI window spans 2025-01-10 by construction. Whether the SI values embed the inflated day is not read here. See row IRPT_BCKEND-W122-S1.

**Withdrawal set (exactly one key):** `platinum/advi/49financial/perfrp_performance_account.json`, ETag `9873b72ef5da73fc0399d2905d4f7821`, VersionId `E78kI4KB4KsZhdwsAFzfSvkI.kn5Snim`.

**Rollback:** versioning is Enabled, so the delete leaves a delete marker. Restore by deleting the marker (`aws s3api delete-object --bucket opal-data-portal-v2 --key <key> --version-id <marker id>`) or `copy-object` from `?versionId=E78kI4KB4KsZhdwsAFzfSvkI.kn5Snim`. No byte copy is written.

**Stop rule:** stop if the key's ETag at act time differs from `9873b72ef5da73fc0399d2905d4f7821`, or its current VersionId is not `E78kI4KB4KsZhdwsAFzfSvkI.kn5Snim`.

**After-read:** one 49F login on PROD (https://opalinvest.dev/advisor-intelligence): the leaf request returns 404 and the page shows its designed shell state.

**Blast radius:** may touch the one withdrawal key. Never touches the other three perfrp keys, any other platinum/advi key (including `_manifests/`), any other bucket or firm, the bucket policy, versioning, logging, CloudFront, the router or the portal. The 49F gold publisher can re-emit the key; its schedule is not touched here.

CTO half: ____

Andrew: ____
