# NEGATIVE CONFIRMATION — zero portal DISPLAY consumption of opal-data-mdpf + associated resources

**Author:** 0.4.0_DE_ClientPlatform · **Date:** 2026-08-04 ~04:4xZ · **Trigger:** Andrew-direct
(COO relay 035923Z): *"there is nothing that opal-data-mdpf and associated resources should be
doing that matters. We can have DE check the routes again to see if any of that is consumed by
the portal and actually displayed but it shouldnt be."* **Sequenced after the canonical-map
commit (portal DEV `7d544d27`), as dispatched. Feeds MDPF_GLOBAL T5 kill evidence (display-side
leg).** Grounding base: my as-displayed assessment @b48634789a.

## VERDICT: ZERO. No portal display path resolves to opal-data-mdpf, measured on four
## independent axes — and one of them is structural: the distribution has no such origin.

**Axis 1 — the live CloudFront origin set (STRUCTURAL, the strongest):** distribution
`EVTSA9VEHNZVH` (opalinvest.dev), live `get-distribution-config` 2026-08-04: exactly **7
origins** — `opal-data-portal-v2`, `opal-data-inf`, `opal-data-cot`, `opalinvest-portal`,
`opal-data-bd`, APIGateway-portal, APIGateway-portfolio. **opal-data-mdpf is NOT an origin**,
so no CloudFront-served display path CAN reach it, regardless of any URL any code composes.

**Axis 2 — same-origin closure:** `.env.production` (both DEV HEAD and origin/PROD) sets
`VITE_PORTAL_API_URL=` **EMPTY** → `API_BASE_URL = ''` (api-client.ts:14) → every fetch-layer
request is SAME-ORIGIN relative → every display fetch flows through the Axis-1 distribution.
Raw `fetch()` with absolute `https?://` URLs in committed src: **ZERO hits**.

**Axis 3 — the fetch-layer URL census (committed DEV `7d544d27`; PROD is a subset):** every
`apiRequest`/`publicApiRequest` first-argument enumerated and prefix-classified. Under
`/api/general|scoped|private|public/` + `/auth/` → the enumerated CF behaviors (mdpf paths →
`platinum/mdpf/` on opal-data-portal-v2, deployed router v6 + live-log-exercised
@b48634789a; advisor bases `PLATINUM_BASE = '/api/scoped/advisor-intelligence/platinum'`
:438 → opal-data-bd behaviors). Residue: `/v1/*` + `/aum/*` + `/returns/*` + `/news/*` →
API Gateway origins or the SPA default behavior — **backend-Lambda-mediated or dead paths,
none S3-direct, none mdpf**. Literal string `opal-data-mdpf` in the entire committed src
tree (code + docs): **ZERO hits**.

**Axis 4 — the associated-resources outputs (F5/F6 restated from @b48634789a, both
CVO-validated):** `json/mdpf/*` (smartx-written daily, 11:30Z, unconditional per-firm bell)
— **displayed NEVER** (no code path reaches it; string exists in comments only). The
underscore twins on the serve prefix (`platinum/mdpf/**/aggregate_aua_timeseries.json`,
runner-plane, lineage `opal-data-mdpf/mdpf/feeds`) — **displayed NEVER** (all deployed
fetches are hyphen-family; live router logs show zero underscore rewrites). The discriminating
control stands: the same instrument that returned these zeros DID find a live json-channel
display (F1) — a zero from a sweep proven able to find the class.

## HONEST SCOPE BOUNDS (display-consumption ZERO does not claim these)

1. **Upstream-of-served is NOT zero:** `opal-data-mdpf/mdpf/feeds/*` remains UPSTREAM of
   served content (the runner-written underscore artifacts' `by_feeder` composition —
   0.7.0_AE_CloudOps~F @ea47d52931). That leg is the PRODUCER-side repoint (memo production
   law / C1), not display consumption. A kill of the bucket today would not blank any pixel,
   but it would sever a producer input the canonical chain has not yet replaced — T5's
   ordering (T1-T3 proven first) still binds.
2. **API-GW-backed displays** (advisor-intelligence depth-3, `/v1/*`, portfolio API) are
   backend-Lambda-mediated; their S3 reads are backend edges owned by the kuzu/T1.A census —
   no known mdpf read among them, but my instrument here is the FE fetch layer + CF config,
   and I do not overclaim past it.
3. This is the committed-DEV / deployed-PROD code plane + LIVE distribution config; a future
   commit can add a route — the durable guard is T3.B's router-pin + the origin set staying
   mdpf-free.

## Denominators

25 comp-cluster page sources · 8 live queryKeys on the post-repoint page (was 9; the legacy
json/portfolios metrics fetch died with @7d544d27) · 7 live CF origins · 25 CF behaviors ·
0 `opal-data-mdpf` literals · 0 absolute-URL fetches · 2 composed bases, both resolved
(`PLATINUM_BASE` → opal-data-bd; `API_BASE_URL` → '' same-origin).

— 0.4.0_DE_ClientPlatform
