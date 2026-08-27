# POSN_TENANCY.TO-3-AE -- THE SERVED PLANE, MEASURED

**Assignee:** `0.7.0_AE_CloudOps~Y` · **Issuer:** `2.0.0_SA_COO~Z` · **TO:** @`426d0a8bfe`
**Workspace HEAD at measurement:** `a2fcc5efc4` · **portal HEAD:** `80af31ac`
**Decomp pin:** `07de844b12` · **PRD:** `a7ba82d253`
**Window:** 2026-08-27 ~21:25-21:40Z · **archetype:** VALIDATE

---

## 0. THE HEADLINE: THE TARGET IS UNBUILT, MEASURED POSITIVELY

⛔ **THE FRAME IS AN OPEN TIER-1 DISAGREEMENT AND THIS DELIVERABLE TAKES NO SIDE. I TOOK ONE ONCE AND
AM WITHDRAWING IT.** After `db2409435c` I wrote that `1.0.0_SA_CTO~Z`'s correction settled the
question. It has not:
```
1.0.0_SA_CTO~Z  10329/10344  PT-a-1 is an ACCEPTANCE TARGET. The statement column is the target
                             state, not an assertion about today. Decomp sound, no re-cut, cert holds.
2.0.0_SA_COO~Z  10338        "AND PT-a-1's PREMISE IS FALSE. I WROTE IT." Routed to CVO to rule.
3.0.0_SA_CVO~Z  10349        certified TO-3-AE @2efba0f665 and RE-DERIVED "the premise is false".
```
⭐ **ALL THREE AGREE ON EVERY NUMBER IN THIS DOCUMENT. THE DISPUTE IS DECOMP GRAMMAR, NOT
MEASUREMENT** -- and no verdict below moves on either reading. Recorded, not adjudicated; a Tier-2
seat does not resolve a Tier-1 split, and `2.0.0_SA_COO~Z` has already routed it to the certifier.

⭐ **AND ANDREW SETTLED THE UNDERLYING QUESTION AT ~21:52Z, WHICH IS NOT THE SAME AS SETTLING THE
GRAMMAR.** Verbatim, relayed by `0.4.0_DS_ClientPlatform~L` (10363), recorded not adjudicated:
> *"all of Positioning is general, it was always meant to be a general page, but we are making an
> exception in the case of cottonwood here for the purpose of their "Satellites" portfolios."*
⛔ **SO THE UNSCOPED SERVING THIS TO MEASURED IS THE INTENDED DESIGN, NOT A DEFECT** -- and the
firm-specific content is a NAMED, SCOPED EXCEPTION (Cottonwood Satellites). **That makes
`1.0.0_SA_CTO~Z`'s ordering constraint the operative one rather than a caution:** the exception is
exactly the trigger in s.9, and it is now sovereign-confirmed as coming. ⚠ **What his word does to
`PT-a-1`'s wording and to the uniformity constraint is `1.0.0_SA_CTO~Z` and `2.0.0_SA_COO~Z`'s call,
not mine.**

**MEASURED STATE: Positioning is not served through `/api/scoped/`.**

⛔ **AND `3.0.0_SA_CVO~Z` (10349) RAN THE CONTROL I DID NOT, WHICH CHANGES WHAT THE ABSENCE MEANS:**
```
'api/scoped'  in portal/src -> 47 occurrences
'api/general' in portal/src -> 166
```
>> **THE SCOPED PLANE EXISTS AND IS IN LIVE USE 47 TIMES. Positioning is not waiting on an unbuilt
   feature -- it is the EXCEPTION to a plane the portal already uses.** << ⭐ **An absence that reads
*"not built yet"* and one that reads *"built, and this one opted out"* carry DIFFERENT REMEDIES, and
I established only that the control was absent, never that the plane was.** My s.1 sweep proved
Positioning has no scoped route; it said nothing about whether the route family exists. **That is a
missing control on my own finding, supplied by the certifier.**

```
MEASURED   portal/src/api/portal-proxy.ts:1133 @portal 80af31ac
           apiRequest('/api/general/positioning/positioning_data.json')
```

`/api/general/*` is the **public data path**. It resolves through `public-data-router`, which
rewrites `/api/general/` -> `/json/` (`:64-67`) and contains **zero firm references across all 71
lines** (`grep -c -i firm` = **0 of 71**). There is no firm dimension anywhere on the path Positioning
actually uses.

>> **SO THE THREE CELLS DO NOT SPLIT INTO PASS/FAIL THE WAY THE TO ANTICIPATES.** `PT-a-2` (the header)
   is **correct and live**. `PT-a-1` and `PT-a-3` are not *failing controls* -- **the controls are not
   on this path at all.** The firm-keyed machinery exists, is applied, and is applied SOMEWHERE ELSE. <<

---

## 1. AC1 -- FIRM DISCRIMINATION, BOTH ARMS. **FAIL, and the refusal arm is INEXPRESSIBLE**

The TO warns AC1 fails silently on a single arm. It does -- but the honest finding is stronger and
differently shaped: **there is no "firm B's artifact" to attempt, because only ONE artifact exists.**

**EXERCISED.** Bearer minted `POST /auth/login` as `jane@cottonwood.com` (an Opal-provisioned test
identity, this lane's own, 2026-06-23). JWT claims `{"sub":"jane@cottonwood.com","firmId":"cottonwood",
"role":"admin","tier":"advisor"}`, RS256, TTL 900s.

```
ARM 1  cottonwood bearer -> /api/general/positioning/positioning_data.json
       HTTP 200   8,088 bytes   sha256 8ec27506f7168c084b34a20f70fc3dbc
NEG A  no bearer          HTTP 401  51 B  {"error":"Missing or invalid Authorization header"}
NEG B  bogus bearer       HTTP 401  36 B  {"error":"Invalid or expired token"}
```
Both negative controls fire and are **DISTINCT** (51 B vs 36 B, different messages) -- the instrument
discriminates, so the 200 is a real 200.

**APPLIED -- the origin, swept to exhaustion.**
```
s3://opal-data-portal-v2   4,125 keys swept   IsTruncated: None (no pagination gap)
  keys containing "positioning": 7 of 4,125
    json/positioning/allocation_summary.json            949 B
    json/positioning/holdings_attribution_data.json  377,782 B
    json/positioning/positioning_data.json             8,088 B   <- THE SERVED KEY
    platinum/etfs/positioning_data.json              128,122 B
    positioning/etf_categories.json                    5,522 B
    positioning/holdings_attribution_data.json       202,076 B
    positioning/positioning_data.json                 49,950 B
  keys with a FIRM SEGMENT: 0 of 7
```
**The served key is 8,088 B and the Cottonwood user received 8,088 B.** The artifact certifies its own
plane -- I am not asserting which object was served, the byte count exhibits it.

⛔ **THE SHARPEST FORM OF THE FINDING.** `0.4.0_DS_ClientPlatform~L` measured (TO-2-DS, `PT-b-3`) that
**Cottonwood has a data home and NO Positioning data in it** -- 6,599 objects in `opal-data-cot`, zero
Positioning. **A Cottonwood user nonetheless received 8,088 bytes of Positioning data.** Those bytes
are not Cottonwood's, because Cottonwood has none. **That is the access boundary failing, exercised.**

⚠ **NAMED HONESTLY: I did not obtain a second firm's credential.** `test-regression@49financial.com`
exists in `opal-users-v2` but was slated for decommission (COO log 2026-04-22) and no password is
documented; **I did not reset a production credential to manufacture an arm** -- that is a mutation
outside this TO. The single-artifact result above is *structural* and does not depend on a second
identity: with one key and no firm dimension, every authenticated identity resolves to the same bytes
by construction. **A second credential would add a confirming instance, not a different conclusion.**

**Verdict `T3AE-AC1`: FAIL.** Not "discrimination is weak" -- **discrimination does not exist on this
path**, and the criterion's refusal arm cannot be constructed against a single unscoped object.

---

## 2. AC2 -- `X-Firm-Id` FORGERY. **PASS, on a discriminating oracle**

⛔ **MY FIRST FORGERY TEST WAS WORTHLESS AND I AM RECORDING IT RATHER THAN ITS REPLACEMENT ALONE.**
I forged `X-Firm-Id` against the Positioning path and got byte-identical 200s. **That is what BOTH
hypotheses predict** -- the header being overwritten, AND the header being honoured but the path
ignoring firm entirely. A quantity both hypotheses predict is not evidence. Discarded.

**THE ORACLE THAT DISCRIMINATES:** the scoped router's 403 envelope **echoes the firm it resolved**.
The two hypotheses predict *different values of that field*.

**EXERCISED**, same valid cottonwood bearer, against `/api/scoped/advisor-intelligence/artifacts/advisor_summary.json`:
```
no X-Firm-Id sent        -> {"error":"artifact_forbidden","uri":"/gold/artifacts/advisor_summary.json","firmId":"cottonwood",...}
X-Firm-Id: 49financial   -> ... "firmId":"cottonwood" ...
X-Firm-Id: inflection    -> ... "firmId":"cottonwood" ...
X-Firm-Id: opal-capital  -> ... "firmId":"cottonwood" ...
X-Firm-Id: bd            -> ... "firmId":"cottonwood" ...
X-Firm-Id: demo          -> ... "firmId":"cottonwood" ...
```
**5 forged values, 5 refusals to honour them.** The server resolves the JWT firm and ignores the
client's assertion.

**POSITIVE CONTROL -- is that envelope dynamic, or a constant string?** Vary the URI, same bearer:
```
/artifacts/advisor_summary.json    -> "uri":"/gold/artifacts/advisor_summary.json"
/artifacts/zzz_control_probe.json  -> "uri":"/gold/artifacts/zzz_control_probe.json"
/entities/xyz/abc.json             -> "uri":"/gold/entities/xyz/abc.json"
```
**The envelope is built per-request.** So the constant `cottonwood` across the forgery arms is a real
resolution, not a hardcoded literal.

**SOURCE, at `a2fcc5efc4`:** `infra/aws/lambda-edge/auth-validator-edge/index.mjs:388` --
`request.headers["x-firm-id"] = [{ key: "X-Firm-Id", value: payload.firmId || "" }]` -- a plain
**assignment**, not a merge: it destroys any client value. **APPLIED:** that function is associated as
**`viewer-request`** (`auth-validator-edge:18`) on the Positioning behaviour and on every
`/api/scoped/*` behaviour -- viewer-request runs on **every** request, ahead of cache-key computation.

⚠ **RESIDUAL, NOT WAVED THROUGH -- `:211-212`:**
`if (uri.startsWith("/auth/") || request.method === "OPTIONS") { return request; }` returns the request
**unmodified**, before the `:388` injection. A client `X-Firm-Id` survives on those two paths.
**Measured mitigation:** the live `/auth/*` behaviour carries **NO Lambda association at all**
(distribution `EVTSA9VEHNZVH`, 26 cache behaviours enumerated), so on `/auth/*` the function is not
even invoked; and `shared-advisor-router:92-93` synthesises a 204 for OPTIONS before any artifact is
reached. **Not exploitable as measured, and not a clean guarantee either** -- it is an early-return
that depends on two unrelated configurations staying as they are. Reported, not fixed (design work is
not this TO's grant).

⚠ **UNMEASURED, stated rather than implied:** whether the echoed `firmId` field takes a value **other
than** `cottonwood` for a different identity. One credential. The field's *dynamism* is controlled
(above); its *cross-firm variability* is not.

**Verdict `T3AE-AC2`: PASS.** `X-Firm-Id` is JWT-injected and **not client-assertable**, exercised.
`PT-inv-2` (the standing form, which `3.0.0_SA_CVO~Z` measured as bound by zero criteria) is satisfied
**in substance** by this exercise; its formal binding remains the issuer's one-line write.

---

## 3. AC3 -- CDN CACHE KEY INCLUDES FIRM. **FAIL on Positioning's path; the correct policy exists elsewhere**

**APPLIED**, distribution `EVTSA9VEHNZVH`, live `get-distribution-config`, **26 cache behaviours**:

| policy | used by | headers in cache key | TTL |
|---|---|---|---|
| `opal-scoped-advisor-by-firm` `45eb7514` | `/api/scoped/advisor-intelligence/artifacts,entities,*.json` (S3) | **whitelist `X-Firm-Id`** + qs `firm` | def 60 |
| `Managed-CachingDisabled` `4135ea2d` | all `/api/scoped/*` APIGateway behaviours | none | **0** |
| `opal-api-general-5min-cache` `ce00305d` | **`/api/general/*` <- POSITIONING** | **none** | **def 300** |

**EXERCISED**, response headers on the Positioning fetch:
```
Cache-Control: public, max-age=300, s-maxage=300
X-Cache: Miss from cloudfront
```
⛔ **`public`, 300s, and NO header in the cache key**, on an artifact fetched with a bearer. The firm-
keyed policy `opal-scoped-advisor-by-firm` **does** exist and **is** applied -- to the scoped S3
behaviours, **not to the path Positioning uses.**

⚠ **AND CACHE PARTITIONING WOULD NOT SAVE IT.** With one unscoped artifact, adding firm to the cache
key partitions identical bytes into per-firm entries. **The cache key is downstream of the real defect;
fixing it alone would produce a correct-looking control over an unchanged exposure.** Named because
`PT-a-3` read alone invites exactly that remedy.

**Verdict `T3AE-AC3`: FAIL.**

---

## 4. AC4 / AC5 / AC6 / AC7

- **`T3AE-AC4` (THE BYTES, NOT THE PIXELS) -- PASS.** Every verdict above comes from HTTP status +
  response bytes + sha256, S3 object listings, and live CloudFront policy reads. **No render, no
  screenshot, no UI state was used or consulted.** The client gate `modesFor(firm)` was not exercised
  and is not cited as evidence for anything.
- **`T3AE-AC5` (`PT-inv-3`, null firm fails closed) -- UNMEASURED BY EXERCISE.** Requires a JWT with
  `firmId` absent; the available credentials all carry a firm, and minting a firmless token means
  either signing-key access or mutating a production user record. **Neither is in this TO's grant.**
  Reported as unmeasured rather than inferred from `payload.firmId || ""` at `:388`, which is source,
  not behaviour. **A defensible design exists in the code; the criterion asked for an exercise.**
- **`T3AE-AC6` (other firms byte-identical) -- VACUOUSLY SATISFIED, denominator 0.** This TO changed
  **no code, no policy, no artifact**. Nothing could differ. Recorded as vacuous rather than PASS: a
  criterion that cannot fail over its own window has not been tested.
- **`T3AE-AC7` (DESIRED != APPLIED != EXERCISED) -- PASS.** Every claim above carries its rung.
  Specifically: no Terraform file is cited as evidence that anything is in force. The cache policies,
  behaviour list and Lambda associations are **APPLIED** (live `cloudfront get-*`); the header
  behaviour, the 401/403 arms and the byte counts are **EXERCISED**; `:388`, `:211`, `:64-67`, `:1133`
  are **SOURCE** and are labelled as such wherever used.

---

## 5. THE SEAM I DID NOT CROSS, NAMED BY AN INSTRUMENT

`PT-a-1`'s portal limb is DE-class. **I measured the boundary rather than accepting it:**
```
owned-paths-validate.py --check-agent 0.7.0_AE_CloudOps~Y  (paths on stdin)
  infra/aws/terraform/portal-auth/main.tf     rc=0  PASS
  infra/aws/terraform/shared-infra/main.tf    rc=0  PASS
  portal/src/app/positioning/page.tsx         rc=1  VIOLATION -- not in permitted_agents
  CLAUDE.md                                   rc=1  VIOLATION
  org/tier1_exec/1.0.0_SA_CTO/deliverables/*  rc=1  VIOLATION
NEG CTL  0.4.0_DE_ClientPlatform~Y on the two infra paths   rc=1 VIOLATION
NEG CTL  0.4.0_DS_ClientPlatform~L on the two infra paths   rc=1 VIOLATION
```
The DE limb is **mechanically refused to this lane**, not merely reserved by convention. The React
Query key limb `0.0.0_AB_MSTR~Z` flagged lives in `portal/` and is on the far side of that line.

⛔ **INSTRUMENT TRAP, and it is the same shape as the evening's others.** Run as
`--check-agent <agent> <yaml>` with **nothing on stdin**, the tool returns **rc=0 for EVERY agent** --
it reads its path list from stdin (`:229`), so an empty list is zero checks and a clean exit. My first
two runs returned rc=0 for me *and* rc=0 for the lane COO had measured as violating. **A vacuous pass
is byte-identical to a real one.** It matters because a seating rationale cited this tool. Surfaced to
`3.0.0_SA_CVO~Z` (msg 10212/10213); `3.0.0_SA_CVO~Z` classed it with the commit gate's
`clean for 0 file(s)`.

---

## 6. NOT MINE -- REPORTED, NOT ACTED ON

- **`PT-b-2` substrate shape:** this measurement does **not** force one. The finding is that Positioning
  is on the *general* path with no firm dimension; that is true under either shape. **No shape picked.**
- **`PT-b-4`:** not touched.
- **The remedy for AC1/AC3 is a DESIGN act** (move Positioning to a firm-scoped serving path, produce a
  per-firm artifact, decide the unscoped-default question `PT-e-2`). `PT-e-2` is COO+CTO's, `PT-c-1`
  (who writes the per-firm artifact) is blocked on `PT-b-2`, and the portal half is DE's. **I built
  nothing and propose nothing here.**

## 7. cell_status -- FROM OBSERVED STATES ONLY

```
PT-a-1  OBSERVED -- TARGET UNMET (not "falsified": the statement column is the target state, and
                    nothing has been built against it yet -- 1.0.0_SA_CTO~Z msg 10329). Positioning
                    is on /api/general/, single unscoped artifact, no serving-layer firm
                    discrimination. UNSIZED: whether those bytes are house/global or another
                    partner firm's book is NOT measured -- routed as a cell, see s.9.
PT-a-2  OBSERVED -- HOLDS. X-Firm-Id is JWT-injected and not client-assertable, exercised 5 arms
                    with a dynamic-envelope positive control. Residual: :211-212 early return.
PT-a-3  OBSERVED -- DOES NOT HOLD on Positioning's path (cache key has no header; public/300s).
                    The firm-keyed policy exists and is applied to the scoped S3 behaviours only.
```

---

## 8. ADDENDUM -- THE UNIFORMITY CONSTRAINT, **WITHDRAWN BY ITS AUTHOR**

⛔⛔ **READ THIS BEFORE THE SECTION BELOW. `1.0.0_SA_CTO~Z` WITHDREW THIS CONSTRAINT AT 10364, NAMING
THIS SEAT: *"0.7.0_AE_CloudOps~Y: DO NOT BUILD TO MY 10329/10354 s.4. It is withdrawn as stated."***
**Andrew-direct ~21:52Z** -- *"all of Positioning is general... we are making an exception in the case
of cottonwood here for the purpose of their 'Satellites' portfolios"* -- **puts Satellites on a
different footing from Models and ETFs BY DESIGN, which is exactly the shape the constraint forbade.
They cannot both stand.** CTO~Z's own reason for which one goes: *"MINE WAS INFERRED FROM HIS ~21:3xZ
FORKED-ROUTES RULE. HIS ~21:52Z IS A DIRECT STATEMENT ABOUT THIS PAGE. A DIRECT WORD BEATS MY
INFERENCE FROM A GENERAL ONE, EVERY TIME."*

⭐ **NOTHING WAS BUILT TO IT -- THIS WAS A MEASUREMENT TO, AND THE MEASUREMENT IS UNAFFECTED.** The
5-of-5 uniformity figure below is a fact about the world and still holds. **What is withdrawn is what
it IMPLIES for the remedy**, not the number. The section is kept rather than deleted so the withdrawal
is legible; **do not read it as live guidance.**

⚠ **`1.0.0_SA_CTO~Z` explicitly declined to adjudicate between Andrew's two statements** (~21:3xZ
forked-routes vs ~21:52Z this-page) and put the narrow question up rather than resolving it, per
CLAUDE.md:55. **I am not resolving it either.** Their labelled reading, carried as a reading and not a
ruling: *"the same pattern" plausibly governs HOW an exception is built, not WHETHER one exists.*

---

### (superseded) ANDREW'S ~21:3xZ ARCHITECTURE RULE, MEASURED AGAINST THIS CELL

`1.0.0_SA_CTO~Z` (msg 10285) adopted Andrew's ~21:3xZ standing rule as a gate criterion and put it
directly on `PT-a-1`: **where a route forks N ways, the N branches must share a structure; an N-1/1
split is a defect on its face.** Applied within Positioning: the three modes **MODELS | ETFS |
SATELLITES** must not take divergent serving routes.

**MEASURED, portal `80af31ac`, every live Positioning-page fetch site:**
```
:1133  /api/general/positioning/positioning_data.json          (models / shared)
:1328  /api/general/etfs/positioning_data.json                 (ETFs)
:1381  /api/general/positioning/model.json
:1938  /api/general/positioning/holdings_attribution_data.json
: 897  /api/general/benchmarks/etf_returns.json
DENOMINATOR: 5 live sites, 5 on /api/general/.  2 further sites (:1828, :1935) are COMMENTED OUT
and were confirmed non-live by reading, not inferred from path shape.
```
⭐ **TODAY THE THREE MODES ARE UNIFORM.** All of them are served over `/api/general/*` -- the same
behaviour, the same `opal-api-general-5min-cache` policy, the same `public-data-router`. **The 2-of-3
divergence Andrew called unacceptable does NOT currently exist among the Positioning modes.**

⛔ **IT IS CREATED, NOT CURED, BY A PARTIAL FIX.** Moving *one* mode (e.g. Satellites, the mode
`ETFS_SATELLITES` is actively changing) to `/api/scoped/` while Models and ETFs stay on `/api/general/`
produces exactly the N-1/1 split, **inside the one page this project exists to fix.** So `PT-a-1`'s
remedy has an architectural constraint that was not in the cell's wording: **all three modes move, or
none does and the boundary is enforced another way.** `1.0.0_SA_CTO~Z` explicitly did not rule which;
neither do I. **Recorded as a measured constraint on the design, not a design.**

⚠ **AND THE ACROSS-PAGES DIRECTION IS THE OPPOSITE SIGN, per `1.0.0_SA_CTO~Z`:** moving Positioning to
`/api/scoped/` is *convergence* -- AdvisorIntelligence and MDPF_SCOPED already run that pattern. **His
rule endorses the POSN_TENANCY direction while constraining its granularity.**

⛔ **THE RULE BINDS ON TWO AXES AND THEY ARE DIFFERENT FORKS. BOTH ARE RECORDED BECAUSE A REMEDY CAN
SATISFY ONE AND VIOLATE THE OTHER:**
```
MODE AXIS  (1.0.0_SA_CTO~Z, msg 10285)  MODELS | ETFS | SATELLITES must not take divergent serving
                                        routes. MEASURED UNIFORM TODAY (5 of 5 sites on /api/general/).
FIRM AXIS  (2.0.0_SA_COO~Z, msg 10287, standing clause @e97731773a)  "Whatever shape /api/scoped/
                                        takes for one firm, EVERY firm's route takes the same shape."
                                        UNMEASURED -- no per-firm Positioning route exists yet to compare.
```
>> **`2.0.0_SA_COO~Z` names the mechanism precisely: the 2-of-3 split is the NATURAL OUTCOME of a
   per-firm rollout, which is how this work would otherwise proceed. It is forbidden BEFORE the first
   line is written rather than after the third firm.** For this TO that is a constraint on the remedy,
   not on the measurement -- and the measurement is what says the remedy has not started. <<

---

## 9. THE DECIDING FACT, MEASURED: **OPAL-COMMON. A DESIGN GAP, NOT AN INCIDENT.**

`1.0.0_SA_CTO~Z` (10329, 10344) and `2.0.0_SA_COO~Z` (10338) independently converged on one unmeasured
fact that inverts the severity of s.1, and Andrew already holds the fork as of ~21:4xZ. **Answered here.**

```
IF positioning_data.json is FIRM-SPECIFIC  -> a firm received ANOTHER FIRM'S data.   AN INCIDENT.
IF it is OPAL-COMMON model data            -> unscoped serving of SHARED reference.  A DESIGN GAP.
MEASURED ANSWER: OPAL-COMMON.
```

**METHOD, and it stays inside the authorised read.** `1.0.0_SA_CTO~Z` bound this explicitly: *"The
discriminating read is on the artifact's PROVENANCE AND SHAPE -- does it carry a firm segment, a house
identifier, a partner's model set -- NEVER on its holdings."* **I read top-level keys, the portfolio
KEY NAMES, and an identifier token census. I did not enumerate a single position, ticker, weight or
amount.** No new fetch was needed -- these are the bytes already retrieved for the AC1 arm.

```
top-level keys   generated_at · data_as_of · note · benchmarks · portfolios · current_holdings · data_date
portfolios       dict[5]  -> UST · ST · INT · LT · ULT          <- the FIVE OPAL DURATION MODELS
current_holdings dict[6]  -> those five + AGG                    <- AGG is a benchmark index
benchmarks       dict[2]  -> etf · index
note             "Optimized positioning data with benchmarks and segments -- eliminates need for
                  model PKL load"
generated_at     2026-08-27T11:05:19Z    data_as_of 2026-08-26
```
**FIRM-IDENTIFIER CENSUS -- 14 tokens, ALL ZERO, denominator 73,424 chars decompressed:**
`cottonwood` 0 · `49financial` 0 · `49f` 0 · `inflection` 0 · `blackdiamond` 0 · `schwab` 0 ·
`custody` 0 · `firmid` 0 · `firm_id` 0 · `"firm"` 0 · `tenant` 0 · `advisor` 0 · `account` 0 ·
`client` 0.

**CONTROLS ON THAT CENSUS -- added after `2.0.0_SA_COO~Z` ran one and I had not.** Fourteen zeros
prove nothing without evidence the scan can find anything in this file:
```
POSITIVE  portfolio 19 · ust 31 · holdings 17 · agg 15 · benchmark 7 · note 4
NEGATIVE  zzz_no_such_token_9999 -> 0
```
⚠ **I SHIPPED THE FIRST VERSION OF THIS SECTION WITH AN UNCONTROLLED CENSUS.** My parse succeeded and
exhibited real structure, so the zeros were not the gzip artifact -- but *"a positive control proves
the engine, not your pattern"* and I had not run one. `2.0.0_SA_COO~Z` did. **Their `portfolio = 19`
and mine agree exactly, independently.**

⛔ **AND THEIR CLASSIFICATION IS SHARPER THAN MINE -- ADOPTED, WITH CREDIT.** I wrote *"a design gap,
not an incident."* `2.0.0_SA_COO~Z` (10345) shows it is **neither of the two on offer**:
```
NOT an incident   the bytes a Cottonwood identity received are the bytes EVERY firm gets BY
                  CONSTRUCTION -- shared reference data, exactly what POSN_CUSTOM registered
NOT benign        the SERVING PLANE HAS NO FIRM DISCRIMINATION AT ALL
=> LATENT EXPOSURE WITH A NAMED TRIGGER: the moment firm-specific content enters this artifact it
   leaks BY CONSTRUCTION -- and making Positioning firm-specific is what POSN_TENANCY EXISTS TO DO.
```
⭐ **THE PROJECT'S OWN SUCCESS IS THE TRIGGER.** That reframes the remedy from *"fix a leak"* to
***"build the scoping BEFORE the data lands"***, and makes the sequencing load-bearing rather than
tidy. **It also sharpens s.3's cache-key trap one turn further than I had it:** adding firm to the
cache key today partitions identical bytes -- a green-looking control over **no exposure yet**, which
then does nothing about the one that arrives WITH the data. **Built, green, and measured against the
wrong era.**

⚠ **BOTH OF US HIT THE GZIP TRAP AND IT FAILED DIFFERENTLY, WHICH IS THE TRANSFERABLE PART.**
`2.0.0_SA_COO~Z` grepped the raw object and got **ten clean zeros that meant nothing** -- a verdict
pointing exactly at the expected conclusion. I called `json.load` on the same bytes and got a
`UnicodeDecodeError` at byte 1. **Same trap, same file: the grep failed SILENTLY toward the expected
answer, the parse failed LOUDLY.** Choosing an instrument that must succeed to return anything is what
made the difference, and it was luck of habit rather than design.

⭐ **THIS IS CORROBORATION IN THE STRICT SENSE, NOT REPETITION.** `2.0.0_SA_COO~Z` noted that
`POSN_CUSTOM`'s registration says the five models come from Yang's Bloomberg PKL via
`generate_positioning_json.py` and are *"Opal model data, NOT bd/49F/Schwab custody"* -- **but flagged
that as a PROJECT RECORD, a claim about the pipeline, and from July.** I did not read that pipeline.
**I read the SERVED BYTES.** A record about a producer and a census over the artifact are **different
instruments**, and they agree.

⚠ **WHAT THIS DOES AND DOES NOT ESTABLISH.** It establishes that the served artifact carries **no
firm-identifying or firm-partitioned content** and that its portfolio set is the five Opal duration
models. It does **not** establish the producer's provenance by reading the producer -- that remains
COO's project record, now independently corroborated at the artifact. **A firm receiving this file
receives Opal's own model reference data, not another firm's book.**

⛔ **THE FINDING IN s.1 IS UNCHANGED AND SO IS THE PROJECT'S JUSTIFICATION.** Unscoped serving of
common data is still exactly the gap `(b) ACCESS` was ruled on, `AC1` is still FAIL, and Cottonwood
still receives an artifact its own home cannot produce. **What changes is the CLASS: this is a scoping
gap to close, not a leak to escalate.** Neither word should have been used before this read, and
`2.0.0_SA_COO~Z` was right to withhold both.

⚠ **INCIDENTAL, and it refines s.1's byte-match rather than weakening it:** the object is stored and
served **gzip**, so the 8,088 B is the COMPRESSED artifact (73,424 B decompressed). The served-bytes /
S3-object match in s.1 was compressed-to-compressed and still holds exactly.

⛔ **AND `0.4.0_DS_ClientPlatform~L` (10363) UPGRADED THE IDENTITY EVIDENCE MY MATCH RESTED ON.**
They pulled the object's `ETag "8c27325ff6a08e1ea6466cae172ff534"` and `VersionId
98l2svntFj4TsS9mxW1h5HGkVJeorjHN`, and named the gap exactly:
>> ***"a size match is a coincidence candidate, an ETag match is not."*** <<
**My s.1 claim that the served bytes ARE that key rested on a byte COUNT.** A count is a weak identity
oracle -- two different 8,088-byte objects are perfectly possible. **Accepted as a correction to my
evidence, not merely as corroboration of my conclusion.** Their independent census (13 tokens, 0 hits,
81,786 chars serialized) and mine (14 tokens, 0 hits, 73,424 chars decompressed) differ in denominator
because we serialized differently -- **two instruments, same verdict.**

### SURPRISE-CHANNEL ITEM (off-cell, surfaced not chased)
`portal-proxy.ts:962` fetches **`/returns/etf-periods`** -- no `/api/` prefix. `API_BASE_URL` is
`VITE_PORTAL_API_URL ?? ''` (`:49`), i.e. **same-origin**, and of the **26 CloudFront behaviours on
`EVTSA9VEHNZVH`, ZERO match `/returns*`** (families: `/api/*` 23, `/auth/*` 1, `/json-tiered/*` 1,
`/v1/*` 1). A same-origin `/returns/...` therefore falls through to the **DEFAULT** behaviour, whose
origin is the SPA bucket `S3-opalinvest-portal` -- i.e. it would resolve to the app shell, not JSON.
**This is the "one unique pattern" shape on the very page in question**, but it is a DE/portal surface
and a returns endpoint, not the access boundary. **Not investigated further, not acted on.** Filed to
`3.0.0_SA_CVO~Z`, cc `2.0.0_SA_COO~Z`. *(Unverified at runtime: `VITE_PORTAL_API_URL` may be set at
build time, which would change this entirely -- I did not read the build env, so this is SOURCE-level
and explicitly not a runtime claim.)*
