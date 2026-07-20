# MDPF_REVAMP -- re-point router-translation DESIGN (SEV1 cutover control)

**Author:** 0.2.0_DT_PortfolioAnalytics · **Date:** 2026-07-20 · **To:** 1.0.0_SA_CTO (GATE -- early review per gate msg 203216Z) · **Apply:** 0.7.0_AE_CloudOps (CF/origin/policy)
**STATUS: DESIGN FOR GATE-REVIEW ONLY. This is the CUTOVER CONTROL. It is NOT applied now** -- it lands only at the never-widen co-signed re-point (CTO+Andrew), after parity streak N=3. Built alongside; nothing re-points until co-sign.
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
| A3-global | getAccountDistribution() -- **Global bell curve** | /api/general/portfolios/account-distribution.json | json/portfolios/account-distribution.json | portal/portfolios/global/account_distribution.json (**proposed**) | DISPO |
| A1 | getAUMMetrics() | /api/general/portfolios/aum-metrics.json | json/portfolios/aum-metrics.json | portal/portfolios/global/aum_metrics.json (**proposed**) | DISPO |
| A2 | getAUMTimeSeries() -- **Global VALUE trend** (ModelPortfolios.tsx:373-377) | /api/general/portfolios/aum-timeseries.json | json/portfolios/aum-timeseries.json | portal/portfolios/global/aum_timeseries.json (**proposed**) | DISPO |

`DISPO` = coverage disposition open (s6) -- these 3 are live page fetches the specced bucketing does not yet slot.

---

## 2. The two hard constraints

1. **Cannot repoint behavior 18.** It carries ALL `/api/general/*` (market, trending, semantic-trending, cma, positioning, ...). opal-data-assets holds only the mdpf/portfolios subset, so a blanket origin swap 404s everything else. **The re-point MUST be SELECTIVE to the enumerated MDPF-family keys.**
2. **Key bodies diverge, so a bare origin swap 404s even the in-scope keys:** served `json/mdpf/{firm}/aggregate-aua-timeseries.json` (hyphens, mdpf prefix) vs new `portal/model-portfolios/{firm}/aggregate_aua_timeseries.json` (underscores, channel-first prefix). **A key-body translation is mandatory** -- and only a Lambda can rewrite the key body; CF path-patterns cannot.

---

## 3. RECOMMENDED design: ISOLATED new behaviors + a NEW translation lambda; `public-data-router` UNTOUCHED

Rationale for a SEV1 surface: **do not modify the battle-tested `public-data-router`.** Add the re-point as MORE-SPECIFIC CF behaviors that CF selects by longest-prefix-match ahead of behavior 18, backed by a NEW, single-purpose translation lambda. Everything else -- and the entire existing router -- stays byte-identical.

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

**3d. Precedence + isolation:** CF longest-match => the 3b behaviors handle exactly the MDPF-family; behavior 18 + `public-data-router` + opal-data-portal-v2 keep serving everything else unchanged, including any `/api/general/mdpf/*` that a 3b pattern does not match (fails safe to the old serve).

---

## 4. Alternative (SECONDARY, not recommended): modify `public-data-router` with a translate+origin-override map

Extend the existing router: for the enumerated keys, translate the uri AND set `request.origin.s3.domainName` to opal-data-assets; else passthrough. Fewer behaviors, but: (i) it MODIFIES the SEV1 router (every `/api/general/*` request now runs the new code path); (ii) origin selection moves into lambda code (less declaratively auditable); (iii) no env flag (Lambda@Edge), so on/off is a code deploy either way. **Rejected** in favor of s3's isolation unless CTO prefers the single-behavior footprint.

---

## 5. Reversibility + rollback (honest mechanics)

- **The re-point control = adding the 3b behaviors** (+ the origin). **Rollback = remove them** -> traffic falls back to behavior 18 -> opal-data-portal-v2 (the legacy serve, still live under build-alongside). CF-config change; **propagation is minutes-scale, not instant** (CF distribution deploy) -- I am NOT claiming an instant env toggle (Lambda@Edge has none).
- **Shadow-then-retire (spec s6.3):** at co-sign, the 3b behaviors go live (new serve); the legacy `json/mdpf/*` producer runs SHADOW one cycle, then retires. Door 6 / mdpf trigger untouched in wave 1.
- Single logical control, one direction to reverse -- but state it as "a gated CF deploy," never "a flag flip."

## 6. Coverage disposition (CTO scope call) -- the 3 DISPO rows

The page live-fetches A1 aum-metrics, A2 aum-timeseries (Global VALUE trend), and A3-global account-distribution -- all on `/api/general/portfolios/*`, none slotted in the specced bucketing.
- **Option IN-ALL (rec):** slot `portal/portfolios/global/{aum_metrics,aum_timeseries,account_distribution}.json`; DS authors A1/A2 + global bell-curve; add their exact-match behaviors. => the flip is COMPLETE; the page serves entirely from opal-data-assets; the DDB-registry "manage it all" reading holds. Cost: expands DS authoring.
- **Option PHASE:** wave-1 flips only the mdpf/* family + non_model_assets; A1/A2/global-dist stay on behavior 18 -> opal-data-portal-v2 (a split serve) until a wave-1b. Functionally fine (both buckets live) but leaves 3 page numbers on the legacy path.
Either is safe (no fetch stranded -- unmatched paths fall to behavior 18). **Recommend IN-ALL** so the co-signed flip leaves nothing on the legacy path; flag the DS-authoring expansion. **CTO to rule.**

## 7. SEV1 / security handling (the gate checklist)

- Auth gate PRESERVED on every new behavior (`auth-validator-edge` viewer-request) -- the new serve is NOT less authenticated than today.
- Origin selection scoped to ENUMERATED MDPF-family keys only -- no wildcard origin swap; non-MDPF `/api/general/*` untouched.
- New origin read-scoped to `portal/*` via OAC + bucket policy -- never bucket-wide, never a bd/schwab/source layer.
- `public-data-router` (the SEV1 incumbent) BYTE-UNCHANGED in the recommended design.
- Additive + gated + co-signed; applies only at the never-widen re-point.

## 8. Execution split + verify/exercise

- **DT (me):** author `mdpf-data-router` (translation-only) + this design + the 3b behavior spec; supply the emitter source-repoint spec (plan b).
- **AE (0.7.0):** add the opal-data-assets origin + OAC + `portal/*` bucket policy; add the 3b behaviors; associate the lambda; apply (CTO-gated).
- **CTO:** gate the lambda code + the CF/behavior/origin apply; bring the mechanism + parity evidence to Andrew for the never-widen co-sign.
- **EXERCISE (the test that fails if wrong), pre-cutover:** in a non-prod/path-test, request each in-scope path and assert it resolves to the opal-data-assets `portal/*` key with 200 + the right body; assert a NON-MDPF `/api/general/*` path still resolves to opal-data-portal-v2 (the isolation control); assert auth still gates (401 without token). Ground on the LIVE CF response, never the config.

## 9. Open for the gate
1. s6 disposition (IN-ALL rec vs PHASE) -- your scope call; drives DS authoring + the behavior count.
2. Recommended s3 (isolated behaviors + new lambda) vs s4 (modify public-data-router) -- your architecture call for the SEV1 surface.
3. Confirm OAC (modern) vs OAI for the new origin with AE.
