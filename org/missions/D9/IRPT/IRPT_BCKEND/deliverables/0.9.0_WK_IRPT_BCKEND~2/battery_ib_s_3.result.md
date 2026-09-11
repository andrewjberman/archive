# IB-s-3 BATTERY RESULT -- `IRPT_BCKEND.TO-IB-s-3`

**Serial:** `0.9.0_WK_IRPT_BCKEND~2` (slot ~2, third order) | **Branch:** `wk-irpt_bckend-1-2`
**Worktree:** `/c/tmp/wk-irpt-1-2`, re-cut from CLOUD at `22a125e098`.
**Deliverable source pinned at:** `749415b9a0`.
**Nothing in this cell touched the world.** The face: *"No deploy in this cell."* No apply, no
ledger entry, no S3 write, no vendor call, no monitor. `enforce.py` makes no network call and no
AWS call, and it does not import `jsonschema` (asserted by a test, because the Lambda runtime
does not have it -- the shared layer is IB-s-13's and is in flight).

---

## S3-AC1 -- 5 OF 5 ARMS PASS

```
  ARM (a) PASS: 6 of 6 swaps refused; 6 of 6 refusals leaked 0 of 16 protected tokens; the served baseline trips the same census at 6
  ARM (b) PASS: 3 of 3 outcomes as specified -- served, refused-while-warm (1 cache entries untouched), then served FROM THE STILL-WARM CACHE
  ARM (c) PASS: a job submitted under S and consumed after S was revoked is REFUSED with 0 protected tokens; a job still covered is delivered (1 of 1 control)
  ARM (d) PASS: 3 of 3 operations keyed through _keys with all five required components; 4 of 4 name-shaped components refused; well-shaped components still admitted
  ARM (e) PASS: the firm-authorized viewer sees 5 of 5 firm accounts (the advisor sees 3), is refused on 2 of 2 cross-firm attempts, and does not share the advisor's cache key
  5 of 5 arms PASS
IBS3-AUTHZ-LIBRARY
```

### Every arm's control, in one table

| arm | the absence it asserts | the control that makes the same instrument go non-zero | observed |
|---|---|---|---|
| (a) | a refusal carries no protected bytes | the SERVED baseline, through the same byte census | trips it at `6 of 16` tokens |
| (a) | six swaps are refused | the same request WITHOUT a swap must SERVE | `ok=True`, 3 accounts |
| (b) | a revoked grant is refused while the cache is warm | replay after RESTORING the grant must hit that same entry | `cache_hit=True` |
| (c) | a job is refused at consumption after revocation | a job still covered at consumption must be DELIVERED | `ok=True` |
| (d) | name-shaped key components are refused | well-shaped components (ISO date, enum token) must be ADMITTED | `ok=True` |
| (e) | the firm-authorized viewer is not a bypass | it is refused on another firm's id and another firm's artifact | `2 of 2` refused |

### (a) Six swaps, six refusals, and a byte census on every one

```
  the wrapped handler returns 16 protected token(s) when it runs; a refusal must carry NONE of them
  DENOMINATOR: 6 object kinds the wrapper knows: ['firm', 'advisor', 'account', 'relationship', 'report', 'pdf']
  BASELINE (must SERVE, else six refusals prove only that nothing works): ok=True cache_hit=False accounts=3
    SWAP firm          -> REFUSED OBJECT_NOT_COVERED leaked 0 of 16 protected token(s)
    SWAP advisor       -> REFUSED OBJECT_NOT_COVERED leaked 0 of 16 protected token(s)
    SWAP account       -> REFUSED OBJECT_NOT_COVERED leaked 0 of 16 protected token(s)
    SWAP relationship  -> REFUSED OBJECT_NOT_COVERED leaked 0 of 16 protected token(s)
    SWAP report        -> REFUSED OBJECT_NOT_COVERED leaked 0 of 16 protected token(s)
    SWAP pdf           -> REFUSED OBJECT_NOT_COVERED leaked 0 of 16 protected token(s)
  6 of 6 swaps REFUSED; 6 of 6 refusals carry 0 protected tokens
```

The 16 protected tokens are **derived from the fixture directory** -- every client id,
relationship id, account id, display name and masked discriminator in it -- rather than listed
by hand, so a fixture entry added later cannot fall outside the census without the denominator
moving.

### (b) Revoked against a warm cache -- the difference control

```
  OUTCOME 1 -- BEFORE revocation: ok=True cache_hit=False key=irpt/v1/49financial/directory_search/asf=61484...
    cache now holds 1 entry(ies)
    REVOKED in the fixture POLICY only: the ownership map now grants advisor A 0 account(s); the cache was NOT touched
  OUTCOME 2 -- AFTER revocation, SAME request, cache still warm: ok=False code=EMPTY_GRANT leaked 0 protected token(s)
    cache STILL holds 1 entry(ies), keys unchanged: True
  OUTCOME 3 -- grant RESTORED, same request: ok=True cache_hit=True
```

Outcome 3 is what makes outcome 2 evidence: the entry was never evicted, so the refusal was a
DECISION and not a cold cache. The three runs differ in exactly one thing -- the grant.

### (c) Reauthorize at consumption

```
  job JOB-1 submitted under scope S: ok=True fingerprint=6148451c13b35f92...
    the job record stores the submission fingerprint as EVIDENCE, never as a grant
  consumed AFTER S was revoked: ok=False code=EMPTY_GRANT leaked 0 protected token(s)
  CONTROL: a job still covered at consumption -> ok=True reauthorized_at_consumption=True
```

### (d) Keys through the grammar

```
    directory_search  -> irpt/v1/49financial/directory_search/asf=6148451c...5/src=src-1/sch=sch-1/cfg=cfg-1/p=as_of=2026-09-10&view=OVERVIEW
  3 of 3 keys carry tenant + fingerprint + source/schema/config revisions and are accepted by _keys.key_digest
    param client =Whitfield Family          -> REFUSED KEY_REFUSED   the value appears in the refusal: False
    param owner  =Smith-Family              -> REFUSED KEY_REFUSED   the value appears in the refusal: False
    param cohort =49FINANCIAL               -> REFUSED KEY_REFUSED   the value appears in the refusal: False
    param label  =advisor.a@49financial.com -> REFUSED KEY_REFUSED   the value appears in the refusal: False
```

---

## A LEAK THE BATTERY CAUGHT AND THE UNIT TEST MISSED

Arm (d) **failed on its first run**, and the line that failed is the one above with `True`
instead of `False`: the `KEY_REFUSED` refusal echoed the refused VALUE back to the caller --
`Whitfield Family`, `advisor.a@49financial.com` -- because `_keys` names the offending value in
its exception text (correct for a traceback) and the wrapper passed `str(exc)` straight through
as the refusal reason. **Refusing and disclosing in the same breath satisfies the bound's letter
and inverts its intent.**

The boundary now sits in the wrapper: the reason names WHICH PARAMETERS were refused and never
what they contained, and the offenders are found by **re-building the key one parameter at a
time through the same public `_keys.cache_key`** -- never by parsing the exception text, because
a prose format is not an interface and a check that reads a tool's message reads the TOOL rather
than the world. Filed as row `IRPT_BCKEND-W2-S10` (ARMED) because `_keys` is unchanged and the
next caller that surfaces its exception will leak the same way.

**The second-order lesson, recorded because it cost a green:** this cell's own unit test for
that exact property asserted `"Whitfield Family" not in json.dumps(out.census)` and PASSED,
while the value sat in `out.reason` -- one field over. A verifier scoped narrower than the object
it protects. The battery censused the WHOLE envelope and caught it; the test now asserts over the
whole envelope AND the audit trail, because an audit line is a log line.

---

## S3-AC2 -- THE JUDGMENT, RECORDED AND NOT SELF-GRADED

Addressed to `3.0.0_SA_CVO` at L9. No verdict is claimed here.

### 1. What an in-memory handler CANNOT show -- what IB-sb-3 must

The battery's handlers are Python functions called by the battery. Everything between a browser
and them is absent, and the absent parts are where the estate's real caching lives. Enumerated
**by subtraction from the request path** rather than by recall -- browser -> CloudFront ->
Lambda@Edge -> API Gateway -> authorizer -> integration -> Lambda container -> handler -- so a
stage cannot be dropped without the list disagreeing with the path:

| stage on the real path | what the in-memory test proves about it | what IB-sb-3 must show |
|---|---|---|
| **CloudFront** (28 behaviors, dist `EVTSA9VEHNZVH`) | nothing | whether any behavior caches a scoped response at the edge, where no Lambda runs at all on a hit |
| **Lambda@Edge auth validator** | nothing -- the nine headers are a dict a test wrote | that the headers arriving at the origin are the INJECTED ones, and that a browser-supplied `X-User-*` really is overwritten in flight |
| **API Gateway authorizer** `naqxlm` = `opal-portal-authorizer`, `authorization_type = "CUSTOM"`, REQUEST type, RS256 via Secrets Manager (`infra/aws/terraform/partners-api/api-gateway.tf:7-10,19,28`) | nothing | **its RESULT CACHE.** An authorizer result cache keyed on an identity source returns a PRIOR allow for the TTL's duration; a revocation inside that window is invisible to everything downstream. The TTL is **not declared in that Terraform root** -- the file sets `authorizer_id` on 13 routes and never the authorizer's own caching -- so it must be read from the LIVE authorizer, not inferred from the repo |
| **API Gateway response caching / integration** | nothing | whether a stage-level cache can return a body before the integration is invoked |
| **Lambda execution environment** | nothing -- each battery run is one process | a module-level cache surviving across invocations in a WARM container, which is precisely the "warm cache" arm (b) simulates in memory and cannot exercise for real |
| **IAM on the read path** | nothing | whether `irpt-directory-role` can even fetch the directory artifact the wrapper authorizes against -- a permission failure there produces an empty or erroring read, and the wrapper must not turn that into an empty served set |
| **concurrency and ordering** | nothing -- the battery is single-threaded and sequential | a revocation landing BETWEEN the authorize and the serve of one in-flight request, and two containers disagreeing about the grant for the length of a cache TTL |

**The honest summary:** the battery proves the LIBRARY re-checks; it proves nothing about
whether every serving path in the deployed system goes through the library. Those are different
claims, and the split is the decomposition's own (s.1): this half must land before the handlers
ship, and the end-to-end replay can only run once the routes exist.

### 2. Can the wrapper be bypassed by a handler that forgets it? YES -- and here is the detector

Nothing in Python can stop a route table from pointing at an unwrapped function, and saying
otherwise would be the comfortable answer rather than the true one. So the wrapper does the one
thing that converts "someone might forget" into a MEASUREMENT:

* `guard()` **marks** every function it wraps (`__irpt_guarded__`, plus the operation and the
  unwrapped original);
* `unguarded_routes(route_table)` censuses the **ROUTE TABLE** -- what is reachable -- and
  returns the denominator, the unguarded names and a verdict. It censuses the route table and
  not a module's functions deliberately: an unreferenced unguarded function is not a hole, and
  an unguarded function WIRED TO A ROUTE is.

```
    clean table:         {"guarded": 1, "routes": 1, "unguarded": [], "verdict": "OK: every route is guarded"}
    one unwrapped route: {"guarded": 1, "routes": 2, "unguarded": ["GET /leak"],
                          "verdict": "BLOCKED: 1 of 2 route(s) reach an unguarded handler: ['GET /leak']"}
```

**What this detector does NOT cover, stated so a reader does not over-read it:**

1. it runs where the route table is IMPORTABLE -- so it is a test or a build-time check, not a
   runtime guarantee; nothing here refuses to start a Lambda whose handler is unwrapped;
2. it cannot see a route that reaches a handler WITHOUT passing through a table it is given --
   an API Gateway route wired in the console, or a Terraform-declared route whose Python target
   this census never imports. **A route table census is only as wide as the table handed to it**,
   which is the same class of blindness as a scoped read;
3. it cannot see a handler that IS wrapped but calls an inner function directly (the wrapper
   keeps `__irpt_unwrapped__` for testing, and a caller could use it);
4. **the strongest version is not this census but the DEPLOYED-ROUTE replay IB-sb-3 owns**: for
   every route that exists in Terraform, send a negative request and require a refusal. That
   reads the world rather than the code, and it is the only arm that cannot be satisfied by a
   handler that merely looks wrapped.

### 3. What I would want the CVO to look at hardest

* **`FIRM_OPERATIONS` sees the whole firm population** (5 of 5 in the fixture, where the advisor
  sees 3). That is the face's own arm (e) and it is still the branch where an ambiguous `admin`
  signal buys the most -- and IB-s-2's judgment already recorded that the injected header set
  cannot separate an Opal-platform admin from a firm admin. The wrapper bounds it to the
  verified firm and refuses cross-firm objects, but it does not and cannot resolve that
  ambiguity.
* **The two firm id spellings** (row `IRPT_BCKEND-W2-S9`). The wrapper reconciles them for the
  handlers it wraps; the estate-level question -- which spelling is canonical for
  `verified_request_firm_id`, and whether `ResolvedScope` should carry both -- is a contract
  question this cell has no authority over.
* **`consume_job` decides on the CURRENT scope and only REPORTS the fingerprint change.** That
  is deliberate (a changed fingerprint that still covers the object is not a violation), but it
  means a reader looking for "the scope changed" must read the coverage decision, not the
  fingerprint comparison beside it.
