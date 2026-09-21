# MDPF_TAXSMA.TO-TX-b-1 -- result record

**Worker** `0.9.0_WK_MDPF_TAXSMA~2` · **cell** `TX-b-1` (PRD surface S02, FWD-1/3/5/8) · **branch**
`wk-mdpf_taxsma-1-2` in `C:/tmp/wk-taxsma-2` · **cut base** `2aa1e26cbf` (the COO's release commit, G-R
resolved: the `gateway` row is at HEAD in `infra/logic/registry/systems.json`). **Spec:** the PRD @671925aecc
and `org/standards/MDPF_TAXSMA_DATA_CONTRACT.json` v0.5.0, whose enumerations are the only vocabulary used.

Every value below names its instrument, the UTC time it was measured and its denominator.

## 0. G-R, measured at this cell's HEAD (not relied on from the note)

`python -c "import lib.opal_naming as n; n.address('gateway','49financial','bronze','taxsma_workbook',
'date=20260920','abc-def.json')"`, 2026-09-21T03:0xZ, worktree HEAD `2aa1e26cbf`:
`s3://opal-data-assets/gateway/49financial/bronze/taxsma_workbook/date=20260920/abc-def.json` -- resolves.
`grep -n '"key": "gateway"' infra/logic/registry/systems.json` -A15: the row exists at
`infra/logic/registry/systems.json:144-151`, `class: PLATFORM_SUBSYSTEM`. Negative control:
`address('not-a-registered-source', ...)` -> `ValueError: source 'not-a-registered-source' is not a systems.json
key` (discriminates a real resolution from a vacuous one). This is TXB1-AC1's own measurement (below), repeated
here because the order's note named it a premise, not a given.

## 1. What was built

| Path | What | Instrument / evidence |
|---|---|---|
| `data/mdpf/scripts/gold/taxsma_snapshot.py` (new, 287 lines) | the client-side acquirer: `acquire()` (bounded retry + conditional Bronze persist), `SuccessResult`/`FailureResult`, `BronzeStore`/`LocalBronzeStore`/`S3BronzeStore`, `make_default_gateway_call` | `git status --porcelain` (untracked, pre-commit), `wc -l`, 2026-09-21T03:1xZ |
| `data/mdpf/tests/taxsma/test_taxsma_snapshot.py` (new, 21 tests) | one or more tests per criterion, `test_ac1_*` .. `test_ac9_*` | same |
| `deliverables/.../probes/tx_b_1.py` | the criterion probe: runs the matching `-k test_ac<n>_` subset in a fresh subprocess, refuses a 0-selected run as vacuous | same |

**Design, in the contract's own vocabulary where the contract has a term:** a conditional Bronze create is keyed
by `address("gateway","49financial","bronze","taxsma_workbook","date=<YYYYMMDD>","<snapshot_id>-<response_sha256>.json")`
-- the ONE call site (`_bronze_key`, AST-verified: exactly 1 `Call` node named `address` in the whole module).
Because the key already encodes `response_sha256`, byte-identical replay always lands on the same key
(`run_result` = `NO_CHANGE`) and any byte change lands on a different key (a new object, `run_result` =
`COMPLETE`) -- conditional create needs nothing beyond "does this key already exist". ETag, acquisition time and
`response_sha256` are `BronzeStore.put_if_absent`'s separate `metadata` argument, never spliced into `body`.
`acquire()` bounds `gateway_call` to `gateway_total_seconds` (180) across `source_read_attempts` (3), sleeping
`source_backoff_seconds` (1, 3) between attempts via injected `sleep`/`monotonic` callables (so a test proves the
arithmetic on a fake clock, never a real 180-second wait). A `FailureResult` carries one of the contract's 8
`capability.errors` and `last_snapshot_date` (`None`, never a zero-like placeholder, when the store holds no
prior object) -- and no `rows` or membership field exists on the type at all. `LocalBronzeStore` is the pure-Python
harness every test uses; `S3BronzeStore` (real `boto3`, `IfNoneMatch="*"`) and `make_default_gateway_call` (real
`httpx`, the route-only capability bearer) are the production paths, never constructed or called by this cell's
tests (verified by an AST census of the test file's own `Call` nodes, `test_no_live_route_or_s3_call_site_is_
executed_in_this_test_module`).

## 2. Criteria -- 9 of 9 PASS by output

Instrument: `cd C:/tmp/wk-taxsma-2 && timeout 120 py -3.12 org/missions/D8/MDPF/MDPF_TAXSMA/deliverables/0.9.0_WK_MDPF_TAXSMA~2/probes/tx_b_1.py AC<n>`,
run at HEAD `2aa1e26cbf` (pre-commit; the two files under test show as untracked, not dirty-vs-a-committed-blob --
they do not exist at HEAD yet), 2026-09-21T03:17:25Z-03:17:38Z. Each run starts a fresh `pytest` subprocess
filtered to that criterion's own tests, prints `collected=/selected=/passed=/failed=`, and refuses a 0-selected
run as vacuous before printing the `VERDICT:` line; rc 0 on all 9.

| Criterion | Deciding measurement | Denominator |
|---|---|---|
| AC1 | `address(...)` resolves; exactly 1 `address(` `Call` node in the module (AST), inside `_bronze_key` | 2 of 2 tests passed (resolve + refused-unregistered-source negative control) |
| AC2 | stored bytes == received bytes; `sha256(stored) == result.response_sha256` | 1 of 1 test passed |
| AC3 | `metadata["etag"|"acquired_at"|"response_sha256"]` present and correct; none of those 3 keys appear in the parsed stored body | 1 of 1 test passed |
| AC4 | replay -> `NO_CHANGE`, same key; changed bytes -> `COMPLETE`, a different key; store holds 2 objects, not 1 or 3 | 1 of 1 test passed |
| AC5 | all 8 `capability.errors` map 1:1 to `FailureResult.code`, each carrying `last_snapshot_date == "20260910"` from a pre-populated store | 8 of 8 codes (parametrized) + 1 enum-vs-contract cross-check = 9 of 9 tests passed |
| AC6 | `dataclasses.fields(FailureResult)` names have 0 of 4 forbidden names (`rows`, `membership`, `business_active_accounts`, `expected_accounts`) | 1 of 1 test passed |
| AC7 | empty store -> `last_snapshot_date is None`; `None` is checked distinct from `"", "0", "1970-01-01", 0, "19700101"` | 1 of 1 test passed |
| AC8 | 0 of 9 forbidden substrings (`delegated_token`, `delegated token`, `access_token`, `refresh_token`, `msal`, `entra`, `graph`, `token_broker`, `tid/oid`) in the module source, case-insensitive; `capability_bearer` present | 1 of 1 test passed |
| AC9 | stalling stub: 3 of 3 attempts made, `sleep` called with exactly `[1, 3]`; a 2-second `total_seconds` with the same stub makes fewer than 3 attempts (the bound is real, not decorative); `GATEWAY_TOTAL_SECONDS==180`, `SOURCE_READ_ATTEMPTS==3`, `SOURCE_BACKOFF_SECONDS==(1,3)` match `operations.runtime_budget` read live from the contract file | 3 of 3 tests passed |

**Controls.** MUTANT: in the worktree (reverted; `sha256sum` before/after identical,
`e9f98c40ca4984a5d636030277c7ceec665677e731ead913361b2130db37b206`), `_persist_success` was changed to persist
`json.dumps(parsed).encode()` instead of the raw `body` bytes -- AC2's byte-identity assertion fired
(`1 failed, 1 passed` on `-k "test_ac2_ or test_ac3_"`; AC3 stayed green because it checks the metadata sidecar
and body-key-absence, not full-body equality, which is the correct scope for that criterion). Full suite after
revert: `21 passed in 0.06s`. DETERMINISM: AC9 and AC4 each re-run twice, byte-identical `measurement:` and
`VERDICT:` lines both times (no real clock or randomness in the acquire() loop under test).

## 3. Declared exclusions

| Item | Reason |
|---|---|
| Any call to the live `/ms/taxsma-workbook` route, Microsoft Graph, SharePoint or a real workbook read | Forbidden by the order's bounds; every test supplies a synthetic `gateway_call` stub. `make_default_gateway_call` and `S3BronzeStore` are written (production paths) but never constructed or invoked anywhere in the test module (AST-verified). |
| A real S3 `PutObject`/`HeadObject` | Forbidden by the order's bounds; `LocalBronzeStore` (pure Python, in-process) is the harness every test and the proof use. |
| `S3BronzeStore.latest_snapshot_date()` | Raises `NotImplementedError` -- a live S3 listing proof of "the last successful snapshot's date" against real objects is the release cell's (`TX-r-*`), not this acquirer's; no criterion of TX-b-1 requires it, and `LocalBronzeStore.latest_snapshot_date()` (AC5/AC7's actual instrument) is fully implemented and tested. |
| `TX-b-2` (Silver) and any downstream membership/reconciliation logic | Not this cell's writes (decomp s.3: `TX-b-1` writes source evidence and moves no membership). |
| Packaging/deploy of this module into a Lambda or schedule | No criterion here names it; this cell is source-only, matching the `TX-g-1` precedent for its own packaging cell. |

## 4. Commits

LOCAL on `wk-mdpf_taxsma-1-2`, drained by `2.0.0_SA_COO~T`. See COMMITS in the final worker report.
