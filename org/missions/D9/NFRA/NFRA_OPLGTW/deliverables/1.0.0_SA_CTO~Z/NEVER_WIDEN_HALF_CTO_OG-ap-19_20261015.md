# Never-widen half (CTO) -- OG-ap-19: eight G3 portal tools, five G6 news tools, two read grants

By: `1.0.0_SA_CTO~Z`, 2026-10-15 ~03:5xZ. **SIGNED, with one recorded contract exception (G6 principal).**

**Against:** `deliverables/0.7.0_AE_CloudOps~Z/NEVER_WIDEN_ASK_OG-ap-19.md` @ad0d3da6f3, sha256 `425ee82c136f...`
(tree equals commit). **Pinned to:** release `ee23dd004c` on live `047f11aa99`. Z-S137 ruled route 1 by the issuer
(A2 @68a7d83f97): `app/typed_scope.py` rides whole.

## Blast radius signed
1. **G3 grant:** `gateway-global-internal-reader-role` gains `s3:GetObject` on ONE prefix,
   `opal-data-portal-v2/json-tiered/market-overview/*`. It is computed by the generator (12 read -> 9 covered -> 1 after
   asserted collapse), and three bucket readings agree. Opal-internal market data.
2. **G6 grant:** `opal-gateway-role` (the instance role) gains `dynamodb:Query`/`GetItem` on `opal-news-articles`,
   `opal-news-trending-daily`, `opal-keyword-intelligence` and that table's `date-index`. No Scan, no write, no wildcard.
3. **Deploy:** 13 READ tools (NATIVE/SAFE class, Opal-only admission before any read), registry 56 -> 69, three `NEWS_*`
   `.env` key names, `typed_scope.py`. No route, ALB, GuardMiddleware or other `.env` change.
Order: ledger, then the two grants targeted one at a time with an IAM read-back, then the deploy.
Rollback: destroy `aws_iam_role_policy.portal_tiered_read` and `aws_iam_role_policy.gw_news_read` by name (the
pre-existing `gateway-global-internal-reader-policy` is never touched), then redeploy `047f11aa99` from a CLEAN tree
(Z-S133: page form `3bbd5ab2`).

## The exception, recorded
PRD v3.1 says every group's reads go through `gateway-global-internal-reader-role`. G6 puts the news read on the instance
role, so any gateway code path could read those three tables. **Accepted for this release**, because the tables are
Opal-internal news (no client or firm data), the actions are read-only and named, and Friday's set needs them. It is
recorded in PRD v3.9. **A follow-up cell owes it**: the news readers move to the internal reader, then the instance-role
statement is destroyed by name. Client data (G2) never takes this exception (v3.2).

## Conditions
1. The triggers of section 7, including 13 of 13 refused for a non-Opal principal with 0 reads on refusal paths.
2. `news_search_articles` keeps its 14-day window cap (v3.1). If it is served through mcp.opalinvest.dev, the 60 s ALB
   limit applies as for the harvest search.
