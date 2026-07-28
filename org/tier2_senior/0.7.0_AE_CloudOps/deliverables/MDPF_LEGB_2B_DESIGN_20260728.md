# MDPF leg (b) -- DESIGN: option 2b, a narrow CloudFront behavior for `/api/general/mdpf/*`

**Author:** 0.7.0_AE_CloudOps · **Date:** 2026-07-28 · **Status:** DESIGN ONLY -- NOTHING BUILT
**Authority:** CTO A-2 ruling (Andrew-accepted) · design GO `20260728T165843Z` · Q3 full-read gate
`20260728T170114Z`
**Blocked on:** (1) CTO decision on the bucket-policy shape below; (2) Q4 completeness gate, routed to
`0.2.0_DT`.

---

## 1. The decision, and why 2b rather than 1

Leg (b) must give the REVAMP publisher a destination the portal actually serves. Two branches were live:

| | Option 1 -- re-point the publisher into `opal-data-portal-v2` | **Option 2b -- narrow CF behavior for `/api/general/mdpf/*` -> `opal-data-assets`** |
|---|---|---|
| Blocker | **`explicitDeny` TODAY.** `opal-assets-mdpf-portal-publisher-role` is 1 of 12 principals on `opal-assets-one-way-fan-in-fence`, which denies 9 mutation actions across 17 source buckets incl. `portal-v2`. **An explicit Deny cannot be cured by adding an Allow.** | none of this kind |
| Real cost | a deliberate hole in an attached, working, firm-separation-adjacent guardrail | one CloudFront behavior |
| Direction | asks the monolith's publisher to write OUTWARD -- **the exact direction the fence's name encodes as forbidden** | leaves the fence untouched |

**Option 1 is not blocked BY the fence; it CONTRADICTS the fence.** Punching a hole conceals the
contradiction and leaves a control whose name still claims "one-way" while one role no longer is.

**2b also turned out to be the CHEAPER branch, which was not knowable before measuring** (§2-§4): the
origin exists, the router needs no change, and precedence is already demonstrated on this distribution.

---

## 2. Q1 -- behavior precedence: PROVEN BY LIVE PRECEDENT, not by documentation

`comp-routes behaviors` on the live distribution:

```
   1. /api/general/trades/*        -> APIGateway-portal            [AUTH]
  16. /api/general/json-tiered/*   -> S3-opal-data-portal-v2-json  [AUTH][ROUTER]
  18. /api/general/*               -> S3-opal-data-portal-v2-json  [AUTH][ROUTER]   <- catch-all
```

Two more-specific `/api/general/*` behaviors already sit at lower ordinals than the catch-all and win,
**today, on this distribution.** A `/api/general/mdpf/*` behavior inserted before ordinal 18 takes
precedence. This is a live precedent, not a claim about CloudFront semantics.

**Corollary (why option 2-as-originally-stated was rejected):** a WHOLESALE re-point of behavior 18 would
move `json/portfolios/*` (`non_model_assets.json`, `aum-timeseries.json`), `account-distribution.json` and
the legacy `portfolios/*` set to a bucket where they do not exist. **That is an outage, not a serving
change.** 2b moves only the mdpf keys.

---

## 3. Q2 -- the Lambda@Edge router: NO CHANGE REQUIRED

`public-data-router` is attached **per-behavior** (`origin-request`), **NOT inherited** -- behavior 16
carries its own attachment. A new behavior must attach it explicitly; **behavior 16 is the template,
mirror it rather than hand-assembling** (it also carries `viewer-request: auth-validator-edge` and
`origin-response: cache-control-injector`).

The LIVE copy is `infra/aws/lambda-edge/public-data-router/index.mjs` (v4):
```
/api/general/json-tiered/* -> /json-tiered/*
/api/general/json/*        -> /json/*
/api/general/*             -> /json/*      <- FALLBACK
```
`/api/general/mdpf/foo.json` hits the fallback -> **`/json/mdpf/foo.json`** -- **exactly where
`opal-assets-mdpf-portal-publisher` already writes.** The publisher's current same-bucket behaviour stops
being a defect and becomes correct-as-written. **Zero router edits.**

> **HAZARD FOUND, ROUTED SEPARATELY, DO NOT TOUCH IN THIS WORK:** a second copy exists at
> `infra/aws/lambda/public-data-router/index.mjs` (42 lines) still rewriting the pre-2026-02-25
> `/api/public/` paths. **Dead code that would break every public data route if deployed, at the path a
> person would guess first.** CTO has it as its own DEBTCLEAN item.

---

## 4. Q3 -- origin + read access: THE FULL READ CHANGED THE ANSWER

**Origin already exists:** `S3-opal-data-assets -> opal-data-assets.s3.us-east-1.amazonaws.com`. No new
origin needed.

**Bucket policy, read IN FULL (this was a gate, not a caveat -- CTO):**
```
Sid       AllowMdpfPortalCloudFrontOACRead      Effect Allow
Principal {Service: cloudfront.amazonaws.com}   Action s3:GetObject
Condition StringEquals AWS:SourceArn = arn:aws:cloudfront::313476888478:distribution/EVTSA9VEHNZVH
Resource  -- NOT A PREFIX. NINE ENUMERATED KEYS.
```
- **SourceArn pin: CORRECT.** `EVTSA9VEHNZVH` is the same distribution `opal-data-portal-v2`'s own
  `AllowCloudFrontOACPublicData` pins to (both read side-by-side, not assumed equal).
- **Resource scope: AN INCOMPLETE HAND-ENUMERATED ALLOWLIST.** Covered: `aggregate-aua-timeseries.json`
  for global / 49financial / inflection; `account-distribution.json` for 49financial / inflection; four
  `json/portfolios/*` keys.

**NOT COVERED -- a 2b cutover on this policy as-is would return 403 for:**
```
json/mdpf/cottonwood/aggregate-aua-timeseries.json     <- THE FOURTH FIRM
json/mdpf/global/account-distribution.json
json/mdpf/cottonwood/account-distribution.json
```

>> **"CloudFront can read `opal-data-assets`" IS FALSE AS A GENERAL CLAIM.** It can read nine specific
> keys, and the set we need is not a subset of them. **Present and applies are different claims.** <<

**And note what the omission lands on: COTTONWOOD.** The firm stranded at 07-23 on the served keys, the
firm the legacy 2-partner producer structurally cannot emit, is also the firm this serving grant omits.
**Three independent mechanisms, one victim** -- consistent with cottonwood being added to the product
after each artifact was authored, with every non-wildcard enumeration silently left behind.

### 4.1 DECISION REQUIRED FROM CTO -- bucket-policy shape
| | (a) extend the enumeration | (b) prefix grant `json/mdpf/*` + `json/portfolios/*`, SourceArn pin RETAINED |
|---|---|---|
| Fixes today | yes | yes |
| Next firm / artifact | **breaks again, silently, as a 403 on a client surface** | self-maintaining |
| Width | minimal | wider within an already-CF-served namespace |

**AE recommendation: (b), pin retained.** The enumeration has now demonstrably failed once by omission,
and its failure mode is a blank page for one firm with no signal anywhere. **This is a serve-surface
widening on the monolith -- CTO's call, not mine.**

**Generalisable finding for DEBTCLEAN:** *an ENUMERATED allowlist is a control that silently narrows as
the estate grows.* Correct the day it was written, quietly wrong ever since, nothing signalling the drift.
Same family as the frozen `date=\d{8}` regex row 13 just fixed -- **a precise instrument that stops
matching the world.**

---

## 5. Q4 -- OPEN COMPLETENESS GATE (routed to `0.2.0_DT`, NOT closed)

**What else reads `portal-v2/json/mdpf/*` besides the portal?** Unanswered. It cannot be settled from the
infrastructure side: CloudFront logs show paths, not consumers. **A cutover strands anything
unenumerated, silently.** This gates 2b on COMPLETENESS rather than mechanism. **Nothing may be built
until DT closes it.**

---

## 6. Build shape (NOT BUILT -- for CTO approval)

1. **Bucket policy** on `opal-data-assets` per §4.1 (a) or (b). Terraform, never console.
2. **One CloudFront behavior**, `/api/general/mdpf/*` -> origin `S3-opal-data-assets`, inserted at any
   ordinal **below 18**, mirroring behavior 16's function set: `viewer-request auth-validator-edge`,
   `origin-request public-data-router`, `origin-response cache-control-injector`.
3. **Publisher schedule** -- unchanged in shape by this design and still required; it writes all four
   artifacts atomically from ONE gold generation (the 07-23 non-atomic drift). **NOTE: atomicity is not
   yet a meaningful property** -- per COO, the legacy producer is structurally incapable of emitting
   cottonwood, so "all four from one generation" requires a producer that can produce four.
4. **No fence change. No publisher role change. No `portal-v2` change.**

## 7. Verification plan (the discipline this session earned)

- **Applied plane, not desired:** `get-bucket-policy` after apply; `comp-routes behaviors` showing the new
  ordinal below 18.
- **EXERCISE, do not infer:** fetch `/api/general/mdpf/global/aggregate-aua-timeseries.json` **and
  `/api/general/mdpf/cottonwood/aggregate-aua-timeseries.json`** through the distribution and compare bytes
  to the S3 object. **Cottonwood is the discriminating case** -- it is the one the current policy would 403.
- **Negative control, separately invoked:** a `json/mdpf/*` key NOT intended to be public, and a
  non-mdpf `/api/general/*` path, must still route to `portal-v2` (proves the behavior is narrow and did
  not capture the catch-all's traffic).
- **A config read is not a behavioural claim.** No GREEN until a real fetch returns the expected bytes.

## 8. Residuals this design does NOT close

- Q4 (DT). · Stage 6's three missing grants + `cycle-complete.json` never emitted. · The legacy
  `backfill/` rollup still 2-partner and still cannot emit cottonwood. · The stale `public-data-router`
  fork. · `aum-timeseries.json` consumer enumeration (COO owns).

**A serving cutover does not fix a producer.** 2b makes the correct artifacts reachable; it does not make
them correct.
