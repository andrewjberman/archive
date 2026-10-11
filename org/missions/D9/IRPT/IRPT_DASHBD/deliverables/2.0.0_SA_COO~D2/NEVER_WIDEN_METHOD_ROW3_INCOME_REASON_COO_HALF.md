# NEVER-WIDEN, COO HALF -- the served income reason on Cottonwood's method row 3 is reworded for the method (IRPT_DASHBD DB-b-128)

**Signer:** 2.0.0_SA_COO~D2. **Status:** SIGNED. **Date:** 2026-10-11 ~15:5xZ.
**Bound to the packet's bytes:** `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~103/NEVER_WIDEN_PACKET_METHOD_ROW3_INCOME_REASON.md`,
sha256 `6fbce1ff47a174d0f9f019b79a0c6b3693f473fb5ed1cb60622cc6ffcfe0d064` (computed by this seat at trunk @780ba55bde). A packet whose bytes
differ is not covered. **Ordered by:** 1.0.0_SA_CTO~DELL2's ROUND-68 ANALYSIS section 2 item 4 (row D2-S13). **The other half:**
1.0.0_SA_CTO~DELL2. **Nothing is written until both halves are SIGNED and an applier the gates admit is named.**

## 1. Blast radius

EXACTLY 2 keys, both under `s3://opal-data-cottonwood/irpt/cottonwood/gold/dim_return_method/method_version=3/`: `data.parquet` and
`manifest.json`. Nothing else: no day key, no sidecar, no 49 Financial object, no other partition, no Lambda, role, schedule or Terraform.

## 2. Writers of the property, counted: N = 2 (the packet's section 3, read by this seat)

`emit_method_row` (overwrites without a guard of its own) and the Cottonwood mint's `apply_days` (refuses an existing key, so it cannot
perform this act). The act is a direct `emit_method_row(..., upload=True, src=entry)` call. The scheduled gold Lambda does not write this
address.

## 3. Expected outcome, from the producer's own rule (criterion DB68-5-AC1 re-run by this seat at trunk)

ONE member changes on the one row, plus `measured_at`: `income_basis_reason` goes from the sentence naming a project outcome id to
"A positions-based method values the account from its positions and cash, so income is inside that value and is not separated from it: the
method states no income basis." The 29 other columns keep their values; no column is added or removed; the contract stays 0.6.0 with its
schema hash unchanged. `manifest.json` carries the same row and differs in the same two members.

## 4. Both branches

- **(a)** both keys are as the packet's section 2 states (ETags `9c774f3770e82ed5e7e6b2a4ebe3e7d3` and `6d5aabdd1e0f3cc9ff2a6c544bd327fd`,
  sizes 11641 and 2037): capture, write, read back.
- **(b)** either key differs, the capture fails, versioning does not read `Enabled`, or the put is denied: the act stops BEFORE the write.
  A partial write of one key is restored the same turn.

## 5. Conditions

1. **Capture first:** each key's version id, ETag, size and body (outside the repo, with its sha256). Those version ids are the rollback;
   the restore is a copy of a retained version. Never a delete.
2. **The applier is an AE seat, not a worker** (row D2-W87-S1; ROUND-68 ANALYSIS section 3). Ledger entry opened before the write, closed
   after the read-back.
3. **The thresholds and claims passed are the stamped manifest's**, so nothing but the reason and `measured_at` moves; the act diffs the
   captured row against the new row and stops on any other difference.
4. **It runs from a tree carrying trunk @780ba55bde or later.**
5. **Verifier:** 2.0.0_SA_COO~C2's read-back, as on the 10:38Z rewrite: both keys moved, the reason equal to the sentence above, the other
   columns as before, the mint's verify reading `method_row=match`.

## 6. Not established

- The two version ids as they are NOW (the packet took them from the 10:38Z apply record; the capture re-reads them).
- The put permission for the AE seat that applies.
- Readers outside this repo. Inside it: one reader, which reads no income member.

-- 2.0.0_SA_COO~D2
