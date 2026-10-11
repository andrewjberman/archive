# The one resident release -- census PART 2: what each group DOES when it lands (served, or inert until what)

**By:** `2.0.0_SA_COO~G2`, 2026-10-11, on `1.0.0_SA_CTO~DELL2` msg 4521 items 2 and 3. Part 1 (every member, its commits, its
load class): `RELEASE_CENSUS_PART1_MECHANICAL_20261011.md` @8e5ae4a62c. Pin `37210c771a`; running root `e606008994-st27`.
Built LOCALLY only. Nothing is staged, installed or deployed.

**The pair's first line, as the CTO asked: MORE THAN FOUR groups change what the resident does. Seven change a served
answer or a recorded outcome; four are inert until a named binding or caller; four were read with no served change
found for the resident; two items are not classified.**

How each line below was reached is stated in its last column: READ means I read the diff of the running root's file against
the new one; MEASURED means a script compared the two; NOT READ means exactly that.

## 1. Groups that CHANGE a served answer or a recorded outcome when this lands

| # | group (project) | members | what changes for the resident | after-read | basis |
|---|---|---|---|---|---|
| S1 | The stated reason and the page sentence (IRPT_YCDGEN) | `ycharts/research/held_data.py`, `layout_overview.py`, `opal_producer.py` | An Opal-held section with no rule states `NOT_IN_THIS_VERSION`; one with no store row states `INPUT_MISSING:security_not_covered`; the page prints one sentence per cause and no raw string | The section census re-run on a report generated AFTER the install: 0 sections stating `INPUT_MISSING:held_<group>` for a no-rule or no-row cause, and the page text read | READ (cells YCD-a-9, YCD-a-10; 250 tests) |
| S2 | The ticket reference (IRPT_ANLREQ release 4) | `docs/contracts/.../AnalysisSubmissionRequest.schema.json`, `ycharts/generate/submission.py`, `resident_worker.py` (`mark_ready`) | A request that carries `ticket_id` is admitted by the resident (schema and `validate_public_request`), and its READY receipt names the ticket | `REL4-READ5`: one ticket-bound request reaches READY | READ |
| S3 | The 390 s read-back release (IRPT_BCKEND, CTO rulings batch 262) | `ycharts/generate/resident_worker.py` (`poll_once`), `recipe.py` (comment only) | A job that raises `ReadBackPending` releases its message for 390 s, not 900. YCharts producer path only; the Opal path never reaches a read-back | NOT DRIVABLE without a vendor-facing run, which this release does not order. Evidence in hand: the 5 release tests at the pin. The first pending read-back after install prints nothing new unless the visibility call fails (`IRPT_RESIDENT_READ_BACK_RELEASE_KEPT_900`) | READ |
| S4 | The research policy row (IRPT_YCDGEN round 7, carried by st29 and not by st27) | `infra/logic/registry/reporting_policies.json` | Row `irpt-ycdgen-research-v1` names 3 firms, not 1, so its policy digest changes (`6e3286a3d962` to `aebe35b9a054` by this census's canonical hash). `irpt-x10-v1` and `irpt-dashbd-x10-v1` are byte-equal rows (SAME). Retention compares a stored record's digest with the packaged one: a research-family artifact retained under the OTHER digest is refused on a resident read (row W3-S14's class) | Both branches, stated before the install and NOT yet measured on a record: by the retention rule, an Opal artifact retained on st29 (the new digest) reads after the install and is refused today; one retained on st27 or st28 (the old digest) is refused after it. One read of each, by request id | the digest change is MEASURED (row-by-row hash); the two branches are read from the rule, not from a record |
| S5 | A READY job now logs a line (IRPT_ANLREQ AR-g-21) | `resident_worker.py` (`send_ready`, `signal_ready`), `durable_job.py` (`mark_i3_sent`, `get_state`) | Every READY write, and every redelivery of a READY job with no `i3_sent_at`, calls `send_ready`. With `IRPT_ANALYSIS_READY_QUEUE_URL` unset it prints `WARN: ANALYSIS_READY_QUEUE_UNSET <request id>` and sends nothing. So: one new journal line per READY, no message | The journal of the regenerated report's READY shows that WARN line and 0 I3 messages. **PRE-READ, before the install: the unit's Environment on the host does not set `IRPT_ANALYSIS_READY_QUEUE_URL`.** If it does, I3 goes live with this release, against the CTO's ordering rule | READ |
| S6 | Refusals carry a reason class (IRPT_BCKEND, CTO batch 253 and rows W142-S1, S175, S260) | `_scope/maintained_sources.py`, `_scope/canonical_profile_reads.py`, `_authz/loaders.py`, `intake/uploads.py` (the two access refusals) | The same refusals at the same sites now raise a subclass that declares `NOT_AUTHORIZED`, `NOT_READY`, `INVALID_INPUT`, `NOT_FOUND` or `FIRM_BINDING`. Base classes are kept, so every existing `except` still catches. On the resident this can change the reason a FAILED job records; no success path changes | No positive read exists without making a job fail. Covered by the suites at the pin (generate 498 passed) | READ (4 of 4 diffs) |
| S7 | Report and request schemas gain OPTIONAL members (IRPT_ANLREQ AR-y-32, AR-y-11) | `AnalysisReport.schema.json` and `AnalysisReport.v2.schema.json` (`retained_ref`), both copies; the request schema of S2 | Additive: a new optional property, no new required member. A document valid before stays valid; a document carrying the new member is now admitted where it was refused | Covered by S1's regenerated report persisting (it validates against v2) | READ (3 diffs) |

## 2. Groups that are INERT on the resident until a named binding or caller

| # | group (project) | members | inert until | basis |
|---|---|---|---|---|
| I1 | The packager and its poll (IRPT_ANLREQ AR-g-12, 13, 22, 31) | `ycharts/research/opal_packager.py` (ADDED), `resident_worker.py` (`poll_package_once`), `resident_main.py` (the package loop), `reports/resident_installed.py` (`make_packager`), `opal_producer.produce_package`, `layout_overview._commentary_section` | the bindings carry `commentary_ready_queue_url`. The new package's bindings do not (read from the built `resident_bindings.json`); `build_resident_runtime` adds the packager only `if bindings.get("commentary_ready_queue_url")` | READ |
| I2 | The I3 SEND itself (IRPT_ANLREQ AR-g-21) | as S5 | the bindings carry `analysis_ready_queue_url` (absent), which is the only place `resident_installed` sets the variable. See S5's pre-read for the one other way it can be set | READ |
| I3 | Named service subjects (IRPT_BCKEND IB-pr-386, IRPT_ANLREQ AR-t-12) | `reports/repository.py` (`SERVICE_READERS`, `SERVICE_WRITERS`, the `_allow` branches, `ArtifactAlreadyWritten`), `reports/retention.py` (`_allow`) | a caller builds a principal of class `SERVICE_READER`. On the resident only the packager's commentary reader does (I1). A user principal, including `svc-irpt-analysis`, is not of that class and takes the unchanged branch | READ |
| I4 | Custody reports (IRPT_BCKEND E8, IRPT_DASHBD) | `repository.py` (`KINDS` gains `CUSTODY_REPORT`, `revisions`), `reports/composition.py` (`CUSTODY_POLICY_REVISION`, `revisions` passed through), ADDED `_scope/custody_ports.py`, `reports/custody_write.py`, `reports/commentary_composition.py`, `reports/commentary_draft_store.py`, the custody fixtures and response schemas, policy rows `irpt-custody-x10-v1` and `irpt-anlreq-x10-v1` | a caller passes a custody revision or imports the three added modules. None of the three is imported by any module the resident can import (part 1: NOT_IMPORTED), and `resident_installed.py` does not pass `revisions` | READ for the two changed modules; MEASURED (import closure) for the added ones |

Also inert, by part 1's load class: the 16 fixtures and tests (13 fixtures, 3 tests), and the `.py` members nothing imports (`ops/entry.py`,
`ops/owned_report.py`, `ops/pdf_link.py`, `ops/prospect_dates.py`, `reports/generate_installed.py`,
`reports/status_installed.py`, `ycharts/generate/custody_submission.py`, `submission_service.py`,
`_scope/retained_input_authorizer.py`, `ycharts/research/file_stop_row.py`). They are the Lambdas' entry modules, packaged
beside the resident's and never loaded by it. `ycharts/generate/acceptance.py` `accept` gains a REQUIRED keyword
(`acting_principal_id`); its one caller is `submission_service.py`, which the resident does not import.

## 3. Read, and no served change found for the resident

| group (project) | members | finding | basis |
|---|---|---|---|
| The naming builder and its registries (LGIC_BLANKFIX, LGIC_CANON, MDPF_CANON, ADVI_FIRMBKTS, NFRA_CTLPLN) | `lib/opal_naming.py` (+488 lines), 5 changed and 8 added registry files, `org/standards/NAMING_SCHEMA.json` | The old and the new builder, each in its own interpreter, were asked for the object address of every family of every reporting policy for the 3 firms, and for the producer's two run-record addresses. 57 of 57 addresses of the 19 existing families are IDENTICAL; the 6 extra answers are the 2 added families. `name()` outputs were NOT probed | MEASURED (`naming_differential`); the 488 lines themselves NOT READ |
| The served-authorization layer (IRPT_BCKEND, FIRM_BINDING) | `_authz/served.py` (+224) | Its entry (`Entry.handle`) is constructed by five Lambda entry modules; `resident_main.py`, `resident_worker.py` and `resident_installed.py` contain no reference to it. Importable, never entered | MEASURED (grep of the three resident files); the diff's function list READ, its bodies NOT READ |
| Internal on-behalf uploads (IRPT_BCKEND IB-yr-631, IB-pr-354) | `intake/uploads.py` (`_internal_for_allowed_firm`), `_scope/interactive_access.py` (`profile_reader`, `_allowed_firm_ids`) | The door opens only for a principal that carries `allowedFirmIds`, which `InteractiveAccess` adds only when a `profile_reader` is wired. `resident_installed.py` names no `profile_reader` (0 occurrences) | READ |
| History reads (IRPT_ANLREQ AR-y-32) | `ops/owned_requests.py` (+99) | The changed functions are the history page and its client claim, a served route of irpt-status. The resident reads single accepted records | READ; "the resident never calls `history`" is by reading the three resident files, not by a call trace |

## 4. NOT CLASSIFIED

| member | why |
|---|---|
| `_ids/ids.py` (1 line, `project`) | A mapped value that is empty, `none`, `nan` or `null` is no longer taken as an id. `project` is named by resident-reachable modules. I have not read which resident path passes it a null-like string, so I do not call it inert or served |
| `docs/contracts/investor-reporting/v1/routes.json` (+62 -4) and the 6 other changed schemas loaded by glob | Loaded as documents for `$ref` resolution. I read `AnalysisReport`, its v2 and the request schema (S7). The others were NOT READ |

## 5. The 25 added members

By name in part 1, section 4. Classed here: 1 packager module (I1); 4 custody and commentary modules (I4); 1 test; 9 fixtures;
2 response schemas; 8 registry files, of which 5 are named by a reachable module and covered only by the address
differential of section 3, and 3 are not named by any.

## 6. Rollback

The running root `e606008994-st27`: package tar `e606008994-st27.tar.gz`, sha256
`20916261074c356ab31497b338a6957e3d72cb252b8a3f54432db98610da39e4` (read 2026-10-11 from `C:/dev/irpt-release-st27/`), 270
members. One rollback restores all of it. That tar is the BUILD INPUT of the running root; the host's own bytes were not
listed (the 07:4xZ host listing read the unit's root path and the brand directory only).

## 7. What this census does not establish

- No group was exercised on the host. Every line is a read of bytes or a script over two packages.
- "Inert" means the gate that keeps it off was read in the code. It does not mean the code behind the gate is correct.
- S3 has no after-read this release can drive, and S6 has none short of a failing job. The pair says so; it does not offer a
  green line for them.
- Part 1's import closure is a lower bound (its section 8).
