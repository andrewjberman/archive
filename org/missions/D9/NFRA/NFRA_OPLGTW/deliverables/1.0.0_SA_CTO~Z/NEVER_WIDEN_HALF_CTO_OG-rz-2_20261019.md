# Never-widen half (CTO) -- OG-rz-2: the t4g.large resize plus the master 08403355 registration (release 13917ef993) (SIGNED)

By: `1.0.0_SA_CTO~Z`, 2026-10-19 ~21:3xZ.
Against: `deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-rz-2.md`, sha256 prefix `5dfadc6c78c3`. This seat recomputed it,
and it is equal.
Release: `13917ef993` on the live ref `6d1b5dcb64`.
Window: 2026-10-20 06:00Z-06:45Z (02:00-02:45 ET).
Basis:
- Andrew-direct ~18:3xZ, "lets raise it to large" (@439343a969);
- Andrew-direct ~19:55Z, add the 0840 master to Alyssa (laptop @3c6ce94b4f).

## Read by this seat (`git diff 6d1b5dcb64 13917ef993`: 10 files, +158 -27)

- **`data_entitlement.py:77`:** `MASTERS` gains `08403355`. This only lets a grant name the master. No principal's grant changes
  here; Alyssa's addition is `OG-ms-2`'s own ask.
- **`client_adapter_schwab.py`:** the alias masters are pinned to the two existing masters (`_ALIAS_MASTERS`). So the `client_*`
  tools keep refusing 08403355 with `master_not_registered`. This is a deliberate non-widening, and it is correct.
- **`schwab_audit.py`:** the audit master set gains 08403355.
- **The contract, both copies:** the `TaxSMA` label, the four `schwab/08403355/silver/*` read prefixes and the completion prefix
  are added, and `target_instance_type` becomes t4g.large. The reader IAM already lists the prefix (COO msg 36107).
- **The unit:** `MemoryHigh` goes 1200M -> 5600M and `MemoryMax` 1400M -> 6400M, which leaves about 1.8 GB of 8 GiB to the
  system. `OOMScoreAdjust` stays 300.
- **`scopes.json`:**
  - The 08403355 MASTER row carries firm `49financial` and bucket `opal-data-49financial`, the same values as the two existing
    master rows.
  - The other seats' hunks are inert. The `alongside` FIRM row has `bucket_provisioned: false`, and its note says it is never
    provisioned. The two `separated_from` additions only add a separation, which is a narrowing.

## The two choices

1. **`scopes.json` taken whole from trunk: ACCEPTED.** The extra hunks are inert or narrowing, and re-cutting into two hunks
   would buy nothing.
2. **Order: ACCEPTED as written.** The rollback tarball is taken first, then the resize, then the raised limits. The limits must
   never land before the resize: 6400M on a 2 GiB host would starve the system.

## Non-blocking note (not a condition on these bytes)

The contract's `capacity.target_memory_mib` still reads 2048 beside `t4g.large`. No gateway code reads it (comp-find: 1 hit, the
contract itself). It is corrected to 8192 in the next release that touches the contract, never as a release of its own.

## SIGNED

Signed on the COO half's conditions. Any change to the ask's bytes or to `release_sha` re-opens this half.
