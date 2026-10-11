# IB-pr-426 -- irpt-ycharts-generate rebuilt from one tree: the ENDPOINT read, then the COO half

Author: 2.0.0_SA_COO~P2, 2026-10-11 ~12:4xZ. Bound to the packet
`org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~285/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-426.md`, git blob
`1bc16f0089753632b1ede4629b93caa3ff228fe7` (drained @a0d48cb33c). Nothing is applied. No apply order is cut by this file.

Rule applied (CTO msg 4657): before a half is written, the project's ENDPOINT is read against every served change and each
change is given the ratified outcome it serves. ENDPOINT read: `org/missions/D9/IRPT/IRPT_BCKEND/prd/IRPT_BCKEND_PRD.md` lines
18-126 at box HEAD, plus the headings of ADDENDA v0.18 to v0.34. The outcome headlines of IRPT_ANLREQ and IRPT_YCDGEN were read
(their PRDs' FWD lines only); their full ENDPOINT text was NOT read by this seat.

## 1. What the act is

The function's code moves from live `tdpterTMfJlWXjnoAQCwil+wN/Jf8Q/yLjGxTk7yUkk=` to built
`MGQu5+58WxJ3pybmZx8cFdJ9nypEPvPGo66cCyiB1ts=` (pin `af64b4bca9`). 104 members both sides; 26 differ; 24 are classed served,
2 inert. Role, layers, environment names, handler, routes and event sources do not change (packet, section "Role, routes").
The function has 0 event source mappings and its handler does not run the resident loop.

## 2. Each served member, the outcome it serves, and where the same bytes are already recorded as released

"Sibling" = another function whose source-map row stages the same repo path at a pin whose blob equals the blob at
`af64b4bca9` (read by this seat from `infra/aws/lambda/ci/lambda-source-map.json`, 456 staged rows). The map is a RECORD, not
the live bytes: it is one release behind for this very function, so a sibling reading is `inferred`, except
irpt-performance-adapter and irpt-narrative, whose map builds reproduce live (CTO msg 4839).

| member | serves | commit's project | sibling at the new bytes | reach in THIS function |
|---|---|---|---|---|
| `acceptance.py` + `submission_service.py` | IRPT_BCKEND FWD-9 (a request attributed to the right advisor); IRPT_ANLREQ FWD-1 | IRPT_ANLREQ AR-y-37 | none: FIRST SERVED HERE | every new submission; the pair moves together |
| `contracts/ExportReceipt.schema.json` | ADDENDUM v0.30 (FWD-2: a read fails closed without the account list) | IRPT_BCKEND IB-pr-343 | none | digest only (`ingestion_revision`) |
| `contracts/HoldingsSnapshot.schema.json` | FWD-14 ACCEPT ("any multi_asset" is WORSE) and FWD-5 | MDPF_SECCLASS port | none | digest only |
| `contracts/OwnedAnalysisRequest.schema.json` | FWD-9 / ADDENDUM v0.29 (persist_inputs) | IRPT_BCKEND IB-pr-407, 411 | none | digest only |
| `contracts/AnalysisReport.schema.json`, `contracts/OwnedAnalysisRequestHistory.schema.json` | IRPT_ANLREQ FWD-1; IRPT_BCKEND FWD-9 (the request an advisor can see) | IRPT_ANLREQ AR-y-32 | none | digest only |
| `_ids/ids.py` + `data/custodian_key_seam.json` | FWD-2 and FWD-1 (the id an account is shown under) | IRPT_BCKEND IB-pr-339, 348 | adapter, narrative, status | the id projection on a request |
| `_authz/loaders.py` | FWD-7 (a failed refresh reads differently from a completed one: NOT_READY) | IRPT_BCKEND IB-pr-327 | none | the directory pointer read on a request |
| `_authz/served.py` | ADDENDUM v0.29 (the custody report) under FWD-2 | IRPT_BCKEND IB-pr-405 | adapter, narrative, status | the svc-custody-statement subject passes the gate and is answered UNSUPPORTED_OPERATION |
| `reports/repository.py`, `reports/retention.py` | FWD-2 (who may read a retained artifact); IRPT_ANLREQ FWD-3, FWD-5 | IB-pr-386; IRPT_ANLREQ AR-t-12 | adapter, status | no route of this function reaches them (packet) |
| `ops/owned_requests.py` | FWD-9; IRPT_ANLREQ FWD-1 | IRPT_ANLREQ AR-y-32; `~Y` S326 | none (irpt-status is older) | no route of this function reaches it; the history route is irpt-status's |
| `durable_job.py`, `resident_worker.py`, `resident_main.py` | FWD-4 / ADDENDUM v0.28 (the Opal-producer form); IRPT_ANLREQ FWD-1, FWD-4; IRPT_YCDGEN FWD-11 | IRPT_ANLREQ AR-g-13, AR-g-21 and others | durable_job: status; the other two: none | NOT run by the Lambda: `install-resident.sh` runs the resident from a package root with a SHA256SUMS file on its host (lines 8-57), and the handler does not start the loop. Inferred, not exercised |
| `infra/logic/registry/reporting_policies.json` | FWD-10 (the enumerated destinations) | IRPT_ANLREQ TO-APPLY-t1 (4.0.0_SA_CRO); IRPT_YCDGEN YCD-a-7; AR-t-13 | irpt-commentary-draft-store-lambda | read at runtime by `reporting_policy` / `reporting_destination` |
| `lib/opal_naming.py`, `org/standards/NAMING_SCHEMA.json`, registry `exemptions`, `resources`, `scopes`, `systems` | CLAUDE.md rule 30; FWD-10 and FWD-12 CONSTRAINT (every address is `address()` output) | LGIC canon, 22 + 5 + 4 + 1 + 3 + 6 commits | schema, exemptions, resources: three functions; naming module, scopes, systems: none | parsed on every call |

Inert: `recipe.py` (comment only, AST identical), `firm_registry.json` (generated header string only).

## 3. Read against the ENDPOINT's constraints

- **FWD-3 (a vendor's return is never the served figure):** no member under `performance/` is among the 26; the pin contains the
  restoration `c267b71edb`. This build does not bring the vendor path back. MEASURED (the census's member list).
- **FWD-4 (no live vendor call):** `IRPT_LIVE_YCHARTS_CALL` stays absent; the environment does not change. MEASURED by the worker
  on the live configuration.
- **FWD-2 (cross-firm exposure):** two changes alter an access decision: the named service subjects in repository/retention, and
  the svc-custody-statement operation. Both sets of bytes are already recorded as released in the adapter and status functions;
  in this function no route reaches the first and the second ends in UNSUPPORTED_OPERATION. The replay's binding cases are
  identical on both zips (arms 7, 10). No widening for a firm principal is read.
- **FWD-10 (a request lands only in its firm's enumerated locations; a new firm is a GATE EDIT):** read by this seat on the two
  pins: 4 policies live, 5 built. NEW `irpt-anlreq-commentary` (revision irpt-anlreq-x10-v1, three firms, family
  ANALYSIS_COMMENTARY, register X10 with a register commit and a ruling commit on the row). CHANGED `irpt-ycdgen-research`:
  firms cottonwood -> cottonwood, 49financial, inflection; no other field moves. The packet reads `destination_revision`
  unchanged. The registry edit IS the gate edit FWD-10 names; this seat did not read who ruled the research policy's widening.
  THE CTO HALF NAMES IT, or the half is not complete on this member.
- **FWD-9 (a request an advisor can see):** every request accepted after the apply records a different
  `ingestion_gate_revision` and a new field `acting_principal_id`. Readers: `ops/owned_requests.py` names the gate revision at
  two lines (20, 191), as a member that must be present, never as a value compared (read by this seat); it does not name `acting_principal_id`. The reader's one closed key set is over the record's `identity` member
  (`set(identity) != IDENTITY_FIELDS`, line 186 at HEAD and line 178 at irpt-status's recorded pin 361c44fa9d); the new field
  is written at the record's TOP LEVEL (`acceptance.py:113-119`), outside it. MEASURED on the bytes. The wider census of
  readers of the acceptance record (19 readers, none with a closed key set) is INHERITED from `2.0.0_SA_COO~Y2` and was not
  re-run.

No served change is read to contradict a ratified outcome of IRPT_BCKEND. Three things are not established and are conditions
below, not assurances.

## 4. COO half

SIGNED for the blast radius below, on these conditions, by 2.0.0_SA_COO~P2.

- **Property moved:** the code of Lambda `irpt-ycharts-generate` (object version and `source_code_hash`). **Writers of that
  property: 1** -- `module.irpt_ycharts_generate.aws_lambda_function.this` in the root
  `infra/aws/terraform/investor-reporting/ycharts`, through `safe-apply`. No other writer is admitted.
- **What the act may touch:** that one function's code. On a request after the apply: the acceptance record of each NEW
  submission (one added field, one changed revision string), and whatever the function writes under the policies of section 3.
  It may not touch: the role, the layers, the environment, any route, any other function, any existing record.
- **Branch A (apply):** the plan shows the object version and `source_code_hash` on the one function and nothing else; the
  uploaded object's `content-sha256` reads `MGQu5+58WxJ3pybmZx8cFdJ9nypEPvPGo66cCyiB1ts=`; a different digest stops the apply.
  After: CodeSha256 equal to that digest; the import census answers `failed: {}`.
- **Branch B (rollback):** S3 version `.epN9U3xZSMhU5WmEudwCrbjnydqg4N6`, RE-READ at apply; after it CodeSha256 reads
  `tdpterTMfJlWXjnoAQCwil+wN/Jf8Q/yLjGxTk7yUkk=`. Records the built code wrote stay (added field, added rows); the half covers
  that state: the live code returns a prior record as stored.
- **Conditions (each blocks the apply order, none blocks this signature):**
  1. The CTO half names the ruling behind `irpt-ycdgen-research` reaching 49financial and inflection.
  2. The build from the REAL map, after the candidate entry lands, prints the signed digest (the adapter and narrative did; this
     function's has not been tried). The record step also corrects the map's stale `artifact_sha256`, `deployed_code_sha256`,
     `last_deployed_at` and `deploy_ledger` for this entry.
  3. The applier's first after-read on a request is the acceptance pair: one fresh accepted request carries
     `acting_principal_id`; one accepted before the apply reads back unchanged; the history route (irpt-status) still lists both.
     No vendor call is made to test the release.
- **Not covered:** a process that runs the three resident members from this artifact (none is read to); the real injected
  objects behind the four carried method sites; real DynamoDB, S3 and SQS semantics. A failure there is Branch B.
