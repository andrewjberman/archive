# Never-widen sign-off packet -- IB-pr-498: irpt-holdings rebuilt from one pin (the HoldingsSnapshot schema copy re-pinned to f91aedd1ef)

Prepared by 0.9.0_WK_IRPT_BCKEND~348 for 2.0.0_SA_COO~P2 (COO half) and 1.0.0_SA_CTO~DELL2 (CTO half), on TO-IB-pr-498 (round 171, amendment 1). **Nothing here was uploaded, applied or deployed**: BUILD_ONLY from the committed tree, offline replays of the packaged schema document, and AWS reads only (one `get-function` and one download of the live zip to scratch). No Lambda was invoked, nobody signed in, no vendor was called. No client data is in this packet or its files: counts, sha256 and reason codes only.

## READ THIS FIRST

1. **The served change, in words. MEASURED, and wider than the order's one-member description.** The packaged schema copy (`contracts/HoldingsSnapshot.schema.json`) differs from the live copy. Structural diff of the two packaged documents (647 leaves built, 557 live): 93 leaves only in the built copy, 3 only in the live copy, 9 differing.
   - (a) ADDITIVE, the change the order names: `nodes[].account_id`, an optional string on ACCOUNT nodes. Nothing is served differently until the builder first writes it.
   - (b) ADDITIVE, NOT NAMED BY THE ORDER: two optional top-level arrays, `class_totals_target` and `security_aggregates_target`. `holdings/snapshot.py:336-343` (`target_admitted()`) reads the packaged copy's own properties, and `holdings/snapshot.py:562` serves both blocks only when the request carries `include=target`. The live copy admits neither, so `include=target` serves no TARGET block today. On the built copy `target_admitted()` is True, so the apply would start serving them.
   - (c) NARROWING, NOT NAMED BY THE ORDER: `multi_asset` is absent from the `asset_class` enums of `nodes`, `class_totals` and `security_aggregates` (the live copy admits it in all three). No code under `holdings/` (non-test) names `multi_asset`. Whether the builder writes it is unmeasured here; the live pin's commit subject says no row carried it yet.
   - No figure moves in any arm of this packet. The replay arms validate the schema document only; they do not exercise (b) or (c).
2. **The serve path reads the schema differently from the order's Why (surprise row IRPT_BCKEND-D2-W348-S4).** At serve the packaged copy is read for property presence only: `load_contract()` (`snapshot.py:104-112`), `aggregates_admitted()` (`:223-231`) and `target_admitted()` (`:336-343`). `jsonschema` runs only in `validate_slice()` (`:115-137`), and its callers are tests (`tests/test_snapshot.py:315`, `tests/test_aggregates.py:168` and `:196`, `tests/test_target_fold.py:82`). Whether any other code refuses a served `account_id` is unmeasured here.
3. **The latent attribute mismatch (row IRPT_BCKEND-D2-W348-S1, ruled not a stop).** The packaged `_authz/served.py` (pin 74a62fb346c) sets `render["load_report_owner"]` and passes it to `enforce.Enforcer`, whose packaged copy (pin 21eca74f40) has no such keyword. The instrument reads it on the built zip and on the live zip alike (`ATTR_MISMATCH served:856`, attr_mismatched 1 on both). It is unreachable in this function: `holdings/entry.py:22` imports `served`, no non-test file under `holdings/` names `render_ports` (native Grep, 0 matches), and `served.py` sets the key only inside `if self.render_ports is not None`. Its repair is a SEPARATE later cell (the issuer's), not made in this release.
4. **The red list reads differently from the order (row IRPT_BCKEND-D2-W348-S3).** The changed member's repo path lies under the red-list target prefix `docs/contracts/investor-reporting/`. It names no red operation. `pytest _contracts -rf` at the worktree HEAD (the same docs bytes) reads 4 failed, 201 passed, not the 2 the r278 red list names. See the section on the red list.

## Base, pin and the two zips

| item | value |
|---|---|
| base_commit (HEAD before the first build commit; the branch's parent of a6fe8afec6) | `f91aedd1efd0ea1f36966593fbf949595e49737e` |
| pin_commit (the tree the schema copy is taken from) | `f91aedd1efd0ea1f36966593fbf949595e49737e` |
| function | `irpt-holdings` (the source map row for `docs/contracts/investor-reporting/v1/HoldingsSnapshot.schema.json`) |
| built sha256 (zip, hex) | `c07833d87d366dc921188956441bc6a35450fa832011b452988ec4c7e5b97452` (CodeSha256 `wHgz2H02bckhGIlWRBvGo1RQ+oMgEbRSmI7Ex+W5dFI=`, 299747 bytes) |
| built twice, byte-identical | YES: two packs this session, both `c07833d8...` (the inherited build record agrees) |
| live sha256 (zip, hex, `Code.Location` downloaded to scratch) | `49645f51f1dd25aaced9185bc70fca40af3c0de0cda2b42e8e4691d6352e65cd` (CodeSha256 `SWRfUfHdJarO2Rhbxw/KQK88DeDNorQujkaR1jUuZc0=`, 299273 bytes; equals the source map row's `artifact_sha256`) |
| real `lambda-source-map.json` sha256 before / after the builds | `a8c55c584d0f346bbf552dad63871a040e8eb12a8774d613ccf160126b739987` / same (byte-identical) |
| members, built / live | 36 / 36; only in one zip: none |
| changed members vs live | 1 of 36: `contracts/HoldingsSnapshot.schema.json` |
| staged rows whose built member equals the repo blob at the pin | 35 of 35 |

| changed member | built member sha256 | repo blob sha256 at the pin | live member sha256 |
|---|---|---|---|
| `contracts/HoldingsSnapshot.schema.json` | `5d9e7fe165e2326fc4d56ae0bad1836138a65e7154dd41ecc8223b52e35cc738` | `5d9e7fe165e2326fc4d56ae0bad1836138a65e7154dd41ecc8223b52e35cc738` | `fde5dd4171793c7f3410ba4198cf5431791335e8ff054fa1dd02d8ae28dddf76` |

Signature instrument `deliverables/0.9.0_WK_IRPT_BCKEND~278/signature_closure_attr.py` (both limbs, run with `-I` on each zip's own bytes):
- built: `signature_closure calls=42 checked=42 skipped_unpack=0 mismatched=0 attr_skipped_unpack=0 attr_checked=57 attr_mismatched=1` (rc 1), with one line `ATTR_MISMATCH: served:856 calls enforce.Enforcer -- unknown keyword(s) ['load_report_owner']`
- live: the same last line and the same single ATTR_MISMATCH line
- signature mismatches 0 on both; the built attribute list is a subset of the live list (equal here). Full record: `IB171-3_release_census.json`.

## Branch A -- land it (digest-gated, never a mint)

1. Open the NEVER-2 ledger entry under `org/critical_paths/change_management/` before any change, and commit its `.open_deploys` sentinel at once. It names every task family that pulls `irpt-holdings.zip`. The same schema copy is also staged by `irpt-ycharts-generate`; that function is NOT moved by this order and waits for the IRPT_ANLREQ reader release.
2. **START READ:** `get-function-configuration` CodeSha256 must equal `SWRfUfHdJarO2Rhbxw/KQK88DeDNorQujkaR1jUuZc0=`. Anything else: STOP, no apply.
3. Land the single re-pin into `infra/aws/lambda/ci/lambda-source-map.json`: the `irpt-holdings` row for `docs/contracts/investor-reporting/v1/HoldingsSnapshot.schema.json` only, `pin` `4cc72587d6336809adbb3a46b119a304ef0a6dff` to `f91aedd1efd0ea1f36966593fbf949595e49737e`, `sha256` `fde5dd4171793c7f3410ba4198cf5431791335e8ff054fa1dd02d8ae28dddf76` to `5d9e7fe165e2326fc4d56ae0bad1836138a65e7154dd41ecc8223b52e35cc738`. Nothing else in the map changes (the candidate map in this folder is that exact edit).
4. `BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-holdings`; the printed sha256 must equal `wHgz2H02bckhGIlWRBvGo1RQ+oMgEbRSmI7Ex+W5dFI=` (hex `c07833d8...452`). **ABORT on any difference: never upload a different digest than the one signed, never mint a new artifact in place of it.**
5. Then the same without BUILD_ONLY (upload), then the function's Terraform path (`infra/aws/terraform/investor-reporting/holdings/lambda.tf`, resource `module.irpt_holdings.aws_lambda_function.this`): `s3_object_version` and `source_code_hash` only; a plan to a planfile showing 1 change and 0 to destroy; apply with `bash .tools/safe-apply.sh`. No IAM, route, schedule, layer, environment or table change.
6. **ORDER CONDITION:** this apply lands BEFORE the builder first writes `account_id` (CTO ROUND-171 analysis, row D2-W344-S1). **And BEFORE the pair has decided (b) and (c)** of READ THIS FIRST item 1.
7. After: live CodeSha256 equals the built value; re-plan shows 0 changes; the direct proof below; close the ledger entry.

## Branch B -- restore the live version (rollback)

- **What is restored:** the live code, CodeSha256 `SWRfUfHdJarO2Rhbxw/KQK88DeDNorQujkaR1jUuZc0=` (hex `49645f51...65cd`), which equals the `artifact_sha256` of the source map at HEAD.
- **Named and re-read at apply:** the S3 object version of `investor-reporting/irpt-holdings.zip` whose content-sha256 equals that CodeSha256 is NOT read here (an S3 version listing is outside this order's allowed AWS calls). The apply worker names it at step 1 of Branch A, BEFORE any upload, writes it into the ledger entry, and re-reads at restore time that the live CodeSha256 is still the built value and that version is still addressable.
- **Rollback per key:** one key, `investor-reporting/irpt-holdings.zip`, redeployed through the same Terraform path (`s3_object_version` and `source_code_hash`), never a console edit and never `aws lambda update-function-code`. Then CodeSha256 equals the live value and the re-plan is 0 changes. Nothing else is moved, so nothing else is restored.
- **Served values on restore:** `include=target` stops serving the TARGET blocks (b) and the multi_asset admission returns (c); no figure moves either way. Whether stored documents carry the new member or the removed enum value is not measured here.
- **Trigger:** a 5xx or `TypeError` in the function's log group after the apply; a direct-invoke arm below that fails; a figure that differs from its before-read; or any `include=target` response carrying a TARGET block before the pair has signed (b). Restore at once.

## The ADDENDUM 18 red list

- The r278 red list (`deliverables/0.9.0_WK_IRPT_BCKEND~278/IB117-1_red_list.json`) names `target_prefixes` `infra/aws/lambda/investor-reporting/_contracts/` and `docs/contracts/investor-reporting/`, the red operation `analysis-request-original`, and 2 failed nodes at its base.
- **This member touches a target prefix.** Its repo path `docs/contracts/investor-reporting/v1/HoldingsSnapshot.schema.json` lies under `docs/contracts/investor-reporting/`. So the order's line "your member touches none of its targets" does not hold as written (row IRPT_BCKEND-D2-W348-S3). The member names no red operation, and no path in this cell's changed set names `analysis-request-original`.
- **Measured:** `python -m pytest _contracts -rf` from `infra/aws/lambda/investor-reporting/` at the worktree HEAD (which carries the same docs bytes as the candidate): **4 failed, 201 passed** in 7.08s. The FAILED nodes: `test_every_declared_route_has_a_response_contract_whose_refs_resolve` and `test_control_a_known_good_document_conforms_and_a_known_bad_one_does_not[analysis-request-original]` (both in the r278 list), plus `test_the_consumer_fixture_source_is_named_and_non_empty` and `test_the_operation_map_covers_the_consumers_own_denominator` (not in the r278 list). The last two were NOT measured against the live docs bytes, so their cause is not established here.
- The packet does not cite "suite green". The pair decides whether this reading is acceptable for the apply.

## The replay arms (offline; jsonschema Draft 2020-12)

Instance: the `instance` key of `infra/aws/lambda/investor-reporting/_contracts/fixtures/HoldingsSnapshot.valid.json`. Schema: each zip's packaged `contracts/HoldingsSnapshot.schema.json`. Script: `replay_arms_498.py` in this folder. Record: `IB171-3_replay_arms.json`.

| arm | built verdict | live verdict (contrast) |
|---|---|---|
| node with `account_id` (a) | valid | refused (1 error) |
| node without `account_id` (b) | valid | valid |
| node with `unknown_member` (c) | refused | refused |

Bound counters, all 0: `served_figures_changed`, `functions_invoked`, `sign_ins_made`, `aws_writes_made`, `accounts_written`, `figures_written`, `vendor_requests_sent`. These arms test the schema document only (see READ THIS FIRST item 2) and never test `include=target` or `multi_asset` (item 1 b and c).

## The consumers of `contracts/HoldingsSnapshot.schema.json` inside irpt-holdings (one read-through each; cites at `f91aedd1ef`)

| cite | reads | read-through |
|---|---|---|
| `holdings/snapshot.py:63` | `CONTRACT_NAME = "HoldingsSnapshot.schema.json"` | the packaged name; the staged member is `contracts/` + this name |
| `holdings/snapshot.py:84-101` | `_contract_candidates()`: `CONTRACTS_DIR`, then `_HERE/contracts` (the packaged copy, `/var/task/contracts` at runtime), then `/opt/python/irpt_contracts`, then `_HERE.parent/_contracts`, then the repo docs path | the packaged copy is the first file found in the zip; the comment at `stage.py:72` says the layer is first, which the code does not do (noted, not changed) |
| `holdings/snapshot.py:104-112` | `load_contract()`: the one reader; the first candidate that is a file | returns the packaged copy in the built and live zips |
| `holdings/snapshot.py:115-137` | `validate_slice()`: `jsonschema.Draft202012Validator` over the slice body | called by tests only (`tests/test_snapshot.py:315`, `tests/test_aggregates.py:168,196`, `tests/test_target_fold.py:82`); no runtime path calls it (S4) |
| `holdings/snapshot.py:223-231` | `aggregates_admitted()`: reads `properties` for `security_aggregates` and `class_totals` | admitted on both copies; unchanged by the re-pin |
| `holdings/snapshot.py:336-343` | `target_admitted()`: reads `properties` for `security_aggregates_target` and `class_totals_target` | False on the live copy, True on the built copy (item 1 b) |
| `holdings/snapshot.py:556` and `:562` | `project()`: the aggregates when admitted (556); the TARGET blocks when `include` holds `target` and `target_admitted()` (562) | the served change of item 1 (b) |
| `holdings/entry.py:61-64` and `:86` | `requested_includes()` reads the `include` query; passed to `project()` | the request side of `:562` |
| `holdings/tests/test_snapshot.py:391` and `:403` | `load_contract()` under `CONTRACTS_DIR` | test-only |
| `holdings/stage.py:74-77` | the stage script's own `CONTRACTS` tuple (repo path, packaged name) | a writer's tuple; the build reads the source map's `staged_from` row, which is the one this order moves |

## Direct proof, to run AFTER the apply (by `0.7.0_AE_CloudOps~IB2`, not by this worker)

1. The order's instrument: the function's own validator, `snapshot.validate_slice()`, run in a harness on the valid fixture with and without `account_id`, expecting `valid` on both. No live data. **Caveat (S4):** this reads the packaged copy and does not exercise the serve path.
2. The serve-path arm, which the apply order must name: one direct `aws lambda invoke` of the DEPLOYED function, one READ operation, an Opal principal, the function's own role, no new grant. Two requests: without `include`, and with `include=target`. Each is read before the apply and after. Expected after the apply: the figures unchanged (record a sha256 of each figure, never the figure); the `include=target` response carries a TARGET block only if the pair has signed item 1 (b).
3. Account ids stay in the invoker's scratch and out of the repo.

## Blast radius

- **Function:** `irpt-holdings` only. `irpt-ycharts-generate` stages the same schema copy and is not moved by this order.
- **Member:** `contracts/HoldingsSnapshot.schema.json` only (1 of 36).
- **Served effect:** per READ THIS FIRST item 1: (a) nothing until the builder writes `account_id`; (b) `include=target` serves two TARGET blocks; (c) `multi_asset` is no longer admitted by the three enums.
- **Never-widen:** (b) widens a served surface and (c) narrows an admitted set. The packet ships only under the pair below.

## The pair

Both halves sign the same facts: built `c07833d87d366dc921188956441bc6a35450fa832011b452988ec4c7e5b97452`, live `49645f51f1dd25aaced9185bc70fca40af3c0de0cda2b42e8e4691d6352e65cd`, one changed member `contracts/HoldingsSnapshot.schema.json`, and the served change in READ THIS FIRST item 1 (a), (b) and (c). A half that signs different sha256 values, or omits (b) or (c), is void.

- **COO half -- `2.0.0_SA_COO~P2`:** signs the served change as read here, including (b) and (c), which the order did not name; and that the apply order carries the Branch A digest gate, the Branch B restore and the rollback, and the order condition. Signed: ______________________  at: ____________
- **CTO half -- `1.0.0_SA_CTO~DELL2`:** signs the served change in words, the red-list reading (S3), and the choice of Branch A. Signed: ______________________  at: ____________

## Rows

- `IRPT_BCKEND-D2-W348-S1` -- the latent attribute mismatch in `served.py` against `enforce.py` (pre-existing; ruled not a stop). BLOCKING, ARMED, disarm owner `2.0.0_SA_COO~P2`.
- `IRPT_BCKEND-D2-W348-S2` -- the schema copy also admits the two opt-in TARGET blocks and drops `multi_asset` from three enums. BLOCKING, ARMED, disarm owner `2.0.0_SA_COO~P2`.
- `IRPT_BCKEND-D2-W348-S3` -- the red-list reading: the member is under a target prefix; the suite reads 4 failed. BLOCKING, ARMED, disarm owner `2.0.0_SA_COO~P2`.
- `IRPT_BCKEND-D2-W348-S4` -- the serve path reads the schema for property presence; `validate_slice` is test-only. OBSERVATION, INERT.

Files beside this packet: `IB171-3_release_census.json`, `IB171-3_replay_arms.json`, `candidate_source_map_498.json`, `census_498.py`, `replay_arms_498.py`, `schema_delta_498.py`.
