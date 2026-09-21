# MDPF_TAXSMA.TO-TX-b-2 -- result record

**Worker** `0.9.0_WK_MDPF_TAXSMA~2` · **cell** `TX-b-2` (PRD surface S19, FWD-1/3/5/8) · **branch**
`wk-mdpf_taxsma-1-2b` in `C:/tmp/wk-taxsma-2b` · **cut base** `3dfb7e08de` (the COO's release commit for G-R
on this cell). **Spec:** the PRD @671925aecc and `org/standards/MDPF_TAXSMA_DATA_CONTRACT.json` v0.5.0
(`workbook.silver`, `workbook.row_kind`, `workbook.row_metadata`), whose enumerations are the only
vocabulary used. **Input:** `TX-b-1`'s typed acquirer (`data/mdpf/scripts/gold/taxsma_snapshot.py`, drained
@5c80dc5d98), whose `SuccessResult` names the Bronze address and `response_sha256` this cell's Silver key is
built from.

Every value below names its instrument, the UTC time it was measured and its denominator.

## 0. Gate G-R re-measured at this cell's HEAD (TXB2-AC1)

The task order's HELD status is read from a released issuance (`3dfb7e08de`), not trusted from the note; this
worker independently re-measured G-R's condition -- the `gateway` row in `infra/logic/registry/systems.json`
-- at cell HEAD before writing any code: `infra/logic/registry/systems.json:144-150` carries `"key": "gateway"`,
`"class": "PLATFORM_SUBSYSTEM"`, `"long": "opal-gateway"`. `lib.opal_naming.address("gateway", "49financial",
"silver", "taxsma_workbook", "date=2026-09-19", "snap-1-abc.parquet")` resolves (TXB2-AC1's own invocation,
below) rather than raising `ValueError`, which is the live proof the row is registered and both source
addresses (Bronze and Silver) resolve.

## 1. What was built

| Path | What | Instrument / evidence |
|---|---|---|
| `data/mdpf/scripts/silver/taxsma_workbook.py` (new) | S19: typed workbook Silver builder -- reads a Bronze envelope through an injected `bronze_reader`, types every business cell per `business_scalar_schema`, serializes a typed parquet table with envelope+lineage file metadata, persists via a `SilverStore` at the ONE `address()`-computed key | `git status --porcelain` (untracked pre-commit), this record's own reads |
| `data/mdpf/tests/taxsma/test_taxsma_workbook_silver.py` (new) | 17 tests, `test_ac1_` .. `test_ac11_`, one or more per criterion; synthetic Bronze envelopes and `LocalSilverStore` only | `py -3.12 -m pytest ... -q`: `17 passed in 0.5s` |
| `org/missions/D8/MDPF/MDPF_TAXSMA/deliverables/0.9.0_WK_MDPF_TAXSMA~2/probes/tx_b_2.py` (new) | the criterion probe: one AC per invocation, fresh subprocess, vacuous-pass refused | 11 of 11 `AC1`..`AC11` invocations below |

**Design decision this cell makes that the contract does not fix (declared, not hidden):** the contract fixes
the Gateway response ENVELOPE fields but not a per-row JSON shape. This module's own row shape --
`{"row_number", "row_kind", "other_business_cells_present", "business": {<the 7 business_columns>: <raw
scalar or null>}}` -- is documented in the module's own docstring ("ROW SHAPE") so a later cell (`TX-m-1`,
the reader) can rely on it as the one page in this cell's authority.

## 2. Criteria -- 11 of 11 PASS by output

Instrument: `cd C:/tmp/wk-taxsma-2b && timeout 120 py -3.12 org/missions/D8/MDPF/MDPF_TAXSMA/deliverables/0.9.0_WK_MDPF_TAXSMA~2/probes/tx_b_2.py AC<n>`,
run at HEAD `3dfb7e08de` (2 of the 2 files under test dirty -- new, pre-commit; the same 2 files, unstaged,
committed in this order's own commit below), 2026-09-21T04:07Z. Each run prints its measurement, its
denominator and exactly one `VERDICT:` line; rc 0 on all 11.

| Criterion | Deciding measurement | Denominator |
|---|---|---|
| AC1 | `address()` resolves; exactly 1 call site, inside `_silver_key` | 2 of 2 sub-tests passed |
| AC2 | 4 rows (ACCOUNT_SLOT, BLANK, TOTAL, UNRECOGNIZED) -> parquet row count 4, row_numbers `[1,2,3,4]` | row_kinds observed == `ROW_KINDS`, 4 of 4 |
| AC3 | every business cell's struct: kind in `SCALAR_KINDS`, exactly the matching value field populated, other 3 null | checked over every row (2 rows x 7 columns = 14 cells) |
| AC4 | zero-row snapshot: 0 parquet rows, all 12 `ENVELOPE_FIELDS` present in file metadata, `rows` absent | 12 of 12 envelope fields present |
| AC5 | file metadata carries `bronze_address`, `response_sha256`, `snapshot_id` matching the build inputs | 3 of 3 lineage fields present and equal |
| AC6 | two rows sharing `Account Number` `00012345` -> row_count 2, row_numbers `[1,2]` | 2 of 2 rows retained distinct |
| AC7 (difference) | identical replay -> `NO_CHANGE`, same key, leaves stay 1; changed bytes -> `COMPLETE`, different key, leaves become 2 | 1 leaf before, 2 after; differed only on changed `response_sha256` |
| AC8 | same key + different body -> `ValueError` raised; `get_body(key)` after the raise still returns the ORIGINAL bytes | mutant control below: removing this check flips the test to FAIL |
| AC9 | a nested dict, a list, and a NaN float each raise `UnrepresentableScalarError`; 0 objects persisted in all 3 arms | every other JSON scalar type (None/str/int/float/bool) representable, 5 of 5 |
| AC10 | missing Bronze (`KeyError`) -> `SOURCE_UNAVAILABLE`; invalid JSON -> `SOURCE_SCHEMA_INVALID`; `complete:false` -> `SOURCE_SCHEMA_INVALID`; store untouched (0 objects) in all 3 | 3 of 3 corrupt/missing arms, 0 empty parquet ever persisted |
| AC11 | output column set == `BUSINESS_COLUMNS` (7) + `ROW_METADATA_FIELDS` (3) = 10, exactly | matches `MDPF_TAXSMA_DATA_CONTRACT.json` `workbook.silver.business_columns`/`workbook.row_metadata`/`workbook.row_kind` directly, 3 of 3 arrays equal |

**Controls.**
- **MUTANT** (AC8): removed the `LocalSilverStore.put_if_absent` conflict check (a same-key/different-body
  call fell through to `PERSIST_NO_CHANGE` instead of raising) -- `test_ac8_conflicting_bytes_at_one_key_raise_and_never_overwrite`
  FAILED (`Failed: DID NOT RAISE <class 'ValueError'>`), probe printed `VERDICT: FAIL-TXB2-AC8`. Reverted;
  re-run: `1 passed`, `VERDICT: PASS-TXB2-AC8`. FIRED-AS-EXPECTED.
- **DETERMINISM**: AC1 run twice back to back; outputs identical modulo the vintage/UTC-time and `elapsed:`
  lines (`diff` of the two runs with those lines stripped: empty). STABLE.

## 3. Bounds and exclusions

- No egress: no call to the live `/ms/taxsma-workbook` route, Graph or SharePoint; no `S3SilverStore`
  constructed by any test (checked by `test_no_live_route_or_s3_call_site_is_executed_in_this_test_module`).
  No real S3 write.
- No private data: fixture account numbers are synthetic 8-digit forms (`00012345`, `00099999`, `00012345`);
  no client name, balance, token or credential appears in the module, tests or this record.
- Every S3 key is `address()` output, computed at exactly one call site (`_silver_key`, AC1).
- `TX-b-1`'s Bronze acquisition, `TX-m-1`'s reader and the pipeline wiring that invokes S19 on a successful
  S02 acquisition are out of this cell's scope; declared in the proof-of-spec instance.

## 4. Surprises

None filed. G-R's condition (the `gateway` registry row) was independently re-measured at this cell's HEAD
(s.0 above) and found satisfied, consistent with the issuance note; no premise failed, no path was missing,
and every criterion as written was met without a route this order does not name.
