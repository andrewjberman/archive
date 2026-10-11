# IB126-1 -- does the handler's own answer have the producer fixture's shape? Five routes and a control (TO-IB-pr-428)

Worker 0.9.0_WK_IRPT_BCKEND~287, tree HEAD 329be12f74, 2026-10-11. Read only: existing handler tests and in-memory fakes, no AWS call, no live request.
Data: `IB126-1_handler_shape_vs_fixture.json`. Rerun: `ib126_run_all.sh`. Member names and JSON types only; no value is written anywhere.

**What this is NOT.** It is the handler's answer built in process from the TREE, over each test's synthetic fakes. It is not a byte read off the live
function, and the fakes show the shape the code emits for that fake world, not every state a live caller can reach. The deployed build can be older than the
tree: per function, the source map pins every staged answer-building file to an OLDER commit than HEAD (none to HEAD itself); each of those blobs has the same
bytes as HEAD's file, except `_authz/served.py` on three functions (below). The map's `last_deployed_commit` is a record, not proof of the deployed bytes.

**Envelope finding.** The handler's response wrapper, `response_envelope` (`_authz/served.py:403`, the member is added at :419), ALWAYS adds a top-level member
`unprojected_grant` to every served answer. Of the 21 v1 response schemas (`docs/contracts/investor-reporting/v1/responses/`), 17 declare that member; 4 are closed
(`additionalProperties: false`) and omit it: `analysis-request-pdf`, `comparison-catalogue`, `custody-report-persist`, `custody-report-read` (my own count; it equals the issuer's four).
So the whole answer of any of those four routes fails its own schema on that one member. Measured here on three of them: `custody-report-read`, `custody-report-persist` and the
control `comparison-catalogue`; `analysis-request-pdf` is not one of the six routes read and was not run. On all six routes read, the `data` member has the fixture's member
names and JSON types. This is a finding about the four schemas. It does not say which side moves (schema, handler or reader); that is the CTO's ruling. The portal reads the
control route today, so a reader that accepts the extra member exists. Rows `IRPT_BCKEND-D2-W287-S1` (ruled by AMENDMENT 1) and `-S2` stand as filed.

**Two verdicts per route.** `verdict` grades the whole answer (shape AND it validates its schema). `data_verdict` grades the `data` member alone. `envelope_schema_gap` lists the
envelope members the handler emits that the route's schema does not admit.

| operation (function) | answer built at | evidence | whole answer vs v1 schema | `verdict` (whole answer) | `data_verdict` (data alone) | `envelope_schema_gap` |
|---|---|---|---|---|---|---|
| directory-browse (irpt-directory-search) | directory/entry.py:378 | existing test, run | VALID | SAME_AS_FIXTURE | SAME_AS_FIXTURE | [] |
| analysis-request-history (irpt-status) | ops/owned_requests.py:393 | existing test, run | VALID | SAME_AS_FIXTURE | SAME_AS_FIXTURE | [] |
| analysis-input-upload (irpt-ycharts-generate) | intake/uploads.py:504 (NORMALIZED), :393 (RESOLVING) | existing test, run | VALID | SAME_AS_FIXTURE | SAME_AS_FIXTURE (NORMALIZED) | [] |
| custody-report-read (irpt-export-render) | export/custody_read.py:78 | in-process call | INVALID | DIFFERS | SAME_AS_FIXTURE | [unprojected_grant] |
| custody-report-persist (irpt-export-render) | export/custody_persist.py:177 | existing test, run | INVALID | DIFFERS | SAME_AS_FIXTURE | [unprojected_grant] |
| control: comparison-catalogue (irpt-ycharts-generate) | ycharts/generate/comparison_catalogue.py:200 | existing test, run | INVALID | DIFFERS | SAME_AS_FIXTURE | [unprojected_grant] |

The control reads SAME_AS_FIXTURE on `data`, as the issuer expected; its only envelope difference is `unprojected_grant`.

**Custody `report.accounts`.** `custody-report-read`: `report.accounts` is NOT an array in the handler's answer; it is absent (the run's `data.report` carries `as_of_date, title, sections`
beside `composition_sha256`). `data.report` is the persisted document passed through (`custody_read.py:78`), so whether `accounts` is present depends on the document the persister
sends; the handler neither builds nor checks it. `custody-report-persist`: not applicable, it returns a reference only (kind, id, revision, sha256), never the document.

All envelopes are built by `response_envelope` (`_authz/served.py:403`) and carry `contract_version, operation, firm_id, data, unprojected_grant`. Call sites:
:1321 (directory, custody, control), :982 (history, owner-read branch), :1040 (upload, prospect branch). Rows 1-5 of `routes.json` match the order's table.

**directory-browse.** `test_bootstrap_browse.py::test_initial_page_and_continuation_are_whole_and_stable` (which itself validates each page) was run unaltered; the last
page was compared. Four fixture-only members (`entries[].access.reason`, `.cohort.capability_facts`, `.cohort.hierarchy_path`, `.ids.relationship_id`) are optional by
schema (the envelope still validates without them); the test's fake directory does not carry them, so this run did not show the handler passing them through.

**analysis-request-history.** `test_owned_entry.py ... [history]` run unaltered. One member, `items[].client_id`, was `null` in the handler's sample (an upload row) and
`null|string` in the fixture; the string state was not exercised through the entry. `test_history_row_client.py` (5 passed) exercises it at payload level against the schema.

**analysis-input-upload.** The fixture is state NORMALIZED. The NORMALIZED answer (`test_deferred_resolution.py`, run unaltered) matches; it comes through the
repository's `build_upload_entry` (same `served.Entry`, `UploadService`, CREATE_INPUT mode), NOT `generate_installed.build_boundary`. The function's own boundary
(`test_generate_installed.py`) answers RESOLVING: `upload_id, input_id (null), state` only. That differs from the fixture on `input_id` (null vs string) and the absent
`input_ref`, `portfolio`; the schema makes those state-dependent, so it is the state, not a defect. A browser polling the route sees RESOLVING first. The fixture's
`portfolio` is `{}`, so the handler's 15 members under it are unobservable against it (the schema leaves it free-form).

**custody-report-read / persist.** `data` matches the fixtures on both. `report.accounts` is NOT an array in the handler's answer: it is absent. `data.report` is the
persisted document passed through (`custody_read.py:78`); in the run it carries `as_of_date, title, sections` beside `composition_sha256` (three handler-only members under a
free-form object, optional by schema). The handler neither builds nor checks `accounts`; whether it is present depends on the document the persister sends. Persist returns a reference only.

**Control.** comparison-catalogue: `data` matches (`entries[].ticker` null-only in the sample, `null|string` in the fixture; the string state is built by
`test_the_catalogue_lists_the_models_then_the_named_tickers_only_and_validates`, 12 passed). The envelope fails as above. Of the 21 v1 response schemas, 17 declare
`unprojected_grant`; the four that do not are analysis-request-pdf, comparison-catalogue, custody-report-persist, custody-report-read. `test_seam_paired.py` adds the member only
where a schema requires it, so no existing test validates a real handler envelope against these.

**Source-map pins (per function).** irpt-directory-search: `entry.py` native, same at last_deployed_commit 4850c85632 and HEAD. irpt-status: `owned_requests.py` native, same at
d6d7bb5a84; `entry.py`, `status_installed.py`, `served.py` staged at ee3fd7c5e5, same bytes as HEAD. irpt-ycharts-generate: `uploads.py` f09b802cdc, `upload_entry.py` and `entry.py`
3f29017cfc, `generate_installed.py` 0ee21c796f (all same bytes as HEAD); `comparison_catalogue.py` native, same at 5d3eed8904. irpt-export-render: `custody_read.py`,
`custody_persist.py` native, same at 6a0226dc02; `entry.py` d34a46f37d, same bytes. `served.py` is pinned at 74a62fb46c on directory, ycharts-generate and export-render and differs from HEAD by one
constant (`SVC_CUSTODY_STATEMENT_OPERATIONS`); `response_envelope`, `_handle_owner_read`, `_handle_prospect` and `handle` are byte-identical, so these verdicts hold for the pinned blob.

**Not established.** Which side moves on the four closed schemas. Whether `analysis-request-pdf` (the fourth closed schema, not one of the six routes) behaves the same: not run. The live function's bytes or its zip. The production port composition (every run substitutes in-memory ports for `submit_installed.compose` and the directory deps).
The optional directory members and the `client_id` / `ticker` string states through the entry. The upload NORMALIZED answer through the function's own boundary. The portal readers (not read).
Also: the upload schema's `x-response-contract.handler` says `irpt-analysis-upload`, the standalone entry name at `intake/upload_entry.py:72`; routes.json and the source map say irpt-ycharts-generate, which I used.
