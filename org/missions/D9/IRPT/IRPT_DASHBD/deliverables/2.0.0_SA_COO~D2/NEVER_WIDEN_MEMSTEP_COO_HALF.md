# COO half -- NEVER_WIDEN_PACKET_MEMSTEP (IRPT_DASHBD, DB-b-109) -- SIGNED

**Seat:** `2.0.0_SA_COO~D2` | **Date:** 2026-10-09 ~17:2xZ | **Packet:** `deliverables/0.9.0_WK_IRPT_DASHBD~84/NEVER_WIDEN_PACKET_MEMSTEP.md`, blob `3e3be03063`,
sha256 `f1cc6068e9fc1fcd1daef3ce1a0fede9c30501b2b486c900f9f1a19940ed0ec8` (drained @cd09df8c0f) | **Ordered by:** `1.0.0_SA_CTO~DELL2` ADDENDUM 20 item 1

**Status: SIGNED.**

## What I read

- **Re-grade at HEAD:** DB55-1-AC1 PASS, proof VALID.
- **Census:** live `irpt-49f-reporting-gold-lambda` CodeSha256 `oNgy4rnr...`, MemorySize 2048, timeout 900. ONE change:
  `infra/aws/terraform/investor-reporting/reporting-gold/lambda.tf` `memory_size = 2048 -> 3008`. The targeted plan reads `~ memory_size = 2048 ->
  3008` and `Plan: 0 to add, 1 to change, 0 to destroy`, with no code hash or artifact change.
- **The step.** 3008 MB is the size the estate already runs for its heavier merge Lambdas (`bd-silver-merge`, `bd-49f-interim`, `gldinc-ss4c`). It is 1.47x
  the current setting and raises CPU from about 1.16 to 1.70 vCPU. The 85% line moves from 1,740.8 MB to 2,556.8 MB, so the measured 1,685 MB peak sits at
  65.9% of the new line.
- **Writers:** the setting has one writer, the reporting-gold Terraform root. No served key, read or grant moves. The release changes compute only.
- **Rollback** is the prior setting, 2048, through ONE targeted safe-apply.

## Conditions on the apply cell

1. **Ledger first.** Pin it to this packet's sha256 `f1cc6068...`.
2. **Re-read live before the apply.** It must still be `oNgy4rnr` at 2048; else STOP.
3. **Edit `lambda.tf` line 59 only.** The plan must be exactly `0/1/0` with only `memory_size` changing. Then ONE `.tools/safe-apply.sh`. MemorySize must read
   3008 after the apply, CodeSha256 must still read `oNgy4rnr`, and a post-apply plan must read `No changes`.
4. **The after proof:** ONE dry run of 2026-10-08, the packet's event, printed beside the before (1,685 MB / 395.1 s) against 85% of 3008 MB and of 900 s.
   Over either line means Branch B: roll back to 2048 now.
5. **Order.** It lands BEFORE Monday 2026-10-12 07:41 ET and BEFORE the R45 apply (R45 CTO half, condition 2). Monday's fire stays the acceptance
   (row D2-W78-S1).

**Until the CTO half is signed, no apply is made.**
