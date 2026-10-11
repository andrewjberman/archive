# Never-widen sign-off packet -- IB-pr-421: irpt-performance-adapter's fresh vendor path no longer requires an installed one-use plan

Prepared by 0.9.0_WK_IRPT_BCKEND~282 for 2.0.0_SA_COO~P2 (COO half) and 1.0.0_SA_CTO (CTO half), on TO IRPT_BCKEND.TO-IB-pr-421, ordered by 1.0.0_SA_CTO~DELL2 msg 4416 on Andrew-direct 2026-10-09 (`org/tier0_exec/0.0.0_AB_MSTR/deliverables/ANDREW_DIRECT_20261009_024xZ_LAW_EDIT_CLAUDE_MD_EGRESS_OPEN_EXCEPT_BBG.md`). Nothing here was uploaded, deployed or applied: BUILD_ONLY from a committed tree, offline replays against SYNTHETIC data with in-memory fakes, AWS reads only (the live zip, its layers, CodeSha256, S3 versions, the role's policy names, the function's environment variable names). No vendor was called and no Secrets Manager value was read. No client data is in this packet or its files: counts, sha256 and reason codes only.

**READ THIS FIRST.**

1. **This packet WIDENS served output.** Today every fresh performance request from a signed-in Cottonwood or Inflection user ends at `authorization.py` line 90 (`VendorEgressRefused`, public code `OBJECT_NOT_COVERED`) because no operator-installed plan exists (the function's environment carries neither plan variable). After this change an admitted fresh request for either firm builds the firm's vendor transport and CALLS THE VENDOR (Black Diamond for Cottonwood, Orion for Inflection) with the firm's stored credentials, and logs one use row. Who may ask is unchanged (`_authz/`, `_scope/`, `served.py` and `entry.py`'s authorization are untouched); 49 Financial never reaches this path.
2. **The role does not yet permit the whole new path (row `IRPT_BCKEND-D2-W282-S1`).** The use-record write is permitted; the Secrets Manager read of each vendor session is NOT granted, because both grants are `count`-gated on the plan variable in Terraform. Landing Branch A alone therefore changes the failure, not the outcome: the request logs a use row and then the credential read is denied. The IAM change is outside this cell and this packet.
3. **A vendor figure is served once, then a repeat is refused (row `IRPT_BCKEND-D2-W282-S2`).** `retained.py` refuses to reopen a vendor-calculated report by name (batch 66 item 2). Unchanged by this cell; stated so the widening is read with its effect.

## What changed (product commit `cd833e66cb7d7a90e84581eee145a13564e92e71`)

- `performance/authorization.py`: `OneUseTransportFactory` becomes `VendorUseTransportFactory`. The plan, its digest, the expiry, the conditional claim and `environment=` are gone; `IRPT_PERFORMANCE_APPROVED_PLAN` and `IRPT_PERF_VENDOR_EGRESS_AUTHORIZED` are not read on this path. Kept: the packaged-firm check (`firm_paths()`), the vendor requests built from the verified request's firm, its ONE account and the firm's own mapping (so the vendor account id and external id come only from the mapping), `_BoundTransport` (a body that differs from the built requests is refused), and ONE use record per vendor use as a LOG (unconditional put, key `PERFORMANCE_USE#<uuid4 hex>` unique per use, carrying firm, request sha256, requests sha256, mapping revision and time; a failed write refuses egress, never retried).
- `performance/bd_live.py`, `performance/orion_live.py`: the two vendor transports no longer derive from `LiveTransport` and take no per-use token.
- `performance/runtime.py`: builds `VendorUseTransportFactory(table)`.
- `performance/transport.py`: `LiveTransport` and its env-var check remain for the legacy generic live arm only (`default_transport("live")`); the module docstring now says so. `performance/build_tools/cot_probe.py` follows (its token option is removed).
- Tests: new `tests/test_vendor_use_gate.py` (the six named behaviours, 14 tests), `tests/test_authorization.py` rewritten to the new behaviour, `tests/test_bd_live.py` and `tests/test_orion_live.py` changed only where the retired gate made them false.

## Live, built, rollback

| item | value |
|---|---|
| function | `irpt-performance-adapter` |
| live sha256 (CodeSha256) | `9kYLdR64P0p2TEbDXcQu1hrpQ9KtqjPNnFDpoE/W31A=`, last modified 2026-10-11T03:59:40.000+0000 |
| live equals the latest S3 version's `content-sha256` | yes: version `7IkeCAOa8F8IzqgaW1_WCLczFhmtzaLn` of `s3://opal-313476888478-lambda-artifacts/investor-reporting/irpt-performance-adapter.zip`, 445438 bytes |
| built sha256 (CodeSha256 form) | `OF+8j4ucXsxwJ195NKEQZnma22T8bYVUriw9YP859RU=` (hex `385fbc8f8b9c5ecc70275f7934a11066799adb64fc6d8554ae2c3d60ff39f515`, 445481 bytes) |
| built twice identical | YES (two BUILD_ONLY runs, same bytes) |
| rollback S3 version | `7IkeCAOa8F8IzqgaW1_WCLczFhmtzaLn` (re-read at apply: it must still be the version whose `content-sha256` metadata equals the live CodeSha256 at that moment; after Branch A's upload it is no longer the latest) |
| pin | candidate map committed at `247a30072a`; every investor-reporting staged row pinned to the one product commit `cd833e66cb` |

Closure limbs on the built zip (instruments as in IB-pr-416; each run at its own path): name limb `signature_closure calls=185 checked=185 skipped_unpack=0 mismatched=0`; attribute limb `attr_checked=114 attr_mismatched=0`; method limb `method_call checked=272 skipped_unpack=8 not_packaged_method=2721 mismatched=0`. Built: **0 / 0 / 0**. The live zip reads 0 / 0 / 0 on the same instruments.

## Changed members (5 of 71; all inside `performance/`; census `IB119-1_adapter_census.json`)

| member | built | live | owner commit |
|---|---|---|---|
| `authorization.py` | `8e967e21a7f0` | `346be20736ba` | `cd833e66cb` |
| `bd_live.py` | `db907c0d6a5f` | `c815a8ca2b5d` | `cd833e66cb` |
| `orion_live.py` | `4e311bbb2365` | `c39bca88128e` | `cd833e66cb` |
| `runtime.py` | `f7a245ee69a7` | `935d563346c2` | `cd833e66cb` |
| `transport.py` | `b87f88aed5f1` | `4714482707b9` | `cd833e66cb` |

The other 66 rows are re-pinned to the product commit with unchanged bytes (see `candidate_source_map.json`, `_repins_IB_pr_421`).

## Blast radius

- **Function:** `irpt-performance-adapter` only. No other function, layer, IAM, route, schedule, environment variable or table definition changes.
- **Vendor calls now reachable:** per firm. Cottonwood: Black Diamond, 1 session GET plus 2 POSTs (`performancePeriod`, `performanceSeries`) per fresh request, one account. Inflection: Orion, 1 Scope POST per fresh request, one account. Only for a request already admitted by the unchanged authorization, for a firm with a packaged path. 49 Financial: none.
- **Use-record writes:** one `PutItem` per fresh vendor use into the requests table, partition = the verified firm, sort key `PERFORMANCE_USE#<uuid>`; no read of these rows exists in the package. Rollback of the rows: they are inert log rows; none needs deleting for a rollback.
- **Reopen (retained path):** builds no transport and writes no use row (replay arm `cache_hit_no_vendor_call`).

## What the function's role already permits for the new path

Read from Terraform (`infra/aws/terraform/investor-reporting/performance/retained.tf`, `iam.tf`, `lambda.tf`) and the live role; **nothing changed**.

| need of the new path | held? | where |
|---|---|---|
| `dynamodb:PutItem` for the use row, partition = Cottonwood or Inflection | yes | `performance_retained` policy, `ReportAndRetentionIndexInServedFirmPartitions`, LeadingKeys = the three served firms |
| KMS for that table write | yes | same policy, `RequestEncryptionViaDynamoOnly` (`Decrypt`, `GenerateDataKey` via DynamoDB) |
| `secretsmanager:GetSecretValue` on the Cottonwood session secret | **NO** | `performance_approved_session` exists only when `var.approved_performance_plan` names Cottonwood (`count`); the variable is unset; the live role lists 7 policies and none of them reads a secret |
| `secretsmanager:GetSecretValue` on the Orion session secret | **NO** | `performance_approved_inf_session`, same `count` gate |
| outbound network | yes | the function is not in a VPC (`VpcId` null) |

So the new path is not yet complete in IAM. The two session-read grants would have to stop being plan-gated (exact-secret, read-only), by a separate order on the laptop applier's surface (IAM is a surface the Dells cannot write). Row `IRPT_BCKEND-D2-W282-S1`.

## The two environment variables

`IRPT_PERFORMANCE_APPROVED_PLAN` and `IRPT_PERF_VENDOR_EGRESS_AUTHORIZED` are **no longer read** by this path. They are not set on the live function, and `lambda.tf` still declares them behind `var.approved_performance_plan`. Left in place, untouched, for a later cleanup (together with the plan-gated session policies of the previous section).

## Branch A and Branch B

- **Branch A (land it):** from a clean tree at the candidate-map commit `247a30072a` (or a descendant whose `performance/`, `reports/`, `_authz/`, `_scope/`, `_ids/` and `_render_identity/` trees and the candidate's adapter entry are unchanged) with the candidate's `irpt-performance-adapter` entry landed in the source map, `BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-performance-adapter` and compare the printed sha256 to `OF+8j4ucXsxwJ195NKEQZnma22T8bYVUriw9YP859RU=` (ABORT if different), then the same without BUILD_ONLY, then the module's Terraform path (`s3_object_version` + `source_code_hash` only). No IAM, route, schedule, layer or environment change. Before landing, read the IAM section above: without a separate grant the request still fails, at the credential read.
- **Branch B (redeploy the rollback version):** redeploy S3 version `7IkeCAOa8F8IzqgaW1_WCLczFhmtzaLn` of `investor-reporting/irpt-performance-adapter.zip` (CodeSha256 `9kYLdR64P0p2TEbDXcQu1hrpQ9KtqjPNnFDpoE/W31A=`) through the same Terraform path (`s3_object_version` + `source_code_hash`). Re-read at apply: `get-function-configuration` CodeSha256 and that the version's `content-sha256` metadata still equals it. The rollback restores the refusal for every fresh vendor request; use rows already written stay as inert log rows.

## Replay (offline; live zip against built zip; `IB119-1_replay.json`)

17 arms: 15 `identical`, 2 `expected-diff`, 0 other; 6 of the arms are negative controls. Harness: `replay/run_replay_421.py`; the IB-pr-416 runners are used in place and unchanged; the new runner is `replay/vendor_path_runner_421.py` (one tree per process, `python -I`, fakes only).

- IB-pr-416's adapter arms (prospect arms with their controls, enforcer build with its control, no-row-internal enforcer scope, binding cases through the real `entry.ENTRY`, method-call arm): all `identical`.
- `fresh_vendor_path_no_plan` -- `expected-diff`: with neither plan variable set, live refuses `VendorEgressRefused` for 2 of 2 packaged firms (0 use rows, 0 transports); built produces a transport for 2 of 2, the fake transport is sent exactly the provider's built requests (Cottonwood 2 routes, Inflection 1), an altered body is refused, 1 unconditional use row per request.
- `cache_hit_no_vendor_call` -- `identical`: both trees reopen an accepted report with 0 transport constructions, 0 use rows and 0 S3 puts (the reopen of a vendor figure is a named refusal in both trees; row S2).
- Negative control: the built tree with `authorization.py` and `runtime.py` put back to the live bytes refuses again, 2 of 2 firms -- `expected-diff`.
- Hygiene: the only module the runner took from the worktree rather than the zip is the repo's in-memory table fake (`test_retention`).

## What is NOT exercised

- **No real vendor call was made by this cell**, and no Secrets Manager value was read: Black Diamond's token and period/series calls, Orion's Scope call, and both session-credential loads are exercised only against fakes in the tests and the replay.
- No Lambda invocation, no DynamoDB write to the real table, no apply and no upload.
- The credential-read denial in row S1 is read from the Terraform and the live role's policy list, not observed by an invocation.

## Tests

`performance/tests/test_vendor_use_gate.py` and `test_authorization.py` pass (AC1). The whole `performance/tests` directory last line is recorded in the proof instance and the worker report; one failure predates this change and is named in row `IRPT_BCKEND-D2-W282-S3`.

## Rows

- `IRPT_BCKEND-D2-W282-S1` -- the role holds no Secrets Manager read (OBSERVATION, INERT).
- `IRPT_BCKEND-D2-W282-S2` -- a vendor figure is served once, a repeat is refused (OBSERVATION, INERT).
- `IRPT_BCKEND-D2-W282-S3` -- one calendar test fails outside this cell (OBSERVATION, INERT).
