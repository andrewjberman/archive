# IB-s-15 BATTERY RESULT -- `IRPT_BCKEND.TO-IB-s-15`

**Serial:** `0.9.0_WK_IRPT_BCKEND~2` (slot ~2, sixth and last) | **Branch:** `wk-irpt_bckend-1-2`
**Worktree:** `/c/tmp/wk-irpt-1-2`, cut from CLOUD at `269945b272`.
**Source pins:** `bef9b459f3` (the api root, `_scope/global.py`, the api ledger's OPEN sentinel),
`d0a61c6acb` (the one CloudFront behavior and the cloudfront ledger's OPEN sentinel).

> ## THE HEADLINE: THE ORDER STAYS OPEN, AND THAT IS THE BOUND WORKING
>
> **The API half is LIVE.** 11 routes on `7k3ed8px20` under the existing `naqxlm` authorizer,
> applied `23 added / 0 changed / 0 destroyed`, root converged.
>
> **The CloudFront half was REFUSED BEFORE IT STARTED.** The pre-apply plan on `portal-auth`
> named THREE resources where the bound allows one. `safe-apply` was never invoked on that root;
> the distribution is verified byte-identical to its pre-act state. Arms (b), (c) and (f) read
> BLOCKED, `S15-AC1` withholds its token, and **this order is NOT complete.**
>
> Row `IRPT_BCKEND-W2-S12` (BLOCKING) is the carrier.

---

## S15-AC1 -- 5 OF 8 ARMS PASS, 3 BLOCKED, TOKEN WITHHELD

```
  ARM (a) PASS: 11 of 11 DECLARED routes live with CUSTOM/naqxlm; 11 of 11 integration targets are this project's; the NO-HANDLER route is enumerated and NOT live
  ARM (b) BLOCKED: the behavior is NOT applied (row IRPT_BCKEND-W2-S12)
  ARM (c) BLOCKED: the plan names 3 resources, not 1 (Plan: 0 to add, 3 to change, 0 to destroy.)
  ARM (d) PASS: 4 of 4 Global cases
  ARM (e) PASS: the catalogue is the registry: 3 of 3 enabled client firms, 2 test/demo excluded by kind
  ARM (f) BLOCKED: both sentinels committed and both entries closed -- BUT the cloudfront entry closed on NON-EXECUTION
  ARM (g) PASS: 3 outcomes: intersection with 1 reasoned gap; absent projection REFUSES with UNPROJECTED_GRANT; the projection equals the runner's one definition on 3 of 3 samples
  ARM (amend) PASS: 0 of 11 routes.json DECLARED routes unguarded; a non-reconciling FirmBinding REFUSES while a reconciling one serves; 0 occurrences of a refused client name across the whole envelope and audit trail
  5 of 8 arms PASS; 3 BLOCKED: ['b', 'c', 'f']
TOKEN WITHHELD
```

**The battery does not soften this.** IB-s-4's face carried an explicit rule admitting one
blocked arm; **this face carries none**, so a BLOCKED arm withholds the token. The battery says
so in its own output rather than leaving a reader to wonder why 5 of 8 did not round up.

### (c) THE STOP, IN FULL -- the plan that was not applied

```
Plan: 0 to add, 3 to change, 0 to destroy.
  # aws_cloudfront_distribution.portal will be updated in-place
  # aws_cloudfront_function.spa_fallback will be updated in-place
  # aws_wafv2_web_acl.opal_cloudfront_protection will be updated in-place
```

| resource | whose | what the diff actually is |
|---|---|---|
| `aws_cloudfront_distribution.portal` | **this cell's** | exactly **ONE** added `ordered_cache_behavior` -- `/api/scoped/investor-reporting/*` -> `APIGateway-portal`, caching disabled, one viewer-request association to `auth-validator-edge:19`. **1 added block, 0 removed.** No existing behavior touched. The clean half. |
| `aws_cloudfront_function.spa_fallback` | NOT this cell's | a **CRLF checkout artifact**, measured not inferred: `spa-fallback-function.js` is **26 CRLF / 0 bare LF** on disk in this fresh worktree while the HEAD blob is **0 CRLF / 26 LF**. Every diff line shows byte-identical text on both sides. |
| `aws_wafv2_web_acl.opal_cloudfront_protection` | NOT this cell's | **real churn**: 3 managed-rule blocks removed and 3 re-added -- `common-rule-set` p4, `ip-reputation` p3, `known-bad-inputs` p5. This is the WAF in front of the whole portal. |

**Why the behavior was appended at the END of the ordered list, and why that is correctness and
not tidiness:** `ordered_cache_behavior` is a LIST and its order IS CloudFront's precedence.
Inserting mid-list shifts every later block, and the plan would then show changes across
behaviors this cell must not touch -- **the STOP condition would have fired on my own edit.**
Appending shifts nothing. Precedence is unaffected either way: the pattern is disjoint from all
27 existing ones (nearest neighbours `/api/scoped/advisor-intelligence/*` and `/api/general/*`;
there is no `/api/*` or `/api/scoped/*` catch-all above it, checked by reading every
`path_pattern` in order).

**THE WORLD IS VERIFIED UNCHANGED.** `get-distribution-config` on `EVTSA9VEHNZVH` taken after
the plan is byte-identical to the one taken before any act: 27 ordered behaviors then and now,
identical pattern list, `investor-reporting` present `False`, full `DistributionConfig` JSON
identical. **Nothing is half-landed because nothing landed.**

### (b) The difference control, half-recorded and honest about it

```
  PRE-APPLY (recorded before any act):
    HTTP_STATUS=200  CONTENT_TYPE=text/html  SIZE=1068
    <!doctype html><html lang="en" data-theme="opal-capital"> ...
  POST: 200 -- unchanged, because the world is unchanged
```

The PRE half is exactly what the face predicts: with no behavior claiming the prefix, the
request falls through to the SPA. The POST half needs the behavior. Reporting this arm as
anything but BLOCKED would be reporting an unchanged number as a result.

### (a) The routes, live

```
  routes.json DENOMINATOR: 12 route(s) total = 11 DECLARED + 1 NO-HANDLER-AT-HEAD
  get-routes --api-id 7k3ed8px20 rc=0: 84 route(s) on the API, 11 under this prefix
  DECLARED routes present live: 11 of 11
  carrying AuthorizationType CUSTOM + AuthorizerId naqxlm: 11 of 11
  integration targets: 6 distinct function(s) -- all irpt-*
  the NO-HANDLER route is enumerated and NOT live (correct)
```

**The 12th route is the point of the file.** `GET /api/scoped/investor-reporting/holdings/{accountSetId}`
has **no Lambda to target at HEAD** -- measured: `list-functions` returns 8 `irpt-*` functions
and none is a holdings handler; IB-s-12 shipped a gold runner and a DISABLED schedule slot, not
a Lambda. It is enumerated with `status: NO-HANDLER-AT-HEAD` and deliberately **not** declared
in Terraform, because a route pointing at an integration pointing at nothing answers 5xx from
**inside** the auth boundary -- which reads like a broken handler rather than an unbuilt one.
`routes.json` carries its own arithmetic (`declared + no_handler == total`) because **11 of 11
and 11 of 12 say different things about this project**, and IB-sb-3's N must be the honest one.

### (d), (e), (g), (amend)

* **(d) 4 of 4.** An Opal principal reaches clients at two firms **one at a time**, each result
  attributed, the two permitted sets intersecting in **0** accounts -- Global is a SELECTOR, and
  bound 3's "no new all-firm financial aggregate" holds by SHAPE. A firm advisor replaying the
  same request is REFUSED. Same client + revision is identical Global vs firm-scoped, and the
  fingerprint MOVES on a different revision so the equality is not a constant. Revoking the
  roster takes effect.
* **(e) 3 of 3.** The catalogue IS `data/firm_registry.json`'s enabled `kind=client` firms;
  2 test/demo tenants are excluded **by kind, not by name**.
* **(g) three outcomes.** Projection present -> the intersection with every unmatched id
  carrying one of `CROSS-FIRM | NOT-IN-DIRECTORY | UNPROJECTED-ID`. Projection absent with a
  grant present -> **REFUSED** `UNPROJECTED_GRANT`, never an empty 200. The projection equals
  `directory_runner.opaque_id` on 3 of 3 samples **by construction** -- it IS that function
  object, not a second implementation that happens to agree, and the arm says so rather than
  claiming an independent check.
* **(amend) 0 of 11 unguarded**, censused over the REAL `routes.json`, with a 1-of-2 positive
  control; a non-reconciling `FirmBinding` REFUSES while a reconciling one serves; 0 occurrences
  of a refused client display name across body + reason + audit trail, with a 1-hit control.

## S15-AC2 -- THE API ROOT IS CONVERGED

```
No changes. Your infrastructure matches the configuration.
```

---

## THE CROSS-FIRM HOLE THIS CELL FOUND IN ITSELF

The first draft of `resolve_for_request` defaulted the directory-join firm to
`directory["firm_id_opaque"]` when no binding was supplied -- it took the firm from the **artifact
handed in**. A 49financial advisor replaying a request against inflection's directory then
**received inflection accounts**, because the ownership map keyed the same advisor id and the
intersection had nothing left to stop it.

The test that caught it is the acceptance clause's own sentence: *"a firm advisor replaying the
same requests is refused."*

An artifact's declaration of its own firm is a **CLAIM**; only the `FirmBinding` -- registry id
plus opaque id, proven against that declaration -- is a **VERIFICATION**, and neither can be
derived from the other without recomputing an opaque id, which would be the second definition
rows W2-S9/W2-S11 forbid. The binding is now REQUIRED, must NAME the firm the request resolves
to, and must PROVE the artifact. Revocation reads harder and truer as a result: with the roster
emptied, an Opal subject carries no verified firm of its own, so the request that reached firm B
a moment ago resolves to no firm at all and is refused.

---

## S15-AC3 -- THE JUDGMENT, RECORDED AND NOT SELF-GRADED

Addressed to `3.0.0_SA_CVO` at L9. No verdict is claimed here.

### 1. How the Opal principal is distinguished -- the claim, the file, the line

**It is NOT distinguished by any injected claim, and this cell did not invent one.** IB-s-2's
Phase-1 finding stands and was re-read at HEAD:

* `infra/aws/lambda-edge/auth-validator-edge/index.mjs:205` -- `if (payload.firmRole === "admin") return null;`
  under `:202-204`, which says master `role` *"remains reserved for Opal-platform admins per the
  firmRole framework"*. **`firmRole` is injected ZERO times**; the nine injected headers are at
  `:383-391`. It dies inside the edge function.
* `index.mjs:184-185` says the opposite of `:202-204`: *"Any jwt.role === 'admin' bypasses ...
  Opal staff AND partner-firm admins (e.g. Travis at 49financial, role=admin)"*. A named
  partner-firm user carries the supposedly reserved claim.
* `tier` / `userType` are unenumerated free text with no registry; `tier` defaults to the
  literal `"unknown"` (`:385`).

**So the class comes from a SERVER-SIDE ROSTER**, read by NAME (`/opal/irpt/opal-principal-roster`,
a name and not a value) and **EMPTY by default** -- the capability is ABSENT rather than
silently granted. Every failure path returns an empty roster **with a reason**: unreadable is
not granted, and not a crash either (a crash on the Global path would take out the firm-scoped
path beside it). The roster's error TEXT is withheld from the provenance record, because a
parameter error can echo the value.

**DID IT REQUIRE A CHANGE OUTSIDE THIS PROJECT? It did not, and that is the point of the roster
path.** The one-line edge fix beside `index.mjs:390`
(`request.headers["x-firm-role"] = [{ key: "X-Firm-Role", value: payload.firmRole || "" }];`)
would make the discriminating claim visible downstream, and it is **outside this order's
`<paths>`**. `.owned-paths.yaml` carries no rule for `auth-validator-edge` (the only
`lambda-edge` carve-out is `public-data-router` at `:1870-1872`), so the longest match is
`infra/aws/**` -> lane **`CLOUD_OPS_OR_ETL`**, *"any AE agent"* -- `0.7.0_AE_CloudOps` and its
lanes, or `0.8.0_AE_CloudComp`. It is also a served-output act on a distribution fronting 28
behaviors. **The roster satisfies arm (d) without it**, so no BLOCKING row was needed on that
axis; the upstream claim remains the cleaner long-run answer and is named, not taken.

### 2. What the unauthenticated 401/403 proves -- and does not

**It proves nothing yet, because it was not obtained: the behavior is unapplied.** When it is,
here is precisely what it will and will not establish.

**WILL:** that a request to the prefix is intercepted by the edge validator before reaching any
handler -- i.e. that the prefix is claimed by a behavior with the auth association, rather than
falling through to the SPA. That is a statement about **routing**, and the PRE reading (200
text/html, 1068 bytes of index.html) is what makes it a difference rather than an assertion.

**WILL NOT -- and this is IB-sb-3's territory, not a gap this cell can close:**

1. **Nothing about an AUTHENTICATED cross-firm request.** A valid JWT for firm A asking for firm
   B's client passes the edge validator by construction -- the validator checks a token, not an
   entitlement. Every control that matters then lives *downstream*: `FirmBinding`, the
   intersection, `_authz.guard()`. The 401 exercises none of them.
2. **Nothing about the authorizer's RESULT CACHE.** `naqxlm` returns a prior allow for its TTL,
   and that TTL is **not declared in `partners-api/api-gateway.tf`** (13 `authorizer_id`
   references, 0 caching declarations) -- it must be read from the live authorizer.
3. **Nothing about the two handlers that PREDATE the wrapper.** `irpt-directory-search` (IB-s-1)
   and `irpt-performance-adapter` (IB-s-11) merged before `_authz.guard()` existed. My arm
   (amend) censuses the ROUTE TABLE and reads `0 of 11` unguarded -- but it censuses **handlers
   this battery wraps**, not the deployed code behind those routes. **A route census is not a
   handler census**, and the deployed-route replay is the only instrument that can tell them
   apart.
4. **Nothing about a 403 from the WRONG cause.** A refusal because the edge rejected the token
   and a refusal because the scope covered nothing are both 403s to a client. Only the response
   body's reason code distinguishes them, and an unauthenticated probe never sees one.

### 3. Did the `portal-auth` apply change anything I did not intend?

**There was no apply.** That is the honest answer to the question as asked, and the plan is the
evidence -- printed verbatim above and saved. The distribution config before and after the plan
is byte-identical.

What I would ask the CVO to weigh:

* **The stop was correct and cheap.** The behavior is committed and unapplied; the remaining act
  is a re-plan and an apply under the same (currently closed-on-non-execution) entry once
  `portal-auth` plans clean. **No rework.**
* **The CRLF half is nearly free to clear** and would clear for any actor whose worktree renders
  that file LF. The **WAF half is a real decision** someone must take about a rule set protecting
  the whole portal -- and taking it from inside this order would be exactly the widening the
  bound forbids. Both belong to the `portal-auth` root's owner.
* **The ledger's vocabulary strained here.** `deploy_ledger.py` refused to `hold` an entry with
  an open activation leg (correctly -- a half-landed deploy stays RED), but nothing was
  half-landed: nothing started. I closed each leg on **non-execution** with the world verified
  unchanged, then closed the entry, and appended a **READ-THIS-FIRST** block above its status
  line so the word CLOSED cannot be misread as "the behavior is live". Arm (f) reads BLOCKED for
  the same reason: letting it read PASS would let that word stand for a deploy that did not
  happen. **A tool with no state for "refused before starting" is worth the CVO's attention** --
  this is the second cell in this slot to bend the ledger's vocabulary around a real shape it
  does not carry (the first was the sentinel-vs-close contract, row W2-S6).
