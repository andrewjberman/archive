# MDPF_REVAMP -- re-point router-translation DESIGN (SEV1 cutover control)

**Author:** 0.2.0_DT_PortfolioAnalytics · **Date:** 2026-07-20 · **To:** 1.0.0_SA_CTO (GATE -- early review per gate msg 203216Z) · **Apply:** 0.7.0_AE_CloudOps (CF/origin/policy)
**STATUS: GATE-APPROVED (CTO 204033Z) -- Q1=IN-ALL, Q2=s3 (isolated), Q3=OAC; 2 hard reqs folded (s7). This is the CUTOVER CONTROL. It is NOT applied now** -- it lands only at the never-widen co-signed re-point (CTO+Andrew), after parity streak N=3. Built alongside; nothing re-points until co-sign.
**Surface class: SEV1** (`public-data-router` / the public-data CF behavior) **+ security-adjacent** (S3 origin selection). Designed to touch the SEV1 router as little as possible.
**Plan parent:** `MDPF_REVAMP_DT_PAGE_PORTAL_PLAN_20260720.md` (a)/(b)/(c) @0da51a8c9.

---

## 1. Grounding (@HEAD, this session)

- **CF behavior 18 `/api/general/*`** (`comp-routes behaviors`): -> origin `S3-opal-data-portal-v2-json`; viewer-request `auth-validator-edge` (AUTH); origin-request `public-data-router` (rewrite `/api/general/*`->`/json/*`); origin-response `cache-control-injector`. **This ONE catch-all behavior carries EVERY `/api/general/mdpf/*` AND `/api/general/portfolios/*` request** -- there is no mdpf- or portfolios-specific behavior (1-17 are trades/advisor-intelligence/security-scanner/data-refresh/tickets/json-tiered; 19-24 are private/v1/auth/partners).
- **`public-data-router`** (`infra/aws/lambda-edge/public-data-router/index.mjs`): pure URI rewrite, origin unchanged. **Lambda@Edge => NO environment variables** (AWS constraint) -- any config/flag must be baked into code or expressed in CF config, never an env toggle.
- **Complete MDPF-family FE fetch map** (grounded at the page: `ModelPortfolios.tsx:365-394`; `aum.ts:517-597`; `portal-proxy.ts:255-506`):

| # | FE hook (queryKey) | Request path | Served key (opal-data-portal-v2) | Wave-1 bucket slot (opal-data-assets) | Scope |
|---|---|---|---|---|---|
| A5/A6-firm | getMdpfAggregateAUATimeSeriesByFirm(firm) (`mdpf-per-firm-timeseries`) | /api/general/mdpf/{49financial,inflection}/aggregate-aua-timeseries.json | json/mdpf/{firm}/aggregate-aua-timeseries.json | portal/model-portfolios/{firm}/aggregate_aua_timeseries.json | IN |
| A5/A6-global | getMdpfAggregateAUATimeSeriesByFirm('global') (`mdpf-aggregate-timeseries`) -- **Global COUNT path only** | /api/general/mdpf/global/aggregate-aua-timeseries.json | json/mdpf/global/aggregate-aua-timeseries.json | portal/model-portfolios/global/aggregate_aua_timeseries.json | IN |
| A3/A7-firm | getAccountDistributionByFirm(firm) (`mdpf-per-firm-distribution`) | /api/general/mdpf/{49financial,inflection}/account-distribution.json | json/mdpf/{firm}/account-distribution.json | portal/model-portfolios/{firm}/account_distribution.json | IN |
| A4 | getNonModelAssets() | /api/general/portfolios/non_model_assets.json | json/portfolios/non_model_assets.json | portal/portfolios/global/non_model_assets.json | IN |
| A3-global | getAccountDistribution() -- **Global bell curve** | /api/general/portfolios/account-distribution.json | json/portfolios/account-distribution.json | portal/portfolios/global/account_distribution.json | IN (Q1=IN-ALL) |
| A1 | getAUMMetrics() | /api/general/portfolios/aum-metrics.json | json/portfolios/aum-metrics.json | portal/portfolios/global/aum_metrics.json | IN (Q1=IN-ALL) |
| A2 | getAUMTimeSeries() -- **Global VALUE trend** (ModelPortfolios.tsx:373-377) | /api/general/portfolios/aum-timeseries.json | json/portfolios/aum-timeseries.json | portal/portfolios/global/aum_timeseries.json | IN (Q1=IN-ALL) |

**ALL 7 MDPF-family fetches are IN scope (CTO Q1=IN-ALL, 204033Z)** -- the flip leaves NOTHING on the legacy path; the 3 global portfolios/ homes are already A1/A2/A3 projection scope (DS TO-2/TO-3), so this is homes+behaviors, not new projection work. DS emit-set updated (msg 204149Z).

---

## 2. The two hard constraints

1. **Cannot repoint behavior 18.** It carries ALL `/api/general/*` (market, trending, semantic-trending, cma, positioning, ...). opal-data-assets holds only the mdpf/portfolios subset, so a blanket origin swap 404s everything else. **The re-point MUST be SELECTIVE to the enumerated MDPF-family keys.**
2. **Key bodies diverge, so a bare origin swap 404s even the in-scope keys:** served `json/mdpf/{firm}/aggregate-aua-timeseries.json` (hyphens, mdpf prefix) vs new `portal/model-portfolios/{firm}/aggregate_aua_timeseries.json` (underscores, channel-first prefix). **A key-body translation is mandatory** -- and only a Lambda can rewrite the key body; CF path-patterns cannot.

---

## 3. RECOMMENDED design: ISOLATED new behaviors + a NEW translation lambda; `public-data-router` UNTOUCHED

Rationale for a SEV1 surface: **do not modify the battle-tested `public-data-router`.** Add the re-point as MORE-SPECIFIC CF behaviors placed at HIGHER ORDERED PRECEDENCE than behavior 18 (see s3e.1 -- CF is ordered precedence, NOT automatic longest-match), backed by a NEW, single-purpose translation lambda. Everything else -- and the entire existing router -- stays byte-identical.

**3a. New S3 origin (AE):** add `opal-data-assets` as a 2nd origin on the distribution with **OAC** + a bucket policy allowing that OAC `s3:GetObject` on **`portal/*` ONLY** (prefix-scoped, never bucket-wide, never a source layer).

**3b. New CF behaviors (AE), each MORE SPECIFIC than behavior 18** (so they win by CF precedence), each preserving the existing edge chain:
- viewer-request `auth-validator-edge` (**PRESERVE the auth gate -- these are authenticated `/api/general/*` paths**)
- origin `opal-data-assets` (the 3a origin)
- origin-request = **NEW** `mdpf-data-router` lambda (key translation only, s3c)
- origin-response `cache-control-injector` (unchanged)

Patterns:
- `/api/general/mdpf/*` (ONE wildcard behavior -- covers global-slice + per-firm aggregate-aua-timeseries + per-firm account-distribution; `mdpf/*` is a clean MDPF-only family).
- EXACT-match behaviors for the in-scope portfolios/ artifacts (NOT a `/api/general/portfolios/*` wildcard -- that prefix also carries non-MDPF artifacts): `/api/general/portfolios/non_model_assets.json` (IN); `+ account-distribution.json / aum-metrics.json / aum-timeseries.json` iff the s6 disposition includes them.

**3c. `mdpf-data-router` lambda (DT authors) -- TRANSLATION ONLY, no origin logic** (origin is set by the CF behavior in 3b, kept in declarative config):
```
// origin-request; associated ONLY with the 3b behaviors.
// Input request.uri is already the rewritten /json/... form? NO -- these are NEW behaviors that
// do NOT run public-data-router, so request.uri arrives as /api/general/...  => translate from there.
const MAP = [
  [/^\/api\/general\/mdpf\/([^/]+)\/aggregate-aua-timeseries\.json$/, (m)=>`/portal/model-portfolios/${m[1]}/aggregate_aua_timeseries.json`],
  [/^\/api\/general\/mdpf\/([^/]+)\/account-distribution\.json$/,      (m)=>`/portal/model-portfolios/${m[1]}/account_distribution.json`],
  [/^\/api\/general\/portfolios\/non_model_assets\.json$/,             ()=>`/portal/portfolios/global/non_model_assets.json`],
  // + the 3 DISPO entries iff s6 rules them IN.
];
```
The map is a small, explicit, reviewable table (the SEV1-relevant content). Baked into code (Lambda@Edge = no env vars); the "which keys" is auditable at review.

**3d. Precedence + isolation:** the 3b behaviors are inserted ABOVE behavior 18 in the ordered_cache_behaviors list (s3e.1) => they handle exactly the MDPF-family; behavior 18 + `public-data-router` + opal-data-portal-v2 keep serving everything else unchanged, including any `/api/general/mdpf/*` that a 3b pattern does not match (fails safe to the old serve).

**3e. AE mechanism precision (0.7.0_AE_CloudOps 204433Z -- baked in):**
1. **CF selection is ORDERED PRECEDENCE, not automatic longest-match.** The 3b behaviors MUST be earlier in the ordered_cache_behaviors list than the `/api/general/*` catch-all (behavior 18); placed after it, 18 matches first and the new behaviors never fire. AE owns the ordering.
2. **The opal-data-assets bucket policy is a PURE-ADD.** The bucket already carries a live policy (the Rule-17a `.parquet`-under-`bronze/` deny, landed 2026-07-16). AE grounds the live policy first and ADDS the OAC `portal/*` grant as a new statement -- never clobbers the bronze-parquet-deny. OAC impl: `aws_cloudfront_origin_access_control` (type=s3, signing_behavior=always, sigv4) + policy statement principal `cloudfront.amazonaws.com` `s3:GetObject` on `opal-data-assets/portal/*` with `Condition AWS:SourceArn = <portal distribution ARN>`.
3. **`mdpf-data-router` is Lambda@Edge:** must be a PUBLISHED numbered VERSION in **us-east-1** (not `$LATEST`), role trust includes `edgelambda.amazonaws.com` (replication). DT authors + publishes; DT sends AE the published VERSION ARN at wire time; AE associates it in the behavior. A `$LATEST` or non-us-east-1 build will not associate.

---

## 4. Alternative (SECONDARY, not recommended): modify `public-data-router` with a translate+origin-override map

Extend the existing router: for the enumerated keys, translate the uri AND set `request.origin.s3.domainName` to opal-data-assets; else passthrough. Fewer behaviors, but: (i) it MODIFIES the SEV1 router (every `/api/general/*` request now runs the new code path); (ii) origin selection moves into lambda code (less declaratively auditable); (iii) no env flag (Lambda@Edge), so on/off is a code deploy either way. **Rejected** in favor of s3's isolation unless CTO prefers the single-behavior footprint.

---

## 5. Reversibility + rollback (honest mechanics)

- **The re-point control = adding the 3b behaviors** (+ the origin). **Rollback = remove them** -> traffic falls back to behavior 18 -> opal-data-portal-v2 (the legacy serve, still live under build-alongside). CF-config change; **propagation is minutes-scale, not instant** (CF distribution deploy) -- I am NOT claiming an instant env toggle (Lambda@Edge has none).
- **Shadow-then-retire (spec s6.3):** at co-sign, the 3b behaviors go live (new serve); the legacy `json/mdpf/*` producer runs SHADOW one cycle, then retires. Door 6 / mdpf trigger untouched in wave 1.
- Single logical control, one direction to reverse -- but state it as "a gated CF deploy," never "a flag flip."

## 6. Coverage disposition -- RULED IN-ALL (CTO 204033Z)

The page live-fetches A1 aum-metrics, A2 aum-timeseries (Global VALUE trend), and A3-global account-distribution -- all on `/api/general/portfolios/*`, none slotted in the specced bucketing.
- **Option IN-ALL (rec):** slot `portal/portfolios/global/{aum_metrics,aum_timeseries,account_distribution}.json`; DS authors A1/A2 + global bell-curve; add their exact-match behaviors. => the flip is COMPLETE; the page serves entirely from opal-data-assets; the DDB-registry "manage it all" reading holds. Cost: expands DS authoring.
- **Option PHASE:** wave-1 flips only the mdpf/* family + non_model_assets; A1/A2/global-dist stay on behavior 18 -> opal-data-portal-v2 (a split serve) until a wave-1b. Functionally fine (both buckets live) but leaves 3 page numbers on the legacy path.
Either is safe (no fetch stranded -- unmatched paths fall to behavior 18). **RULED: IN-ALL (CTO 204033Z)** -- the flip leaves nothing on the legacy path (the legacy opal-data-mdpf feed can retire). The 3 global portfolios/ homes are already A1/A2/A3 projection scope (DS TO-2/TO-3): homes+behaviors, not new projection work. => 4 exact-match portfolios/ behaviors (non_model_assets, account-distribution, aum-metrics, aum-timeseries) + the one /api/general/mdpf/* wildcard.

## 7. SEV1 / security handling (the gate checklist)

- **HARD REQ 1 (CTO, non-negotiable, verified at gate):** Auth gate PRESERVED on EVERY new behavior (`auth-validator-edge` viewer-request) -- the new serve is NOT less authenticated than today.
- **HARD REQ 2 -- CUTOVER PRECONDITION (CTO):** PREFLIGHT-GATE the flip -- assert EVERY in-scope portal/ key EXISTS + ties the baseline (N=3) in opal-data-assets BEFORE any behavior is associated. The fail-safe covers UNMATCHED patterns only; an in-scope key whose gold artifact is missing would 404 from the new origin. No behavior goes live until the FULL in-scope artifact set is present + parity-verified.
- Origin selection scoped to ENUMERATED MDPF-family keys only -- no wildcard origin swap; non-MDPF `/api/general/*` untouched.
- New origin read-scoped to `portal/*` via OAC + bucket policy -- never bucket-wide, never a bd/schwab/source layer.
- `public-data-router` (the SEV1 incumbent) BYTE-UNCHANGED in the recommended design.
- Additive + gated + co-signed; applies only at the never-widen re-point.

## 8. Execution split + verify/exercise

- **DT (me):** author `mdpf-data-router` (translation-only) + publish it as a numbered VERSION in us-east-1 (s3e.3) + this design + the 3b behavior/pattern spec; supply the emitter source-repoint spec (plan b). **Hand AE at wire time:** the published mdpf-data-router VERSION ARN, the final IN-ALL pattern/behavior set + translation map, and the present+parity-verified confirmation.
- **AE (0.7.0):** ground the LIVE distribution first (origins/edge-chain/behavior-18 order); add the opal-data-assets origin + OAC + `portal/*` bucket-policy statement (PURE-ADD to the existing 17a deny, s3e.2); insert the 3b behaviors ABOVE behavior 18 (s3e.1); associate the published lambda VERSION ARN; apply (CTO-gated); HOLDS the behavior apply until presence+parity is green (the cutover precondition). Needs from DT: portal distribution ID (AE grounds it), the pattern set, the version ARN, the presence+parity confirmation.
- **CTO:** gate the lambda code + the CF/behavior/origin apply; bring the mechanism + parity evidence to Andrew for the never-widen co-sign.
- **EXERCISE (the test that fails if wrong), pre-cutover:** in a non-prod/path-test, request each in-scope path and assert it resolves to the opal-data-assets `portal/*` key with 200 + the right body; assert a NON-MDPF `/api/general/*` path still resolves to opal-data-portal-v2 (the isolation control); assert auth still gates (401 without token). Ground on the LIVE CF response, never the config.

## 9. Gate questions -- ALL RULED (CTO 204033Z)
1. s6 disposition -> **IN-ALL** (DS adds the 3 global portfolios/ homes; msg 204149Z).
2. Architecture -> **s3** (isolated behaviors + new lambda; public-data-router byte-unchanged).
3. Origin -> **OAC** (AE implements origin + portal/* bucket policy with OAC; confirming w/ AE msg 204201Z).
Both hard reqs folded into s7. Design is gate-approved; refinements track here as the build proceeds.

## 10. OPEN CONSTRAINT (surfaced 2026-07-20 ~2050Z, grounded) -- CloudFront behavior quota

`comp-routes behaviors` shows the portal distribution carries **25 cache behaviors (0-24) -- AT the CloudFront default limit of 25/distribution.** The IN-ALL s3 design ADDS behaviors: exact-match = 9 (5 mdpf keys + 4 portfolios keys) -> 34; a `/api/general/mdpf/*` wildcard + 4 exact portfolios = 5 -> 30. **Both exceed 25.** This was not accounted for in the s3 approval. Dispositions (routed to CTO+AE 205xZ):
- **(A) quota increase** -- if "25 behaviors/distribution" is raisable in our account (Service Quotas), s3 stays cleanest; AE requests it (lead time). **AE to ground whether it is raisable or a HARD cap** -- this is the pivot.
- **(B) if 25 is HARD:** (i) **s4** (modify public-data-router with a translate+origin-override map = ZERO new behaviors) becomes the feasible path despite touching the SEV1 router -- reopens Q2 under the constraint; (ii) consolidate/retire existing behaviors to free slots; (iii) a `/api/general/mdpf/*` + `/api/general/portfolios/*` wildcard pair (2 behaviors) + lambda origin-override-BACK to opal-data-portal-v2 for non-MDPF portfolios/ keys (FRAGILE -- replicates public-data-router logic; not recommended).
- **My read:** flips to s4 ONLY if the limit is hard (zero new behaviors beats a fragile wildcard-override); else s3 + a quota bump. **Lambda authoring HELD until this resolves** (the mechanism may change). Also affects the exact-vs-wildcard sub-choice (exact-match is safer -- no orphan-404 -- but costs more of the scarce behavior budget).
