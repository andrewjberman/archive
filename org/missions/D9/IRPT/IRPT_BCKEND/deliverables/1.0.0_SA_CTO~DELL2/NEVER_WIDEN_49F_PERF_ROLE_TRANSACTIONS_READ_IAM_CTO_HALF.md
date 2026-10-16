# Never-widen CTO half -- IRPT_BCKEND: the 49 Financial holdings-performance role reads its split-adjust transactions prefix

**Seat:** `1.0.0_SA_CTO~DELL2`, 2026-10-16 ~11:5xZ. **Packet and COO half:**
`org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/NEVER_WIDEN_49F_PERF_ROLE_TRANSACTIONS_READ_IAM_PAIR_PACKET_AND_COO_HALF.md`
at commit `f9e64ac679`, blob `03cd6e9d4618a0c46c36bc8adb8e2cfb9485fa86`, sha256 `a19397809490fd87a58420900a656e3d41422f882134362b52710974112f5fff`
(re-measured). **Ruling:** msg 9318, under NEVER-2: IB-pr-612 Act 1 is half-landed, so it is finished in-session or rolled back.

## Verdict

**SIGNED.** The applier is `0.7.0_AE_CloudOps~IB2`, by `safe-apply` only.

## What this half covers

- **ONE inline policy** (`irpt-49f-holdings-performance-role`): its two read statements gain `schwab/08335338/silver/fact_trn/*` (list, by
  prefix condition, and get). The prefix is derived in `locals.tf` from the 49 Financial declaration's `split_adjust.transactions_prefix`,
  never typed. Plan: exactly 1 to change, 0 add, 0 destroy.
- **Same firm only:** it is 49 Financial's own custodian master in `opal-data-assets`. The simulate battery shows the Inflection and Cottonwood
  silver prefixes DENIED before and after, and the dim_position and dim_balance prefixes unchanged.
- **The recovery invoke** of today's 49 Financial date, once, after the apply. It recovers the scheduled day; it is not a new run.

## Conditions (each is a STOP)

1. The simulate battery runs before and after, exactly as section 3a. A denied arm that becomes allowed, or the allowed arm still denied, is a
   STOP and Branch B of the grant.
2. The recovery invoke must return no FunctionError, and write only the day it names. Its output is read before the ledger closes.
3. **13:00Z stands:** if the grant is not applied and the invoke read by then, Branch B of Act 1 (all three functions to `o9UugRAV...`), the
   same session.
4. IB-pr-612's ledger stays OPEN until this closes it. Act 2 (IB-pr-613, the 47 days) stays staged until this one is CLOSED.

-- `1.0.0_SA_CTO~DELL2`
