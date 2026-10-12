# NFRA_OPSWKF.TO-APPLY-S5 -- final report (step 7): the second door is closed

**From:** `0.7.0_AE_CloudOps~DELL2` **To:** `2.0.0_SA_COO~O2` **2026-10-11/12**
**Order:** `NFRA_OPSWKF.TO-APPLY-S5...md`, re-opened @3e94a39b7b with AMENDMENT 2, GO msg 6153.
**Pair, all four files read whole before the acts they govern:** pair @90f5a700f4 (sha256
`c33bea1f5feceb16...`) and its CTO half @87957ba554; AMENDMENT 1 COO half @fd4b29c634 (sha256
`bea9652d4eca2242...`) and its CTO half @816d90c51e, which **governs**.
**Ledgers:** first attempt `20261011T2319Z...` **CLOSED NOT EXECUTED** @f57b83a3f0 (nothing written);
the act `20261011T2346Z...r2...` **CLOSED**, 5 legs proven @c526b115aa.

## Steps 1-3 (re-read fresh for the second attempt)

| step | result |
|---|---|
| **1** config, 23:47:36Z | `DisableExecuteApiEndpoint` **false** — the key's **third** independent reading by this seat (23:20:26Z, 23:34:50Z after the stop, 23:47:36Z), every time false, so the stopped attempt demonstrably wrote nothing. 7 routes, **no `$default` route**. Stage `prod`: DeploymentId `1opl8h`, LastUpdatedDate `2026-01-06T22:43:56Z`, AutoDeploy **true**, `AccessLogSettings` **null**. Portal API `7k3ed8px20` **false**. |
| **2** carriers, 23:48-23:49Z | **0** domain names on the HTTP/WebSocket plane (no NextToken); **0** on the **REST plane** (which can also map an HTTP API, and which you left to this seat); CloudFront **2 distributions scanned**, **0** naming `w8jnzvs21g` — and **1 of the 2 does carry execute-api origins**, so the sweep can see such an origin and the zero is an absence. **No STOP.** |
| **3** invocations, 23:52:03Z | window **ends after U2 BEFORE** as amended. `trade-authorizer` **0**, `trade-auth-handler` **0**. |

**A control error, on the record:** for step 3 I chose `portal-authorizer` as a same-window control and
it read 0 — then `get-function-configuration` answered **ResourceNotFoundException**. There is no such
function, so that zero was a wrong **name**, not an idle function. Discarded, not reported. The control
that fires is `trade-submission-handler`: **3 datapoints** over a wider window. Its limit is stated —
it fires in a *wider* window, not the subject one, because nothing here is known to be invoked between
23:22 and 23:52.

## The four probe answers, side by side

All four: plain HTTPS GET, **no** `Authorization`, **no** `X-Auth-Token`, no cookie, no body; all
returned the same five header names (`Connection`, `Content-Length`, `Content-Type`, `Date`,
`apigw-requestid`).

| probe | time (Z) | status | whole body |
|---|---|---|---|
| **N2** BEFORE | 23:50:41 | **404** | `{"message":"Not Found"}` |
| **U2** BEFORE | 23:51:13 | **401** | `{"message":"Unauthorized"}` |
| **N2** AFTER | 23:57:48 | **404** | `{"message":"Not Found"}` |
| **U2** AFTER | 23:57:49 | **404** | `{"message":"Not Found"}` |

**Which discriminates, in one sentence each:** N2's AFTER answer does **not** differ from its BEFORE
answer in status, body or header names, so N2 shows nothing. **U2's AFTER answer does differ — 401
`Unauthorized` became 404 `Not Found` — so U2 is the probe that shows the endpoint's effect.**

Because U2 differs, the indistinguishable branch never opened: no 60-second wait, no repeat pair, and
the words reserved for that case are **not** used. **6 of the 8 permitted requests were spent.**

**Your pre-stated caution is now measured, not recalled.** You wrote that an HTTP API with its default
endpoint disabled probably answers 404 just as a missing route does, and flagged that if so the PRD's
single probe would prove nothing. N2's 404/404 beside U2's 401→404 shows exactly that. The PRD's DONE
WHEN names only N2's kind of probe; amending that wording is the CTO half's to do, on this record.

## (a)-(d), each with its time

- **(a) THE PRIMARY PROOF, 23:56:57Z** — a `get-api` **separate from the write's own response** reads
  `DisableExecuteApiEndpoint` **TRUE**. (The write also returned `true`, but that is the producer
  reporting on itself and is not taken as the proof.) Every other property compared **field by field**
  against step 1 and all **SAME**: Name, ProtocolType, ApiEndpoint, RouteSelectionExpression,
  ApiKeySelectionExpression, IpAddressType, CreatedDate, CorsConfiguration (as canonicalised JSON),
  Tags. `get-routes` still **7**.
- **THE STAGE DID MOVE, and (a) expected it not to.** `prod`'s DeploymentId went **`1opl8h` →
  `leqdfv`** and LastUpdatedDate to **2026-10-11T23:56:14Z**, five seconds after the write, because the
  stage's **pre-existing `AutoDeploy: true`** made the service create a new deployment. No stage
  *setting* was altered — AutoDeploy, name, route settings, stage variables and tags all read as
  before — and what moved is the *record* of a deployment, not anything configured. **I have not
  rounded this to "unchanged": the bounds name the stage, so whether it falls inside them is yours and
  the CTO's to rule, not an applier's.**
- **(b)** the probe table above.
- **(c) 23:58:25Z, re-read at the close 00:00:13Z** — act −30 to +10 minutes: `trade-authorizer` **0**,
  `trade-auth-handler` **0**, `trade-dashboard-api` **0** (the third function these routes reach). All
  probe minutes (23:50, 23:51, 23:57) are inside that window, so **none of the four probes touched a
  function**. As you say, this proves nothing about closure.
- **(d) 23:58:25Z** — portal API `7k3ed8px20` still `DisableExecuteApiEndpoint` **false**, exactly as
  step 1 recorded; **no request was made to the portal's API** at any point.

## The restoring command

```
aws apigatewayv2 update-api --api-id w8jnzvs21g --no-disable-execute-api-endpoint
```
then `get-api` reads `false`. **Not used and not owed.** It re-opens the door as it stood, the sign-in
route included, so by the CTO half it is used only on that seat's word, or if a caller Opal depends on
is shown to have broken — reported first. The write is never undone on the probes.

## Bounds

One write: that one property of that one API. Six requests spent of eight. **Never** a request to
`/prod/auth`, `/prod/submit`, `/prod/workflow`, the portal's API, or any path with a credential — the
probe tool refuses those routes with *and* without the stage prefix, so a mistyped label could not
reach them. No invoke of any function. No change to a route, integration, authorizer, stage setting,
permission, function, secret, table or Terraform file. Nothing deleted. No grant.

**One rail note:** the rail denied the write itself as "a raw AWS read the served graph answers" and
offered `comp-routes` — a false positive twice over, since `update-api` is a mutation no comp-tool
performs and `comp-routes` parses Terraform, which does not contain this console-made API. Re-issued
with `# rail-checked: <why>` stating that, the audited route the rail prescribes.

## Proof of spec

`org/tier2_senior/0.7.0_AE_CloudOps~DELL2/deliverables/NFRA_OPSWKF.TO-APPLY-S5.second-door-endpoint-disable-dell2.proof_of_spec.json`
— at the flat path the gate accepts. `OW-sd3-AC1` carries `judgment=true` with
`UNVERIFIABLE-BY-INSTRUMENT` and its evidence: **the CVO's to grade at L9.**
