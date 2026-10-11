# The one resident release -- census of every member it moves, PART 1: mechanical (no judgment yet)

**By:** `2.0.0_SA_COO~G2`, 2026-10-11, on `1.0.0_SA_CTO~DELL2` msgs 4502 and 4521. Built LOCALLY only; nothing is staged,
installed or deployed. Record: `RELEASE_CENSUS_PART1_MECHANICAL_20261011.json` (every member with its commits).

**PART 2 IS NOT WRITTEN.** The CTO's item 2 (does a served answer change when a group lands, or is it inert until a
binding or caller this release does not carry) needs each loadable diff READ. This part gives what a script can measure.
No pair is offered for signature on part 1.

## 1. The build

- Pin `37210c771a` on scratch branch `rel-resident-r5`: box/dell2 @f6b74199a9 plus a cherry-pick of the 390 s resident
  half 766a03a0f1. Tests at the pin: `ycharts/generate` 498 passed, 0 failed; `ycharts/research` 250 passed; the offline
  suite passes; the 5 release tests pass.
- Recipe: `build_resident_package.py --pin 37210c771a --census-pin 2874e37647 --research --opal-map <the Overview map>`
  with two `--member`s (the classifier client, the logo). No `--base-pin`: every member is read at the one pin.
  `brand.json` is now packaged by `--research` itself; the logo still needs its `--member` (row D2-W10-S4).
- Running root: `e606008994-st27`, 270 members. New package: 295 members. **25 added, 62 changed, 208 identical, 0 removed.**
- Bindings in the new package carry NO `commentary_ready_queue_url`, NO `analysis_ready_queue_url` and NO `packager` key.
- The packaged `AnalysisSubmissionRequest.schema.json` names `ticket_id`.

## 2. How each member is classed (mechanical)

| class | meaning | members |
|---|---|---|
| REACHABLE | a `.py` the resident's entry `ycharts/generate/resident_main.py` can import (static import closure over the built package: 68 of 117 `.py` files) | 23 |
| NAMED | a data file whose file name appears in a reachable module's source | 15 |
| LOADED_BY_GLOB | a `*.schema.json` in the schema directory, which `reports/resident_installed.py` loads by glob | 7 |
| NOT_IMPORTED | a `.py` no reachable module imports: it cannot run in the resident | 14 |
| NOT_NAMED | a data file no reachable module names | 25 |
| TEST | a test file | 3 |

Reachable is necessary, not sufficient: a reachable module may hold a changed function the resident never calls.
That is exactly what part 2 has to read.

## 3. By project (a member counts once per project its commits name)

| project | members | of which REACHABLE, NAMED or LOADED_BY_GLOB |
|---|---|---|
| IRPT_BCKEND | 42 | 16 |
| IRPT_ANLREQ | 25 | 16 |
| LGIC_BLANKFIX | 9 | 7 |
| (no project named in a commit subject) | 7 | 3 |
| IRPT_YCDGEN | 7 | 7 |
| NFRA_CTLPLN | 5 | 3 |
| IRPT_DASHBD | 4 | 2 |
| ADVI_COTBKF | 3 | 3 |
| LGIC_CANON | 3 | 3 |
| FIRM_BINDING | 3 | 3 |
| MDPF_CANON | 2 | 2 |
| ADVI_FIRMBKTS | 2 | 2 |
| MDPF_SECCLASS | 2 | 1 |
| IRPT_CUSTDY | 1 | 1 |
| MDPF_DEMQUE | 1 | 1 |
| NFRA_SPRINTWIN | 1 | 1 |
| LGIC_ENFORCE | 1 | 1 |
| OPAL_ENGINE | 1 | 0 |

## 4. The 25 added members, by name (new surface)

| member | class | projects | first owning commit |
|---|---|---|---|
| `_contracts/fixtures/OwnedAnalysisRequest.persist_inputs.extra_member.invalid.json` | NOT_NAMED | IRPT_BCKEND | 0a193c6ea5 |
| `_contracts/fixtures/OwnedAnalysisRequest.persist_inputs.missing_member.invalid.json` | NOT_NAMED | IRPT_BCKEND | 0a193c6ea5 |
| `_contracts/fixtures/OwnedAnalysisRequest.persist_inputs.no_sha256.invalid.json` | NOT_NAMED | IRPT_BCKEND | aff85bff09 |
| `_contracts/fixtures/OwnedAnalysisRequest.persist_inputs.null_index.valid.json` | NOT_NAMED | IRPT_BCKEND | 0a193c6ea5 |
| `_contracts/fixtures/OwnedAnalysisRequest.persist_inputs.valid.json` | NOT_NAMED | IRPT_BCKEND | 0a193c6ea5 |
| `_contracts/fixtures/custody-report-persist.response.invalid.json` | NOT_NAMED | IRPT_BCKEND | 5020b450a7 |
| `_contracts/fixtures/custody-report-persist.response.valid.json` | NOT_NAMED | IRPT_BCKEND | 5020b450a7 |
| `_contracts/fixtures/custody-report-read.response.invalid.json` | NOT_NAMED | IRPT_BCKEND | 5020b450a7 |
| `_contracts/fixtures/custody-report-read.response.valid.json` | NOT_NAMED | IRPT_BCKEND | 5020b450a7 |
| `_contracts/test_persist_inputs_contract.py` | TEST | IRPT_BCKEND | 0a193c6ea5 |
| `_scope/custody_ports.py` | NOT_IMPORTED | - | 4ee5392232 |
| `docs/contracts/investor-reporting/v1/responses/custody-report-persist.response.schema.json` | NOT_NAMED | IRPT_BCKEND | 5020b450a7 |
| `docs/contracts/investor-reporting/v1/responses/custody-report-read.response.schema.json` | NOT_NAMED | IRPT_BCKEND | 5020b450a7 |
| `infra/logic/registry/event_rules.json` | NOT_NAMED | LGIC_BLANKFIX | d85328ec6c |
| `infra/logic/registry/feeds.json` | NAMED | MDPF_CANON | 9a00f02d65 |
| `infra/logic/registry/key_rulings.json` | NOT_NAMED | LGIC_BLANKFIX | 662cbb0be5 |
| `infra/logic/registry/legacy_addresses.json` | NAMED | ADVI_COTBKF, LGIC_BLANKFIX, IRPT_CUSTDY | 4991b8b11b |
| `infra/logic/registry/mail_parties.json` | NOT_NAMED | NFRA_CTLPLN | f5accebd7c |
| `infra/logic/registry/name_rulings.json` | NAMED | LGIC_CANON, LGIC_BLANKFIX | 331e3fe609 |
| `infra/logic/registry/platinum_destinations.json` | NAMED | ADVI_FIRMBKTS | b9557fdc67 |
| `infra/logic/registry/root_map.json` | NAMED | LGIC_BLANKFIX | 650452aae2 |
| `reports/commentary_composition.py` | NOT_IMPORTED | - | 20534db618 |
| `reports/commentary_draft_store.py` | NOT_IMPORTED | IRPT_ANLREQ | 589aee38f0 |
| `reports/custody_write.py` | NOT_IMPORTED | IRPT_BCKEND | b4073d3a57 |
| `ycharts/research/opal_packager.py` | REACHABLE | IRPT_ANLREQ | 7e66decdff |

## 5. The changed members the resident can load, largest diff first

| member | class | + | - | projects | commits in range |
|---|---|---|---|---|---|
| `lib/opal_naming.py` | REACHABLE | 488 | 37 | ADVI_FIRMBKTS, MDPF_CANON, LGIC_ENFORCE, LGIC_BLANKFIX, NFRA_CTLPLN, ADVI_COTBKF | 21 |
| `_authz/served.py` | REACHABLE | 224 | 10 | IRPT_BCKEND, FIRM_BINDING, IRPT_YCDGEN | 8 |
| `infra/logic/registry/systems.json` | NAMED | 122 | 93 | MDPF_DEMQUE, LGIC_BLANKFIX, NFRA_SPRINTWIN | 6 |
| `ycharts/generate/resident_worker.py` | REACHABLE | 136 | 9 | IRPT_YCDGEN, IRPT_ANLREQ | 5 |
| `ops/owned_requests.py` | REACHABLE | 99 | 37 | IRPT_ANLREQ, IRPT_BCKEND | 3 |
| `_scope/maintained_sources.py` | REACHABLE | 65 | 46 | IRPT_BCKEND, FIRM_BINDING | 1 |
| `reports/repository.py` | REACHABLE | 79 | 9 | IRPT_ANLREQ, IRPT_BCKEND | 6 |
| `ycharts/research/opal_producer.py` | REACHABLE | 67 | 14 | IRPT_YCDGEN, IRPT_ANLREQ | 3 |
| `docs/contracts/investor-reporting/v1/routes.json` | NAMED | 62 | 4 | IRPT_BCKEND, IRPT_ANLREQ, IRPT_DASHBD | 9 |
| `_contracts/AnalysisReport.v2.schema.json` | NAMED | 64 | 0 | IRPT_YCDGEN | 2 |
| `reports/resident_installed.py` | REACHABLE | 52 | 4 | IRPT_ANLREQ | 4 |
| `docs/contracts/investor-reporting/v1/ExportBundle.schema.json` | LOADED_BY_GLOB | 51 | 1 | IRPT_BCKEND | 2 |
| `intake/uploads.py` | REACHABLE | 45 | 4 | IRPT_BCKEND | 2 |
| `docs/contracts/investor-reporting/v1/OwnedAnalysisRequestHistory.schema.json` | LOADED_BY_GLOB | 40 | 2 | IRPT_ANLREQ | 2 |
| `ycharts/research/layout_overview.py` | REACHABLE | 38 | 4 | IRPT_YCDGEN, IRPT_ANLREQ | 4 |
| `infra/logic/registry/reporting_policies.json` | NAMED | 37 | 1 | IRPT_ANLREQ, IRPT_YCDGEN, IRPT_BCKEND | 5 |
| `infra/logic/registry/exemptions.json` | NAMED | 36 | 0 | NFRA_CTLPLN | 4 |
| `_scope/interactive_access.py` | REACHABLE | 32 | 2 | IRPT_BCKEND | 1 |
| `_contracts/AnalysisReport.schema.json` | NAMED | 32 | 0 | - | 1 |
| `docs/contracts/investor-reporting/v1/AnalysisReport.schema.json` | LOADED_BY_GLOB | 32 | 0 | - | 1 |
| `ycharts/generate/resident_main.py` | REACHABLE | 26 | 6 | IRPT_ANLREQ | 1 |
| `_scope/canonical_profile_reads.py` | REACHABLE | 15 | 15 | IRPT_BCKEND | 1 |
| `org/standards/NAMING_SCHEMA.json` | NAMED | 19 | 10 | LGIC_BLANKFIX, LGIC_CANON, NFRA_CTLPLN | 5 |
| `ycharts/research/held_data.py` | REACHABLE | 20 | 8 | IRPT_YCDGEN | 1 |
| `reports/retention.py` | REACHABLE | 20 | 6 | IRPT_ANLREQ | 3 |
| `ycharts/generate/durable_job.py` | REACHABLE | 19 | 2 | IRPT_ANLREQ | 1 |
| `docs/contracts/investor-reporting/v1/OwnedAnalysisRequest.schema.json` | LOADED_BY_GLOB | 20 | 0 | IRPT_BCKEND | 2 |
| `infra/logic/registry/scopes.json` | NAMED | 19 | 1 | ADVI_COTBKF, LGIC_CANON, IRPT_DASHBD | 3 |
| `_authz/loaders.py` | REACHABLE | 16 | 2 | IRPT_BCKEND, FIRM_BINDING | 3 |
| `docs/contracts/investor-reporting/v1/ExportReceipt.schema.json` | LOADED_BY_GLOB | 14 | 3 | IRPT_BCKEND | 1 |
| `ycharts/generate/acceptance.py` | REACHABLE | 12 | 3 | IRPT_ANLREQ | 2 |
| `reports/resident_bindings.json` | NAMED | 2 | 10 | - | 0 |
| `reports/composition.py` | REACHABLE | 7 | 1 | IRPT_BCKEND | 2 |
| `ycharts/generate/submission.py` | REACHABLE | 6 | 1 | IRPT_ANLREQ | 1 |
| `infra/logic/registry/resources.json` | NAMED | 0 | 6 | LGIC_BLANKFIX | 1 |
| `docs/contracts/investor-reporting/v1/AnalysisSubmissionRequest.schema.json` | LOADED_BY_GLOB | 5 | 0 | IRPT_ANLREQ | 1 |
| `docs/contracts/investor-reporting/v1/HoldingsSnapshot.schema.json` | LOADED_BY_GLOB | 0 | 5 | MDPF_SECCLASS | 1 |
| `ycharts/generate/recipe.py` | REACHABLE | 3 | 2 | IRPT_BCKEND | 1 |
| `_ids/ids.py` | REACHABLE | 1 | 1 | IRPT_BCKEND | 2 |

## 6. The changed members the resident cannot load

| member | class | projects |
|---|---|---|
| `SHA256SUMS` | NOT_NAMED | - |
| `_contracts/ExportBundle.schema.json` | NOT_NAMED | IRPT_BCKEND |
| `_contracts/ExportReceipt.schema.json` | NOT_NAMED | IRPT_BCKEND |
| `_contracts/HoldingsSnapshot.schema.json` | NOT_NAMED | MDPF_SECCLASS |
| `_contracts/fixtures/ExportReceipt.invalid.json` | NOT_NAMED | IRPT_BCKEND |
| `_contracts/fixtures/ExportReceipt.valid.json` | NOT_NAMED | IRPT_BCKEND |
| `_contracts/fixtures/OwnedAnalysisRequestHistory.invalid.json` | NOT_NAMED | IRPT_ANLREQ |
| `_contracts/fixtures/OwnedAnalysisRequestHistory.valid.json` | NOT_NAMED | IRPT_ANLREQ |
| `_contracts/test_owned_request_contracts.py` | TEST | IRPT_ANLREQ, IRPT_DASHBD |
| `_contracts/test_upload_contract.py` | TEST | IRPT_DASHBD |
| `_ids/data/custodian_key_seam.json` | NOT_NAMED | IRPT_BCKEND |
| `_scope/retained_input_authorizer.py` | NOT_IMPORTED | IRPT_BCKEND |
| `docs/contracts/investor-reporting/v1/responses/analysis-report.response.schema.json` | NOT_NAMED | - |
| `docs/contracts/investor-reporting/v1/responses/analysis-request-read.response.schema.json` | NOT_NAMED | IRPT_BCKEND |
| `ops/entry.py` | NOT_IMPORTED | IRPT_BCKEND, IRPT_ANLREQ |
| `ops/owned_report.py` | NOT_IMPORTED | IRPT_BCKEND, IRPT_ANLREQ, OPAL_ENGINE |
| `ops/pdf_link.py` | NOT_IMPORTED | IRPT_ANLREQ |
| `ops/prospect_dates.py` | NOT_IMPORTED | IRPT_BCKEND |
| `reports/generate_installed.py` | NOT_IMPORTED | IRPT_BCKEND |
| `reports/status_installed.py` | NOT_IMPORTED | IRPT_ANLREQ, IRPT_BCKEND |
| `ycharts/generate/custody_submission.py` | NOT_IMPORTED | IRPT_BCKEND |
| `ycharts/generate/submission_service.py` | NOT_IMPORTED | IRPT_ANLREQ |
| `ycharts/research/file_stop_row.py` | NOT_IMPORTED | NFRA_CTLPLN |

## 7. Rollback

The running root `e606008994-st27`. Its package tar `e606008994-st27.tar.gz` and install script are in
`C:/dev/irpt-release-st27/` on dell2; the tar's sha256 is printed in part 2 beside the staged copy's, read at staging.

## 8. Method limits

- Owning commits are `git log <from>..37210c771a -- <repo path>`, with `<from>` the old base pin 3d705e700f, or the st27
  pin e606008994 for the 11 files the old recipe took from it. The st27 pin is a scratch branch, so for those 11 the
  range over-counts trunk commits whose content st27 already carried by cherry-pick.
- A project is read from commit subjects by pattern; `SHA256SUMS` and `reports/resident_bindings.json` are build outputs
  with no repo path.
- **The import closure is a LOWER BOUND, and an earlier version of this line was wrong.** It said no module is loaded by a
  computed name. Measured on the built package afterwards: `ycharts/generate/resident_main.py:46` loads the runtime with
  `importlib.import_module(module)`, the module coming from the unit's `--factory module:function` argument;
  `lib/opal_naming.py:2337` and `_authz/routetable.py:222` load a file by path (`spec_from_file_location`); and
  `_contracts/opal_naming_runtime.py:8` imports `lib.opal_naming` by a constant string. The closure follows import
  statements and constant-argument `import_module` calls only. So REACHABLE is "at least these"; a member classed
  NOT_IMPORTED may still be loaded by one of those three paths. Part 2 reads each of them before any member is called inert.
