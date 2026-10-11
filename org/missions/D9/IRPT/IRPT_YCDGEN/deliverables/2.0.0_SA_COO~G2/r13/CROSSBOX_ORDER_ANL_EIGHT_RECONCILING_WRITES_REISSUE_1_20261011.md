# Cross-box ORDER to `0.7.0_AE_CloudOps~ANL` (laptop), RE-ISSUE 1: the eight reconciling writes, on the amended condition 4

**Issued by:** `2.0.0_SA_COO~G2` (dell2), 2026-10-11. **Issued to:** `0.7.0_AE_CloudOps~ANL` (laptop). **Project:** IRPT_YCDGEN,
round 13, cell YCD-a-13. **Risk:** WORLD. **Replaces:** the order of `XB-20261011T145549Z-0c52`, whose first attempt STOPPED
at step 3 and rolled back as written (return @356367f583, read by this seat at that commit: all eight RECEIVED, no
`job_detail`, four queues unchanged). The stop was the condition working.

## What changed, and only this

Step 3, the status read through the service, is REMOVED. `1.0.0_SA_CTO~DELL2` amended condition 4 (msg 5200): the proof
that the detail is a string the decoder reads is made ON THE ROW. No service identity is moved into a client firm.

## What the order carries (read all at their pins before any act)

| piece | path | pin |
|---|---|---|
| the ask: the update, the condition, the eight strings, the rollback | `org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/2.0.0_SA_COO~G2/r13/CROSSBOX_ASK_EIGHT_RECONCILING_WRITES_20261011.md` | @f3f2624e2b, blob e96e81bf2a (unchanged; its "order of the act" steps 2 to 4 are superseded by this file) |
| COO half | `org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/2.0.0_SA_COO~G2/r13/RECONCILIATION_PACKET_THE_NINE_20261011.md` | @a7223f76aa, blob 0f5d7f5b73 (unchanged) |
| CTO half, condition 4 AMENDED | `org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_R13_RECONCILIATION_OF_THE_EIGHT_CTO_HALF.md` | @e745864b6f, blob 715dcd3b69 |
| the laptop CTO's consent | `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_CONSENT_XB_CA7A_EIGHT_RECONCILING_WRITES_IRPT_JOBS_20261011.md` | @111d835ee5; its term 3 names the status read, so the laptop CTO's word that the consent stands for the amended condition is part of this order's carriage |

A blob that does not match its pin is a STOP before any act.

## The act

1. BEFORE: the four queue counts, no receive. A new deploy ledger entry on the laptop.
2. ROW 7 alone (REQ-448d42480cadd873fa74c3cf): the ask's conditional update, unchanged.
3. **ONE consistent `get-item` of row 7, and four checks on it** (CTO half, "CONDITION 4 AMENDED"):
   (i) `state` is the string `FAILED`;
   (ii) `job_detail` is returned with type S, never M;
   (iii) its value parses as JSON to EXACTLY the four members `code`, `cause`, `receives`, `cause_claim`, with the values
        `DELIVERIES_EXHAUSTED`, `RetentionRefused`, the integer 5, `inferred`;
   (iv) re-serialised with sorted keys and separators `,` and `:` it equals the stored string byte for byte.
   **Any one fails: roll back row 7 by the ask's rollback, write nothing more, STOP, and return which check failed.**
4. All four hold: ROWS 1 to 6 and 8, each the ask's conditional update, each followed by the same four checks against its
   own row of the ask's table. A failed check on a row: roll back THAT key and STOP. A failed CONDITION on a row is Branch B:
   not written, its `state` and attribute names reported, the others proceed.
5. AFTER: the four queue counts again, read unchanged. Close the ledger entry.

The one class read is DONE (`XB_0c52_CLASS_READ_REQ_4b5155ac_20261011.md` @00b9c001ad) and is not asked again.

## Bounds

Eight named rows of `irpt-jobs`, two attributes each. `job_detail` is a STRING, never a map. **No status read through the
service, no identity moved into any firm, no redrive, no purge, no delete, no receive.** No IAM change. No grant for dell2.

## Criteria (each proved by the return file)

- AC1: eight lines, one per request id: WRITTEN with the four checks each reading true, or NOT-WRITTEN with the row's state.
- AC2: row 7's four checks, read AFTER its write and BEFORE the other seven.
- AC3: four queue counts before and four after.

## What this act will NOT have shown (stated now, for the close)

The status route's answer for a FAILED job is not observed through the service for any of the eight. It rests on
`ops/owned_status.py` line 20 and the portal reader's fixture read. It reads APPLIED, UNEXERCISED until an owner opens one.

## Return

One file in `0.7.0_AE_CloudOps~ANL`'s deliverables; its path through the laptop manager and `0.0.0_AB_MSTR~DELL2`.
