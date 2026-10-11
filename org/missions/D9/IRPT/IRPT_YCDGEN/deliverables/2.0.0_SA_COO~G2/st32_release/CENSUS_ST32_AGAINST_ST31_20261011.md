# st32 -- census of every member that moves against the running st31

**By:** `2.0.0_SA_COO~G2`, 2026-10-11. Pin `0485393f3a`, cut FROM THE TRUNK (box/dell2) with no cherry-pick and no member
override. Running root `19b02b2971-st31`. Built locally; nothing is staged or installed.

Members: st31 294 plus SHA256SUMS, st32 297 plus SHA256SUMS. **Added 3, removed 0, changed 17, identical 277** (the package
gate's G5; my own comparison of the two package folders reads the same 17).

Added: `_contracts/fixtures/analysis-report.sections.opal.invalid.json`, `...opal.valid.json`, `...vendor.valid.json`.

| changed member | + | - |
|---|---|---|
| `_authz/loaders.py` | +22 | -3 |
| `_authz/served.py` | +1 | -1 |
| `data/firm_registry.json` | +1 | -1 |
| `docs/contracts/investor-reporting/v1/responses/analysis-report.response.schema.json` | +67 | -13 |
| `docs/contracts/investor-reporting/v1/routes.json` | +5 | -1 |
| `infra/logic/registry/exemptions.json` | +94 | -0 |
| `infra/logic/registry/scopes.json` | +2 | -0 |
| `lib/opal_naming.py` | +268 | -19 |
| `ops/entry.py` | +12 | -4 |
| `ops/owned_report.py` | +44 | -3 |
| `reports/commentary_composition.py` | +33 | -7 |
| `reports/resident_bindings.json` | +3 | -3 |
| `reports/resident_installed.py` | +43 | -1 |
| `ycharts-host/ycharts_session.js` | +33 | -0 |
| `ycharts/generate/resident_worker.py` | +2 | -1 |
| `ycharts/research/opal_packager.py` | +23 | -18 |
| `ycharts/session/host_capture.py` | +223 | -3 |

## What each group does on the resident (READ = I read the diff against st31; MEASURED = a script compared the two)

| # | group | members | on the resident | basis |
|---|---|---|---|---|
| D1 | The capture keeps its sign-in receipt (IRPT_BCKEND `IB-pr-434`, drained @231219c1f4) | `ycharts/session/host_capture.py` (+223 -3: `capture_env`, `stderr_sink`, `keep_tail`, one line of `run_capture`) | SERVED ONLY AT A CAPTURE: when the worker runs a host capture, the receipt of the sign-in is kept through a whitelist and the wrapper's stderr is kept per run. Nothing runs at start | READ by function name and size, not line by line; the cell's own record `IB132-1_capture_receipt_record.json` states 43 whitelisted leaves and 0 of 4 planted secrets persisted |
| D2 | The capture library | `ycharts-host/ycharts_session.js` (+33 -0) | SERVED ONLY AT A CAPTURE, and it MOVES A HOST FILE: one new branch. After ONE submitted sign-in, a page that reads as app chrome with no identity cookie fails at once with its own reason `SIGNED_OUT_APP_CHROME_AFTER_SUBMIT`, carrying booleans, a status, the URL's path and no page text. No second submission, no retry | READ, whole diff |
| D3 | The worker stamps its claim (IRPT_YCDGEN `TO-YCD-d-13`, PRD v0.12) | `ycharts/generate/resident_worker.py` (+2 -1) | SERVED: the dead-letter record gains `cause_claim: "measured"`. The journal line is unchanged | READ; `r13_checks.py d13` |
| D4 | The packager's token port and its binding (IRPT_ANLREQ `AR-g-41`, `AR-g-42`) | `ycharts/research/opal_packager.py` (`live_ticket_ports`, +23 -18), `reports/resident_installed.py` (+43 -1) | INERT: the built bindings carry no `commentary_ready_queue_url`, no `analysis_ready_queue_url` and no `packager`. The new refusal `RESIDENT_PACKAGER_REQUIRED` fires only on a bindings document that binds the commentary queue | READ; bindings keys read from the built package |
| D5 | The ownership-map read for one firm (ADVI_FIRMBKTS `FB-g-16`) | `_authz/loaders.py` (+22 -3) | NOT ON THE RESIDENT'S PATH. `load_ownership` now reads 49financial's map from a bucket named in a generated table (`opal-data-bd`, same key) where it took the bucket from `IRPT_DIRECTORY_BUCKET_MAP`. Its callers in the package are the Lambda boundary (`_authz/served.py` `Entry`, `_authz/enforce.py`, `reports/generate_installed.py`, `_scope/custody.py` through an `Entry`); the resident constructs no `Entry`. The two resident-side modules that import `loaders` (`_scope/interactive_access.py`, `_scope/custody.py`) import only `bucket_for`, which is unchanged | READ (native search of the package for every importer of `loaders` and every caller of `load_ownership`); MEASURED: importing `resident_installed`, `resident_worker` and `resident_main` from the built package loads 25 package modules and `loaders` is not one. NOT measured: a job's execution on the host. P1 prints whether the unit's process carries the variable at all, as information |
| D6 | The report read's optional ticket selector, and the sections contract (IRPT_ANLREQ `AR-y-71`, IRPT_BCKEND `IB-pr-432`) | `ops/owned_report.py` (+44 -3), `ops/entry.py` (+12 -4), `_authz/served.py` (one refusal name added to a tuple), `routes.json`, `responses/analysis-report.response.schema.json` (+67 -13), 3 added fixtures | NOT ON THE RESIDENT'S PATH: these serve the report and status Lambdas. Native search of the package: `owned_report` is named in `ops/read_memo.py` and `reports/status_installed.py` only. `_authz/served.py` IS loaded by the resident; its change is one more name in a tuple of public reasons | READ, except the response schema (by size and shape) |
| D7 | The drafter's READY gate (IRPT_ANLREQ `AR-y-81`) | `reports/commentary_composition.py` (+33 -7) | NOT ON THE RESIDENT'S PATH: a Lambda handler module; named in the package only by `reports/commentary_draft_store.py`. Its hazard row IRPT_ANLREQ-D2-S53 is about a Lambda upload, not this host | READ |
| D8 | The naming builder and two registries | `lib/opal_naming.py` (+268 -19: `validate`, `_ownership_canonical`, `_irpt_bucket`, generation helpers), `infra/logic/registry/exemptions.json` (+94), `scopes.json` (+2), `data/firm_registry.json` (header) | NO SERVED CHANGE FOUND: 129 of 129 addresses the resident can ask for are identical between the two packages, each asked in a separate interpreter (63 refused in both) | MEASURED (`naming_differential.json`); the builder's diff was read by function name, not line by line |
| D9 | Build outputs | `reports/resident_bindings.json` (the pin, the build time, the library pin), `SHA256SUMS` | the generated lines; the library pin is D2's | READ |

## Not established

Nothing here was exercised on the host. D1 and D2 run only at a capture, and no capture is driven by this release. D3
fires only on a job that raises five times. D5 is off the resident's path by an import read, not by a host run. The comparison is against the st31 package
tar (sha256 `00532ad07e3e250b...`), the BUILD INPUT of the running root; st31's V1 read the worker's sha256 on the host equal
to that build's.
