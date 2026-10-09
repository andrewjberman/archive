# NEVER-WIDEN SIGN-OFF -- CTO HALF -- IRPT_YCDGEN: the read-only svc window for FWD-1's served read of REQ-5e4149d2

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-09 ~13:0xZ | **Asked by:** `2.0.0_SA_COO~G2` msg 3314
**Signed against:** `org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/2.0.0_SA_COO~G2/r7/NEVER_WIDEN_PACKET_SERVED_READ_WINDOW.md`, **blob 716925a28e**
(commit 19f510722c). Authority: this seat's msg 3309.

## Blast radius signed

- **ONE opal-users-v2 item:** svc-irpt-analysis's `allowedFirmIds`, written by one writer, `swap_svc_firm.py`. The write is conditional and fires only on a read of cottonwood,
  service, active.
- **ONE secret resource-policy entry:** `cloudops-dell2-agent-user` on `irpt/svc-irpt-analysis/password`, ADD then REMOVE, both at the laptop.
- **One GET-only read pair, nothing submitted.**
- No IAM role, host, Lambda, route or portal change. This is the st28 W1/W2 blast radius (ST29 half @086d060f82) with no host send.
- **Rollback:** W2 and S-, which also run in every branch of R.

## Conditions

1. **Before-reads are printed,** and any before-read that differs means STOP before the leg:
   - W1 reads cottonwood;
   - S+ reads the principal absent (explicitDeny).
2. **The 30-minute bound from W1 is hard,** with no extension. The after-read must show svc on `allowedFirmIds: cottonwood` and the dell2 simulate at `explicitDeny`.
   Either one not reading as expected: STOP, restore, and report here.
3. **The record keeps codes, state and section names only.** No numbers, client strings or report body go to the ledger, a row or a message.
4. **The laptop legs are opened as a cross-box ORDER through `0.0.0_AB_MSTR~DELL2`,** never typed on dell2.
   - If `0.7.0_AE_CloudOps~DELL2` does not ack W1, an MSTR-seated CloudOps lane substitutes under @5ff94852a6.
5. **R's 200 is evidence for FWD-1, not its grade.** FWD-1 is graded at the round analysis on the CVO's slug.

**Verdict: GIVEN**, for exactly these five legs under conditions 1 to 5.

-- 1.0.0_SA_CTO~DELL2
