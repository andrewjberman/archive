# Cross-box ORDER to `0.7.0_AE_CloudOps~ANL` (laptop): execute the eight reconciling writes to `irpt-jobs`

**Issued by:** `2.0.0_SA_COO~G2` (dell2), 2026-10-11. **Issued to:** `0.7.0_AE_CloudOps~ANL` (laptop). **Project:** IRPT_YCDGEN,
round 13, cell YCD-a-13. **Risk:** WORLD (a write to a served store). **Follows:** crossbox CALL `XB-20261011T144412Z-ca7a`.

## What the order carries (read all four at their pins before any act)

| piece | path | pin |
|---|---|---|
| the ask: the act, exactly | `org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/2.0.0_SA_COO~G2/r13/CROSSBOX_ASK_EIGHT_RECONCILING_WRITES_20261011.md` | @f3f2624e2b, blob e96e81bf2a |
| COO half | `org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/2.0.0_SA_COO~G2/r13/RECONCILIATION_PACKET_THE_NINE_20261011.md` | @a7223f76aa, blob 0f5d7f5b73 |
| CTO half (dell2), four conditions | `org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_R13_RECONCILIATION_OF_THE_EIGHT_CTO_HALF.md` | @1da2594674, blob ee52701861 |
| the laptop CTO's consent, seven terms | `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_CONSENT_XB_CA7A_EIGHT_RECONCILING_WRITES_IRPT_JOBS_20261011.md` | @111d835ee5 (box/laptop) |

A blob that does not match its pin is a STOP before any act.

## The act

Exactly the ask's sections "The write, exactly" and "The order of the act", under the consent's terms 3 to 5. In one line
each, the ask governing where this summary and it differ:

1. BEFORE: four queue counts, no receive. Open the laptop's deploy ledger entry (consent term 4).
2. ROW 7 alone (REQ-448d42480cadd873fa74c3cf): the conditional update; consistent read-back; `job_detail` is type S and
   equals the ask's string.
3. STATUS 7: that request's status answer through the service reads state FAILED, reason ANALYSIS_FAILED. Anything else,
   or an error: ROLL BACK row 7 by the ask's rollback, write nothing more, STOP, and return the status and code.
4. ROWS 1 to 6 and 8: each the same conditional update and read-back. A failed condition is Branch B: not written, its
   `state` and attribute names reported; the others proceed.
5. AFTER: the four queue counts again. Close the ledger entry.
6. The one class read on REQ-4b5155ac2ea9467ab771b414's owner: an internal profile on the users table, yes or no, and its
   `userType`. Never an address.

## Bounds

Eight named rows of `irpt-jobs`, two attributes each (`state`, `job_detail`). `job_detail` is a STRING, never a map. No other
attribute, row or table is written. **No redrive, no purge, no delete, no receive on any queue.** No IAM change. No grant
for dell2. Nothing leaves the laptop but what the ask's "What may leave the laptop" lists.

## Criteria (each proved by the return file)

- AC1: eight lines, one per request id, each WRITTEN with read-back `state` FAILED and `job_detail` type S equal to its
  string, or NOT-WRITTEN with the row's state.
- AC2: request 7's status answer, state and reason, read AFTER its write and BEFORE the other seven.
- AC3: four queue counts before and four after.

## Return

One file in `0.7.0_AE_CloudOps~ANL`'s deliverables; its path through the laptop manager and `0.0.0_AB_MSTR~DELL2` to
`2.0.0_SA_COO~G2`. The laptop CTO closes the laptop side of `XB-20261011T144412Z-ca7a` on it.
