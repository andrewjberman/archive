# MDPF_GLOBAL.T3A -- Cache Census, live-grounded

**Author:** 0.7.0_AE_CloudOps~F | **Captured:** 2026-08-03 20:40-20:55Z | **Status:** COMPLETE (read-only; zero mutations, zero invalidations fired)
**Vintage:** workspace @440d16e018, portal @5ef651b202 (DEV), distribution EVTSA9VEHNZVH config ETag E1H04CVXQPZ22Z (LIVE pull)
**Machine-readable:** `cache-map.json` (same directory). **Raw measured headers:** `headers-pass1.txt`, `headers-pass2.txt`.
**Grounding:** every layer grounded per Rule 22a -- live `get-distribution-config` / `get-cache-policy`, DEPLOYED lambda artifacts
(`get-function` on the exact versions the distribution pins, zips downloaded and read), `s3api head-object`, and measured viewer
headers via authenticated curl (short-lived QA token, minted and destroyed in-session). comp-routes seeded the behavior denominator
only (it is cache-policy-blind -- CVO register @aeca48e395; gap still open, confirmed this run).

---

## The headline

**The MDPF serve path has FIVE cache layers, and the one every browser obeys is ungoverned.** Since the 07-29 router flip
(`/api/general/mdpf/` -> `/platinum/mdpf/`, deployed public-data-router v6), the cache-control-injector no longer fires on MDPF
responses -- its deployed v2 stamps only URIs starting `/json/`. The MDPF publisher sets no S3 Cache-Control metadata either.
**Measured result: every MDPF response reaches the browser with NO Cache-Control header at all** (9/9 live routes, both passes).
CloudFront still caches fine (DefaultTTL 300 applies at the edge), but the browser falls back to RFC 9111 heuristic freshness
(~10% of object age) -- a silently growing client-side TTL nobody set and no invalidation can reach.

This also closes DT's behavior-16 nuance from this morning with a source-confirmed mechanism: json-tiered responses show bare
`max-age=300` because there too the injector does not fire (rewrite is `/json-tiered/`, not `/json/`) -- but json-tiered
producers stamp S3 metadata (`rsi-summary.json` CacheControl `max-age=300`, measured live) and it passes through. Same mechanism,
different producer discipline: **the stamp DT saw on json-tiered is S3 metadata; mdpf has none.**

## Layer map (route family `/api/general/mdpf/*` -> behavior `/api/general/*`)

| # | Layer | TTL | Invalidation mechanism | Measured evidence |
|---|---|---|---|---|
| 1 | CloudFront edge | **300s** (policy `ce00305d` opal-api-general-5min-cache, min 0 / def 300 / max 31536000; DefaultTTL operative because origin sends no Cache-Control). Cache key: qs=none, headers=none, cookies=none. **Policy exclusive to this behavior** (blast radius 1). | **None on publish** (publisher fires no create_invalidation; `lambda_function.py:133` is a bare put_object). TTL-expiry only. DataRefresh ROLLBACK invalidates `/api/general/*` (covers mdpf as a side effect; does NOT restore platinum/mdpf objects). | Pass1 20:51Z: 9/9 `Miss from cloudfront`. Pass2 +2m45s: `Hit`, Age 160-167. Pass3 +3m30s: `Hit`, Age 208-214. Cycling under 300. |
| 2 | cache-control-injector (origin-response edge) | Stamps `public, max-age=300, s-maxage=300` **only when post-rewrite URI starts `/json/`** | n/a (stateless) | Deployed v2 (sha `MzQqr+iR...`, 2026-04-15) read in full: single `startsWith("/json/")` conditional. Router v6 rewrites mdpf to `/platinum/mdpf/` -> **injector never fires on mdpf**. Confirmed at viewer: zero cache-control headers on all responses. |
| 3a | React Query (client) | `staleTime` **5 min** on all 5 mdpf keys (client default is Infinity; mdpf keys override). `gcTime` Infinity. | staleTime expiry + remount; `queryClient.clear()` on logout. **Zero `invalidateQueries` on mdpf keys.** | `ModelPortfolios.tsx:417-548` (5 keys); `main.tsx:37-59` defaults. @5ef651b202 |
| 3b | Module memory caches (client) | **60 min** (`ACCOUNT_DIST_CACHE_TTL`, `aum.ts:510`) on account-distribution + aum-metrics fetchers | `forceRefresh` param (no live caller) + page reload only | `aum.ts:528-546, 606-624`. Stacking: an RQ refetch at 5m re-invokes the fetcher and gets the SAME bytes back from this cache -- **effective client TTL up to 60 min** for those two artifact types. Timeseries fetchers have no module cache (RQ 5m is operative). |
| 3c | Browser HTTP cache | **Heuristic** (no Cache-Control served; ETag + Last-Modified present) -- ~10% of object age, growing | None (no header governs it); ETag revalidation only after heuristic expiry | All 9 routes: no cache-control, ETag + Last-Modified present (headers-pass1.txt) |
| 4 | S3 origin metadata | **None** -- CacheControl null on 9/9 served keys | Overwrite on publish (same key) | head-object 9/9 keys ~20:47Z: CacheControl null, all LastModified 2026-08-03 16:15:31-33Z. Publisher `opal-assets-mdpf-portal-publisher` deployed sha `WSwmCWpl...` 07-28, SERVE_ROOT=platinum/mdpf. |

## Denominators (printed per s.C.4)

- **CF behaviors: 25/25 enumerated live** (24 + default), every one with policy identity + TTLs resolved from the live
  distribution (full table in `cache-map.json.behavior_denominator_all_25`). Policy sharing: ce00305d x1 (mdpf, exclusive),
  3eda5c45 x2 (json-tiered pair), 45eb7514 x4 (advisor S3), 4135ea2d Managed-CachingDisabled x17, 658327ea CachingOptimized x1
  (SPA default). comp-routes DESIRED plane and live config agree 25=25, patterns 1:1.
- **Edge functions on the serve path: 3/3 deployed artifacts pulled and read** (auth-validator-edge:18, public-data-router:6,
  cache-control-injector:2 -- the exact versions the live distribution pins).
- **Live scopes: 4/4** (`49financial`, `cottonwood`, `inflection`, `global`) from the live bucket listing; 9 served hyphenated
  keys + 1 legacy root route = **10/10 routes measured** (9x 200, 1x 403 dead-legacy).
- **Client: 5/5 mdpf React Query keys + 2/2 module caches + QueryClient defaults** grounded at file:line @5ef651b202;
  comp-cache captured 103/103 useQuery sites (collision view clean for mdpf).
- **S3: 9/9 served keys head-checked** for metadata.

## W9/W9b baseline folded (not rediscovered)

- W9: `ce00305d` DefaultTTL 300 on `/api/general/*` -- confirmed live this census, unchanged since the 17:10Z deploy (tag portal-auth-v1.21.0).
- W9b: `45eb7514` opal-scoped-advisor-by-firm DefaultTTL 60, X-Firm-Id + qs-whitelist cache key intact -- confirmed live on all 4 advisor S3 behaviors (tag portal-auth-v1.22.0). Not on the mdpf path; recorded for the policy-sharing denominator.
- DT's dual-TTL authenticated capture (Age 81/82 under 300; Age 20 under 60) stands as the behavioral baseline; this census adds the mdpf-route-specific measurements + the injector/metadata mechanism grounding.

## T3.B clash flags (flag only -- nothing fixed)

1. **F1 NO-CLIENT-TTL (the real one):** no Cache-Control on mdpf -> browser heuristic caching grows with artifact age
   (~2.4h at 1 day). A daily publish can be invisible to returning browsers for hours and NO invalidation reaches them.
   T3.B options: extend the injector stamp to `/platinum/mdpf/` (edge deploy) OR stamp CacheControl at the publisher
   put_object (one-line lambda change + republish). The second also fixes it for any future non-CF consumer.
2. **F2 NO-PUBLISH-INVALIDATION:** edge staleness after publish bounded by 300s -- fine for a daily clock, but if T2.C rules a
   tighter freshness expectation the 300s tail clashes; publisher-side create_invalidation would need `cloudfront:CreateInvalidation`
   the egress role deliberately does not hold today.
3. **F3 60-MIN-MODULE-CACHE:** the client 60-min in-memory caches span any publish window in an open tab regardless of edge
   design; changing this is a portal release, not infra.
4. **F4 ROLLBACK-SEMANTICS:** DataRefresh rollback purges the mdpf edge cache (path `/api/general/*`) while not restoring
   platinum/mdpf objects -- a rollback re-pulls the same post-publish mdpf bytes fresh. Coherent, but T3.B should state it.

## Non-blocking findings (routed, not mine to fix)

- **N1** Source-comment drift: `aum.ts:520-523,560` + `portal-proxy.ts:497-501,515-519` still describe the pre-flip `/json/`
  rewrite + `json/mdpf/*` keys (DE/DT lane touch).
- **N2** Dead root fetcher: `portal-proxy.ts:505-509` targets a key that no longer exists (measured 403); zero page consumers.
- **N3** `aum-metrics.json` exists only for cottonwood -- matches the cottonwood-only `enabled` predicate; by design, not a gap.
- **N4** ce00305d has qs=none -- query-string cache-busting is a NO-OP on mdpf routes; any T3.B buster must be path-based.
