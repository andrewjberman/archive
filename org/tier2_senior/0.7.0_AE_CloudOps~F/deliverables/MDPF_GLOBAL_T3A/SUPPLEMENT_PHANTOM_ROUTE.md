# T3.A Supplement -- Phantom root route: live behavior, plane-labeled (COO 210339Z / CTO T2.B ruling item 4)

**Author:** 0.7.0_AE_CloudOps~F | **Captured:** 2026-08-03 21:06-21:08Z | **Raw:** `headers-supplement.txt`
**Status note:** COO 210601Z ruled the supplement retroactively satisfied by the census's 20:51:16Z 403 row; this addendum
is the DEEPER capture that was already in flight when that ruling landed -- filed as T5.A input, no reopen implied.

## A. What the phantom route actually serves

`GET /api/general/mdpf/aggregate-aua-timeseries.json` (authenticated) ->
**HTTP 403, `Content-Type: application/xml`, S3 `AccessDenied` XML body, `Server: AmazonS3`, `X-Cache: Error from cloudfront`.**

**Plane label: the S3 ORIGIN answered.** The request passed the edge validator (a rejected token returns the edge's own 401,
not S3 XML), passed router v6's rewrite (`/api/general/mdpf/` -> `/platinum/mdpf/`), and died at S3 on the nonexistent key
`platinum/mdpf/aggregate-aua-timeseries.json` -- 403-not-404 because the origin access identity has no ListBucket. It is NOT an
edge-generated error, NOT a custom error page (live distribution has `CustomErrorResponses.Quantity=0`), NOT a stale cached
object, and NOT a fallback to the per-scope global key.

Error-caching probe (hit 2, +3s): second 403, no `Age` header on either -- cached-vs-refetched is NOT distinguishable from
these headers alone; with zero CustomErrorResponses the distribution is on CloudFront default error caching. No number
asserted (measured-inconclusive).

## B/C. The vintage contrast the phantom hides (T5.A input)

| Route (same behavior, same policy) | Status | S3 key | Last-Modified | Body vintage |
|---|---|---|---|---|
| `/api/general/mdpf/aggregate-aua-timeseries.json` (phantom) | **403** | `platinum/mdpf/aggregate-aua-timeseries.json` -- DOES NOT EXIST | -- | -- |
| `/api/general/mdpf/aggregate_aua_timeseries.json` (underscore sibling -- the file portal_data_proxy `/aum/aggregate-mdpf` reads) | 200 | `platinum/mdpf/aggregate_aua_timeseries.json` | 2026-07-31 15:00:01Z | `as_of_last=2026-07-31`, `n_dates=436`, `generated_at=2026-07-31T15:00:00Z` |
| `/api/general/mdpf/global/aggregate-aua-timeseries.json` (the live portal consumer route) | 200 | `platinum/mdpf/global/aggregate-aua-timeseries.json` | 2026-08-03 16:15:32Z | `as_of_last=2026-07-30`, `n_dates=453`, `generated_at=2026-07-31T15:00:37Z` |

Three facts for T5.A, recorded not adjudicated:

1. **The underscore sibling is REACHABLE through the same CF behavior and serves the 07-31-generated root artifact** -- anyone
   "fixing" the phantom client-side by switching hyphen->underscore silently binds to a DIFFERENT artifact than the per-scope
   global key the portal actually consumes.
2. **The two 200s disagree on frontier and coverage:** underscore root `as_of_last=07-31` / 436 dates vs global scope
   `as_of_last=07-30` / 453 dates, generated 37s apart in the same 07-31T15:00Z window. (Calendar note: 08-03 is a Monday;
   07-31 Friday is the correct T-1 frontier. The global slice sits one trading day behind the root on `as_of_last` while
   carrying 17 MORE dates. Mechanism not established here -- `INFERRED` candidates: different slicers, different
   None-padding/coverage rules. T5.A's delta census owns the adjudication.)
3. **The 08-03 12:15 publisher run re-wrote the global key with content generated 07-31** (S3 Last-Modified 08-03 16:15:32Z vs
   body `generated_at=2026-07-31T15:00:37Z`) -- an S3 write timestamp on this path is a PUBLISH event, not a data-vintage claim.
