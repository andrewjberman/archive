# IB-s-15 BATTERY RESULT -- `IRPT_BCKEND.TO-IB-s-15`

**Serial:** `0.9.0_WK_IRPT_BCKEND~2` (slot ~2, sixth and last) | **Branch:** `wk-irpt_bckend-1-2`
**Worktree:** `/c/tmp/wk-irpt-1-2`, cut from CLOUD at `269945b272`.
**Source pins:** `bef9b459f3` (the api root, `_scope/global.py`, the api ledger's OPEN sentinel),
`d0a61c6acb` (the one CloudFront behavior and the cloudfront ledger's OPEN sentinel).

> ## THE HEADLINE, AFTER THE RESUME: COMPLETE -- AND THE STOP IS WHY
>
> **The first pass STOPPED.** The `portal-auth` plan named three resources where the bound
> allowed one, so `safe-apply` was never invoked and this order stayed OPEN with a BLOCKING row
> and the plan verbatim. That was the designed outcome of the bound, not a failure.
>
> **The stop produced exactly what a sign-off needed.** `1.0.0_SA_CTO`, as the gate over that
> root, ruled on row `IRPT_BCKEND-W2-S12` (msg 95933): the `spa_fallback` half was the CRLF
> checkout artifact this cell had **measured**, closed at `b9b3eafb6b`; the WAF half is a
> hashicorp/aws 5.100.0 **read-normalisation artefact** (`version` reads `""` refreshed vs
> `null` in config and stored state) that recurs on every plan of that root until the provider
> is bumped -- the CTO's durable item, owner `0.7.0_AE_CloudOps`. The bound was then widened
> **for this apply only** to "ONE change plus the classified WAF no-op", under both never-widen
> halves.
>
> **On the re-plan the gate conformed and the apply landed.** `0 to add, 2 to change, 0 to
> destroy`; behaviors **27 -> 28** with the new pattern last and the prior 27 untouched; the WAF
> `Rules` JSON **byte-identical** before and after; and the unauthenticated request that
> returned the SPA now returns **401**. 8 of 8 arms PASS, `IBS15-ROUTES-LIVE`.
>
> Everything below the S15-AC1 heading is the RESUMED reading. The first pass's evidence is kept
> further down, because a record that dropped the refused window would lose the measurement that
> got the bound ruled.

---

## S15-AC1 -- 8 OF 8 ARMS PASS, TOKEN MINTED

```
  ARM (a) PASS: 11 of 11 DECLARED routes live with CUSTOM/naqxlm; 11 of 11 integration targets are this project's; the NO-HANDLER route is enumerated and NOT live
  ARM (b) PASS: the behavior is live and the same unauthenticated request that returned the SPA now returns 401
  ARM (c) PASS: the plan names exactly the 2 resources the ruling admits; the distribution adds 1 behavior and removes 0; 0 WAF field(s) differ outside `version`; applied '0 added, 2 changed, 0 destroyed'
  ARM (d) PASS: 4 of 4 Global cases
  ARM (e) PASS: the catalogue is the registry: 3 of 3 enabled client firms, 2 test/demo excluded by kind
  ARM (f) PASS: 3 of 3 ledger entries CLOSED with their OPEN sentinels committed
  ARM (g) PASS: 3 outcomes: intersection with 1 reasoned gap; absent projection REFUSES with UNPROJECTED_GRANT; the projection equals the runner's one definition on 3 of 3 samples
  ARM (amend) PASS: 0 of 11 routes.json DECLARED routes unguarded; a non-reconciling FirmBinding REFUSES while a reconciling one serves; 0 occurrences of a refused client name across the whole envelope and audit trail
  8 of 8 arms PASS; 0 BLOCKED: []
IBS15-ROUTES-LIVE
```

### THE APPLY, AND THE FOUR READS THE AMENDMENT NAMED

| read | result |
|---|---|
| the apply | `Apply complete! Resources: 0 added, 2 changed, 0 destroyed.` -- WAF 19s, distribution 47s; Status now `Deployed` |
| behaviors | **27 -> 28**. The new pattern is **LAST** and is the only investor-reporting behavior. `diff(declared order, live order) = 0 lines`, and the behavior commit was **38 insertions / 0 deletions**, so the 27 pre-existing blocks are byte-identical to before -- those two together are what "the prior 27 unchanged IN ORDER" rests on |
| WAF | 6 rules before and after, names identical and in order, **`Rules` JSON sorted-key diff EMPTY (0 lines)**. `LockToken` is excepted by the sign-off and in fact reads identically, which is stronger than required |
| the difference control | PRE `HTTP 200 text/html 1068 bytes` (the SPA) -> POST **`HTTP 401 application/json 51 bytes`**, body `{"error":"Missing or invalid Authorization header"}` -- the edge validator refusing, no protected data in the body |
| the root's steady state | post-apply plan `0 to add, 1 to change, 0 to destroy` naming ONLY the WAF. **The distribution is converged**; the read artefact recurs exactly as the ruling predicted |

### HOW ARM (c) GRADES THE WIDENED BOUND -- A WIDENED BOUND IS STILL A BOUND

The arm was rewritten rather than relaxed. It does not accept "2 is fine"; it requires the plan
to name **exactly** the two resources the ruling admits, the distribution to add **exactly one**
behavior and remove none, and **every** WAF rule-field difference to be `version` alone --
proven by a rule-name set comparison plus a per-field diff of all six visible fields per block,
not by counting blocks. A synthetic third resource is run through the same classifier as a
positive control and comes back NOT ADMITTED.

### TWO INSTRUMENTS IN THIS BATTERY WERE WRONG AND WERE FIXED ON THE RESUME

1. **Arm (c) still encoded the pre-ruling bound** and would have reported BLOCKED against a plan
   that the sign-off explicitly covers. An arm that grades against a superseded bound is as
   wrong as one that grades against none.
2. **Arm (f) read `NONE` for two sentinels that are demonstrably committed.** `git log -- <path>`
   returns ZERO for an **add-then-delete inside merged history** -- and every sentinel is added
   then deleted by its own close. `--full-history` is the fix. The first run of the resumed
   battery FAILED that arm on real, correct history; the instrument was the defect.

### THE FIRST PASS, KEPT: THE STOP, IN FULL -- the plan that was not applied

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

### THE FIRST PASS, KEPT: the difference control, half-recorded at the time

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

**On the first pass there was no apply** -- that answer stands as the record of the stop.
**On the resume there was one, and the answer is: nothing beyond the two resources the ruling
admits, measured on three independent planes.**

* **Terraform plane:** `0 added, 2 changed, 0 destroyed`, and the post-apply plan of the root
  reads `0 to add, 1 to change` naming ONLY the WAF -- the distribution is converged.
* **CloudFront plane:** behaviors 27 -> 28, the new one last, the live order equal to the
  declared order with a zero-line diff, and the behavior commit carrying 0 deletions.
* **WAF plane:** `get-web-acl` `Rules` JSON byte-identical before and after. The classified
  no-op changed **no rule**, which is the claim the sign-off's Branch A was written around, and
  it is now measured rather than predicted.

What I would still put in front of the CVO:

* **The WAF no-op is signed for THIS apply and remains open as a condition of that root.** The
  post-apply plan still reads `0 to add, 1 to change`. Nothing this cell did fixed it and
  nothing this cell did should have: it is the CTO's durable item with owner
  `0.7.0_AE_CloudOps`, and the next actor to apply that root will meet the same plan.
* **An instrument limitation, stated rather than papered over:** the pre-apply pattern LIST from
  the first window did not survive the worktree re-cut, so "the prior 27 unchanged IN ORDER" is
  established by `git numstat` (38 insertions, **0 deletions**) plus declared-vs-live equality,
  not by diffing a stored pre-list. The counts and the absence of the pattern before the act are
  in the first ledger entry. I would rather name the chain than let a reader assume a file-diff
  that no longer exists.
* **The stop cost one round trip and bought a classification.** The same plan, applied blind on
  the first pass, would have rewritten a WAF ACL in front of the whole portal on an unexamined
  diff. It turned out to be a no-op -- and that was not knowable from inside this order, which
  is exactly why the bound names the reader rather than the outcome.
