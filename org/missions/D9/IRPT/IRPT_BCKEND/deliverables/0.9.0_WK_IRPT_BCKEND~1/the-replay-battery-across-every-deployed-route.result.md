# IB-sb-3 RESULT -- THE REPLAY BATTERY: swapped identifiers across EVERY deployed route,
a revoked grant against a warm cache, an Opal principal against a firm advisor -- the
exercised proof of FWD-2. The last cell of the round.

**TO:** `IRPT_BCKEND.TO-IB-sb-3` | **worker:** `0.9.0_WK_IRPT_BCKEND~1` | **branch:** `wk-irpt_bckend-1-1`
**base commit:** `845cb2b6acc5bbd4f510efe473d5a5efc69a8024` (HEAD of `CLOUD` at hand-off)
**Read-only against the deployed plane, as bounded.** No infrastructure applied by this
cell. Two planes replayed and both recorded, per the issuer's mid-task supplement.

## Criteria

| id | verdict | invocation | deciding line |
|---|---|---|---|
| `SB3-AC1` | **PASS-by-output** | `timeout 600 python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~1/battery_ib_sb_3.py` | rc=0, `"overall_pass": true` then `IBSB3-REPLAY-CLEAN` |
| `SB3-AC2` | **RECORDED (judgment)** -- no verdict | evidence assembled for `3.0.0_SA_CVO` at L9 | in the proof-of-spec instance under `UNVERIFIABLE-BY-INSTRUMENT` |

Transcript committed beside this file: `IB-sb-3_SB3-AC1_battery_output.txt`.

## (a) The plane -- TWO planes, both recorded

At hand-off, no test-JWT-minting mechanism a worker may use without a human existed, and
IB-s-15's CloudFront behavior was committed-and-unapplied (row W2-S12). Mid-task, the
issuer's supplement reported the behavior now APPLIED and LIVE -- **verified independently
this turn, not merely cited**: `get-distribution-config` on `EVTSA9VEHNZVH` reads 28
behaviors with `/api/scoped/investor-reporting/*` -> `APIGateway-portal` last.

- **Plane 1 -- POST-AUTHORIZER** (used for the six-swap authorization proof, arms b-e and
  amend): the test-principal question stands exactly as investigated at hand-off --
  `infra/aws/users/lambda/portal-authorizer/index.mjs` requires an RS256 JWT signed by the
  production auth-handler's private key, PLUS an origin-verify shared secret only
  CloudFront's own origin config can set; the production login flow
  (`infra/aws/opalinvest_dev/lambda/auth-handler`) requires a real password + MFA with no
  dev bypass in that source. This is independent of whether CloudFront is applied, so the
  authenticated replay still runs here: each deployed handler's own `lambda_handler` /
  registered guarded route, invoked directly with the edge validator's injected header set
  -- the SAME plane this project's own export cell documents exercising its routes in.
- **Plane 2 -- REAL PATH** (used for the LIVE BOUNDARY measurement, added after the
  supplement): 11 of 11 declared routes, unauthenticated, through the real distribution
  (`d2n2nzpeqf34ge.cloudfront.net`) -- all read `401`, 0 protected bytes. A malformed
  bearer token and a forged-shaped JWT both read `401 "Invalid or expired token"`
  (proving the authorizer actually attempts verification, not just presence-checking). A
  direct-to-API-Gateway bypass (skipping CloudFront's origin-verify header entirely) reads
  `401 "Unauthorized"` -- API Gateway's own GENERIC message, distinct from the
  authorizer's custom ones, confirming `isOriginVerified()` is a real, separately-enforced
  gate and not merely declared in source. Authenticated replay is NOT RUN on this plane --
  the SAME test-JWT gap blocks it here too, stated rather than left implicit.

## (b) Every route, six swaps -- 12 of 12 counted, 9 of 9 reauthorization-testable holds

| route | handler | status |
|---|---|---|
| GET directory/search | irpt-directory-search | MEASURED-UNGUARDED (row S9's population) |
| POST directory/resolve | irpt-directory-search | same handler |
| GET performance/{id} | irpt-performance-adapter | MEASURED-UNGUARDED (row S9's population) |
| POST analysis | irpt-ycharts-generate | VACUOUS (hard consent gate refuses before identity is read) + UNGUARDED (newly observed, filed) |
| GET analysis/{id}/sections | irpt-status | GUARDED, all 6 swaps refused |
| GET narrative/{id} | irpt-narrative | STRUCTURAL EXEMPTION (no identity field of its own) + UNGUARDED (newly observed, filed) |
| GET status | irpt-status | GUARDED, all 6 swaps refused |
| GET status/{id} | irpt-status | GUARDED, all 6 swaps refused |
| POST export | irpt-export-render (submit) | GUARDED, all 6 swaps refused |
| GET export/{id} | irpt-export-render (capabilities only) | STRUCTURAL GAP (no distinct guarded status op) + UNGUARDED (newly observed, filed) |
| GET export/{id}/download | irpt-export-render (download) | GUARDED, swapped id + revoked-then-right-id both refused |
| GET holdings/{id} | none | NO-HANDLER-AT-HEAD, counted in N per fact 2 |

## (c) Revoked against a warm cache

Served (cache populated) -> revoked (refused `EMPTY_GRANT`, cache untouched, 0 protected
bytes) -> restored (served again from the SAME warm cache entry, `cache_hit=True`).
Reauthorization, not a cache read -- matches `_authz/tests/test_enforce.py`'s own proof of
this property, re-run live as this cell's own evidence.

## (d) Opal vs firm

Reused IB-s-15's own two-firm fixtures (`_scope/tests/test_global.py`, imported and driven
directly -- the estate already built and proved this shape). An Opal principal reaches
both firm A and firm B's clients, one at a time, never a union (disjoint account sets,
different `verified_request_firm_id` per resolve). A firm advisor (49financial) replaying
the SAME request against firm B is refused `FIRM_BINDING`.

## (e) The download -- against four REAL synthetic objects, never a client artifact

Replayed against the four labelled synthetic export objects IB-s-14 landed under
`firms/49financial/generations/GENIBS14SYN/attempts/1/exports/{r1,v0-11-overview,
v0-11-comparison,v0-11-multicomp}/report.pdf` (real S3 reads, sha256 computed from the
STORED bytes -- never a vendor call). Authorized: served, `artifact_sha256` matches the
receipt built from the stored bytes, the signed URL names Opal's own bucket, never a
vendor host. Swapped PDF id: refused `OBJECT_NOT_COVERED`, 0 protected bytes. Revoked
grant then the RIGHT id replayed: refused `EMPTY_GRANT`.

## (amend) Guarded, bound, and silent on the refused value

`unguarded_routes()` over the REAL `routes.json` (S13's real-file case): **5 of 11
guarded, 6 of 11 unguarded**. Three of the six match row S9's disclosed population exactly
(directory search, directory resolve, performance). **Three more were not disclosed
anywhere and are filed as row `IRPT_BCKEND-W1-S10`**: `POST /analysis`
(irpt-ycharts-generate -- its own source comment says it registers no route because it
predates `routes.json`; `routes.json` now maps this route to it anyway), `GET
/narrative/{reportId}` (irpt-narrative -- no `_authz` import, no disclaimer), `GET
/export/{exportId}` (irpt-export-render -- no distinct guarded status operation exists in
the codebase for this route at all; the deployed function answers `action=capabilities`
regardless of path). None currently discloses protected data (each has its own,
independent, unrelated reason), which is why this reads OBSERVATION rather than BLOCKING
-- printed as measured, never repaired.

FirmBinding non-reconciling fixture: refused `FIRM_BINDING`, never served empty. Key
refusal (a client display name as a parameter): refused `KEY_REFUSED`, and the value is
absent from the WHOLE envelope (body + reason) AND the audit trail.

## Fact 4 (row W3-S12): the S3-key census

Every key this battery observed -- the four synthetic export keys, and every firm's QA
`holdings`/`directory` pointer + dated key (real S3 reads) -- censused for name-shaped or
email-shaped components: **0 of N flagged**.

## Fact 5 (row W1-S9 correction): the id-space seam, live

The prefix is minted at `data/assets/scripts/gold/investor_reporting/holdings_snapshot.py`
lines 370/486/638 as `<firm>:acct:<opaque>`; `strip_firm_acct_prefix()` strips exactly
`^(49f|inf|cot):acct:` and nothing else. Real QA holdings + directory objects, all three
firms, both counts printed:

| firm | as written | after normalisation |
|---|---|---|
| 49financial | 0 of 5873 | **5856 of 5873** |
| inflection | 0 of 790 | 0 of 790 |
| cottonwood | 0 of 946 | 0 of 946 |

Exactly the shape the amendment names. INF/COT stay at 0 after normalisation -- the W1-S7
raw-key difference, unaffected by prefix stripping, unchanged and not fixed here.

## Fact 6: no live vendor call

The generation route is replayed on `ycharts.generate.transport.ReplayTransport` behind a
hard consent-env-var gate that always refuses before any transport is even reached; the
export render worker's own `IRPT_EXPORT_RENDERER=unavailable` state is read, never a
`HeadlessBrowserRenderer` constructed; the intake poller is not an API-exposed route in
`routes.json` and is not replayed by this battery at all.

## A genuine bug found in existing merged code, measured and NOT fixed

`performance/handler.py`'s own exception clause references `transport_mod.
VendorEgressRefused`, which raised `AttributeError` the first time this replay actually
exercised that branch with a correctly-resolved scope, because the module-loading
collision (performance's and ycharts/generate's same-named `transport.py`) had to be
diagnosed and isolated first (`_isolated_load`, evicting stale `sys.modules` entries
between cell loads) before this route's OWN pre-existing defect became visible rather than
masked by an import-time crash. Not filed as a fresh row: this is a downstream symptom of
the ALREADY-DISCLOSED row-S9 population's "predates the wrapper" status, not a new
authorization gap, and the BOUNDS forbid fixing a neighbouring defect. Diagnosed and
worked around in this cell's OWN test harness only (correct `FirmBinding`-based scope
construction, matching `_authz.Enforcer.resolve_now()`'s translation) -- `performance/
handler.py` itself is untouched.

## Rows filed

- `IRPT_BCKEND-W1-S10` (OBSERVATION, ARMED, disarm owner `2.0.0_SA_COO~B`) -- three
  additional unguarded routes (ycharts-generate/analysis, narrative, export-status) not in
  row S9's disclosed population; none currently leaks, each for its own unrelated reason.

## Bounds observed

Read-only against the deployed plane throughout (S3 reads of already-landed QA/synthetic
objects; live HTTPS probes that are refused at the edge before any handler runs). No
protected value printed anywhere -- the byte census reports counts, not content, and
flagged S3-key rows are redacted to their shape. Deploys nothing. No live vendor call
(fact 6). `.tools/commit-gate.sh` rc=0. Every invocation ran under `timeout`. No existing
surprise row edited.
