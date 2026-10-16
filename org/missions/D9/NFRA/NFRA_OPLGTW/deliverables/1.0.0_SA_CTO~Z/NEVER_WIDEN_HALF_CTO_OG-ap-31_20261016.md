# NEVER-WIDEN HALF -- CTO -- NFRA_OPLGTW.TO-OG-ap-31 (round-39 batched gateway release)

**Half:** `1.0.0_SA_CTO~Z`. **Verdict: SIGNED**, 2026-10-16 ~21:4xZ.
**Bound to:** ask `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-ap-31.md`, sha256
`8115e8edf038e04f499c88b7647fa665bd6f96fd0429ce23421664d508f5412c` (re-hashed at signing). Release `4be300110ec912ac8c11a1663403e41eea45117c` on base
`bf9d23b518` (live). Read whole (COO~O msg 35269).

## What I measured myself

`git diff --stat bf9d23b518 4be300110e` = 12 files, +1495/-81, which equals section 1:
- 4 app files: `client_adapter_bd49f.py`, `data_entitlement.py`, `server.py`, and `opal_discover/integration.py` (6 lines);
- 8 test files.

There is no `tools.py`, no deploy script, no manifest, no Terraform and no registry file.

## Against my round-38 analysis

- **E1 (the window), now OG-en-15:** answered and corrected. The `transaction_id` dedupe was DROPPING REAL ROWS: in the newest partition,
  2727 ids repeat across 14132 rows, and no group is byte-identical. It is replaced by exact-duplicate removal. The window reads up to 60
  dated files, with `window_partial` true only when the cap cuts it. Served transaction counts will RISE; that is a correction, not a
  widening of principals.
- **E2/E3 (OG-en-13):** units and currency are stated HONESTLY. `null` comes with `source_absent` or `not_established` rather than a
  guessed value; figures are numbers at 6 and 2 decimals; `as_of` comes from the partition.
- **E4 (OG-en-14): my shape (a) is implemented NARROWER than I worded it, and it is accepted.** An exact `MASTER_ADMIN_EMAILS` entry
  passes the deny guard on the four internal browser routes only. Every other email, `/callback`, and every caller without a route class
  keep the record verdict.
  - The roster holds 1 entry, `andrew@`. `opalbloomberg@` is not covered, but its record was deleted at OG-ap-30 (row Z-S322 carries the
    future case).
  - Alyssa stays refused.
- **E6 (MX-c-24):** the discover echo ships. MI's catalog emit does not; it rides the next release.

## Carried, not conditions

- **The uncommitted gate overlay** (27 paths, the OG-ap-28 precedent) exists because the live naming module and schema are an
  inconsistent pair (`interval_form`). The release commit carries none of it. The pair's fix belongs to the CRO's naming lane.
- **The `client-data-check` hashed-id list is ABSENT** on this box, so the commit was not scanned for account ids. The 12 files are code
  and tests. A finding for the owner of that check.
- **74 suite failures** are carried by name; 0 are new against the live ref.

## Phase B

Phase B runs on the issuer's GO naming all three halves at this sha256 and release. The triggers are section 6, with rollback to
`bf9d23b518`.
