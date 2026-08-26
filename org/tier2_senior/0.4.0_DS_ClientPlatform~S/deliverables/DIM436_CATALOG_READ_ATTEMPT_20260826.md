# DIM-436 CATALOG READ — ATTEMPT RECORD, OUTCOME (d) READ-NOT-PERFORMED

**archetype:** DIAGNOSE
**Author:** `0.4.0_DS_ClientPlatform~S` · **2026-08-26 ~21:4xZ**
**Authority:** Andrew-direct ~19:36Z egress-for-verification (`a9f250f2df`, ON origin) for the READ;
Andrew-direct ~20:39Z **conditional** dim-436 write pre-authorization relayed `2.0.0_SA_COO` 73624
(chain: `1.0.0_SA_CTO` 73613 item 2, record `@d7cea57dd3`).
**Outcome ruling:** `2.0.0_SA_COO` 73730 — **condition UNMET, not FAILED.**

---

## 0. THE ONE-LINE ANSWER

**The catalog read could not be performed from this device. Dim 436's addability to template 390224
is UNKNOWN — exactly as unknown as before the attempt. NOTHING WAS WRITTEN TO BLACK DIAMOND. Andrew's
conditional pre-authorization is UNCONSUMED and has not lapsed.**

---

## 1. THE GRANT ACCOUNTING — WHAT IT COVERED AND WHAT IT DID NOT

`2.0.0_SA_COO` 73624 s.3 asked for this explicitly, whichever way it went.

| | |
|---|---|
| **SPENT** | Vendor READ calls to `bd3.bdreporting.com` on the 49F session: 1 bearer mint (×3 across attempts), 1 qt5 catalog POST, 2 template GETs, 3 auth-arm GETs. **All READS. All returned 401 except the mints.** |
| **NOT SPENT** | **Zero writes.** No `POST /v1/template/`, no `PUT /v1/template/`, no amendment, no clone, no delete. No pre-image was saved because no amendment was attempted. |
| **NOT TOUCHED** | No other template. No other dimension. No adjacent/"close enough" substitute — 73624 s.2(c) prohibits it by name and it was not approached. |
| **ALSO SPENT (Opal-owned, pre-authorized separately)** | AWS reads: Secrets Manager `describe-secret` (metadata only — **the secret value was never printed**), Lambda config/policy, EventBridge both planes, CloudWatch Logs, S3 listings. |

---

## 2. WHAT WAS RUN, AND THE RESULT

Endpoint per `data/black_diamond/API/domains/datamining/DOMAIN.md:23` —
`POST /datamining/request/Query/DimensionsFacts {"queryTypeId": N}`.
Tool: the estate's existing `data/black_diamond/API/tools/bd_endpoint_sweep.py` (BUILD LADDER step 2
— **no new code written**), 49F session, firm-scoped env.

```
GET  /datamining/auth/token                                       -> 200  x-session-expires-in: 7199
POST /datamining/request/Query/DimensionsFacts {"queryTypeId":5}  -> 401
GET  /datamining/request/v1/template/390224   (positive control)  -> 401
GET  /datamining/request/v1/template          (the DOC's own ex.) -> 401
ARM A cookie+token / ARM B token-only / ARM C cookie-only         -> 401 / 401 / 401
```

⛔ **THE FIRST ATTEMPT DID NOT EVEN REACH BD, AND IT EXITED 0.** MSYS rewrote the leading-slash path
to `C:/Program Files/Git/datamining/request/Query/DimensionsFacts`; the tool reported
`status=None bytes=0` and **rc=0**. A failed retrieval wearing a clean exit code — the estate's own
retrieval class. Fixed with `MSYS_NO_PATHCONV=1`. **Had I read rc instead of the printed status, I
would have recorded a successful call that never happened.**

---

## 3. FOUR HYPOTHESES OF MINE, EACH KILLED BY A MEASUREMENT

Recorded in full because the discarded ones are the load-bearing half: each was coherent, each was
supported by real evidence, and each was wrong.

| hypothesis | what killed it |
|---|---|
| Dead/expired cookie | mint returns **200**, `x-session-expires-in: **7199**` (~2h remaining) |
| **The 49F session probe is a false positive and the BD pull is DOWN** | `bd-49f-runner` logged `auth OK firm=49f` and **LANDED `transactions`+`realized` for 2026-08-26** |
| Wrong auth-header combination | three arms (cookie+token / token / cookie), **identical 401** |
| Cloudflare edge rejecting a stale `__cf_bm` | **no `cf-ray`, no `server`, no `cf-mitigated`** on the 401 — BD's app is refusing, not the edge |

⛔ **THE SECOND ONE IS THE ONE TO REMEMBER.** Mid-investigation I held: two 401s + secret
`LastChangedDate 2026-07-27` + the session-trigger log saying *"Lever A: cookie POSITIVE-live -> SKIP
mint"*. That is a coherent, well-evidenced chain for **"the refresher's probe is a false positive and
a product pipeline is silently down."** I was one step from filing it. **The runner's own log
falsified it.** Every input was true and the conclusion was wrong — a false OUTAGE report, which
spends credibility and manufactures pressure to "fix" a working pipeline.

**AND ONE MEASUREMENT OF MINE WAS ABOUT THE WRONG TREE.** I read
`s3://opal-data-assets/blackdiamond/49f/bronze/allocation_390224/` at 2 trading days behind
(`lib/trading_calendar`, 30 partitions materialised) while the runner reports `bucket=opal-data-bd`.
**Different bucket.** That reading is filed as an OBSERVATION with its denominator, **not** a
staleness finding: this seat has not established that table's CADENCE (Rule 28 row 2), today's run
landed `transactions`+`realized` and not allocations, and NEVER#1 forbids reading a wall-clock gap as
a broken producer.

---

## 4. THE RESIDUAL — MARKED INFERRED, NOT PROVEN

**MEASURED:** `bd-49f-runner/lambda_function.py:56-57` pins
`BD_SESSION_SECRET_ID = "blackdiamond/49f/session"` and `BD_BASE = "https://bd3.bdreporting.com"` —
**byte-identical to what this attempt used.** Same credential, same host, same mint flow.
**AWS-origin authenticates today. This device does not.**

**INFERRED, and NOT asserted:** that ORIGIN is the cause. It is the only variable not controlled. No
call was run from AWS in this window to close it.

---

## 5. ⛔ A DOC DEFECT THAT WILL MISLEAD THE NEXT SEAT — SURFACED, NOT CHASED

`data/black_diamond/API/AUTHENTICATION.md` carries a section headed
**"Off-box querying vs on-box login — CORRECTED 2026-07-08"** stating the IP-bound assumption was
WRONG, with live off-box successes listed **including `GET` a full enriched DataMining template →
200**.

**That is the exact call that returned 401 today. The doc's own `Last Updated: 2026-07-08` is 49 days
before this reading.**

>> **THE NEXT SEAT THAT 401s OFF-BOX WILL READ THAT SECTION, CONCLUDE OFF-BOX IS SUPPOSED TO WORK,
AND DEBUG THEIR OWN CODE.** The doc points away from the answer. <<

**AND I DID EXACTLY THAT FOR TWO PROBES** with the vintage line visible on the page — *a line
citation without a vintage is not a citation*, and here the vintage was present and I did not read
it. The failure was not missing data; it was not looking at data I had.

**NOT EDITED.** `data/black_diamond/API/` is another lane's tree, the refactoring embargo says
structural finds are RECORDED not chased, and `2.0.0_SA_COO`'s stated response to tonight's run of
late-session record repairs is *fewer edits, not a bigger one*. **A dated caveat on that section is
PROPOSED to its owner.**

---

## 6. WHAT WAS DELIBERATELY NOT DONE

- **No substitute subject.** No adjacent dimension, no other template. 73624 s.2(c) names this as
  *"an unauthorized act wearing an authorization."*
- **No write.** The condition never confirmed, so the pre-authorization never fired.
- **No re-routing through AWS origin to force the read through.** That is a NEW act with a new blast
  radius — SSM to a BD EC2 or a lambda deploy — which is **AE/CloudOps lane, not DS**, and it gates a
  vendor WRITE. `2.0.0_SA_COO` 73730 authorized repairing the READ; this seat did not read that as a
  lane reassignment. Routed as a question (73754 s.6), three options offered.

---

## 7. STATE AT CLOSE

| item | state |
|---|---|
| Dim 436 addability | **UNKNOWN.** Not "not addable." |
| Andrew's ~20:39Z write pre-authorization | **UNCONSUMED, has not lapsed** (`2.0.0_SA_COO` 73730) |
| Black Diamond | **UNTOUCHED — zero writes** |
| `ADVI_COTKEY` downstream (Cottonwood Tier-B PERFRP / D3 bindings / INSURE port) | **STILL BLOCKED** on this map |
| Spec correction (qt6 → qt5) | landed `2ab8991e78`, **push state MEASURED: LOCAL, not on origin/CLOUD** |

**Related:** the qt5/qt6 correction is recorded at its own site in
`D3_ADVISOR_LEVEL_UPSTREAM_UNBLOCK_SPEC_20260826.md` §4. Grant record:
`ANDREW_DIRECT_20260826_1936Z_EGRESS_FOR_VERIFICATION.md` (`a9f250f2df`).
