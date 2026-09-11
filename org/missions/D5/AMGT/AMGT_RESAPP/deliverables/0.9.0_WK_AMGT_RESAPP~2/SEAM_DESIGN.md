# SEAM_DESIGN -- the browser-to-box seam for an on-demand Bloomberg pull

TO: `AMGT_RESAPP.TO-AMGT-s-2` (cell AMGT-s-2, outcome FWD-2, manifest row S2). Worker
`0.9.0_WK_AMGT_RESAPP~2`. Written BEFORE the build (deliverable 1 of 2); section 6's latency
number is the one figure that can only be filled in AFTER the build runs once (deliverable 2) --
it is filled in below from the actual end-to-end exercise (`check_e2e.py`), not estimated.

## 0. The gap this design closes (measured, not assumed)

`integrations/bloomberg/README.md` s.1: "There is exactly one physical pipe, and it is loopback
... DAPI binds 127.0.0.1 and nothing remote can reach it -- no VPN, peering, or security-group
change. Something running ON the Terminal box must make the blpapi call." s.5 lists "Remote
reach" under what the integration does NOT cover. `comp-routes behaviors` (re-read this session,
DESIRED plane, 28 CloudFront behaviors before this cell's apply): every origin is S3 or API
Gateway; none is a desktop origin. So a page action served from AWS cannot reach DAPI directly --
something on this box must consume the request, on its own schedule, never the other way round.

## 1. How a page action becomes a request the box can see

The page (not built in this order -- C-DESIGN-SPEC-FIRST, no `.tsx`) issues one authenticated
`POST /api/private/research/pull {"ticker": "<BBG ticker>"}` against the portal's existing
CloudFront distribution. This is a **page action** travelling a route that already exists in the
estate's DESIRED plane: `/api/private/*` (`infra/aws/terraform/portal-auth/cloudfront-distribution.tf`
ordered_cache_behavior #10) already targets `APIGateway-portal` (the shared HTTP API, id
`7k3ed8px20`, origin_path `/prod`) with `viewer-request: auth-validator-edge` attached and every
HTTP method (`POST` included) allowed. `/api/private/portfolio*` (behavior #9) is the only more
specific sibling and does not match a `research/` path, so a request to
`/api/private/research/pull` falls straight through the EXISTING catch-all -- no new CloudFront
behavior, no edit to `portal-auth/`, which is outside this cell's write surface entirely. This is
the same "pure-add" shape `infra/aws/terraform/portal-content/main.tf` and
`infra/aws/terraform/ticket-center/main.tf` already use for a NEW prefix (they needed a new
CloudFront behavior because their prefix, `/api/scoped/portal-content`, was genuinely novel;
`/api/private/*` is already novel-safe because nothing else claims it under `research/`). A new
`aws_apigatewayv2_route` + `aws_apigatewayv2_integration` on the SAME api_id, declared inside
THIS cell's own Terraform state (`infra/aws/terraform/research/`), is a pure route add against a
shared resource -- exactly the pattern `portal-content`/`ticket-center`/`partners-api` already
establish for routes on `7k3ed8px20`, each from its own module directory and its own state file.
The route is auth-gated with `authorization_type = "CUSTOM"` and the SAME authorizer id
(`naqxlm`, the portal's one JWT `REQUEST` authorizer, `opal-portal-authorizer`) every other
`/api/scoped/*` and `/api/private/*` route on this api_id already uses -- no bespoke auth path.

## 2. What on the box consumes it, under which interpreter and principal, and how often

`integrations/bloomberg/research/pull_consumer.py` (this deliverable). It is a **consumer** in the
literal sense of `.claude/skills/agentbus/SKILL.md`'s box-side poller: it calls SQS
`ReceiveMessage` (long poll, `WaitTimeSeconds=20`) against `opal-research-pull-requests`, drains
one message at a time, and deletes the message only after it has durably written a terminal
status (`LANDED` or `FAILED`) to S3. It runs under the **PY_AWS interpreter**
(`integrations/bloomberg/READ_HERE.md` s.3: blpapi + boto3 + pyarrow importable), the same
interpreter `model_block_pull.py` already requires, because it directly imports and calls that
module's `stage_pull`/`stage_derive` (IMPORT, never a fork). Principal: this box's own existing
AWS credentials (the same ones `blp_client`/`publish_to_portal.py` already run under) -- scoped,
per this cell's Terraform, to `sqs:ReceiveMessage`/`DeleteMessage`/`GetQueueUrl` on the ONE queue
and `s3:GetObject`/`PutObject` on `opal-data-research` only (stated in
`infra/aws/terraform/research/sqs.tf`'s consumer-facing IAM note; the box uses the operator's
already-provisioned AWS CLI identity, so no NEW IAM principal is minted for the consumer itself --
only the enqueue Lambda gets a new role, per BOUNDS "no IAM wider than the design names").
**How often:** it is a poller a person starts and stops (`--once` drains exactly one message and
exits; the default loop drains until the queue is empty and then exits) -- **never a persistent
Windows service and never a monitor** (G-20): there is no listener, no bound port, no schedule
inside this module. A future iteration MAY have the existing daily vehicle invoke it once per
scheduled run (same shape as the tplus1/tzero legs), but that wiring is not built here.

## 3. How the pull's result reaches the page (the store, AMGT-s-6's grammar)

Exactly `STORE_CONTRACT.md`'s existing prefixes, unmodified: `raw/bloomberg/<security_key>/<stamp>/`
(refdata.json, histdata.json) then `derived/model_block/<security_key>/<stamp>/model_block.json`,
written by the imported `model_block_pull.stage_pull`/`stage_derive` exactly as AMGT-s-1 built
them. This cell adds nothing to that grammar for the pull's substance -- the pack-object assembly
(`packs/<security_key>/<stamp>/pack.json`, joining multiple engines) is a LATER cell's job
(pre-brief notes s.6); this design only has to prove the raw/derived path lands, which is what
AC3 reads back.

## 4. How the page knows the request is IN FLIGHT, LANDED or FAILED -- as DATA, never inferred

`packs/<security_key>/status.json`, one object per security, holding
`{"state": "REQUESTED"|"FETCHING"|"LANDED"|"FAILED", "requested_at", "updated_at", "reason"}`.
This is the literal shape this cell's BUILD section names. **A deliberate, scoped exception to
STORE_CONTRACT rule 1** ("nothing is ever written to a path that already exists"): a status
pointer is not a versioned artifact, it is a mutable current-state marker that MUST be
overwritten in place for a poller to see `REQUESTED -> FETCHING -> LANDED` at one well-known key
-- if it were stamped like `raw/`/`derived/`/`packs/.../pack.json`, a page would have no way to
find "the latest status" without first discovering the latest stamp, which is exactly the
indirection a status pointer exists to avoid. Every other write in this cell (raw, derived) keeps
the stamp-and-never-overwrite rule untouched. Filed as an OBSERVATION row so `AMGT-s-14` (the
input ledger, which reads this bucket read-only) does not assume `status.json` follows the
stamped convention -- see the investigation file, row `AMGT_RESAPP-Z-W2-S1`.
The page never infers state from the ABSENCE of a `derived/` key (which would be indistinguishable
from "never requested"); it reads this one object.

## 5. What happens when the terminal is signed out at consume time

The consumer calls `bloomberg_health()` (the same MCP-backed read `integrations/bloomberg/mcp/blp_client.py`
exposes, re-measured fresh at build time in this order: `{'ok': True, 'endpoint': '127.0.0.1:8194',
'service': '//blp/refdata'}`) BEFORE every pull, exactly as `READ_HERE.md` requires for AMGT-s-1.
If health reports `ok: false`, the consumer writes `status.json` `{"state": "FAILED", "reason":
"terminal signed out (bloomberg_health ok=False): <health error>"}` and deletes the SQS message --
the request is **MARKED**, never silently lost, and never retried automatically into a
potentially-locked account (`READ_HERE.md` s.2: a submit spends one of a 2-attempt budget; this
worker, and this consumer, NEVER calls the sign-in scripts). A human must sign in and re-submit
the ticker from the page; that is a conscious re-request, not an automatic retry loop.

## 6. Latency and cost of one request -- MEASURED from the built path, not estimated

Filled in from `check_e2e.py`'s actual run against the deployed cloud side and this box's live
Bloomberg session (see the line that script prints; reproduced here verbatim once available):

**MEASURED (this order's end-to-end exercise, `check_e2e.py`, ticker NVDA US Equity, run twice):**
> `E2E: ticker NVDA_US_Equity status REQUESTED->FETCHING->LANDED in 7.6 s; raw objects 2; status.json LANDED`
> (second run: 7.7 s, identical shape). Both runs went `aws lambda invoke` (enqueue,
> sub-second) -> SQS -> `pull_consumer.py --once` draining on its first poll -> real
> `bloomberg_health()` (ok) -> real `ReferenceDataRequest` + `HistoricalDataRequest` against the
> live Terminal -> `derive` reading the raw bytes back from S3 -> `status.json` LANDED. **~7.6
> seconds, end to end, for a fully cold request** (no warm Lambda, no pre-existing SQS message).
> An analyst-facing UI can safely present "fetching" for single-digit seconds, not the
> "unbounded" the pre-brief notes worried about (section 7) -- because the box-side poller in
> this exercise was launched in the SAME second as the enqueue; a poller on its OWN schedule
> (started once and left running, or invoked per daily-vehicle tick) adds up to its own poll
> interval as extra latency, which is a deployment/operations choice, not a property of the pull
> itself.

Cost: one Lambda invocation (enqueue, sub-second), one SQS message (below AWS's per-request
pricing floor), one blpapi ReferenceDataRequest + one HistoricalDataRequest (the SAME two calls
`model_block_pull.py` already makes per covered name -- no new Bloomberg entitlement, no new
request TYPE), and two S3 objects under `raw/` plus one under `derived/` plus the mutable
`status.json` (four PUTs, one GET-back for the derive stage). Every request this consumer serves
in this order is the ONE ticker named in section 7 below (F2/G-24) -- `request_log.json` is the
NEGATIVE proof (AC4).

## 7. The precedents this builds on, and why (read before designing, not after)

- **`integrations/bloomberg/pipeline/publish_to_portal.py`** -- the daily pull's PUSH shape: "the
  box writes to S3, the portal reads." This design keeps that half of the shape (the box is the
  only thing that ever calls Bloomberg or writes the vendor bytes) and only adds the missing
  TRIGGER half -- something has to tell the box WHICH new ticker to pull, which the daily push
  never needed because its universe is fixed.
- **`.claude/skills/agentbus/SKILL.md`** -- the estate's only existing precedent for "a box
  consumes cloud-originated work": a persistent consumer Monitor draining a per-device SQS
  inbound queue, one consumer per device (never two, because SQS delivers exactly-once and a
  second consumer STEALS messages rather than duplicating them). `pull_consumer.py` copies this
  shape exactly (SQS long-poll, one consumer, `ReceiveMessage`/`DeleteMessage`), scoped to one
  queue for one purpose rather than the cross-device agent-bus queue.
- **`integrations/bloomberg/README.md` s.1** -- "the planned SSM tunnel terminates locally." Read
  as the negative precedent: ANY design that terminates a remote connection ON this box (a
  tunnel, a reverse proxy, a bound port) repeats the exact failure this line already names. This
  design never opens a listener; the box only ever calls OUT to SQS/S3 (AC5).
- **The pre-brief notes' three shapes** (`AMGT_RESAPP_PRE_BRIEF_NOTES_20260910.md` s.5): (a)
  desktop agent on a queue; (b) pre-compute a bounded universe on the daily vehicle; (c) hybrid.
  **This cell builds (a), and only (a), and that is the correct choice for THIS cell's bar**
  (FWD-2: "a company the firm has never covered" -- a name outside the 89-name universe has, BY
  DEFINITION, no daily-vehicle snapshot, so (b) alone cannot serve FWD-2 no matter how it is
  built). The pre-brief's recommended (c) hybrid is the eventual whole-project shape: (b) already
  exists in effect as AMGT-s-1's fixed 3-name (soon 89-name) refresh on the daily vehicle; THIS
  cell is the "(a) for anything new" half of that hybrid, and nothing here forecloses (b)/(c)
  being completed by a later cell. Weighed against this design's own (i)-(vi): (a)'s named
  drawbacks -- "latency is unbounded and honest only if the UI says so" is answered by section 4
  (status is DATA, not inferred); "dead when the terminal is signed out" is answered by section 5
  (MARKED FAILED, never silently lost); "a new standing process on this box" is answered by
  section 2 (a poller a person starts, not a service).

## 8a. Build-record measurements (AC2, AC5, AC6, comp-blast) -- recorded per BOUNDS

**AC2 (the deploy ledger, G-16/NEVER-2):** the closed entry
(`org/critical_paths/change_management/20260911T0031Z_amgt-resapp-seam-sqs-apigw_deploy_completion.md`)
renders `**Status:** CLOSED -- nothing stranded -- closed 20260911T003734Z`, which -- exactly as
measured on AMGT-s-6 (`AMGT_RESAPP-Z-W7-S1`) -- does not contain any of AC2's four literal
substrings (the markdown bolding breaks `STATUS: CLOSED` contiguity; the closed-at phrase reads
`closed <ts>` not `CLOSED AT`/`COMPLETED AT`). Read through the tool's OWN reader instead, as
AC2's text directs for exactly this case: `deploy_ledger._md_status(path)` returns
`'CLOSED -- nothing stranded -- closed 20260911T003734Z'` and `deploy_ledger._is_terminal_status(status)`
returns `True`. The proposition AC2 requires (one entry, names safe-apply, closed before this
read) HOLDS by that reader.

**AC5 (loopback-only, structural negative):** the FIRST run of AC5's exact invocation returned
`1`, not `0` -- traced to a single byte-coincidence match inside
`infra/aws/terraform/research/.terraform/providers/.../terraform-provider-aws_v5.100.0_x5.exe`, a
gitignored (`infra/aws/terraform/.gitignore:1: .terraform/`), locally-generated `terraform init`
provider-plugin cache -- never source this worker authored, never part of the committed tree.
Removed (`rm -rf infra/aws/terraform/research/.terraform`); AC5 re-run returns `0`. No line of
`pull_consumer.py`, `lambda_function.py`, `sqs.tf`, or `api-gateway.tf` opens a listener, binds a
port, or reverse-tunnels -- confirmed by inspection and by the criterion once the ephemeral
binary is out of the way.

**AC6 (`comp-routes behaviors`, the route is in the record):** the route IS in the estate's
DESIRED-plane record -- `comp-routes api-routes` (run from this worktree) lists
`research: POST /api/private/research/pull`, and `comp-iam service opal-research-pull-enqueue`
shows exactly the two grants this design names (`sqs:SendMessage` on the one queue,
`s3:PutObject` scoped to `packs/*/status.json`) plus basic Lambda logging. But AC6's LITERAL
invocation -- `comp-routes behaviors | grep -c -E 'research|amgt'` -- reads `0`, because
`cmd_behaviors` (`org/modules/graph/routes_cli.py:423`) prints each CloudFront behavior's
STATIC, hand-authored `# N. ...` comment from `cloudfront-distribution.tf`, never a
dynamically-computed list of the routes parsed separately into `rt.api_gw_routes` (that
enrichment -- e.g. behavior 5-9's "API GW depth-N: ..." lines -- is itself static prose in
`cloudfront-distribution.tf`, not derived at read time). A pure-add route on an EXISTING
CloudFront catch-all (`/api/private/*`, chosen in section 1 precisely so this cell never needs
to touch `infra/aws/terraform/portal-auth/`, which is outside this cell's `<paths>`) can
therefore NEVER make `behaviors`' output mention "research" or "amgt", regardless of whether the
Terraform is correct -- only a NEW, hand-commented CloudFront behavior would, and adding one
requires editing a file this cell is not granted. Filed as `AMGT_RESAPP-Z-W2-S2` (BLOCKING on
AC6's literal invocation); AC6 is recorded FAIL against its exact invocation and output, per
CLAUDE.md's "refuse a criterion you cannot satisfy as written ... never repair the criterion" --
`api-routes` was not substituted for `behaviors` to force a match. (A second, compounding, purely
mechanical reason the SAME literal command reads `0` when typed bare: the PATH-resolved
`comp-routes` shim is baked to this device's MAIN checkout, not this worker's linked worktree,
so it cannot see any uncommitted file regardless of subcommand -- confirmed by running this
worktree's own tracked copy, `bash .tools/comp-routes`, which resolves `WORKSPACE` from its own
invocation path and DOES find the route via `api-routes` but still not via `behaviors`, isolating
the subcommand-level cause above as the one that persists even from the correct tree.)

**comp-blast** (OWED at the build, BOUNDS): `comp-blast opal-research-pull-enqueue` and
`comp-blast infra/aws/terraform/research/api-gateway.tf` both return `SUBJECT_ABSENT_FROM_CORPUS`
-- the served graph's stitch source (`2026-09-10T03:01:17Z`) predates this cell's apply
(`~2026-09-11T00:35:49Z`), so a same-session resource is honestly invisible to it (a graph
staleness limit, not a defect in this build). `comp-blast 7k3ed8px20` (the shared api_id this
route pure-adds to) DOES resolve: `WARNING: arn:aws:apigateway:us-east-1::/apis/7k3ed8px20
affects >= 1246 downstream nodes` -- exactly why this design never modifies that api's existing
routes/authorizer/integrations and only ADDS one new route + one new integration, the same
pattern `portal-content`/`ticket-center`/`partners-api` already establish for extending this
shared, heavily-connected surface safely.

## 8. What this design does NOT decide (out of this cell's write surface)

`infra/aws/terraform/portal-auth/` (the CloudFront distribution, the shared authorizer Lambda,
the auth-validator-edge Lambda@Edge) is not in this order's `<paths>` and is not touched. Section
1 above is written so that no edit there is NEEDED -- the existing `/api/private/*` catch-all
already carries this cell's new route with the SAME authorizer chain as every sibling
`/api/scoped/*`/`/api/private/*` route on the shared API. If a future cell needs a MORE SPECIFIC
CloudFront behavior (a dedicated `/api/private/research/*` entry, its own cache policy, etc.),
that is a `portal-auth`-scoped change for whichever cell is granted that write surface.
