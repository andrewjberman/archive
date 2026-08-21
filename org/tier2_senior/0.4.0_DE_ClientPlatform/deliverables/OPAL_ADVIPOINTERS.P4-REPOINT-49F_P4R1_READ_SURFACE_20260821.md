# P4R-1 -- PER-KEY READ-SURFACE ENUMERATION (ADVI / 49 Financial), + the reachability blocker on P4R-3

**TO:** OPAL_ADVIPOINTERS.P4-REPOINT-49F (COO @49dd8469d1) -- **Author:** 0.4.0_DE_ClientPlatform
**Authorizing chain:** LD-0441 (DE repoint leg, spawn-on-publish-landing) -- LD-0429 -- push plan section 3 row 4c
**Denominator:** the FROZEN KEY LIST P4E-1 (`org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/P4E1_FROZEN_SERVED_KEY_LIST_49F_20260818.md`), EMIT rows = **15 legacy keys -> 15 advi twin objects**.
**Scope handed to this seat:** the **10-key flipped set ONLY**; the 4 held keys + d14 stay legacy-served.

---

## 0. TRIGGER VERIFICATION (LD-0441 pre-flight: "verify the trigger artifact on live S3, not a report")

Verified at this seat, live, before any work:

| check | instrument | result |
|---|---|---|
| twins-publish landed | `comp-keys prefix s3://opal-data-portal-v2/platinum/advi/49financial/` | **12 keys** -- 10 leaves + `_manifests/2026-08-20/933dfc1bf6b1.json` + `_manifests/latest.json`, LastModified 2026-08-21T15:03:23Z..15:04:19Z (ISO-8601 Z, comp-keys plane) |
| manifest identity | `aws s3 cp` + parse | `run_id=933dfc1bf6b1`, `asof=2026-08-20`, `mode=publish`, `frozen_list=P4E1_FROZEN_SERVED_KEY_LIST_49F_20260818.md`, `inputs_missing=[]`, 11 rows |
| published-vs-held | manifest `rows[].status` | 10 `published` + 1 `held_by_determination` (`partner_analytics_monthly`) |
| CVO cert | `5c004cacf6` | CERTIFIED-FOR-FLIP on all 10 published twins |

**Set arithmetic reconciles independently of the direction message:** 15 EMIT - 10 published = 5 unpublished = `header_metrics`, `dashboard`, `fee_efficiency`, `partner_analytics_monthly` (the 4 held) + `advisor_nna_canonical` (d14). Matches the handed scope exactly.

---

## 1. THE READ SURFACE (P4R-1 deliverable)

**Sweep denominator: 17 hits across 414 files** (`comp-find 'api/scoped/advisor-intelligence' portal/src`). The read surface is **ONE file** -- `portal/src/api/endpoints/advisor-intelligence.ts` -- plus `useLambdaKeepWarm.ts:47`, which hits `/filters` and reads none of these keys. *(The TO said "do not assume it is one file." It was swept, not assumed; it is one file.)*

Portal reads resolve as `/api/scoped/advisor-intelligence/{path}` plus an optional `?firm={bucketSuffix(firmOverride)}`. `PLATINUM_BASE = '/api/scoped/advisor-intelligence/platinum'` (`:438`).

| P4E-1 row | key | legacy served key | portal read site | disposition |
|---|---|---|---|---|
| 6 | `mix_summary` | `platinum/firm/mix_summary.json` | `:508` (PLATINUM_BASE) | **FLIP** |
| 7 | `leaderboard` | `platinum/firm/leaderboard.json` | `:1311` (literal) | **FLIP** |
| 8 | `ownership_map` | `platinum/49financial/ownership_map.json` | **NONE -- not read by the portal** | **FLIP-set member, DISPOSED (see 2C)** |
| 9 | `timeseries_overview` | `platinum/firm/timeseries_overview.json` | `:356` (literal) | **FLIP** |
| 10 | `cumulative_chart` | `platinum/firm/cumulative_chart.json` | `:378` (literal) | **FLIP** |
| 11 | `clients-tab-slim` | `platinum/firm/clients-tab-slim.json` | **NONE -- not read by the portal** | **FLIP-set member, DISPOSED (see 2C)** |
| 12 | `timeseries_chart` (windowed) | `platinum/firm/timeseries_chart.json` | `:409` (literal) | **FLIP** |
| 13 | `timeseries_chart_full` | `gold/artifacts/timeseries_chart.json` | `:300` (literal, `/artifacts/` prefix) | **FLIP** |
| 14 | `partner_analytics_quarterly` | `platinum/firm/partner_analytics_quarterly.json` | `:369` **TEMPLATED** | **FLIP** |
| 16 | `partner_analytics_annual` | `platinum/firm/partner_analytics_annual.json` | `:369` **TEMPLATED (same site)** | **FLIP** |
| 1 | `header_metrics` | `platinum/firm/header_metrics.json` | `:284` (literal) | HELD -- stays legacy |
| 2 | `dashboard` | `platinum/firm/dashboard.json` | `:449` (PLATINUM_BASE) | HELD -- stays legacy |
| 3 | `fee_efficiency` | `platinum/firm/fee_efficiency.json` | `:480`/`:481` (PLATINUM_BASE, **both ternary arms**) | HELD -- stays legacy |
| 15 | `partner_analytics_monthly` | `platinum/firm/partner_analytics_monthly.json` | `:369` **TEMPLATED (same site)** | HELD -- stays legacy |
| 17 | `advisor_nna_canonical` | `platinum/firm/advisor_nna_canonical.json` | `:392` (PLATINUM_BASE) | d14 -- stays legacy |

Counts: **FLIP 10 + HELD 4 + d14 1 = 15.** Reconciles with the CTO/COO never-widen determination (64752/64755) and with the live S3 published/held split, each derived by an independent route.

---

## 2. THREE STRUCTURAL FINDINGS

### 2A. BLOCKER (P4R-3): the flipped twins are UNREACHABLE from every portal route family

**A path-only repoint cannot work.** Source-confirmed, then live-measured.

**Mechanism (source):** `infra/aws/lambda-edge/shared-advisor-router/index.mjs:183-204` resolves the target bucket **solely** from the requesting `firmId` (or, for `opal-capital` staff, the `?firm=` slug), and `:261-265` applies it as the origin domain:

```
const domainName = `${bucket}.s3.us-east-1.amazonaws.com`;
request.origin.s3.domainName = domainName;
```

`FIRM_CONFIG['49financial'].bucket = 'opal-data-bd'` (`infra/aws/lambda-edge/_shared/firm-config.mjs:30-33`). The URL path selects the **key**; nothing in the request selects the **bucket**. The twins are in `opal-data-portal-v2`.

**Live measurement, with the control fired in the SAME bucket** (a 404 in the wrong bucket is the wrong question asked cleanly):

| probe | result |
|---|---|
| `comp-keys prefix s3://opal-data-bd/platinum/advi/` | **0 keys -- LOUD NOT-FOUND** (true zero on this prefix) |
| POSITIVE CONTROL `comp-keys prefix s3://opal-data-bd/platinum/firm/` | **15 keys**, LastModified 2026-08-21T05:19:56Z..05:43:21Z -- live and fresh today |

So repointing `platinum/firm/X.json` to `platinum/advi/49financial/X.json` on this route resolves to `s3://opal-data-bd/platinum/advi/49financial/X.json` = **guaranteed 404 on all 10 keys**.

**The other family does not rescue it.** `opal-data-portal-v2` IS portal-reachable, but only via `/api/general/*` -> `public-data-router`, whose rewrite table (`infra/aws/lambda-edge/public-data-router/index.mjs:23-45`) has exactly four branches -- `json-tiered/`, `json/`, `mdpf/` -> `/platinum/mdpf/`, and a `/json/` fallback. **There is no `platinum/advi/` branch**, so `/api/general/advi/...` falls through to `/json/advi/...` = 404.

**And the history is pointed:** the single `portal-v2` occurrence in any edge router (denominator: 19 files scanned) is `shared-advisor-router/index.mjs:10` -- *"v3: origin migrated from opal-data-portal-v2 to opal-data-bd"*. **The ADVI route was deliberately migrated OFF the bucket the twins were just published into.**

**This is a route act, not a portal act** -- and the TO's own "Do not" reserves it: *"Do not modify the Lambda@Edge router's deployed version yourself -- router changes route through AE if any are needed (surface to COO first)."* Surfaced, not adjudicated. Two candidate remedies, with materially different security postures:

- **(A) RECOMMENDED -- teach the advisor-intelligence router to resolve `opal-data-portal-v2` for `platinum/advi/{firm}/` paths.** Keeps auth-validator-edge, keeps per-firm bucket scoping, keeps the PII posture the route was built for.
- **(B) add an `advi` branch to `public-data-router`, mirroring the WO-3 `mdpf` precedent one-for-one.** Mechanically the smaller change, with direct in-estate precedent -- **but it moves firm-scoped, PII-bearing artifacts onto the general family**, whose sibling behavior `/json-tiered/*` (CF behavior 19) carries **no auth Lambda at all**. The advisor-intelligence router's own comment (`:228-236`) records that `partner_analytics_*` embeds `clients[].label` and that `cumulative_chart.json` `adv_drill` carries `"Last, First (zXXXXXXXX)"` client labels. **Not a portal-seat call.**

**Chain consequence, stated because it is time-sensitive:** LD-0441's second conditional spawn (DT promote) fires on the CVO POST-FLIP landing. No flip means no POST-FLIP, so **that trigger never fires and the seat never spawns.** The chain does not fail loudly here; it goes quiet.

### 2B. The `:369` site serves THREE keys from ONE expression, and the determination SPLITS them

`getPlatinumPartnerAnalytics()` builds `partner_analytics_${suffix}.json` for `quarterly | monthly | annual` at a single call site. The determination flips **quarterly + annual** and holds **monthly**. **The site therefore cannot be flipped as a unit** -- flipping the template would flip the held key too, which is exactly the never-widen breach the per-key discipline exists to prevent. The tolerant read must resolve **per key**, never per call site.

### 2C. Two of the ten flipped keys have NO portal read site (disposed in writing, per P4R-1)

P4R-1 requires that a key the portal does not exercise be stated, never silently skipped. Both censuses run case-insensitively (Rule 21 -- a case-sensitive census undercounts silently and without a caveat):

| key | census over `portal/src` | disposition |
|---|---|---|
| `ownership_map` | `comp-find -i` -> **0 hits across 414 files** (measured zero) | **NOT-READ-BY-PORTAL.** Resolves P4E-1 row 8's open "consumer-cite OPEN at DE row 4c": the portal is not the consumer. The twin is published and certified; **flipping it is a no-op at this surface.** Whether a non-portal consumer reads it is outside this sweep's plane -- a portal sweep answers the portal. |
| `clients-tab-slim` | `comp-find -i` -> **1 hit**, and it is a COMMENT (`types.ts:980`, "absent in clients-tab-slim.json"), not a fetch | **NOT-READ-BY-PORTAL.** Confirms P4E-1 row 11's "key-free family". The portal reads `clients-tab` via the API-GW Lambda (`:321`), which is P4E-1 row 4 -- a different key, DECLARED-GATED. |

**So the portal-side flip population is 8 keys, not 10** -- 10 certified twins, 2 with no portal reader. Both remain flip-set members at the *serving* layer; this statement is scoped to the portal read plane and does not license removing them from the set.

---

## 3. STATE AND NEXT ACTS

- **P4R-1 -- DELIVERED (this document).**
- **P4R-2 (tolerant read) -- proceeding.** Buildable portal-side and unblocked by 2A: a tolerant read whose new-preferred leg is not yet routable simply falls back to legacy, which is what a tolerant read is for. It resolves **per key** (2B), and its new-preferred attempt stays **config-dormant** until the route lands, so no ADVI page load pays a guaranteed-404 round trip. *(Dormant-by-config is not a shadow channel: nothing stands up a parallel emitter, prefix, or comparator -- it is the single tolerant read this TO ordered, with its activation gated.)*
- **P4R-3 (flip) -- BLOCKED on 2A**, owner AE via COO. **DECLARED-HELD, all 10 keys, in writing.** No key flips while its new URL is a certain 404.
- **P4R-5 -- DT baseline confirmed live:** `origin/PROD..origin/DEV` = **0 commits**. The PROD payload will be exactly this seat's repoint commits.

## Compiler tools run

`comp-which` (routing) -- `comp-keys prefix` x4 (live S3, both buckets, positive control) -- `comp-find` / `comp-find -i` / `comp-find --name` (read-surface sweep plus absence censuses, denominators printed) -- `comp-routes behaviors` (27 CF behaviors, origin families).

-- 0.4.0_DE_ClientPlatform, 2026-08-21
