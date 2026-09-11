# BATTERY IB-rt-1 -- THE SEAM -- RESULT

**Run:** 2026-09-11T13:4xZ by `0.9.0_WK_IRPT_BCKEND~2` on branch `wk-irpt_bckend-2-2`, worktree
`/c/tmp/wk-irpt-2-2`, re-cut from `CLOUD` at `c8189bb6ae`.
**Invocation:** `timeout 600 python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~2/battery_ib_rt_1.py`
**Token expected by RT1-AC1:** `IBRT1-SEAM-PUBLISHED`
**Token emitted:** **`IBRT1-SEAM-PUBLISHED`** -- `10 of 10 arms PASS`.

> **THIS DOCUMENT SUPERSEDES THE FIRST RUN'S, AND SAYS WHAT CHANGED.** The first run withheld the
> token on arm (b) as first cut: it graded each handler response against a DOCUMENT schema and
> measured **0 of 11**. That measurement was correct and it is unchanged below. What changed is
> the criterion: the issuer re-cut arm (b) (channel row `IRPT_BCKEND-S26`, commit `c8189bb6ae`)
> because the arm asked this cell to prove a thing only the handler cells can make true -- a proxy
> on the wrong cell. **v1 now publishes the missing half**, and the conformance count is reported
> rather than gating.

---

## SUMMARY

| arm | criterion clause | verdict | the number |
|---|---|---|---|
| a1 | (a) one carrier | **PASS** | one file, one sha256, on both sides |
| a2 | (a) retired carrier | **PASS** | the api root's `routes.json` carries no `routes` key |
| a3 | (a) schemas versioned | **PASS** | **11 of 11** |
| a4 | (a) `CONTRACT.md` census | **PASS** | **83 of 83** fields, **11 of 11** schemas |
| b1 | (b) response contracts published | **PASS** | **11 of 11** DECLARED routes, **17** `data` `$ref`s resolved |
| b2 | (b) `CONFORMS` is reachable | **PASS** | **13 of 13** controls |
| b | (b) the paired census | **PASS** | **11 of 11** classified; **0 of 11** conforming (reported, not gating) |
| c | (c) twenty-two negatives | **PASS** | **22 of 22** |
| d | (d) the api root is clean | **PASS** | `No changes.` |
| e | (e) C-S77 reissued | **PASS** | **3 of 3** headings, **2 of 2** commits |

**10 of 10 arms PASS.**

---

## ARM (a) -- ONE CARRIER

**The mechanism, read from the file rather than asserted.** `routes.tf` declares

```hcl
contract_routes_path = "${path.module}/../../../../../docs/contracts/investor-reporting/v1/routes.json"
contract             = jsondecode(file(local.contract_routes_path))
```

The battery re-derives that path from the HCL expression itself and hashes **what it resolves to**,
so "byte-equals" is a statement about the file Terraform opens, not about a path typed into a test.
Both sides print the same absolute path and the same `sha256`. **They are the same file, not two
copies that currently agree** -- the criterion asks for byte-equality; what was built is stronger,
and the difference matters because two files that agree today are one edit away from disagreeing.

**WHICH MECHANISM WAS CHOSEN**, as the decomposition requires stating: the api root **READS the
contract path**. Not a re-export, not a symlink. The api root's own `routes.json` is retired in
place as a **pointer document** -- so a stale path answers **loudly** instead of 404-ing.

**The eleven document schemas:** 11 of 11 carry `$id` containing `/v1/`, `x-contract-version: v1`
and a `contract_version` property with `const: v1`, optional and never required.

**`CONTRACT.md`'s field census is RE-DERIVED by the battery every run** rather than read back from
the document: **83 of 83** PRD-derived properties carry a meaning citing a PRD location (82 a
CONTRACTS **table** row with its required-meaning item, 1 -- `DirectoryEntry.cohort` -- a CONTRACTS
**section** paragraph, **0** uncited), across **11 of 11** schemas. The census excludes the eleven
`contract_version` properties this cell authored: counting a cell's own writing as PRD coverage
would certify its author.

**`CONTRACT.md` gained three things at the re-cut**, each derived from `routes.json` rather than
written by hand:

* a **PRODUCER column** per schema -- ten are `IRPT_BCKEND`'s and **`RenderPackage` is the
  FRONTEND's** (row `IRPT_BCKEND-W2-S17`), so for exactly one contract of the eleven "the producer
  defines, the consumer conforms" points the other way and this backend conforms;
* the **operation <-> route table as the ONE authority** (row `W2-S13`), with both orphan
  directions named: the two consumer operations marked `NOT-A-ROUTE` **with their reasons**, and
  the three producer routes with no consumer operation **with theirs**. An absence cannot be read
  as a statement -- "missing from the file" and "deliberately unserved" look identical until one
  of them says so;
* the **wire-casing rule** (row `W2-S14`): the counterpart's **generated client camelizes at the
  wire boundary and back. No meaning moves, and nothing in v1 changes for it.**

---

## ARM (b) -- THE RESPONSE CONTRACTS AND THE PAIRED CENSUS

### (b1) THE HALF THAT IS THIS CELL'S: the contracts are published

```
denominator: 12 route(s) in routes.json = 11 DECLARED + 1 NO-HANDLER-AT-HEAD
published, valid as schemas, every data $ref resolved ... 11 of 11 DECLARED
holdings-snapshot: NO response contract, and that is the answer -- it answers nothing
```

**ONE ENVELOPE FOR EVERY ROUTE:** `{contract_version, operation, firm_id, data, status?}`,
`additionalProperties: false`. A consumer writes **one** response parser and branches on
`operation` -- which is what three ad-hoc envelopes currently cost it.

Each contract is checked as a **schema**, not merely as JSON (`check_schema`): a published schema
no validator accepts refuses nothing at all and would read as coverage. **17** `data` `$ref`s were
resolved to a published document schema, each by opening the target file and walking the JSON
pointer.

**`data` NEVER INVENTS A MEANING.** It is the whole producer document by `$ref`, or a **declared
slice** whose every property `$ref`s that document's own property subschema. A slice cannot `$ref`
the whole document -- the document is `additionalProperties: false` with required fields, so a
subset fails it -- so the slice references the **same definitions at a finer grain** rather than
restating them, and a definition cannot drift from itself.

**`firm_id` is typed at the boundary:** it `$ref`s `ResolvedScope.verified_request_firm_id` for its
MEANING and constrains the WIRE FORM to the issued opaque id. The registry spelling and the opaque
spelling reconcile only through `FirmBinding` (row `W2-S9`).

**Both denominators are printed, deliberately.** The re-cut names "one per route in `routes.json`"
(12) and "the eleven response schemas ... `11 of 11`" (11); both hold only if the
NO-HANDLER-AT-HEAD route gets none, which is how it was built -- a route that answers nothing
cannot have a response contract without describing a response that cannot exist. The **absence is
asserted by test**, not merely left empty. Row `IRPT_BCKEND-W2-S18` records the reading.

### (b2) THE CONTROL -- without it the census below is not a measurement

```
control: a known-good document CONFORMS and a known-bad one does NOT, per response contract ... 13 of 13
```

**A `0 of 11` from a broken validator reads exactly like a `0 of 11` from non-conforming
handlers.** So every response contract is exercised against a known-good and a known-bad document
taken from the estate's **own** per-document fixtures (`_contracts/fixtures/<Document>.valid.json`
and `.invalid.json`, written by IB-s-18 -- not minted here to suit this test), and each fixture's
own `_expect` string is asserted against the role it is being used in, because a control built on a
fixture that turned out to mean the opposite would invert without failing. The envelope is also
shown to refuse a registry-spelled `firm_id`, a display name, a wrong-shaped opaque id, a foreign
`operation`, a foreign `contract_version` and any additional property.

**`CONFORMS` is therefore REACHABLE, and the `0` below is a fact about the handlers rather than
about this file.**

### (b) THE PAIRED CENSUS -- four closed outcomes, every operation in exactly one

```
directory-search     BLOCKED-BY-W2-S16  ... the envelope it returned instead: {ok, op, reason, result}
resolve-scope        BLOCKED-BY-W2-S16  ... the envelope it returned instead: {ok, op, reason, result}
performance-report   BLOCKED-BY-W2-S16  ... the envelope it returned instead: {body, statusCode}
analysis-requests    BLOCKED-BY-W2-S16  ... {budget_seconds, live_call, measured_overview_seconds, note, ok, reason}
analysis-report      DEPLOYED-ONLY      builds its own S3 client, no in-process fixture path (NoSuchKey)
submit-correction    NOT-A-ROUTE        v1 declares no route; routes.json names it with the reason
holdings-snapshot    BLOCKED-BY-W2-S16  the dispatcher refused with ROUTE_NO_HANDLER
narrative-packet     BLOCKED-BY-W2-S16  ... the envelope it returned instead: {body, statusCode}
export-preview       NOT-A-ROUTE        v1 declares no route; routes.json names it with the reason
submit-export        BLOCKED-BY-W2-S16  ... the envelope it returned instead: {body, statusCode}
export-receipt       BLOCKED-BY-W2-S16  ... the envelope it returned instead: {body, statusCode}
---
CONFORMS .................. 0 of 11
BLOCKED-BY-W2-S16 ......... 8 of 11   (IB-rt-2 arm (g) owns and deploys the six handlers)
DEPLOYED-ONLY ............. 1 of 11   (row W2-S15; graded at IB-rtb-1)
NOT-A-ROUTE ............... 2 of 11   (row W2-S13; named in routes.json with its reason)
```

**The outcomes are a CLOSED set derived by subtraction** -- the request either produced a gradeable
response or it did not, and if not, why not -- and `classify_operation` **raises** rather than
inventing a fifth, because an unanticipated outcome absorbed into "blocked" is how a census stops
measuring.

**ONE DISTINCTION THE BUCKET HIDES, STATED SO THE READING IS NOT WRONG:** of the 8
`BLOCKED-BY-W2-S16`, **7 are envelope mismatches** by a handler that ran, and **1
(`holdings-snapshot`) is a published route with no handler at all** -- it refuses with
`ROUTE_NO_HANDLER`, its own code, rather than pretending. Both are IB-rt-2's, but they are
different work and the detail line says which.

**THREE ENVELOPES FROM SIX HANDLERS**, measured: `directory/handler.py` returns
`{ok, op, result, reason}`; `performance`, `narrative` and `export` return the API-Gateway
`{statusCode, body}`; `ycharts/generate/job.py` returns
`{ok, live_call, reason, measured_overview_seconds, budget_seconds, note}`.

**The printed envelopes carry KEYS ONLY**, asserted free of the five protected strings before
printing -- the keys are the finding, the values are a firm's data.

**Two of the eleven document schemas can never be an HTTP response at all:** `AnalysisRequest` is
the queue message the intake produces, and `RenderPackage` is the package handed to the export
renderer (and the frontend's, not this repo's). That is why response contracts had to be a
separate publication rather than a reuse.

**The handler entry points are DERIVED, not typed:** `lambda-source-map.json` gives each
function's `source_dir` and `tf_file`, and that Terraform file's own `handler = "<module>.<attr>"`
gives the entry point AWS calls. The first version of this test typed the map and sent
`POST /analysis` to `ycharts/generate.py`, which does not exist; the resulting `None` read as
`ROUTE_NO_HANDLER` -- a **legitimate** refusal code -- so every assertion passed through a
wrong-object error. The real entry point is `ycharts/generate/job.py`, and it **refuses the live
vendor call** itself.

**Consumer fixtures answered from the PRIMARY CHECKOUT** (`C:\Users\AndrewBerman\Desktop\ajb_workspace\portal`),
printed by the test: `portal/` is a gitlink and a linked worktree does not populate it, so an
unprinted resolution is how a `0 of 0` becomes a pass.

**WHAT WAS NOT DONE, DELIBERATELY.** No handler was edited (six handler directories are outside
this order's `<paths>`), no schema was loosened to admit an ad-hoc envelope, no client was patched
into a real handler to get past the AWS reach, and the dispatcher does not wrap a handler's answer
into a document it did not produce.

---

## ARM (c) -- TWENTY-TWO NEGATIVES -- **22 of 22**

```
mismatched X-Contract-Version refused with CONTRACT_VERSION ........ 11 of 11
wrong firm refused through FirmBinding, 0 protected bytes ..........  11 of 11
```

The version negative is refused **first**, before any scope is resolved, any firm is bound and any
route is looked up -- a caller speaking a different contract may be sending a body this version's
rules would **misread** rather than reject. The firm negative is refused **before the route is
looked up**: authorization precedes existence, because telling an unentitled caller "that route
exists but has no handler yet" discloses this estate's build state. (The paired test caught this
ordering: the holdings wrong-firm negative first returned `ROUTE_NO_HANDLER` -- a correct answer to
the wrong question.)

**BYTE CENSUS:** each of the 22 refusal envelopes was serialised and searched for the refused
version string, the claimed firm token, the bound opaque firm id, a client surname and an e-mail
address: **0 bytes of any of them in any envelope.**

**The check is COMMITTED AND NOT SERVED.** No Lambda deploy in this cell, per its own bound; the
deploy rides IB-rt-2, so no live request is version-checked today. Arm (c) grades it in process;
IB-rt-2 arm (g) grades it served.

---

## ARM (d) -- THE API ROOT IS CLEAN AFTER THE MOVE

```
No changes. Your infrastructure matches the configuration.
```

`.tools/terraform.exe` by path (never a PATH substitute -- a substitute re-pins remote state), on
`infra/aws/terraform/investor-reporting/api`, after `init` (the re-cut worktree carries no
`.terraform/`, and bound 4 anticipates it). **The contract produces byte-identical routing to the
hard-coded HCL map it replaced**, and it still does after `routes.json` gained its `operation`,
`consumer_operation` and `response_schema` keys: the carrier move and the authority additions
changed the source of truth and not the served surface. The 11 live routes on `7k3ed8px20` were
never touched.

---

## ARM (e) -- C-S77 REISSUED AT THE APPLY VINTAGE

**3 of 3** headings the ruling names, **2 of 2** apply commits (`a7659fa6af`, `ac202969e8`):

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
| `IRPT_BCKEND-W2-S13` | OBSERVATION / INERT | the two sides disagree on what an operation IS: 11 flat slugs vs 12 nested routes; **settled** by the operation <-> route authority in `routes.json` and `CONTRACT.md`, both orphan directions named with reasons |
| `IRPT_BCKEND-W2-S14` | OBSERVATION / INERT | naming is totally disjoint: 194 of 293 producer names snake, 0 camel; 139 of 220 consumer keys camel, 0 snake; 55 of 194 match only after camelizing. **Settled** by the wire-casing rule -- the client camelizes, no meaning moves |
| `IRPT_BCKEND-W2-S15` | OBSERVATION / INERT | `ops/status.py` builds its own S3 client -- printed `DEPLOYED-ONLY`, graded at IB-rtb-1 |
| `IRPT_BCKEND-W2-S16` | BLOCKING / **DISARMED** | the published schemas were document contracts with no response half. **Disarmed by the issuer's criterion re-cut** (channel row S26); the response contracts are published here and handler conformance is IB-rt-2 arm (g) |
| `IRPT_BCKEND-W2-S17` | OBSERVATION / INERT | self-correction on W2-S16, filed rather than edited: the eleventh schema is `RenderPackage`, not `FirmDestinationPolicy` -- and `RenderPackage` is the one contract of the eleven the **frontend** produces |
| `IRPT_BCKEND-W2-S18` | OBSERVATION / INERT | the re-cut names two denominators for the response set (12 routes vs eleven schemas); both hold only if the NO-HANDLER route gets none, which is how it was built, with both numbers printed |

---

## WHAT THIS BATTERY CANNOT SHOW

* **Handler conformance.** `0 of 11` operations conform today. The contracts say what each route
  MUST answer; making the six handlers answer it is **IB-rt-2 arm (g)**.
* **Anything between the client and `dispatch()`**: the CloudFront behavior's precedence among 28
  ordered behaviors, the edge validator's actual header injection for a real token (the test
  **supplies** the nine headers), and API Gateway authorizer `naqxlm`'s **result cache**, whose TTL
  is not declared in `partners-api/api-gateway.tf` (13 `authorizer_id` references, 0 caching
  declarations) and must be read from the live authorizer. Those are **IB-rtb-1**'s.
* **The served version check** -- committed, not deployed, until IB-rt-2.

An in-process paired test grades the seam's **contract**; only the replay grades the seam's
**wire**.
