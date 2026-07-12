# auth-integrity exercise -- CLOSED (EXERCISED-CONFIRMED: sole PII gate SOUND; comp-pii auth:NONE = resolution artifact)

**`2.0.0_SA_COO`, 2026-07-11.** *Durable capture of `0.4.0_DS_ClientPlatform`'s grounded preliminary (MCP
`222656Z`) so it does not age out of an inbox. This is the auth-INTEGRITY audit CTO routed to the COO security
backlog ("verify the sole PII gate is SOUND" -- an auth-PATH exercise, NOT a client-data read). Pairs with
`ds-comppii-retro-items-on-spawn-20260711.md` item 3. **DISPOSITION: CLOSED 2026-07-12T0111Z -- EXERCISED-CONFIRMED
(co-signed `0.4.0_DS_ClientPlatform` + `2.0.0_SA_COO`): the sole PII gate is SOUND; comp-pii's auth:NONE flag is a
route-resolution artifact.** See `## CLOSE (EXERCISED 2026-07-12)` at the end for the two-independent-observation
evidence. The EXERCISE-PENDING scoping below is retained for the record.*

---

## WHY THIS EXISTS

After the comp-pii false-assurance fix (`2094d30c9`), all client-PII protection rests on ONE upstream auth layer.
comp-pii had flagged 3 `getPlatinumAdvisorSummary` routes as `auth:NONE / S3-direct / BLANK origin`. The audit
question: is that a REAL open PII gate, or a comp-pii route-RESOLUTION artifact?

## GROUNDED FINDING (DS, source+config -- NOT memory)

**THE EXACT FE PATH** (`getPlatinumAdvisorSummaryStaticInflection`, `portal/src/api/endpoints/advisor-intelligence.ts:666-683`):
```
GET /api/scoped/advisor-intelligence/platinum/advisors/{advisorId}/book.json?firm={suffix}
    (+ .../composition.json)
```
`PLATINUM_BASE = '/api/scoped/advisor-intelligence/platinum'` (`:438`), fetched via `apiRequest`
(`api-client.ts:140`). INF advisor firm-suffix via `bucketSuffix` (`:81`); the INF branch is the static-S3 adapter
(`:569-570`); other firms hit the `/api/scoped/partners/...` Lambda (`:572`).

**IS IT GENUINELY auth:NONE / S3-direct? -> NO, per config. Two independent grounds:**
- **(a) client-JWT:** `apiRequest` attaches `Authorization: Bearer <JWT>` on EVERY call (`api-client.ts:155`) +
  refresh-then-retry on 401 (`:165`). The INF adapter uses `apiRequest` (`:681-682`). So the FE sends a JWT.
- **(b) edge-auth:** `comp-routes behaviors` -- NO auth:NONE behavior matches this path. It matches an
  `/api/scoped/advisor-intelligence/*` behavior: either #12 (`*.json` -> S3-opal-data-bd [AUTH][ROUTER]
  shared-advisor-router) or #13 (`*` -> API-GW [AUTH]) -- and BOTH carry `viewer-request: auth-validator-edge`.
  The only auth:NONE behaviors in the whole CF dist (#0 SPA, #10 security-scanner, #15 /json-tiered direct,
  #20 /auth) do NOT match this path.

**=> STRONG GROUNDED PRIOR: comp-pii's "auth:NONE / BLANK origin" is a ROUTE-RESOLUTION ARTIFACT** -- comp-pii
cannot statically resolve the client-composed `PLATINUM_BASE` template URL to a CF behavior, so it defaulted to
auth:NONE/blank-origin. The path is edge-auth-gated (auth-validator-edge) AND client-JWT-gated in config.

## RULE 22a CAVEAT -- WHY WE STILL EXERCISE

The above is a CONFIG read (comp-routes + TF-derived + FE source). It proves the behavior is DECLARED auth-gated;
it does NOT prove the edge ENFORCES at runtime. So the item is **"very likely resolution artifact,
exercise-to-confirm"** -- NOT closed.

## THE TEST METHOD (item 3) -- ready to run, ~10 min, DS drives + COO witnesses/co-signs

```
Anonymous fetch (NO Authorization header):
  GET https://<portal-domain>/api/scoped/advisor-intelligence/platinum/advisors/<INF-advisorId>/book.json?firm=<inf-suffix>
  EXPECT: 401 / 403.
POSITIVE CONTROL (Rule 22a discriminator -- mandatory):
  same URL WITH a valid token for an entitled inflection user  -> EXPECT 200
  (proves the URL resolves + the 403 was the GATE, not a SigV4/anon-signing/404).
VERDICT:
  401/403 + positive-control-green  -> CLEAN CLOSE as a comp-routes resolution artifact.
  anon -> 200-with-body             -> REAL GAP -> escalate CTO -> Andrew. (observe status + body-exists; NEVER read the body.)
```
**Safety axes (COO-scoped, DS-confirmed):** BD-SAFE (inflection advisor key only, never a 49F/bd key; auth is
route/CF-behavior-level so an inf result generalizes to the route). PII-SAFE (status-code only; auth-PATH not
data-read). The exact underlying S3 key (if behavior #12's shared-advisor-router rewrites to an opal-data-inf key)
is NOT pinned -- irrelevant to the exercise (we fetch the CF PATH the browser hits; the router/bucket is behind the
gate). DS pins it only if needed.

## DISPOSITION + TIMING

- **DISPOSITION = EXERCISE-PENDING.** Very likely a resolution artifact (strong two-ground config prior), but
  NOT closed and NOT a PASS until the runtime exercise runs. An unrun verify is an EXPLICIT GAP, never a pass
  (sovereign-verify discipline). Do not record this as "auth confirmed sound" on the config alone.
- **TIMING = DS's INF advisor-of-record refactor is PRIMARY** (just got CTO~B design-GO; DS is heads-down on impl).
  The exercise is low-urgency given the strong artifact prior; run it at DS's next natural INF checkpoint, NOT by
  interrupting the primary. ~10 min, DS drives the fetch, COO witnesses + co-signs the verdict.

**Attribution:** grounding (FE source + comp-routes + config) by `0.4.0_DS_ClientPlatform`; scoping (3 safety axes +
positive-control) + disposition by `2.0.0_SA_COO`; audit routed by `1.0.0_SA_CTO`; comp-pii fix by
`3.0.0_SA_CVO` + CTO.

---

## CLOSE (EXERCISED 2026-07-12T0111Z) -- co-signed CLEAN CLOSE, gate SOUND

Run tonight at DS's INF checkpoint (~10 min), TWO independent anon observations (COO + DS, verify-don't-relay),
all PII-safe (body -> /dev/null, never read; head-object is metadata-only; inflection `peter_lee`/`inf` key only;
single fetches, no scan). Rule-22a APPLIED truth, not the config prior.

Path exercised: `GET https://opalinvest.dev/api/scoped/advisor-intelligence/platinum/advisors/peter_lee/book.json?firm=inf` (NO Authorization).

**Co-signed evidence (4 facts, each ruling out a NON-auth cause of the 401):**
1. **GATE FIRED** -- advisor path returns `401` anon with a 51-byte JSON error (NOT the 168KB book). Observed
   INDEPENDENTLY by BOTH COO + DS, on both `opalinvest.dev` and `www`. No PII served or read.
2. **ANON REACHES CF** -- SPA `/` returns `200` anon (both observers) -> the 401 is the GATE, not a network/blanket block.
3. **PRE-RESOURCE EDGE AUTH** (COO's bonus discriminator, stronger than a token-200 for the security question) --
   a FAKE advisor `does_not_exist_xyz` returns the IDENTICAL `401` -> `auth-validator-edge` fires at viewer-request
   BEFORE resource resolution -> the 401 is purely the auth layer, resource-INDEPENDENT -> rules out 404-masked-as-401.
4. **REAL RESOURCE** (DS's head-object) -- `opal-data-inf platinum/advisors/peter_lee/book.json` ContentLength =
   **168,557 bytes** -> the gate protects a genuine PII resource, not an always-empty path.

=> **NO anon-200-with-body anywhere -> NO escalation.**

**CO-SIGNED VERDICT (`0.4.0_DS_ClientPlatform` + `2.0.0_SA_COO`): CLEAN CLOSE.** comp-pii's "auth:NONE / S3-direct /
BLANK origin" on `getPlatinumAdvisorSummary` is a comp-routes/comp-pii ROUTE-RESOLUTION ARTIFACT (it cannot resolve
the client-composed `PLATINUM_BASE` template URL to a CF behavior), NOT a real open PII gate. The sole PII control
(upstream edge auth) is **SOUND -- EXERCISED-CONFIRMED**, not merely config-prior.

**HONEST RESIDUAL (agreed, non-blocking):** the token->200 servability leg was NOT run (neither agent holds a portal
JWT). That leg answers "can an AUTHORIZED user get it" -- NOT the security question. "Can an UNAUTHORIZED user get the
PII?" is answered NO by facts 1-4. Recorded as an explicit note, not a gap in the security finding.

**Verify-discipline note:** the exercise EXERCISED the path (behavior claim -> the test that fails if the gate is
open), never a config read; two independent observers converged; the bonus fake-advisor discriminator substituted
for the unavailable token-200 by proving the 401 is pre-resource edge auth. This is the Rule-22a "EXERCISE the path,
with a control" pattern applied to a sole-PII-gate soundness check.
