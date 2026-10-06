# Lead Panel load time -- findings for a brief (2.0.0_SA_COO~Z to 4.0.0_SA_CRO~Z, 2026-10-05)

**Purpose.** Brief input. Everything measured on the Lead Panel load question so far, what is fixed, what is not, and what is
still unknown. Each figure names the plane it was read on.

## 1. The question

**Andrew-direct 2026-10-05 ~15:0xZ**, record
`org/tier1_exec/2.0.0_SA_COO/deliverables/ANDREW_DIRECT_20261005_150xZ_SECURITY_ANALYSIS_ALL_OPAL_EMPLOYEES_REQUIREINTERNAL_LEADPANEL_LOAD_TO_COO_Z.md`:

> "I suspect that some lambdas are doing live computation when the served file should be precomputed. Specifically ... what
> appears in the lead panel; the chatter/price views take almost a minute to load."

His follow-up, about 16:4xZ, asked four things:
- Is everything precomputed?
- Is this progressive disclosure or loading practice?
- Is it data size, and is everything gzipped?
- Is there computation or retrying that a load is contingent on?

Related: the DSGN PROD promote waits on this answer (COO~D msg 29675, record
`org/tier1_exec/2.0.0_SA_COO/deliverables/ANDREW_DIRECT_20261005_155xZ_DSGN_PROD_PROMOTE_ALL_UPDATES_AFTER_LEAD_PANEL_SPEED_CLARITY.md`).

## 2. Short answer

- **The data is precomputed.** The time goes to work each request does around the stored data, not to computing the
  rankings or counts. The price lists read a ranking the producer already built and stored. Before answering, each request
  then fetches extra details for every ranked name: about 100 network reads, one after another. Nothing is kept between
  requests, so a warm call costs about the same as a cold one.
- **It is not data size.** Responses are 87-110 KB, which is 7-11 KB gzipped. The declared edge behavior compresses.
- **Retries are a multiplier, not the cause.** Every Lead Panel read retries twice on failure. No failure was seen in our runs.
  Andrew's sessions are unmeasured.

## 3. Measurements

### 3a. Deployed function, timed inside the Lambda

The deployed function is `opal-amgt-scoped-api`, CodeSha256 `GS//XHnV...`, 1769 MB. Times are REPORT Duration. Read
2026-10-05 ~16:4xZ, two calls each, warm container.

| route | in-Lambda time | wall time | body | gzipped |
|---|---|---|---|---|
| `/lead-panel/timeseries/collected/chatter?days=30` | 10.6-11.0 s | 10.7-11.4 s | 87,021 B | 7,481 B |
| `/lead-panel/rankings/trending/price` | 4.5-4.9 s | 4.5-5.0 s | 108,832 B | ~10,350 B |
| `/lead-panel/rankings/breakout/price` | 4.6-4.8 s | 4.7-4.9 s | 109,994 B | 10,708 B |
| `/lead-panel/rankings/trending/chatter` | 39 ms | ~0.1 s | 1,129 B | 601 B |

- **Wall time is about equal to in-Lambda time**, so transfer and invoke overhead are not the cost; the function's own work is.
- **The trending/chatter ranking is not a fair fast control.** Its 1,129 B body serves no rows, an EMPTY list (research read of
  2026-10-05).
- **The issuer's warm sweep over 9 reads** (`round71/checks/r71_latency.py --where deployed`, about 15:1xZ) agrees:
  chatter 9.4-9.8 s at days 30/90/365, and price rankings 3.7-4.9 s at the default window, 90 and 365.

### 3b. Where the time goes (local phase timing; the local network inflates every read)

The issuer instrumented the functions. One warm-up run, then a timed run, on 2026-10-05.

| route | total | the largest phase |
|---|---|---|
| `read_rankings("trending", "price")` | 16.4 s | `_join_classification` 12.6 s (one call) |
| `read_monthly_chatter(30)` | 60.8 s | `_join_classification` 13.2 s, plus repeated pointer and generation reads |

The rest of the rankings run:
- the pointer reads, 0.66 s over 5 calls;
- the backward pointer walk, 0.53 s;
- `_join_places_moved`, which reads the previous generation, 0.51 s;
- the generation rows, 0.44 s;
- `_join_covered_identity`, 0.28 s;
- `_serve_percent`, about 0 over 94 rows.

The chatter route aggregates 58,512 `chatter_daily` rows and 31,042 `article_security_mention` rows in Python. On a warm
process that took well under a second; the cold read of those gold objects was not timed separately.

### 3c. The worker's call census

Source: `AMGT_RESAPP.TO-AMGT-au-6`, worker `0.9.0_WK_AMGT_RESAPP~236`, `PROFILE.md` @4f9322fad7. It is on the worker's branch
until the drain.

- **Botocore network time** is 25 of 26 s on a rankings call and about 52 s on chatter, both local. Python decode plus compute
  is under 0.6 s.
- **Calls per request** (GetItem / List / GetObject / Query):
  - chatter: 289 / 58 / 53 / 2;
  - rankings: 99 / 25 / 25 / 2.
- **What the calls are:**
  - one serial `etf-classifications` GetItem per ranked name, 94-110 per rankings request, about three times that on chatter;
  - one model-block List plus GET per name the crosswalk does not name, 23-57 per request;
  - the generation-pointer walk;
  - a fresh `boto3.resource` built on every call.

### 3d. The edge and the portal (read from source, the DESIRED plane)

**Edge** (`comp-routes behaviors`, and the cloudfront-distribution.tf behavior for `/api/scoped/amgt/*`):
- the behavior goes to API Gateway, behind `auth-validator-edge`;
- `compress = true`;
- `cache_policy = caching_disabled`.

This is the declared config, not a live `describe-distribution`. The function itself returns no `content-encoding`.

**Portal** (`portal/src/pages/SecurityAnalysis/hooks/useLeadPanelApi.ts`):
- Every Lead Panel query has `retry: 2` and `staleTime` 5 min, including rankings, the rank time series and collected chatter.
  Under React Query's default backoff, one failed request can cost roughly three times its own time, plus about 3 s.
- `LeadPanel.tsx:432` fetches collected chatter only when the Chatter face is chosen.
- `SecurityOverlay.tsx:310` calls `useCollectedChatter()` with no condition, so opening a security overlay pays the
  10-11 s chatter read. It shares the cache key, so the read is deduplicated with the Lead Panel's.
- The timeline queries use `retry: 0`.

## 4. What this rules in and out

| hypothesis | finding |
|---|---|
| Heavy computation at serve time | **Mostly no.** Rankings are read from stored generations. Chatter recounts gold rows per request, but that compute is under 1 s. |
| Payload size or no gzip | **No.** 7-11 KB gzipped, and the edge is declared to compress. |
| Many sequential network reads per request, nothing cached | **Yes: this is the measured cost.** About 100-290 serial AWS calls per request. |
| Retries | **A possible multiplier, unmeasured in a real browser session.** Two retries per query. |
| Progressive disclosure | **Partial.** The chatter read is deferred on the Lead Panel, but the overlay requests it unconditionally. |

**"Almost a minute" is NOT reproduced on the deployed function warm**; the worst warm read is 11 s. Unmeasured candidates:
- a cold container, which pays its start (pyarrow import) plus the same serial reads;
- several cold requests at once on first page load;
- a failure followed by retries.

A browser network trace of a real session is the instrument that would settle it, and none has been taken.

## 5. What is done, and what remains (with owners)

**Fix built, not yet served: `AMGT_RESAPP.TO-AMGT-au-6`.** Worker `~236`, @4f9322fad7, proof VALID.
- A per-container memo (`lib/research/api/served_cache.py`):
  - the generation rows are keyed on generation id plus row count, so they are never stale;
  - the pointer is held 60 s;
  - classification and model-block name lookups are held 300 s;
  - misses are read 8 at a time;
  - one DynamoDB resource per container.
- **Values are unchanged:** 9 of 9 bodies are equal before and after.
- **Local results** (cold / warm): chatter 7.8-18.6 s / 0.92-0.97 s; price rankings 5.1-29.4 s / 0.15-0.35 s. Local network
  adds about 150-250 ms per call.
- The 60 s and 300 s bounds are the worker's choice and are not ratified.

**Remaining:**

| step | owner | state |
|---|---|---|
| Drain au-6 into CLOUD | `2.0.0_SA_COO~Z` | held by the PARITY HOLD (Andrew-direct ~16:2xZ via MSTR~Z msg 29693) until PARITY CLOSED |
| Redeploy under a never-widen pair; the deployed bar is 2,000 ms warm on all 9 reads (`r71_latency.py --where deployed`) | `0.7.0_AE_CloudOps~A` (`AMGT_RESAPP.TO-AMGT-au-7`), halves from COO~Z + CTO~Z | staged; the deployed result is unmeasured until it lands |
| Cold first read: the producer stores classification and name on the ranking generation rows, so a request does no lookups (row `AMGT_RESAPP-Z-W236-S1`) | not yet owned; a new producer act, so a brief or round-72 item | open |
| Chatter monthly aggregate stored at the gold build as a served object, instead of recounted per request | not yet owned; same class | open (a proposal) |
| The overlay's unconditional chatter read becomes on demand | DSGN_AMGTV1 (portal) | open (a proposal) |
| A browser network trace of a real session, cold, to confirm the "almost a minute" path | unassigned | open |
| Edge caching of these daily-changing reads (today `caching_disabled`) | CTO decision | a proposal only. These responses are auth-gated and firm-scoped, so any cache must key on the firm. |

## 6. Adjacent finding (same root as "the served file should be precomputed")

**The producers' universe object is stale.** `universe/v1/2026-09-16.json` holds 53 of the 95 covered names.
- `/freshness` read from it and missed 42 names. au-4 fixed that, drained @18931420f3.
- The gold mention producer's own securities reader reads the same object, so a gold rebuild reaches 53 of 95 names. This is
  au-3 row `AMGT_RESAPP-Z-W233-S2`, on the worker branch @95efb21eb1.
- A served file built from a stale input list is precomputed and still wrong. Refreshing that object is a producer act with
  no owner yet.

## 7. Sources

- Issuer checks: `org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round71/checks/r71_latency.py` and `r71_served.py`
  (issuance @46bc7b252a).
- Decomposition s.79: `org/missions/D5/AMGT/AMGT_RESAPP/decompositions/AMGT_RESAPP_DECOMP.md`.
- The au-6 profile: worker branch `wk-AMGT_RESAPP-236` @4f9322fad7,
  `org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~236/PROFILE.md`. It reaches CLOUD at the drain.
- Route code:
  - `lib/research/api/scoped_amgt.py` `read_rankings` (~:1261) and the dispatch (~:6030-6060);
  - `lib/research/api/monthly_chatter.py` `read_monthly_chatter` (:255).
- Portal: `portal/src/pages/SecurityAnalysis/hooks/useLeadPanelApi.ts`, `components/LeadPanel.tsx:432`,
  `components/SecurityOverlay.tsx:310`.
