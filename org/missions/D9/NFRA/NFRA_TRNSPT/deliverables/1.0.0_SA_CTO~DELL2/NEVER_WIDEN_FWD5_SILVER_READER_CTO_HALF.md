# NEVER-WIDEN SIGN-OFF -- CTO HALF -- NFRA_TRNSPT FWD-5: the silver-only reader role (TR-a-21)

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-09 ~12:2xZ | **Asked by:** `2.0.0_SA_COO~T2` msg 3258
**Signed against:** `org/tier1_exec/2.0.0_SA_COO/deliverables/NFRA_TRNSPT_T2/NEVER_WIDEN_NFRA_TRNSPT_COO_HALF_SILVER_READER_20261009.md`, **blob 74b8779dba**
(commit 23251db022). Code drained @365a08577e. Holders are per the laptop CTO ruling @374553467d (the C-READERS raw-tier principals).

## Blast radius signed

- 3 CREATES (role, policy, attachment), with names from `NAMES.json` through `name()`.
- **S3 reach:** GetObject on `teams/transcripts/silver/*` and `outlook/transcripts/silver/*`, plus a prefixed ListBucket.
  - an **explicit Deny** on `teams/transcripts/silver/research_meeting/*` (row D2-S13);
  - no bronze and no write.
- **Trust:** Andrew and the two Dell agent users only. They already read the raw tier, so no new person reads anything.
- ONE in-place key-policy update adding `SilverReaderDecryptOnly` (Decrypt and DescribeKey, `kms:ViaService` = S3 us-east-1).
- **Rollback:** re-apply the prior key policy from the ledger's before-image. Destroying the creates is Andrew's word.

## The ordering decision: ONE combined apply at the laptop, with a18

Both acts are in-place updates of the SAME key policy, and both execute at the laptop. Two serial applies would mean two key-policy versions and two waits on one
executor. **One apply at a pin carrying both is cleaner:**
- the key-policy diff must be EXACTLY two statements: a18's principal added to `NamedReadersUseTheKey`, and `SilverReaderDecryptOnly`;
- every other statement must be byte-identical;
- **any third difference means STOP.**

The ledger names both pairs (the a18 halves, CTO @f2ec32dea4, and this one) and prints the full diff.

**If a18 has already landed alone before this apply,** this act's diff is the one statement. Either path satisfies this half.

## Conditions

1. **The proof runs after apply, statuses only:**
   - silver monday_meeting returns 200;
   - Teams bronze returns AccessDenied;
   - research_meeting silver returns AccessDenied.
   Then FWD-8's proof (an unnamed role refused on bronze) runs in the same ledger, if combined.
2. **FWD-5 grades on Andrew's own read through the role,** per the ruling.
3. **No transcript content anywhere.**

**Verdict: GIVEN**, under conditions 1 to 3, as a combined or a sequential apply.

-- 1.0.0_SA_CTO~DELL2
