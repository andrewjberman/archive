# IRPT_BCKEND.TO-IB-rtc-9: runners validate under the host's jsonschema (result)

**Assignee:** `0.4.0_DS_ClientPlatform~X` | **Issuer:** `2.0.0_SA_COO~B` | **Worktree:** `/c/tmp/wk-irpt-3-ds5`
(branch `wk-irpt_bckend-3-ds5`, cut @ea3fa54c2b) | **Cut on row:** `IRPT_BCKEND-W2-S56` | **Written:** 2026-09-18

## What was done

Both gold runners called a jsonschema API that the MDPF host lacks:

| Runner | 4.x-only calls |
|---|---|
| `directory_runner.py` | `jsonschema.Draft202012Validator` and `ValidationError.json_path` |
| `holdings_snapshot.py` | `jsonschema.Draft202012Validator` |

`Draft202012Validator` arrived in jsonschema 4.18.0 and `json_path` in 4.0.0; the host has 3.2.0. The fix is in the
callers, in the DS lane, as the order directs. The contracts are unchanged, and nothing on the host was installed or changed.

| Commit | What |
|---|---|
| `de4e176cc3` | The two runner edits and `tests/test_runner_jsonschema_tolerance.py` |
| `163c3bf7b0` | Change-management entry `irpt-bckend-rtc9-jsonschema-mint` OPENED, with its sentinel committed before the act. This is the tree the guard packed. |
| (act) | `HALT_ACK=1 bash .tools/safe-deploy.sh --mint-bundle investor_reporting`, 2026-09-18T07:58:33Z |
| `dfdd58a2a6` | Entry CLOSED, 2 of 2 legs proven and the sentinel removed, committed before the grading reads |
| `0101c370c9` | Battery `battery_ib_rtc_9.py` + row `IRPT_BCKEND-S71` |

### The fix (arm a)

Each runner gains two helpers, **duplicated verbatim** in both files. A shared module would be a new bundle member,
which means a guard edit outside this order's paths. A test checks that the two copies are identical by AST.

- `contract_validator_class()` returns `vars(jsonschema).get("Draft202012Validator") or jsonschema.Draft7Validator`.
  - It uses `vars()`, not `getattr(..., None)`, because jsonschema 4.x defines a module-level `__getattr__`.
  - Once the name is removed from the module, that `__getattr__` raises `NameError`, not `AttributeError`, and a `getattr` default cannot catch that.
  - The mutant-environment test found this: the `getattr` form crashed under `monkeypatch.delattr`.
- `error_path(err)` builds the JSONPath from `absolute_path`, which exists in 3.2.0.
  - On 4.x it renders the same text as `json_path`; the test checks this on the real invalid fixture.
  - `validate_entries()` now uses it in place of `json_path`.
  - `validate_snapshot()` error lines now also start with their path. Before, they carried the message only, and the
    order wants "refused with a path" for both. Accept and reject are unchanged, and the lines go only into the run's
    `schema_errors` result field, never into the landed snapshot.

### The test (arm b)

`data/assets/scripts/gold/investor_reporting/tests/test_runner_jsonschema_tolerance.py`, 6 tests:

- **(i) AST walk.** Over the bundle's 7 runtime `.py` members, read from the guard's declaration: 0 attribute
  references to `Draft202012Validator`, `Draft201909Validator` or `json_path`. The 2020-12 name appears only as the
  string key inside `contract_validator_class`, once per runner. The two helper copies are AST-identical.
- **(ii) Real contracts, real fixtures.** Valid documents are accepted; invalid ones are refused, and the error line
  names the path (`entry[0] $.cohort.fee_taking_status: ...` and `$.nodes[0].classification.fee_taking_status: ...`).
  On 4.x, `error_path == json_path` for every error.
- **(iii) Fallback branch.** With `monkeypatch.delattr(jsonschema, "Draft202012Validator")`, both runners choose
  `Draft7Validator` and grade (ii) identically. A mutant that hard-codes `jsonschema.Draft202012Validator` fails
  (`NameError` on 4.x, `AttributeError` on 3.2.0).
- **Whole directory suite:** 68 of 68 pass (62 existing plus 6 new); collected equals passed.

## The minted object (R-40 identities)

| Item | Before (IB-rtc-8's mint) | After (this cell) |
|---|---|---|
| key | `s3://opal-data-mdpf/code/scripts/assets_gold/investor_reporting/investor-reporting.tar.gz` | same key |
| VersionId | `q8myxeHdNw48w1uDb7YTcBh8DHV9TzU2` | `0XLkiPt4wljdniLnF2fkPKN4qAIkjUbc` |
| ETag | `479af04c0a3a1eb6651707b340df9926` | `4c942a76f990874838e33e37f24ed69a` |
| sha256 (downloaded) | `0bd71b5f1f5c8b4204096dbcd765b77b241250201357d92d228f90094f814758` | `e2a933b923d50626578969b3544e070161f029bdb4132b6f600db66859504b3b` (61540 bytes) |
| `directory_runner.py` | sha256 `a16b5396...` | git blob `30ffce2eff13eba7eaf64deddfde675fdb6dc772`, sha256 `95bd6043c7bca2ab04a28f55175e0af40d9eccf34b9558c72f6a9a8364045360` |
| `holdings_snapshot.py` | sha256 `2afde9ae...` | git blob `46faa8a93b8a82b0b97b7470579dca6f9db9e755`, sha256 `ce063c4188c52d1a1ed28d9be607ae548e5de0ba99e6d21b9dd57953480e9b29` |
| other 7 stamps | -- | unchanged, 7 of 7 |

## R39-AC1: the battery

- **Invocation:** `timeout 900 py -3.12 org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.4.0_DS_ClientPlatform~X/battery_ib_rtc_9.py`
- **Where it ran:** from a fresh detached checkout at `0101c370c9`.
- **Result:** rc=0, `R39-AC1: 4 of 4 graded arms PASS`, `IBR39-RUNNERS-VALIDATE-UNDER-HOST-JSONSCHEMA`.
- **Determinism:** identical to the authoring-worktree run, 72 lines each, once paths, times and SSM ids are masked.
- **Recorded output:** `IB-rtc-9_R39-AC1_battery_output.txt`.

| Arm | Result | Deciding evidence |
|---|---|---|
| (a) AST WALK | PASS | The walk reads the **served** tarball: 9 members, 7 of them `.py`, all 7 walked. Attribute references to the three names: 0. String references: 2, both in `contract_validator_class`. Difference control: the same walk over the pre-cell tarball finds 3 (`directory_runner.py:804 .Draft202012Validator`, `:810 .json_path`, `holdings_snapshot.py:1157 .Draft202012Validator`). |
| (b) SUITE | PASS | 68 passed, 68 collected. The three code files at HEAD are the same blobs as `de4e176cc3`. Fallback: `Draft7Validator`, grades identical to native `True`. Mutant: `NameError` on both calls. |
| (c) RE-MINT | PASS | The minted version is pinned by id: md5 == ETag. The closure is 8, unchanged from IB-rtc-8, and the new test file is not a member. `source-repo-paths` names 8 of 8. Both edited members' tarball bytes equal their blobs at `de4e176cc3`, `163c3bf7b0` and `dfdd58a2a6`; stamp == sha256; each moved off the pre-cell bytes. The other stamps equal the pre-cell object's, 7 of 7. Negative control against `479af04c` / `q8myxeHd`: the ETag differs and the VersionId differs. Distribution legs: `CONSISTENT: 3 of 3`, with 0 commits to them in `ea3fa54c2b..dfdd58a2a6`. |
| (d) HOST | PASS | SSM `7f9333d4-3cdc-4356-ab58-1fc616422382` on `i-02448edb624a7a7cf`, running and Online, so no StartInstances. See the host detail below. |

**Host detail, arm (d):**

- **Environment:** jsonschema **3.2.0**, with no 2020-12 class. The host's sha256 of the served key equals the minted
  version's. All 9 members were extracted at repo shape: IMPORT-OK 7 of 7 `.py`, LOAD-OK 2 of 2 `.json`.
- **New members:**
  - DirectoryEntry valid: `[1, []]`
  - DirectoryEntry invalid: `[0, ["entry[0] $.cohort.fee_taking_status: 'CLIENT' is not one of [...]"]]`
  - HoldingsSnapshot valid: `[true, []]`
  - HoldingsSnapshot invalid: `[false, ["$.nodes[0].classification.fee_taking_status: 'CLIENT' is not one of [...]"]]`
  - Totals: valid accepted 2 of 2; invalid refused with a path 2 of 2.
- **Positive control:** the pre-cell members raise `AttributeError: module 'jsonschema' has no attribute
  'Draft202012Validator'` on all 4 calls (`validate_entries` 2 of 2, `validate_snapshot` 2 of 2). That is the same
  interpreter in the same SSM command.
- **Network:** 0 events for both trees, and the positive control fired for both. No firm build was run and no source bucket was read.
- **Supplied to the host, each sha256-matched on arrival (6 of 6):**
  - the pre-cell tarball, because the host role has no `s3:GetObjectVersion`;
  - the four fixtures, which are not bundle members;
  - the HoldingsSnapshot contract the bundle does not carry (row S71).
  - They were shipped as 6 base64 chunks over SSM, not through a signed URL (bound 6).

## Row filed

**`IRPT_BCKEND-S71` (OBSERVATION, INERT).**

- `holdings_snapshot.py` reads `docs/contracts/investor-reporting/v1/HoldingsSnapshot.schema.json`: blob `9ec70af2`,
  34577 bytes.
- It does not read `_contracts/HoldingsSnapshot.schema.json`, the copy the face censused: blob `95e4d500`, 26022
  bytes. These are different files.
- The draft-7 claim still holds for the file it reads: 0 of the 11 `docs/contracts/v1` schemas use a
  2019-09/2020-12-only keyword, a `$ref` or an array-form `items`.
- **The bundle does not include that file.** So `holdings_snapshot.py` run from the bundle on the host raises
  `FileNotFoundError` at `load_contract()`, with or without this fix. The `irpt-holdings-snapshot` schedule is
  DISABLED, so nothing reaches it today.
- It is not fixed here: adding a member is a guard edit, outside this order's paths.

## R39-AC2: judgment, recorded for `3.0.0_SA_CVO`, no verdict

**1. Does the validator the host now runs grade the two contracts the way the intended 2020-12 validator would?**

The contracts the runners actually read are:
- `directory_runner.py`: `infra/aws/lambda/investor-reporting/_contracts/DirectoryEntry.schema.json`
- `holdings_snapshot.py`: `docs/contracts/investor-reporting/v1/HoldingsSnapshot.schema.json` (row S71)

Two instruments were used:

- **Keyword census** over both directories, 22 schemas. It includes those two, which have 139 and 391 keys walked:
  - 0 uses of a 2019-09/2020-12-only keyword (`prefixItems`, `$defs`, `unevaluatedProperties`, `unevaluatedItems`,
    `dependentRequired`, `dependentSchemas`, `$dynamicRef`, `$dynamicAnchor`, `$anchor`, `contentSchema`,
    `minContains`, `maxContains`, `$recursiveRef`, `$recursiveAnchor`, `$vocabulary`);
  - 0 `$ref` (draft 7 ignores keywords next to a `$ref`, and 2020-12 does not);
  - 0 array-form `items`;
  - 0 draft-7-only keywords (`dependencies`, `additionalItems`, `definitions`).
- **Behavioural comparison:** `Draft7Validator` and `Draft202012Validator` (jsonschema 4.26) on every fixture
  instance of every contract in both directories. They agree on **46 of 46** instances: the same error count, and
  the same (path, validator, message) set.

Limits:
- The fixtures carry 0 or 1 error each, so the behavioural check discriminates on one refusal per contract.
- `format` is annotation-only in both classes as called; neither run passes a format checker.

On the host, the draft-7 class is jsonschema **3.2.0**'s `Draft7Validator`, not 4.26's. The host arm shows it
accepting and refusing the same four fixtures.

**2. Does any other bundle or Lambda member in this project carry a jsonschema-4.x-only call?**

The AST census (attribute references to `Draft202012Validator`, `Draft201909Validator`, `json_path`) walked two
populations:

- **The bundle package, `data/assets/scripts/gold/investor_reporting/**`: 7 `.py` files.** The 5 runtime `.py`
  members outside it (three `runner_common.py`, `_ids/ids.py`, `lib/trading_calendar.py`) were walked by arm (a) on
  the served bytes: 0 hits in the 7 served `.py` members.
  - The only hits in the package are in the new test file: `:128 .json_path` and `:146 .Draft202012Validator`.
  - Both are deliberate: the first sits behind a `hasattr` guard that skips it on 3.x, and the second is the mutant.
  - That test is not a bundle member and runs on the local 4.26.
- **The Lambdas, `infra/aws/lambda/investor-reporting/**`: 98 `.py` files, 8 importing jsonschema.** There are 13
  attribute hits:
  - **6 in production modules:**
    - `export/bundle.py:82`
    - `holdings/snapshot.py:119`
    - `narrative/handler.py:74`
    - `performance/normalize.py:390` and `:398`
  - **7 in test files.**
  - The four functions those production modules serve (`irpt-export-render`, `irpt-holdings`, `irpt-narrative`,
    `irpt-performance-adapter`) each carry the layer `irpt-common:5`. That layer's `requirements.txt` at this tip
    pins `jsonschema==4.26.0`, where those names exist.
  - `intake/parse.py` imports jsonschema with no 4.x-only reference, and `irpt-intake-poller` carries no layer.

**Not walked:**
- the installed contents of the deployed layer `irpt-common:5` (I read its `requirements.txt` at the tip, not the
  published zip);
- each Lambda's deployed zip;
- any Python outside those two trees that validates IRPT contracts.
