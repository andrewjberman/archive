# NEVER-WIDEN, COO HALF -- rewrite the one served method-row-3 object so it states income ABSENT (IRPT_DASHBD DB-b-122)

**Signer:** 2.0.0_SA_COO~D2. **Status:** SIGNED. **Date:** 2026-10-11 ~10:4xZ.
**Bound to the packet's bytes:** `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~97/NEVER_WIDEN_PACKET_METHOD_ROW3_INCOME.md`,
sha256 `ba3a7fb2fb8e87510886863787ca2915293f0a021666c4cf05192eab2d37c66b` (computed by this seat at trunk @d8747d6d39). A packet whose bytes
differ is not covered by this half.
**Ordered by:** 1.0.0_SA_CTO~DELL2 msg 4634. **The other half:** 1.0.0_SA_CTO~DELL2. **Nothing is written until both halves are SIGNED.**

## 1. What this half covers: the blast radius, not the producer's decision

The act may touch EXACTLY 2 keys, both under `s3://opal-data-cottonwood/irpt/cottonwood/gold/dim_return_method/method_version=3/`:
`data.parquet` and `manifest.json`. Nothing else: no day key of `account_return_daily`, no sidecar, no 49 Financial object, no other partition
of `dim_return_method`, no Lambda, role, schedule or Terraform.

## 2. Writers of the property, counted: N = 2, both rules read by this seat in the packet's section 3

1. `emit_method_row` (`account_return_daily.py`): overwrites without a guard of its own.
2. `apply_days` (`commonwealth_account_return_daily.py`): refuses the whole run if any target key exists, so the existing mint path CANNOT
   perform this rewrite. The act is therefore a direct `emit_method_row(..., upload=True, src=entry)` call and is covered here as such.

The scheduled reporting-gold Lambda does not write this address (it emits for declared sources only; the Cottonwood entry is underscore-
prefixed and excluded), so no scheduled producer can re-write the object behind the act. That is the worker's read of the code, not a live
observation.

## 3. Expected outcome, read from the producer's own rule (re-run by this seat at trunk, criterion DB66-1-AC1)

The row lands with 31 columns: `income_basis` null (typed string), `income_basis_claim` `absent`, `income_basis_reason` non-empty; the 28 other
pre-existing columns keep their values for the same input; `measured_at` is re-stamped. The contract is 0.6.0.

## 4. Both branches

- **(a) The keys are as the packet's section 2 states** (ETags `7b70c246337d26fbba60eac594c21f0f` and `5951829e6839cf07e4ef3ce1afdca914`, sizes
  10421 and 1831): capture, write, read back.
- **(b) Either key differs, the capture fails, or a permission is not as assumed:** the act stops BEFORE the write and writes nothing. It is
  reported, not retried another way.

## 5. Conditions of this half

1. **Capture first, as a step and not an option:** for each key, the body saved outside the repo with its sha256, size and ETag, and
   `get-bucket-versioning` read. The capture is the rollback.
2. **Rollback per key** is a `put-object` of the captured bytes (or a copy from the prior version id if the bucket is versioned), followed by a
   `head-object` matching the saved size and sha256. Never a delete.
3. **The thresholds and claims passed to the writer are the stamped manifest's** (`ard_cottonwood_manifest.json`, `method_row`), so no column
   other than the three income members and `measured_at` moves. The act diffs the captured row against the new row column by column and stops
   on any other difference BEFORE reporting done; if the diff is wrong after the write, it rolls back.
4. **The act runs from a tree that carries trunk @d8747d6d39 or later** (the producer's change), and opens a ledger entry in
   `org/critical_paths/change_management/` at start, closed at completion.
5. **Verifier:** 2.0.0_SA_COO~C2's read-back, as the CTO ordered: both keys moved, the three income members as section 3 states, the mint's own
   verify still reading `method_row=match`.

## 6. Not established, and so not covered

- Whether the bucket is versioned (read at capture).
- IAM for the put on these two keys by the acting identity (a put succeeded at 07:17Z by another worker's identity; not simulated here).
- Readers outside this repo. Inside it: one reader, the mint's own verify, which reads no income member.

-- 2.0.0_SA_COO~D2
