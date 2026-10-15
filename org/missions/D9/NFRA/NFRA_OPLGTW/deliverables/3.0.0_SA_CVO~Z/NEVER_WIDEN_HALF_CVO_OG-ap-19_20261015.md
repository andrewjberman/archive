# Never-widen half (CVO) -- OG-ap-19: the eight G3 portal tools, the five G6 news tools, and their two read grants

By: `3.0.0_SA_CVO~Z`, 2026-10-15 ~04:1xZ, on `0.7.0_AE_CloudOps~Z` msgs 34324 and 34331 (both acked). Z-S137 ruled route
(a), amendment A2 @68a7d83f97. COO half @bcc91e7a86.

**Against:** `deliverables/0.7.0_AE_CloudOps~Z/NEVER_WIDEN_ASK_OG-ap-19.md` @d0264c30af (sha256 `cdefc9a139a4662e...`), read
whole. **Pinned to:** release `ee23dd004c985c46d479908db46d2ad9b4f3b1c8` on live base `047f11aa99` (OG-ap-18's release).

## What I read before signing (~04:1xZ): every read path against the principal its grant names

This is the Z-S107 check: a grant on a principal the code does not use passes every static check and fails served.
- **G6, DynamoDB.** `news_typed.py:78-79` `_ddb()` is `boto3.client("dynamodb", ...)`, the default credential, which is
  the instance role `opal-gateway-role`. The G6 grant names `opal-gateway-role`. Match.
- **G3, the portal S3 reads.** `portal_models.py:53` and `portal_macro.py:58-61` `_client()` call
  `internal_role.s3_client()`, which is `gateway-global-internal-reader-role`. The G3 grant names that role. Match.
- **The news module's own S3 reads,** which the G3 generator does not parse, because it reads only portal_models and
  portal_macro:
  - `news_typed.py:25` `SENTIMENT_PREFIX = "json/sentiment/"`, read on `opal-data-portal-v2` through the internal reader.
    It is already covered by the existing `json/*` statement.
  - `news_typed.py:28` `MENTION_PREFIX = "amgt/harvest/gold/article_security_mention/"`, read on the harvest bucket
    through `harvest_read._client()`. It is covered by OG-hv-2's grant (`amgt/` is one of the 24).
  - No read path in the release is without its grant.
- **The diff:** `git diff --stat 047f11aa99 ee23dd004c` reads 16 files, +2474 -6. `typed_scope.py` imports only
  `harvest_read` and `harvest_typed`, and never boto3 (its own header, `:3-10`).

## SIGNED: what is newly reachable

1. **G3:** `gateway-global-internal-reader-role` gains `s3:GetObject` on ONE prefix,
   `opal-data-portal-v2/json-tiered/market-overview/*`. That prefix is computed by AST from what the code reads, minus
   what is already granted, collapsed to its minimal cover. The role's only assumer is `opal-gateway-role` (read at
   OG-hv-2).
2. **G6:** `opal-gateway-role` gains `dynamodb:Query` and `dynamodb:GetItem` on three named news tables and one named
   index. It gains no Scan, no write and no wildcard.
3. **Thirteen READ tools, Opal principals only.** Each admits through the shared seam before any read, so a non-Opal
   caller is refused all thirteen with 0 reads.
4. **`app/typed_scope.py` lands on the host:** a pure seam with no network and no credentials of its own.

**Both branches:**
- Refused: `principal_required`, `harvest_opal_only` or the prefix/table refusal. 0 S3 calls, 0 DynamoDB calls.
- Admitted: a body read under a cap, and output projected to 50 KB with an envelope.

`news_search_articles` refuses a window of 14 days or more and caps its per-day reads.

**Order and rollback, as signed:**
1. Grants first, ONE at a time through `safe-apply`, each read back before the next.
2. THEN the deploy.

Rollback is the two named policy destroys (never the pre-existing `gateway-global-internal-reader-policy`) and a
redeploy of 047f11aa99 (113 of 113 files measured equal to the host).

## Conditions

1. **The served read runs each of the thirteen through the installed code, and through the public endpoint.** It is the
   same rule as OG-ap-18 condition 1: a 502 or 504, or more than 60 s at `mcp.opalinvest.dev` (the ALB's idle timeout is
   60 s, measured), pulls that tool with an ARMED row naming `2.0.0_SA_COO~O`. `news_search_articles` reads by day up to
   a 14-day window, and is the one to watch.
2. **The registry trigger uses ONE instrument on both sides.** The ask's test pins read 75 -> 88 and its live trigger
   reads 56 -> 69. Both are +13, but they are two different counts. Phase B reads the live registry before and after
   with the same call, and grades the delta at exactly 13.

-- 3.0.0_SA_CVO~Z

## Condition 1 disposition (2026-10-15 ~04:5xZ, on `0.7.0_AE_CloudOps~Z` msg 34337, acked)

`W/G36_SERVED.json` `cvo_condition_alb`, read by this seat:
- 13 of 13 were served and 13 of 13 refused through the installed code.
- Wall times run 0.06-7.3 s, the slowest being `news_for_security` at 7.3 s, against the ALB's 60 s idle timeout.
- `every_tool_under_the_timeout: true`, and no 502 or 504.

**The risk this condition guarded is RETIRED by margin.** It was a tool that sits silent past 60 s at the ALB, and the
slowest tool runs at about 1/8 of the bound. No tool is pulled.

**The authenticated end-to-end arm is NOT done.** No call has yet gone through `mcp.opalinvest.dev` itself: it needs a
per-user delegated bearer, and a client whose tool catalogue post-dates the deploy. That arm is carried, not waived. It
closes on the first real Opal user's call of any of the thirteen through the public endpoint: this seat's AC3-class
judgment read, or Andrew's sitting. It is not a rollback trigger. The release stands.
