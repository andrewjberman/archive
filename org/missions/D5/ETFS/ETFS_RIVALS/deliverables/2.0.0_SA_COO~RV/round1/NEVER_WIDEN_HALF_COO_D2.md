# NEVER-WIDEN -- COO HALF: the ETFS_RIVALS round-1 live thread (`RIV-d-2`): apply, gateway deploy, BASG backfill, fire

**Signer:** `2.0.0_SA_COO~RV`, 2026-09-30 ~09:4xZ. **Pairs with:** `1.0.0_SA_CTO~Z`'s half (owed).
**Serves:** PRD `org/missions/D5/ETFS/ETFS_RIVALS/prd/ETFS_RIVALS_PRD.md` v0.2 FWD-1 (ONE live journey for BASG), task
order `ETFS_RIVALS.TO-RIV-d-2` with its ISSUER AMENDMENT 1.
**Code pin:** the merged round-1 HEAD the d-2 worktree is cut from. It carries c-1, s-1, g-1, g-2 and p-1 @`b2834dc66a`,
d-1 @`f42f12108f`, w-1 @`2274b529ef`, and w-1's amendment-1 merge. The worker prints `git log --oneline -3` first.

## VERDICT: SIGNED

The blast radius, per key. The act may touch exactly these and nothing else.

| # | key | before (measured 2026-09-30 ~09:3xZ, positive controls beside) | after | rollback |
|---|---|---|---|---|
| 1 | `s3://opal-data-etfs/issuer-site/etfs/bronze/holdings/` | 0 objects | the BASG raw files + sidecars, 2025-06-13..T-1 | a delete is a HUMAN word; forward-only otherwise |
| 2 | `.../issuer-site/etfs/silver/holdings/` | 0 | typed silver, one partition per report date | same |
| 3 | `s3://opal-data-etfs/rivalfunds/etfs/gold/canonical_shape/` | 0 | `holdings-<revision>.parquet` per report date | same |
| 4 | `.../rivalfunds/etfs/gold/trade_schedule/` | 0 | `trades-<revision>.parquet` per report date after the first | same |
| 5 | `.../rivalfunds/etfs/platinum/page/` | 0 | the day's page (+ `revisions/` on a republish) | same |
| 6-10 | `.../rivalfunds/etfs/state/{fetch_holdings,build_silver,build_canonical_shape,build_trade_schedule,publish_page}/` | 0 each | batch-complete markers | same |
| 11 | `opal-data-etfs` bucket notification configuration | EMPTY (`get-bucket-notification-configuration` returned no configuration, rc 0) | EventBridge-only | `terraform destroy -target=aws_s3_bucket_notification.etfs_data` returns it to empty |
| 12 | Lambdas `etfs-rivalfunds-daily-lambda`, `etfs-rivalfunds-fetch-holdings-lambda`, `rivalfunds-build-silver-lambda`, `rivalfunds-build-canonical-shape-lambda`, `rivalfunds-publish-page-lambda` + 5 roles, 5 role policies, 5 basic-exec attachments, 5 log groups | 0 exist (`list-functions` / `list-roles` filtered on `rivalfunds` return none; control: `etfs-netassets-daily` listed) | created | `terraform destroy -target` of each new resource |
| 13 | EventBridge rules `rivalfunds-{build-silver,build-canonical-shape,publish-page}-on-marker-created` + 3 targets + 3 permissions | 0 | created | same |
| 14 | Scheduler `etfs-rivalfunds-daily` (07:00 ET Mon-Fri) and `etfs-rivalfunds-sweep-daily` (09:00 ET) + the scheduler role and policy | 0 | created | same |
| 15 | `aws_iam_role_policy.gw_rivalfunds_read` on the gateway role, named `gateway-rivalfunds-read-policy` | absent | GetObject on key 5 only + ListBucket conditioned to key 5 | `terraform destroy -target` of that one policy |
| 16 | the opal-gateway app on its EC2 host | serving its currently deployed bytes | + `rivalfunds_view.py`, `rivalfunds_location.json`, `gen_rivalfunds_location.py`, the `server.py` routes | redeploy the pre-act bytes (the deploy script's own backup), same window |

**Writers of each named property, counted:**
- **Key 11:** 1 writer. `infra/aws/terraform/etfs-rivalfunds/triggers.tf` is the only `aws_s3_bucket_notification` whose bucket is `opal-data-etfs`, across every `.tf` under `infra/`. The live configuration is empty, so the authoritative replace deletes nothing.
- **Keys 1-10:** 5 writers, the five new Lambdas. Each role policy's PutObject is bounded to its own prefixes, and there is no DeleteObject anywhere (d-1 AC3).
- **Key 16:** 1 writer, `safe-ec2-deploy.sh`.

**Unmoved:**
- `etfs-netassets-daily` and its homes;
- the bucket's tier-first keys (`bronze/`, `silver/`, `gold/`, `daily/`, `platinum/`);
- every other bucket;
- every other gateway route and IAM policy.

## ACT-START GATES (the worker STOPS with a BLOCKING row on any)

1. **No rider on the gateway deploy.** Before step 2 (the deploy), print the file list that differs between the DEPLOYED
   gateway app and HEAD, read on the host by hash through SSM. If ANY file differs besides the four in key 16 and
   `app/tests/`, STOP: another seat's undeployed change would ride this deploy. That is that seat's deploy, never this one.
2. **Plans are create-only.** The `etfs-rivalfunds` plan is create-only, and the opal-gateway plan for
   `gw_rivalfunds_read` is create-only for that resource. Any update or destroy in either plan STOPs.
3. **Keys 1-10 still read 0 objects** at act start. A non-zero count means another writer exists: STOP.
4. **NEVER-2:** the ledger entry `etfs-rivalfunds-thread-r1` is opened, and it and its sentinel are COMMITTED before the
   first apply, after the union read over every live worktree.

## EXPECTED OUTCOME, READ FROM THE PRODUCERS' RULES, BOTH BRANCHES

- **Fetch, Branch A (issuer answers 200 per day):**
  - one raw + sidecar per trading day with status OK and a report date;
  - `r1_reachability.json` read HTTP 200 from the gateway host, so Lambda egress is expected to match;
  - AC3 requires 300 or more BASG raw objects;
  - a 404 day lands as `NOT-PUBLISHED`, is not a failure, and gets no report date (`collector_issuer.land_bronze`).
- **Fetch, Branch B (issuer refuses or times out from Lambda egress):**
  - no silver/gold/page follows;
  - the worker files a BLOCKING row, closes the ledger with the resources left in place (they are inert without data), and does not retry beyond the collector's 3 attempts.
- **Stages:**
  - each writes its marker only when its batch is whole;
  - a guardrail failure publishes a `not-updated` page and returns PARTIAL with NO marker (p-1, row W1-S5). That is an honest outcome and AC1 grades it;
  - every trade grades UNRESOLVED, because the crosswalk resolves 0 of 35 (row W1-S4). This is expected in round 1, not a defect of this act.
- **Gateway:** `/rivalfunds` serves the newest page byte-for-byte behind the ALB OIDC action; `/healthz` reads 200 after the deploy.

## ROLLBACK

- **Keys 11-16:** `terraform destroy -target` of only the new resources, or redeploy of the pre-act gateway bytes, same window.
- **Keys 1-10:** new objects under new prefixes nothing else reads. A delete is a HUMAN word, never the worker's.
