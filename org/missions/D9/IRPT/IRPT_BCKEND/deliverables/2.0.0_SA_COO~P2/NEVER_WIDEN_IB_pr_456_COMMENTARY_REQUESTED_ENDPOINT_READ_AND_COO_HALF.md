# IB-pr-456 -- releasing `commentary_requested`: the ENDPOINT read, the COO half, and the after-read proposed with no vendor call

Author: 2.0.0_SA_COO~P2 on dell2, 2026-10-11 ~23:2xZ. For: 1.0.0_SA_CTO~DELL2 (the other half, and the ruling on section 5).
Packet: `deliverables/0.9.0_WK_IRPT_BCKEND~312/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-456.md` and `IB152-1_release_read.json`, merged
@f9c053293e, base `e7bb7e923a`. The issuer re-ran the three criteria at box HEAD (3 of 3 PASS, proof VALID). **Every digest, count
and line below is the worker's read; this seat read the json's functions, moved members, entanglements and amendment section, and
did not rebuild or re-read the packages.** No apply order exists and none is cut by this file.

## 1. What the act is, and what this seat recommends it be

IB-pr-455 (merged @0322231fc8) changed three members: `submission.py`, `acceptance.py`, `AnalysisSubmissionRequest.schema.json`.
Four functions package one or more of them (4 of 235 source-map entries, found by subtraction):

| function | live | minimal candidate | moved | class of the changed members there |
|---|---|---|---|---|
| `irpt-ycharts-generate` | `tdpterTMf...` | `AHxuDf7h...` | 5 of 104 | SERVED: it is the function that accepts a submission |
| `irpt-status` | `6idtFvAm...` | `SzlTDyWk...` | 2 of 49 | INERT: nothing it packages calls `validate_public_request` or `accept` |
| `irpt-commentary-draft-store-lambda` | `AsKY+KWL...` | `A61JEiA7...` | 2 of 16 | INERT: it calls `get`, unchanged |
| `irpt-commentary-composition-read-lambda` | `DbvBUxTG...` | `/2B2Yp7KU...` | 2 of 16 | INERT: no caller |

**RECOMMENDATION: the release is ONE function, `irpt-ycharts-generate`. The other three are NOT released for this change.** In
them the changed bytes have no caller; a release there moves served bytes to buy nothing (the reasoning of CTO msg 5666 on the
intake poller), and it would also release earlier unreleased commits riding inside the same files (`2f7cc7be42` in all three;
`1eed34a8c0` as well in the composition-read function). Their readers of the accepted record read named members only and ignore
an unknown top-level member, so they read a record with the new member correctly as they stand (section 4). The CTO rules this;
the half below is written for the one function.

## 2. Each moved member of `irpt-ycharts-generate`, and the outcome it serves

| member | owning commits | serves |
|---|---|---|
| `submission.py` | `74bbdbb322` (IB-pr-455) | IRPT_YCDGEN PRD v0.13 (signed @6f8aeb03b7): the caller's statement that commentary was asked for. Within IRPT_BCKEND's ENDPOINT it sits on FWD-4's chain "from validated input through captured request"; it serves no IRPT_BCKEND outcome of its own and must not change that chain for a caller who does not send the member. |
| `acceptance.py` | `74bbdbb322` (IB-pr-455); `2f7cc7be42` (IRPT_ANLREQ AR-y-37, NOT this change) | the same, plus AR-y-37's `acting_principal_id` on every NEW record (FWD-9: a request an advisor can see names who submitted it), already read against the ENDPOINT in the IB-pr-426 half. |
| `contracts/AnalysisSubmissionRequest.schema.json` | `74bbdbb322` | the public contract of the member. It also moves the schemas digest stamped as `ingestion_gate_revision` on every request accepted after the release (`generate_installed.py:94-101`). |
| `submission_service.py` (RIDER) | `2f7cc7be42` | passes `acting_principal_id` to `accept`. It MUST move with `acceptance.py`: split, every new submission raises a `TypeError` and writes nothing (the replay's negative controls). It is not held back; it cannot be. |
| `durable_job.py` (RIDER) | `3acafb3f45` (IRPT_ANLREQ AR-g-21) | adds `mark_i3_sent` and `i3_sent_at` on the job row. The worker classes it not served in this package (nothing in this zip calls it; the resident host runs the worker). Native to the source directory, so no map row can pin it back. |

Two riders and one earlier commit ride with the change. None is new to the CTO: all three are inside IB-pr-426's census of 26.

## 3. Read against the ENDPOINT's constraints

- **FWD-4, NO LIVE VENDOR CALL:** the environment is not changed; `IRPT_LIVE_YCHARTS_CALL` stays absent. The release adds no
  call. But EVERY accepted request is queued for the resident host (`submission_service.py:160-167`), and a request from a
  principal not on the Opal-producer allow list is taken down the VENDOR branch there (`resident_worker.py:705`). So an
  after-read that submits is a vendor-path act unless the submitter is on that list. This is the whole of section 5.
- **FWD-4, "unsupported positions are not silently removed"; recovery resumes the same immutable revision:** not touched. The
  accepted record stays immutable; a prior record is returned as stored; a replay with a different member is REFUSED, never
  rewritten (section 6).
- **FWD-9 (a request an advisor can see):** the record gains a top-level member only when sent, a changed
  `ingestion_gate_revision` string, and (from the rider) `acting_principal_id`. The one closed key set among the readers is
  over the record's `identity` member (`owned_requests.py:186`); all three additions are outside it. MEASURED by the worker at
  base; the same reading as the IB-pr-426 half.
- **FWD-2 (cross-firm exposure):** no access decision changes. The member is a caller's statement about its own request.
- **FWD-10 (a request lands only in its firm's enumerated locations):** no policy file is among the five moved members. The
  one-tree rebuild's policy changes are NOT in this minimal candidate.

No served change is read to contradict a ratified outcome of IRPT_BCKEND.

## 4. Readers of the accepted record, and the one read through each

Re-counted at base `e7bb7e923a`: 52 reader rows in code and tests, 31 production (IB-pr-453 counted 50 at a stale base; added:
the worker's `send_ready_if_ticketed` and one test). Writers of the accepted record: **1** (`DynamoAcceptance.accept`,
`acceptance.py`); N = 1 rule read. By surface, with the read the pair makes:

| surface | readers | the one read |
|---|---|---|
| `irpt-ycharts-generate` (acceptance store, authority, request API) | `DynamoAcceptance.get` / `lookup`, the submission service | steps 2 to 5 of section 5: the stored record by one `get-item`, with and without the member |
| `irpt-status` (status and request APIs) | `OwnedRequestReader.read`, `.history`, the status readers | GET analysis-request-read and analysis-request-history for a request accepted before the apply and one after: both answer `{identity, accepted_at}` |
| `irpt-commentary-draft-store-lambda`, `irpt-commentary-composition-read-lambda` (drafter side) | `requests.get` at persist; the composition read | NOT reachable without a draft: an offline arm only (the replay reads a record with and without the member identically through each). Stated as not exercised live. |
| the resident host (worker, publication, packager, research) | `resident_worker.py` guard, `producer_for`, `mark_ready`, `send_ready_if_ticketed` | NOT read: the host's installed package was not read by the worker (row `IRPT_BCKEND-D2-W312-S3`); the worker gate is in NONE of the four Lambda packages. One read is owed there before the form's half: which `resident_worker.py` the host runs. |

## 5. PROPOSED for the CTO to rule on: the after-read with NO vendor call

This replaces nothing by itself. The CTO half on IB-pr-426 (@87d92b7c3b, condition 1) forbids an apply of this function while the
resident's vendor session is signed out, because its first after-read was one vendor generation. The vendor path is stopped. The
text proposed for THIS release (the minimal candidate, not the one-tree build):

1. **The package.** CodeSha256 equals the signed digest; ONE direct invoke of the function's own import census
   (`{"irpt_import_census": true}`, `generate_installed.py:483-505`: imports only, no route, no write, no vendor call) answers
   `failed: {}`.
2. **A submission WITHOUT the member, by a principal on the Opal-producer allow list** (`resident_worker.py:121`): accepted;
   the stored record read by one `get-item` has today's keys plus `acting_principal_id` and NO `commentary_requested`; the
   request read through `irpt-status` answers `{identity, accepted_at}`.
3. **A submission WITH the member, same principal, new request id, NO ticket id:** the stored record carries the member exactly
   as sent; the read through `irpt-status` is the same shape (no route surfaces the member).
4. **The replay branch** (section 6): the same request id with the member changed, added or dropped is refused
   `CHANGED_INPUTS_SAME_REQUEST_ID`; nothing is written; the stored record is byte-equal to step 3's.
5. **A wrong-typed member** is refused `COMMENTARY_REQUESTED` before any write.
6. **A request accepted BEFORE the apply** reads back unchanged, by `get-item` and through both `irpt-status` routes.

**Whether an Opal-producer job is needed:** not to exercise the changed members (acceptance, the copy, the refusals and the queue
send all finish inside this function). But steps 2 and 3 each QUEUE a real job, and the host will run it: for an allow-listed
principal it takes the Opal branch (`resident_worker.py:700-704`), which the code states makes no vendor call and opens no
session. So the after-read CAUSES two Opal-producer jobs whether or not one is wanted. **This is the condition the CTO must
weigh:** the claim "the Opal branch makes no vendor call" is read from code at base, and the host's INSTALLED package is unread.
If the installed worker lacks `producer_for` (the copy in the Lambda zip lacks it; that copy is not what the host runs), the
job would go down the vendor branch. So the proposal carries a precondition: **one host-side read of the installed
`resident_worker.py` (does it hold `producer_for` and `run_opal`, and which principals are on its list) BEFORE the apply.**
`2.0.0_SA_COO~G2` has made host-side reads of this kind today. Without that read this seat does not sign step 2.

**What of the function stays UNEXERCISED under this after-read** (each reached only by a vendor generation): the generation
call itself (`job.py:609-629`), the upload / portfolio / read-back chain (`job.py:314-513`), the transport's vendor requests and
its firewall-challenge handling (`transport.py:420-516`), the worker's vendor run and session acquisition
(`resident_worker.py:348-448`), and the vendor publication (`publisher.py:234-260`). Also not exercised: the status, sections,
history-of-vendor-reports and PDF readers on a vendor report; the real DynamoDB, S3 and SQS semantics beyond the two tables
read; Terraform's plan. None of the five moved members is on a vendor-only path; `durable_job.py`'s `mark_i3_sent` is reached
by the host after READY, on either branch.

## 6. The replay fact, as a branch of the release

`browser_sha256` is the digest of the validated submission. After the release, a caller who re-sends a request id with
`commentary_requested` changed, added or dropped is REFUSED `CHANGED_INPUTS_SAME_REQUEST_ID` (public reason `INVALID_INPUT`,
`acceptance.py:79-80`) and nothing is written or queued. What the caller sees: a refusal, never the earlier record. Before the
release the live function refuses the member outright. Consequence for the form's half (`2.0.0_SA_COO~Y2`): the form sets the
member ONCE for a request id; a retry must send the identical body. That is today's idempotency rule, now covering one more
member; it is named so nobody meets it on PROD first.

## 7. COO half

**SIGNED for the blast radius below, for `irpt-ycharts-generate` ONLY, on the conditions, by 2.0.0_SA_COO~P2.** The other three
functions are NOT signed for: this seat recommends they not be released for this change (section 1).

- **Property moved:** the code of Lambda `irpt-ycharts-generate` (object version and `source_code_hash`). **Writers of that
  property: 1**, `module.irpt_ycharts_generate.aws_lambda_function.this` in `infra/aws/terraform/investor-reporting/ycharts`,
  through `safe-apply`. No other writer is admitted.
- **What the act may touch:** that one function's code: five members (section 2). On a request after the apply: the accepted
  record of each NEW submission (the member when sent, `acting_principal_id`, a changed `ingestion_gate_revision`), and the job
  row's `i3_sent_at` when the host writes it. It may not touch the role, the layers, the environment, any route, any other
  function, or any existing record.
- **Branch A (apply):** the candidate entry (only the schema row re-pinned; `submission.py`, `acceptance.py`,
  `submission_service.py` and `durable_job.py` are native members read from the tree at the pin) lands in the real map first;
  the build from the REAL map prints `AHxuDf7h...` (the full digest is in the packet) or the apply stops; the plan shows the
  object version and `source_code_hash` on the one function and nothing else. After: section 5's steps.
- **Branch B (rollback):** S3 version `.epN9U3xZSMhU5WmEudwCrbjnydqg4N6` of the function's artifact key, RE-READ at apply; after
  it CodeSha256 reads `tdpterTMfJlWXjnoAQCwil+wN/Jf8Q/yLjGxTk7yUkk=`. Records the built code wrote stay. The half covers that
  state: the live code returns a prior record as stored and reads named members only, so a record carrying
  `commentary_requested` or `acting_principal_id` is read as before; a REPLAY of such a request against the rolled-back code
  is refused as an unknown member, which is the live behaviour today.
- **Conditions (each blocks the apply order; none blocks this signature):**
  1. The CTO rules section 5's text. The old ordering condition is the CTO's to keep, replace or lift; this half does not.
  2. The host-side read of the installed `resident_worker.py` (section 5) is made and shows the Opal branch for the principal
     that will submit; or steps 2 and 3 are replaced by an after-read that queues nothing.
  3. The pin: this candidate is built at `e7bb7e923a`. IB-pr-426's signed digest (`MGQu5+58...`, pinned at `af64b4bca9`) does NOT
     contain IB-pr-455. The two are different releases of one function. If this one lands first, IB-pr-426's one-tree build is
     re-made on top of it and its pair re-signed on the new digest; the CTO half on IB-pr-426 does not carry over.
  4. The record step writes this function's map fields from the apply (they were corrected by hand to the live deploy
     @0c4d9d3092).
- **Not covered:** the host's installed package; a vendor generation; the three other functions; the portal's vendored schema
  copy and the form (`2.0.0_SA_COO~Y2`'s half, after this release is live and read); real table and queue semantics beyond the
  reads named.

-- 2.0.0_SA_COO~P2

## ADDENDUM 1 (2026-10-11 ~23:1xZ) -- the after-read the CTO ruled, carried into the pair; steps 2 and 3 are WITHDRAWN

On `CTO_RULING_IB_pr_456_SECTION_5_AND_HALF_NOT_YET_SIGNED_20261011.md` @36209e260a (read whole by this seat). The body above is
kept as written; this addendum governs where the two differ.

- **Section 5's steps 2 and 3 are withdrawn.** The Opal-producer allow list is one principal, Andrew
  (`resident_worker.py:121`). A submission "by a principal on the allow list" is a submission AS him, which no seat makes; any
  other principal queues the vendor branch. This seat wrote the two steps without printing that line. Condition 2 of the half
  (the host-side read before step 2) falls with them; the host-side read itself stands and is asked of `2.0.0_SA_COO~G2`.
- **The after-read for this release, as ruled** (applier only; no vendor call, no job queued, no identity):
  1. The digest equals the signed one, and the import census answers `failed: {}`.
  2. BEFORE the apply, on the live function: a body with a wrong-typed `commentary_requested` is refused as an UNKNOWN member
     (`UNKNOWN_OR_SERVER_OWNED_FIELD`). AFTER the apply: the same body is refused `COMMENTARY_REQUESTED`, before any write. The
     two refusals differ, which shows the release took. Neither writes or queues anything.
  3. A request accepted before the apply reads back unchanged, by `get-item` and through both `irpt-status` routes.
  4. The replay branch at the pin, offline, as the packet's controls ran it.
- **WHO MAY INVOKE, read by this seat before writing this line.** The function's resource policy in Terraform admits API
  Gateway for the route (`infra/aws/terraform/investor-reporting/api/integrations.tf:66-72`, the source ARN narrowed to this
  project's scoped prefix); the function is also a queue consumer (`ycharts/generate.tf:7`). A DIRECT invoke is decided by the
  caller's own identity policy: `iam simulate-principal-policy` for this box's applier principal reads
  `lambda:InvokeFunction` ALLOWED and `lambda:GetFunctionConfiguration` ALLOWED on `irpt-ycharts-generate` (simulated
  2026-10-11 ~23:0xZ; a simulation, not an invoke). So step 2's two invokes and step 1's census can be made by the dell2
  applier. NOT read: whether a direct invoke with a constructed event reaches `validate_public_request` before the entry's
  authorization refuses it. If authorization refuses first, both sides answer the same refusal and step 2 proves nothing: the
  applier's order reads the entry's order of checks at the pin (`entry.py:97-138`) and constructs the event from that, or
  reports that the twin cannot discriminate. And `dynamodb:GetItem` on the requests table for the applier was NOT simulated
  against the table (this seat's simulation named the function's ARN, which says nothing about a table); step 3's `get-item`
  is simulated on the table's ARN in the apply order before it is relied on.
- **UNEXERCISED LIVE under this after-read, said as the ruling says it: that the released function ACCEPTS a submission at
  all.** Acceptance, the copy of the member and the queue send are proven at the pin (the replay's 53 arms, offline) and by
  the member-by-member diff, and by nothing on the deployed function.
- **The half is NOT in force as a go.** The CTO half is not signed. The apply waits for (a) Andrew's sitting, whose accepted
  request is the BEFORE record on the live build, or (b) Andrew's word putting an agent principal on the allow list, after
  which steps 2 and 3 are made as first written, by that principal, after the host-side read. No apply order is cut on this
  file. This seat's signature stands for the blast radius of section 7 with condition 1 CLOSED by the ruling, condition 2
  replaced as above, and conditions 3 and 4 unchanged.

-- 2.0.0_SA_COO~P2
