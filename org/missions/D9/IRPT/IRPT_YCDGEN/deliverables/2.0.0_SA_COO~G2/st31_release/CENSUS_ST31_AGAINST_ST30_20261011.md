# st31 -- census of every member that moves against the running st30

**By:** `2.0.0_SA_COO~G2`, 2026-10-11. Pin `19b02b2971`, cut FROM THE TRUNK (box/dell2) with no cherry-pick and no member
override. Running root `37210c771a-st30`. Built locally; nothing is staged or installed.

Members: st30 295 files, st31 295 files (294 members plus SHA256SUMS). **Added 0, removed 0, changed 21, identical 273**
(the package gate's G5; my own comparison of the two packages reads the same 21 plus SHA256SUMS).

| member | + | - |
|---|---|---|
| `_authz/loaders.py` | +1 | -1 |
| `_contracts/fixtures/AnalysisUploadResult.valid.json` | +275 | -12 |
| `_contracts/fixtures/DirectoryPage.valid.json` | +20 | -31 |
| `_contracts/fixtures/OwnedAnalysisRequest.persist_inputs.extra_member.invalid.json` | +6 | -3 |
| `_contracts/fixtures/OwnedAnalysisRequest.persist_inputs.missing_member.invalid.json` | +6 | -3 |
| `_contracts/fixtures/OwnedAnalysisRequest.persist_inputs.no_sha256.invalid.json` | +6 | -3 |
| `_contracts/fixtures/OwnedAnalysisRequest.persist_inputs.valid.json` | +6 | -3 |
| `_contracts/test_persist_inputs_contract.py` | +9 | -0 |
| `data/firm_registry.json` | +1 | -1 |
| `docs/contracts/investor-reporting/v1/OwnedAnalysisRequest.schema.json` | +6 | -1 |
| `docs/contracts/investor-reporting/v1/responses/analysis-request-pdf.response.schema.json` | +28 | -1 |
| `docs/contracts/investor-reporting/v1/responses/comparison-catalogue.response.schema.json` | +28 | -1 |
| `docs/contracts/investor-reporting/v1/responses/custody-report-persist.response.schema.json` | +28 | -1 |
| `docs/contracts/investor-reporting/v1/responses/custody-report-read.response.schema.json` | +28 | -1 |
| `infra/logic/registry/name_rulings.json` | +14 | -0 |
| `lib/opal_naming.py` | +16 | -1 |
| `reports/resident_bindings.json` | +2 | -2 |
| `reports/resident_installed.py` | +8 | -6 |
| `ycharts/generate/resident_worker.py` | +54 | -10 |
| `ycharts/research/opal_packager.py` | +77 | -30 |
| `ycharts/research/opal_producer.py` | +16 | -3 |

## What each group does on the resident (READ = I read the diff against st30; MEASURED = a script compared the two)

| # | group | members | on the resident | basis |
|---|---|---|---|---|
| D1 | The dead-letter record (IRPT_YCDGEN `YCD-e-11`, row D2-S49) | `ycharts/generate/resident_worker.py` | SERVED: when a generation job's handler raises on its fifth receive, the job's own row is written FAILED with `{code: DELIVERIES_EXHAUSTED, cause: <exception class>, receives}` and one journal line, then the exception is re-raised. The message is not deleted and its visibility is not changed by that branch. Below the limit nothing changes. The 390 s read-back release is kept (the constant reads 390 in the new member); its `except` branch is restructured into the same handler | READ: 3 hunks; the only removed lines are the old `except ReadBackPending` branch, re-added inside the new one |
| D2 | The packager's own-store pre-check (IRPT_ANLREQ `AR-g-32`) | `ycharts/research/opal_packager.py`, `opal_producer.py` (`produce_package`, `package_logical_id`), `reports/resident_installed.py` (`make_packager`) | INERT: the packager runs only when the bindings carry `commentary_ready_queue_url`; the built bindings carry none and V1 prints the count. `opal_producer.produce`, the Opal report's own path, is not changed by this diff | READ |
| D3 | Generated headers | `_authz/loaders.py`, `data/firm_registry.json` | NO CHANGE of behaviour: one comment line each, the registry hash they were generated from | READ |
| D4 | The naming builder and one registry | `lib/opal_naming.py` (+16 -1), `infra/logic/registry/name_rulings.json` (+14) | NO SERVED CHANGE FOUND: two more generated-view paths for two other Lambdas, and two SMS log-group rulings of another project. Asked the old and the new builder, each in its own interpreter: 129 of 129 policy-family answers identical, and 17 of 17 answers for the research modules' own `name()` and `address()` calls identical | MEASURED; the +16 lines READ |
| D5 | Schemas | `OwnedAnalysisRequest.schema.json` (the `persist_inputs.report_index` members gain types and patterns), four `responses/*.response.schema.json` (each gains a REQUIRED `unprojected_grant`) | TIGHTENING, not reached: the resident passes three schema names to its validator (`AnalysisReport`, `AnalysisReport.v2`, `RequestComposition`; census part 2 of st30, section 8.3) and none of the five is among them or referenced by them. They are the status and export functions' contracts | READ (2 of 5 diffs printed in full; the three other response schemas show the same +28 -1 shape and were NOT each read) |
| D6 | Fixtures and one test | 6 `_contracts/fixtures/*.json`, `_contracts/test_persist_inputs_contract.py` | INERT: not loaded by the resident | by path |
| D7 | Build outputs | `reports/resident_bindings.json` (the pin and the build time), `SHA256SUMS` | the two generated lines | READ |

## Not established

Nothing here was exercised on the host. D1 fires only on a job that raises five times; no such job is driven. The
comparison is against the st30 package tar (sha256 `e5a6b6251b0e5e97...`), the BUILD INPUT of the running root; st30's V1
read the worker's sha256 on the host equal to that build's.
