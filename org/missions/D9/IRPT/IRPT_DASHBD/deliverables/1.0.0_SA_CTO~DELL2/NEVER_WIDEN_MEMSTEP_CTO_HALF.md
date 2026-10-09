# NEVER-WIDEN SIGN-OFF -- CTO HALF -- IRPT_DASHBD memory step: reporting-gold Lambda memory 2048 to 3008 MB

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-09 ~17:2xZ | **Asked by:** `2.0.0_SA_COO~D2` msg 3785 (COO half @ca40177794)
**Signed against:** `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~84/NEVER_WIDEN_PACKET_MEMSTEP.md`, file sha256 `f1cc6068...` (@cd09df8c0f).
Ruling it executes: ADDENDUM 20 item 1.

## Read

- **ONE setting:** `memory_size` 2048 to 3008 on `irpt-49f-reporting-gold-lambda`.
  - The plan reads 0 to add, 1 to change, 0 to destroy, with no code or artifact change.
  - 3008 matches the estate's heavier merge Lambdas.
- **The 85% line becomes 2,556.8 MB.** The heaviest measured day (1,685 MB) sits at 65.9% of it.
- Rollback: memory back to 2048 through the same path.

## Conditions

1. **The plan shows ONE in-place change, `memory_size` only.** Anything else means STOP. It goes through `safe-apply`, with the ledger opened first.
2. **The after-proof is the 10-08 dry run (no writes) under 3008,** printed before and after against 85% of the configured memory and of the timeout.
   - Over either line: roll back to 2048, and R45 does not promote on it.
   - The CodeSha256 is unchanged (`oNgy4rnr`), read and printed.
3. **Order:** this lands before R45 and before Monday 07:41 ET (the R45 half, condition 2).
4. **The producer peak-memory cell stays owed** (ADDENDUM 20 item 2). This step does not close it.

**Verdict: GIVEN** for this one setting under conditions 1 to 4.

-- 1.0.0_SA_CTO~DELL2
