# MDPF_TAXSMA.TO-TX-m-2 -- result record

**Worker** `0.9.0_WK_MDPF_TAXSMA~2` · **cell** `TX-m-2` (PRD surface S04, FWD-2/6) · **branch**
`wk-mdpf_taxsma-1-2d` in `C:/tmp/wk-taxsma-2c` · **cut base** `c1555c428a` (the COO's working branch CLOUD at
spawn, per the identity line; `TX-m-1` is drained and present at this HEAD). **Spec:** the PRD @671925aecc
and `org/standards/MDPF_TAXSMA_DATA_CONTRACT.json` v0.5.0 (`identity`, `status_axes.identity_status`,
`reason_codes` siblings), whose enumerations are the only vocabulary used. **Input:** `TX-m-1`'s typed
membership module (`data/mdpf/scripts/gold/taxsma_membership.py`) is present at HEAD as this cell's stated
dependency; this cell never imports it, since S04's own acceptance list (TXM2-AC1..AC14) is a pure
classification/join surface over caller-supplied `WorkbookExpectedClaim`/`CustodianRecord` records, not a
Silver/membership reader -- no criterion asks it to read a Silver snapshot or a disposition store.

Every value below names its instrument, the UTC time it was measured and its denominator.

## 1. What was built

| Path | What | Instrument / evidence |
|---|---|---|
| `data/mdpf/scripts/gold/taxsma_reconcile.py` (new) | S04: normalizes/dedupes full account identities (3 accepted forms, 9 rejected forms all -> `INVALID_ACCOUNT`), reconciles an expected claim population against synthetic 0833 custodian records into `EXACT_MATCH`/`MASTER_CONFLICT`/`STRATEGY_CONFLICT`/`MISSING_CUSTODIAN` (never dropping the claim), discovers `UNCONFIRMED` Tax-labelled candidates outside the expected set, checks the 0824 base-population overlap (`BASE_OVERLAP`/`BASE_OVERLAP_UNVERIFIED`, never a silent pass by absence), annotates BD technical enrollment on its own axis, and guards the trading-master role `0804-4932` from ever satisfying the reporting-master check | `git status --porcelain` (untracked pre-commit), this record's own reads |
| `data/mdpf/tests/taxsma/test_taxsma_reconcile.py` (new) | 15 tests: `test_ac1_` .. `test_ac14_` (one per criterion) plus one structural forbidden-call-site test; synthetic account keys only, minted through `_key()` and recorded into `ALL_RAW_KEYS` for the AC14 leak scan | `py -3.12 -m pytest ... -q`: `15 passed in 0.10s` |
| `org/missions/D8/MDPF/MDPF_TAXSMA/deliverables/0.9.0_WK_MDPF_TAXSMA~2/probes/tx_m_2.py` (new) | the criterion probe: one AC per invocation, fresh subprocess, vacuous-pass refused | 14 of 14 `AC1`..`AC14` invocations below |

**Design decisions this cell makes that the contract does not fix (declared, not hidden -- see module
docstring "DESIGN DECISIONS" and s.3 below):**
- `status_axes.identity_status` has no "additional candidate outside membership" outcome; the PRD's own
  prose names it "classify them UNCONFIRMED" (s.3.4). This module uses the local constant
  `CANDIDATE_STATUS_UNCONFIRMED = "UNCONFIRMED"`, kept in its own `DiscoveredCandidate` type so it can never
  be mistaken for a contract `identity_status` value.
- The Tax-strategy label a custodian record must carry to be a "Tax-labelled" discovery candidate is not
  fixed by the contract; `discover_unconfirmed_candidates` takes `tax_strategy_label` as an explicit caller
  argument rather than a hand-kept literal.
- `normalize_account_key` treats "an Excel numeric that lost precision" (AC3) and the contract's plain
  "fractional" rejected form identically: both are a `float` failing `float.is_integer()` -- the contract's
  own wording draws no separate mechanical test between the two.
- Duplicate custodian (0833) records sharing one account key are out of this cell's acceptance list (only
  AC4's *input-side* duplicate raise is graded); `reconcile_expected_population` resolves such a case to its
  first-seen `CustodianRecord`, documented at the call site.
- **AC14's scope** ("no captured log line or ordinary return value contains a full account key") binds the
  RECONCILIATION REPORTING surface -- `reconcile_expected_population`, `discover_unconfirmed_candidates`,
  `base_overlap_check`, `annotate_technical_enrollment` -- matching the PRD's own A02 acceptance line ("No
  private IDs appear in consumer/log outputs"). It does NOT bind `normalize_account_key`/
  `normalize_and_dedupe`, whose entire AC1/AC4-tested job is to return the normalized key itself.
  `base_overlap_check` and `annotate_technical_enrollment` therefore return POSITIONALLY-ALIGNED LISTS, never
  a dict keyed by the full account key: a first draft keyed both by the full key, and the AC14 test itself
  (run against that draft) caught the leak -- 6 of 6 full keys appeared in the returned values. The functions
  were reshaped to the current positional-list design before this record was written, and the AC14 test now
  passes clean (s.2 above).

## 2. Criteria -- 14 of 14 PASS by output

Instrument: `cd C:/tmp/wk-taxsma-2c && timeout 120 py -3.12 org/missions/D8/MDPF/MDPF_TAXSMA/deliverables/0.9.0_WK_MDPF_TAXSMA~2/probes/tx_m_2.py AC<n>`,
run at HEAD `c1555c428a` (3 of the 3 files under test dirty -- new, pre-commit; the same 3 files, unstaged,
committed in this order's own commit below), 2026-09-21T06:0xZ. Each run prints its vintage, its measurement,
its denominator and exactly one `VERDICT:` line; rc 0 on all 14.

| Criterion | Deciding measurement | Denominator |
|---|---|---|
| AC1 | 5 accepted-form fixtures (eight-digit str, ten-digit-00 str, hyphen str, Excel int, Excel float) each normalized to the expected ten-digit key | 5 of 5 |
| AC2 | 9 `rejected_forms` fixtures (masked, last-four, nine-digit, other-length, scientific-notation string, fractional, non-ASCII digits, blank, misplaced separators) each refused `INVALID_ACCOUNT` | 9 of 9 |
| AC3 | Excel-precision-loss float, scientific-notation string, non-ASCII full-width digits -- each refused `INVALID_ACCOUNT` | 3 of 3 |
| AC4 | 2 rows sharing one normalized key -> both `key=None`, `DUPLICATE_ACCOUNT`; 1 non-duplicate row normalized cleanly | 2 of 2 duplicate rows, 1 of 1 clean row |
| AC5 | 1 claim matching a custodian record under `REPORTING_MASTER` (0008335338) with agreeing strategy -> `EXACT_MATCH`, no reason_codes | 1 of 1 |
| AC6 | same key, custodian record under `BASE_MASTER_CONTROL` instead -> `MASTER_CONFLICT`, claim retained in the returned population | 1 of 1 |
| AC7 | matching account, custodian strategy "Growth" vs workbook "Tax-Managed SMA" -> `STRATEGY_CONFLICT` | 1 of 1 |
| AC8 | `is_reporting_master`: trading-master role=False, reporting master=True, base master control=False; a custodian record keyed to the trading-master role -> `MASTER_CONFLICT`, never `EXACT_MATCH` | 3 of 3 guard arms + 1 of 1 reconciliation arm |
| AC9 (difference) | before (no workbook row, `expected_keys=set()`): 1 `UNCONFIRMED` candidate discovered; after (same custodian population, key added to `expected_keys`): 0 candidates | 1->0 |
| AC10 (difference) | no-record arm: claim retained, `MISSING_CUSTODIAN`; record-present arm (same claim): `EXACT_MATCH` | 1 of 1 claim both arms, never dropped |
| AC11 | 2 keys checked against a 2-member base population sharing one key: the shared key -> `BASE_OVERLAP`, the other -> no reason | 1 of 2 overlapping |
| AC12 | `base_population=None` -> both checked keys `BASE_OVERLAP_UNVERIFIED`, never an empty/clean result | 2 of 2, 0 of 2 empty |
| AC13 | 5 claims annotated across ACTIVE/PENDING_RESOLUTION/ABSENT/INACTIVE/UNAVAILABLE (last a roster-absent default); `len(claims)` and `len(annotations)` both 5 before and after | denominator held at 5 of 5 |
| AC14 | 6 synthetic full keys x 2 surfaces (captured INFO log text; `repr()` of every reconciliation-reporting return value) scanned for the raw key strings; 0 leaked, >=1 real log line captured | 0 of 12 (6 keys x 2 surfaces) leaked |

## 3. Controls (schema-required)

- **Mutant** (FIRED-AS-EXPECTED): changed `is_reporting_master`'s final line from
  `return candidate_master == REPORTING_MASTER` to `return True` (after the trading-master-role guard).
  Expected AC6 and AC8 to fail; observed both FAILED (`test_ac6`: `'EXACT_MATCH' == 'MASTER_CONFLICT'`;
  `test_ac8`: `is_reporting_master(BASE_MASTER_CONTROL)` returned `True`). Reverted; re-run 15 passed in
  0.38s.
- **Determinism** (STABLE): AC1 invoked twice back to back via the probe; diffed with the vintage/UTC-time
  and elapsed:/pytest-timing lines stripped -- empty diff, byte-identical otherwise.

## 4. Bounds and scope notes

- Synthetic identities only throughout; no real account number, name or balance in code, fixtures, this
  record or the probe output. Every fixture key is a `_key("135000NN")`-shaped synthetic value.
- No egress off Opal infrastructure, no live route/Graph/SharePoint/BD-roster call, no S3 client construction
  anywhere in the module or its tests (checked structurally by `test_module_has_no_source_mutation_or_forbidden_call_site`).
- No new S3 key or resource name is minted by this cell (the decomp's own artifacts table names no dedicated
  TX-m-2 artifact -- it writes code files only), so no `address()`/`name()` builder call was needed or made.
- `.tools/commit-gate.sh` clean for all 3 new files (`py_compile`, `ds-precommit`, `ruff py39`,
  log-open-lint): `OK: pre-commit gate clean for 3 of 3 file(s)`.
- MDPF Gold suite baseline (bound 17, decomp s.7): `py -3.12 -m pytest data/mdpf/scripts/gold/tests data/mdpf/tests -q`
  -> `171 passed, 3 failed`, the same 3 pre-existing `test_global_fold_flag2.py` failures named in the
  decomposition (`test_carry_within_window_carries_and_labels`, `test_carry_beyond_window_absent_for_real`,
  `test_carry_source_is_measured_never_interpolated`); no new failure introduced by this cell's change.

## 5. Surprises filed

None. No premise failed, no path was missing, and every criterion was satisfiable as written against the
contract and decomposition sections named in this order.
