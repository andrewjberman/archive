# BATTERY IB-rt-1 -- THE SEAM -- RESULT

**Run:** 2026-09-11T12:30Z by `0.9.0_WK_IRPT_BCKEND~2` on branch `wk-irpt_bckend-2-2`, worktree
`/c/tmp/wk-irpt-2-2`.
**Invocation:** `timeout 600 python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~2/battery_ib_rt_1.py`
**Token expected by RT1-AC1:** `IBRT1-SEAM-PUBLISHED`
**Token emitted:** **NONE.** `BLOCKED: 1 of 8 arms FAIL -- the token is withheld.`

> **RT1-AC1 IS A FAIL BY OUTPUT AND THE ORDER STAYS OPEN.** That is this cell's report on it, not
> a failure to finish it: seven of the eight arms are met on real artifacts, and the eighth is met
> by nothing that exists at this vintage. The reason is row `IRPT_BCKEND-W2-S16` and the remedy is
> outside this order's `<paths>`.

---

## SUMMARY

| arm | criterion clause | verdict | the number |
|---|---|---|---|
| a1 | (a) one carrier | **PASS** | one file, one sha256, on both sides |
| a2 | (a) retired carrier | **PASS** | the api root's `routes.json` carries no `routes` key |
| a3 | (a) schemas versioned | **PASS** | **11 of 11** |
| a4 | (a) `CONTRACT.md` census | **PASS** | **83 of 83** fields, **11 of 11** schemas |
| b | (b) eleven through the real dispatcher | **FAIL** | **11 of 11** exercised, **0 of 11** validate |
| c | (c) twenty-two negatives | **PASS** | **22 of 22** (11 version + 11 firm) |
| d | (d) the api root is clean | **PASS** | `No changes.` |
| e | (e) C-S77 reissued | **PASS** | **3 of 3** headings, **2 of 2** commits |

**7 of 8 arms PASS.**

---

## ARM (a) -- ONE CARRIER

**The mechanism, read from the file rather than asserted.** `routes.tf` declares

```hcl
contract_routes_path = "${path.module}/../../../../../docs/contracts/investor-reporting/v1/routes.json"
contract             = jsondecode(file(local.contract_routes_path))
```

The battery re-derives that path from the HCL expression itself and hashes **what it resolves to**,
so "byte-equals" is a statement about the file Terraform opens, not about a path typed into a test.

```
resolves to: C:\tmp\wk-irpt-2-2\docs\contracts\investor-reporting\v1\routes.json
published  : C:\tmp\wk-irpt-2-2\docs\contracts\investor-reporting\v1\routes.json
sha256(what Terraform opens) = 98f06e392416393ec8059905ba0cfa7856e22f485b8ba6fb8299ae3d92020715
sha256(the published file)   = 98f06e392416393ec8059905ba0cfa7856e22f485b8ba6fb8299ae3d92020715
```

**They are the same file, not two copies that currently agree.** The criterion asks for
byte-equality; what was built is stronger, and the difference matters: two files that agree today
are one edit away from disagreeing, and nothing would announce it.

**WHICH MECHANISM WAS CHOSEN, as the decomposition requires stating:** the api root **READS the
contract path**. It is not a re-export and not a symlink. The api root's own `routes.json` is
retired in place as a **pointer document** -- `_the_carrier`, `_why`, `_proof` and a note for a
reader who followed a stale link -- rather than deleted, so an old path answers **loudly** instead
of 404-ing into a guess.

**The eleven schemas:** 11 of 11 carry `$id` containing `/v1/`, `x-contract-version: v1` and a
`contract_version` property with `const: v1`. That property is **optional, never required**: the
schemas are `additionalProperties: false` and round-1 instances predate publication, so requiring
it would invalidate documents that are already correct. The **enforced** version is the
`X-Contract-Version` request header.

**`CONTRACT.md`'s field census is RE-DERIVED by the battery every run** (bound 12) rather than read
back from the document: **83 of 83** top-level properties carry a meaning citing a PRD location,
and **11 of 11** schemas have a section. The census excludes the eleven `contract_version`
properties this cell authored -- counting a cell's own writing as PRD coverage would certify its
author.

---

## ARM (b) -- ELEVEN THROUGH THE REAL DISPATCHER -- **FAIL**

```
exercised .................................................. 11 of 11
response VALIDATES against its producer schema .............  0 of 11
response does NOT validate in any document position ........   7 of 11   (row IRPT_BCKEND-W2-S16)
did not reach a response ...................................   4 of 11   (rows W2-S13, W2-S15)
```

**What ran.** Each of the consumer's eleven operations, built from the counterpart's published
fixture, dispatched through `_authz/dispatch.py` to the **real** handler entry point -- and the
entry point is **derived, not typed**: `lambda-source-map.json` gives the function's `source_dir`
and `tf_file`, and that Terraform file's own `handler = "<module>.<attr>"` gives the module and
attribute AWS calls. (The first version of this test typed the map by hand and sent
`POST /analysis` to `ycharts/generate.py`, a file that does not exist; the resulting `None` read as
`ROUTE_NO_HANDLER`, which is a legitimate refusal code, so **every assertion passed through a
wrong-object error**. The real entry point is `ycharts/generate/job.py`.)

**Consumer fixtures answered from the PRIMARY CHECKOUT** (`C:\Users\AndrewBerman\Desktop\ajb_workspace\portal`),
printed by the test: `portal/` is a gitlink and a linked worktree does not populate it, so an
unprinted resolution here is how a `0 of 0` becomes a pass.

**Why 0 of 11 validate.** Three document positions are tried per operation -- the whole response,
`response.result`, and the parsed `response.body` -- so a wrong-position read cannot be mistaken
for a non-conformance. None validates, for a reason that is structural rather than per-field:

* **The eleven published schemas are DOCUMENT contracts, not RESPONSE contracts.** They are the
  PRD CONTRACTS table's artifacts. Two of them can never be an HTTP response at all:
  `AnalysisRequest` is the queue message the intake produces, and `FirmDestinationPolicy` is firm
  configuration.
* **The six handlers return three different envelopes.** `directory/handler.py` returns
  `{ok, op, result, reason}`; `performance`, `narrative` and `export` return the API-Gateway
  `{statusCode, body}`; `ycharts/generate/job.py` returns
  `{ok, live_call, reason, measured_overview_seconds, budget_seconds, note}`.
* Every schema is `additionalProperties: false`, so **an envelope around a correct document is
  itself a validation failure.** The failures are envelope mismatches, not field disagreements.

**The four that did not reach a response**, each enumerated rather than dropped:
`submit-correction` and `export-preview` (the consumer publishes them; v1 declares no route --
row W2-S13); `holdings-snapshot` (published `NO-HANDLER-AT-HEAD` and refusing with its **own**
code rather than pretending); `analysis-report` (`ops/status.py` builds its own S3 client with no
fixture path -- row W2-S15; the dispatcher **admitted** the request and the handler **ran**).

**WHAT WAS NOT DONE, deliberately.** No handler was edited to emit a contract document, no schema
was loosened to admit an envelope, and the dispatcher does not wrap a handler's answer into a
document it did not produce. The first is outside `<paths>`; the second is the producer changing to
match its own test; the third is the self-wrapping harness bound 12 forbids. **The measurement
stands and the criterion fails.**

**The deciding line, verbatim:**

```
E   AssertionError: SEAM GAP (row IRPT_BCKEND-W2-S16): the response of 'directory-search'
    validates against DirectoryEntry in NO document position. whole response: Additional
    properties are not allowed ('ok', 'op', 'reason', 'result' were unexpected) |
    response.result: Additional properties are not allowed ('ambiguous', 'count', ...
```

---

## ARM (c) -- TWENTY-TWO NEGATIVES -- **22 of 22**

```
mismatched X-Contract-Version refused with CONTRACT_VERSION ........ 11 of 11
wrong firm refused through FirmBinding, 0 protected bytes ..........  11 of 11
```

**The version negative** sends `X-Contract-Version: v2-not-published`. The dispatcher refuses with
`CONTRACT_VERSION` **first**, before any scope is resolved, any firm is bound and any route is
looked up -- because a caller speaking a different contract may be sending a body this version's
rules would **misread** rather than reject.

**The firm negative** sends a request-controlled `X-Firm-Id` that does not match the firm the
request was verified against. It is refused with `FIRM_BINDING`, **before the route is looked up**:
authorization precedes existence, because telling an unentitled caller "that route exists but has
no handler yet" discloses this estate's build state. (The paired test caught this ordering: the
holdings wrong-firm negative first returned `ROUTE_NO_HANDLER` -- a correct answer to the wrong
question.)

**BYTE CENSUS.** Each of the 22 refusal envelopes was serialised and searched for the refused
version string, the claimed firm token, the bound opaque firm id, a client surname and an e-mail
address: **0 bytes of any of them in any envelope.** A refusal names the FIELD and carries counts;
it never echoes the value.

---

## ARM (d) -- THE API ROOT IS CLEAN AFTER THE MOVE

```
No changes. Your infrastructure matches the configuration.
```

`.tools/terraform.exe` by path (never a PATH substitute -- a substitute re-pins remote state), on
`infra/aws/terraform/investor-reporting/api`. **The contract produces byte-identical routing to the
hard-coded HCL map it replaced.** This is the proof the carrier move changed the SOURCE OF TRUTH
and not the served surface: the 11 live routes on `7k3ed8px20` were not touched.

---

## ARM (e) -- C-S77 REISSUED AT THE APPLY VINTAGE

**3 of 3** headings the ruling names are present and distinguished, **2 of 2** apply commits named
(`a7659fa6af`, `ac202969e8`):

```
1. THE INTENDED CLOUDFRONT BEHAVIOR      one appended behavior; 27 -> 28; declared order == live order, 0 lines
2. THE CLASSIFIED WAF NORMALISATION      3 blocks re-added, 0 differing fields, Rules JSON diff EMPTY
3. THE OBSERVED REFUSAL PLANE            200 text/html 1068 bytes  ->  401 application/json 51 bytes
```

Addendum: `S15-AC3_reissued_at_apply_vintage.md` (this directory). The original pre-apply judgment
is left **unedited** -- it is the only artifact showing the STOP was taken before the act.

---

## ROWS FILED BY THIS CELL

| id | class / standing | what |
|---|---|---|
| `IRPT_BCKEND-W2-S13` | OBSERVATION / INERT | the two sides disagree on what an operation IS: 11 flat slugs vs 12 nested routes; 11 of 11 consumer paths `ROUTE_UNKNOWN`; 2 consumer operations with no route, 3 routes with no operation |
| `IRPT_BCKEND-W2-S14` | OBSERVATION / INERT | field naming is totally disjoint: 194 of 293 producer names snake, 0 camel; 139 of 220 consumer keys camel, 0 snake; 55 of 194 match only after camelizing |
| `IRPT_BCKEND-W2-S15` | OBSERVATION / INERT | `ops/status.py` builds its own S3 client -- the in-process reach limit, named not hidden |
| `IRPT_BCKEND-W2-S16` | **BLOCKING / ARMED** | the published schemas are document contracts, not response contracts; **0 of 7** reachable operations validate; disarm owner `2.0.0_SA_COO~B` |

---

## WHAT THIS BATTERY CANNOT SHOW

Everything between the client and `dispatch()`: the CloudFront behavior's precedence among 28,
the edge validator's header injection, and API Gateway authorizer `naqxlm`'s **result cache**,
whose TTL is not declared in `partners-api/api-gateway.tf` (13 `authorizer_id` references, 0
caching declarations) and must be read from the live authorizer. Those are `IB-rtb-1`'s, on the
deployed plane. An in-process paired test grades the seam's **contract**; only the replay grades
the seam's **wire**.
