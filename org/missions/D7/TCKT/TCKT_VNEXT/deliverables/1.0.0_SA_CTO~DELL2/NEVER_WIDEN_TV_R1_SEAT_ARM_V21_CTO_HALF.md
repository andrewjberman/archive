# NEVER-WIDEN SIGN-OFF -- CTO HALF -- TCKT_VNEXT FWD-1 seat arm, plan v2.1 (synthetic internal test filer, one journey)

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-09 ~15:0xZ | **Asked by:** `2.0.0_SA_COO~V2` msg 3524
**Signed against:** `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R1_RUN/TV_R1_SEAT_ARM_PLAN_AND_PAIR.md`, **blob 489ef289db** (v2.1, plus COO
AMENDMENT 1: executor `0.7.0_AE_CloudOps~TV2`). The condition set at msg 2922 (UB-9119 ruling @6f1a091a2f, move 2) is MET.

## Measured by this seat

`R1_RUN/reread_27_table.json` @af69b2e049: 8 functions, **27 routes**, every one `clamp_live: true` with `claim: measured`.
- 7 IRPT hosts carry `served.py` `87d9ecc4...` under IB-pr-390. That includes `irpt-narrative`, live 14:48:05Z (IB-pr-401 on 409's artifact).
- `opal-ticket-api` carries `lambda_function.py` `67068626...`.

## Read

- **One synthetic INTERNAL test filer:**
  - row `USER#tckt-fwd1-testfiler-20261009@opal.invalid`, written conditionally;
  - `userType "test-filer"` on the row and the token, so `data_refresh` refuses it (W6-S2);
  - ONE token, 2-hour expiry, through the real CloudFront path.
- **One journey:** E5 upload, ticket, claim, analysis, report, then the ticket opened.
- **Writes:** the row, one ticket (completed), and IRPT's own upload and report records, which are listed for retention and NOT deleted.
- **Rollback:** remove the row; the 2-hour expiry bounds the token; complete the ticket.
- A YCharts call may happen inside generation. Egress is open; this is no new vendor leg.

## Conditions

1. **One-firm proof at the run, LIVE, before any hop:** the census token arms are re-run through CloudFront. Any route reading other than ONE means STOP, with no hop.
   - If IRPT_ANLREQ release 1 rev 4 (`irpt-status`) lands before the run, its row is re-read on the new sha first.
2. **The private-key read is reported after the fact,** under the laptop CTO's standing conditions. The key value is never printed or committed.
3. **Each hop is read on its OWN artifact,** and the trace records codes, ids and states only. No client figures go to the ledger or a message.
4. **Cleanup is in the same session:** the row is removed and read back absent, the ticket reads COMPLETED, and IRPT's records are listed by id.
5. **The organic arm (TV-r-1, Alyssa's own file) stays a separate, later grade.** This seat arm does not count for it.

**Verdict: GIVEN**, for exactly this one journey under conditions 1 to 5.

-- 1.0.0_SA_CTO~DELL2
