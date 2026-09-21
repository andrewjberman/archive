# MDPF_TAXSMA.TO-TX-m-4 -- result record

**Worker** `0.9.0_WK_MDPF_TAXSMA~2` · **cell** `TX-m-4` (PRD surface S05, FWD-3/4/5/8) · **branch**
`wk-mdpf_taxsma-1-2e` in `C:/tmp/wk-taxsma-2c` · **cut base** `5cc9756554` (the COO's working branch CLOUD at
spawn, per the identity line; `TX-m-2` is drained and present at this HEAD, along with `TX-m-1`,
`taxsma_workbook.py` and `taxsma_snapshot.py`). **Spec:** the PRD @671925aecc and
`org/standards/MDPF_TAXSMA_DATA_CONTRACT.json` v0.5.0 (`valuation`, `membership.date_comparison`,
`categories.source_basis` and `reason_codes` siblings), whose enumerations are the only vocabulary used.
**Input:** `TX-m-1`'s `data/mdpf/scripts/gold/taxsma_membership.py` (its `DispositionStore`,
`resolve_date_status`, `AUTOMATIC_DISPOSITION_KINDS`, `REASON_TRADED_EVENT_ORDER_CONFLICT`,
`REASON_TRADED_HISTORY_UNVERIFIED`) is imported directly -- this cell delegates the membership-interval
question to that already-tested function rather than re-implementing a date comparison. `TX-m-2`'s
`taxsma_reconcile.py` is present at HEAD as this cell's stated dependency but is NOT imported: its
reconciliation-reporting surface deliberately returns only `mask_account_key()`'s masked label (its own
AC14), while Gold's `account_key` field is the validated FULL canonical form -- so this cell defines its own
`ExpectedAccountInput` shape (declared design decision, module docstring) rather than consuming TX-m-2's
`ReconciledIdentity` directly. `b00_canonical_valuation.py` is read only as a schema reference
(`account_id`/`business_date`/`net_mv_plus_cash`); no pandas DataFrame or live partition is read -- this
cell's own `CanonicalValuationRow` mirrors that schema over synthetic fixtures.

Every value below names its instrument, the UTC time it was measured and its denominator.

## 1. What was built

| Path | What | Instrument / evidence |
|---|---|---|
| `data/mdpf/scripts/gold/taxsma_assets.py` (new) | S05: emits one `ObservationRow` per expected account per (valuation_date, knowledge_date) carrying exactly the 22 `valuation.history_fields`; joins to b00 canonical_valuation by (account_id, business_date) to the cent as `Decimal`, refusing a missing (`CANONICAL_MISSING`) or duplicate (`CANONICAL_DUPLICATE`) canonical row; accepts and discards the 7 `rejected_substitutes`; splits expected/covered/unresolved with the pre-filter denominator preserved; delegates the membership-interval question entirely to `taxsma_membership.resolve_date_status`; carries `business_active_accounts` through unchanged; computes `complete_value` only when fully resolved; derives a stable, event-keyed `observation_id`; applies the Gold partition NO_CHANGE/CORRECTION_QUEUED policy; resolves an acyclic correction chain and aggregates across every partition before counting; gates the SMA source-basis against the registry; computes the Gold key at one call site | `git status --porcelain` (untracked pre-commit), this record's own reads |
| `data/mdpf/tests/taxsma/test_taxsma_assets.py` (new) | 22 tests: `test_ac1_` .. `test_ac21_` (one per criterion) plus one structural forbidden-call-site test; synthetic account keys only, minted through `_key()` | `py -3.12 -m pytest ... -q`: `22 passed in 0.5s` |
| `org/missions/D8/MDPF/MDPF_TAXSMA/deliverables/0.9.0_WK_MDPF_TAXSMA~2/probes/tx_m_4.py` (new) | the criterion probe: one AC per invocation, fresh subprocess, vacuous-pass refused | 21 of 21 `AC1`..`AC21` invocations below |

**Design decisions this cell makes that the contract does not fix (declared, not hidden -- see module
docstring "DESIGN DECISIONS" and s.3 below):**
- `ExpectedAccountInput` is this cell's OWN input shape, never TX-m-2's masked `ReconciledIdentity` -- Gold's
  `account_key` field is the validated FULL canonical form (contract `field_types.account_key`: "protected
  only", never masked in the data store itself), while TX-m-2's reporting surface deliberately returns only
  a masked label. A later release cell assembles `ExpectedAccountInput` from TX-m-1/TX-m-2's real (unmasked)
  working state; this cell's own tests build it directly with synthetic full keys.
- "Source date" (decomp s.3's "identity, observed membership, source date and value checks") is satisfied by
  construction: the canonical join key IS `(account_key, valuation_date)`, so a resolved join always carries
  the requested date -- there is no separate source-date field to re-check.
- An expected account whose membership status is `OBSERVED_INACTIVE` at `valuation_date` is `unresolved`
  with `MEMBERSHIP_CONFLICT` rather than silently excluded -- the caller's own population, not this module,
  decides who is "expected"; this module never drops a row once given one.
- `value_status` distinguishes an actual zero (`KNOWN_ZERO`) from a covered non-zero value (`COMPLETE`) --
  both are "covered"; only `UNAVAILABLE` is not.
- The Gold-partition NO_CHANGE/CORRECTION_QUEUED comparison is over every field EXCEPT `knowledge_date`
  itself (the partition label; `gold_partition_axis`), since two partitions minted on different UTC dates
  for identical underlying observations must still compare equal to reach NO_CHANGE.
- `_governing_disposition` mirrors `resolve_date_status`'s own filter/sort/walk (same constants, same
  predicate) purely to recover the EVENT the status rests on -- never a second, independent date rule; AC10's
  test asserts `taxsma_assets.resolve_date_status is taxsma_membership.resolve_date_status` (the same function
  object, not a re-implementation).

## 2. Criteria -- 21 of 21 PASS by output

Instrument: `cd C:/tmp/wk-taxsma-2c && timeout 120 py -3.12 org/missions/D8/MDPF/MDPF_TAXSMA/deliverables/0.9.0_WK_MDPF_TAXSMA~2/probes/tx_m_4.py AC<n>`,
run at HEAD `5cc9756554` (3 of the 3 files under test dirty -- new, pre-commit; the same 3 files, unstaged,
committed in this order's own commit below), 2026-09-21T07:0xZ. Each run prints its vintage, its measurement,
its denominator and exactly one `VERDICT:` line; rc 0 on all 21.

| Criterion | Deciding measurement | Denominator |
|---|---|---|
| AC1 | dataclass fields of `ObservationRow` equal the 22-tuple `HISTORY_FIELDS`; one built row populates every field | 22 of 22 |
| AC2 | 5 fixtures (cash, long exposure, short exposure, margin, actual zero) each `value_usd == Decimal(net_mv_plus_cash)` to the cent | 5 of 5 |
| AC3 | no canonical row -> `value_status=UNAVAILABLE`, `CANONICAL_MISSING` present, `value_usd=None` | 1 of 1 |
| AC4 | 2 conflicting canonical rows -> `CANONICAL_DUPLICATE`, `source_hashes` carries both hashes | 1 of 1 |
| AC5 | 6 numeric rejected_substitutes supplied, ignored (`value_usd` unchanged); missing-to-zero proved via AC3's own arm | 7 of 7 rejected_substitutes enumerated |
| AC6 | 3 accounts, 1 passes every filter: `expected_accounts=3` (pre-filter), `covered_accounts=1`, `unresolved_accounts=2` | 3 accounts |
| AC7 | 3 scenarios (0, 1, 5 expected accounts) each satisfy `covered+unresolved==expected` | 3 of 3 |
| AC8 | live claim, `MISSING_CUSTODIAN` -> retained (never dropped), counted in `unresolved_accounts` | 1 of 1 |
| AC9 | valuation date before first observation -> `membership_date_status=UNVERIFIED`, `TRADED_HISTORY_UNVERIFIED`, `value_usd=None` | 1 of 1 |
| AC10 | `a.resolve_date_status is m.resolve_date_status`; 2026-09-15 (before UTC open) = UNVERIFIED, 2026-09-16 (UTC date of a 00:30Z event) = OBSERVED_TRADED | 2 of 2 date arms + 1 identity check |
| AC11 | `business_active_accounts=42` (caller-supplied) while `covered_accounts=1` -- carried, not derived | 1 of 1, values differ |
| AC12 (difference) | before (1 resolved + 1 unresolved): `complete_value=None` with reasons; after (both resolved): `complete_value=300.00`, no reasons | 2 claims, both arms |
| AC13 | `accounts=None` -> `expected_accounts=None` with non-empty reason_codes, `covered=unresolved=0` | 1 of 1, never `0 of 0` |
| AC14 | two independently-built "runs" (different stores, different `knowledge_date`) -> identical `observation_id` | 2 of 2 |
| AC15 | different S03 event -> different id; same event with business_status/row/enrollment/knowledge_date varied -> identical id | 2 of 2 arms |
| AC16 (difference) | 1st publish=COMPLETE; identical re-publish=NO_CHANGE; changed re-publish=CORRECTION_QUEUED, partition still holds the original value | 3 publishes, 1 partition |
| AC17 | 1-hop chain resolves to the correction; 2-hop chain resolves to the tail, not the middle | 2 of 2 chains |
| AC18 | competing corrections, duplicate id with a different payload, and a missing superseded observation each refuse | 3 of 3 refusal arms |
| AC19 | 3 accounts across 3 partitions (1 base + 2 correction-only) -> resolved cohort = 3 of 3, 2 resolve to a correction | 3 of 3 accounts |
| AC20 | `sma_basis_of("tax")==SMA_BASIS_ADDITIVE` (True); monkeypatched mismatch -> `BASIS_MISMATCH`, `value_usd=None` | 1 of 1 registry read + 1 of 1 mismatch build |
| AC21 | computed key matches expected `address()` output; the literal `"mdpf", "49financial", "gold", "taxsma_assets"` argument tuple occurs exactly once in source | 1 of 1 call site |

## 3. Controls (schema-required)

- **Mutant** (FIRED-AS-EXPECTED): changed `build_observation`'s coverage line from
  `covered = identity_ok and membership_ok and canonical_ok and sma_basis_ok` to `covered = identity_ok`.
  Expected AC3/AC4/AC5/AC6/AC9/AC20 (every criterion whose fixture relies on the membership/canonical/basis
  gates) to fail. Observed 6 FAILED exactly those six tests, each asserting `UNAVAILABLE`/`None` and getting
  a populated `COMPLETE` value instead. Reverted; re-run 22 passed in 0.58s.
- **Determinism** (STABLE): AC1 invoked twice back to back via the probe; diffed with the vintage/UTC-time
  and elapsed:/pytest-timing lines stripped -- empty diff, byte-identical otherwise.

## 4. Bounds and scope notes

- Synthetic identities only throughout; no real account number, name or balance in code, fixtures, this
  record or the probe output. Every fixture key is a `_key("135000NN")`-shaped synthetic value.
- No egress off Opal infrastructure, no live route/Graph/SharePoint/BD-roster/b00 call, no S3/boto3 client
  construction anywhere in the module's tests (checked structurally by
  `test_module_has_no_source_mutation_or_forbidden_call_site`); `S3GoldAssetsStore` raises
  `NotImplementedError` and is never constructed by this cell's tests.
- The only new S3 key this cell mints is the Gold `taxsma_assets` key (contract `artifacts.taxsma_assets`),
  computed exclusively through `gold_assets_address()` -> `lib.opal_naming.address()` (AC21); no other
  `address()`/`name()` call was made.
- `.tools/commit-gate.sh` clean for all 3 new files (`py_compile`, `ds-precommit`, `ruff py39`,
  log-open-lint): `OK: pre-commit gate clean for 3 of 3 file(s)`.
- MDPF Gold suite baseline (bound 17, decomp s.7): `py -3.12 -m pytest data/mdpf/scripts/gold/tests data/mdpf/tests -q`
  -> `193 passed, 3 failed`, the same 3 pre-existing `test_global_fold_flag2.py` failures named in the
  decomposition (`test_carry_within_window_carries_and_labels`, `test_carry_beyond_window_absent_for_real`,
  `test_carry_source_is_measured_never_interpolated`); no new failure introduced by this cell's change (193
  vs. the prior cell's 171 passed reflects this cell's own 22 new tests joining the same collection root).

## 5. Surprises filed

None. No premise failed, no path was missing, and every criterion was satisfiable as written against the
contract and decomposition sections named in this order.
