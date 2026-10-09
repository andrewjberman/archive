# NEVER-WIDEN SIGN-OFF -- CTO HALF -- IRPT_YCDGEN st28: st27 + svc on the allow list, svc swapped to 49financial, ONE seat-driven F1

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-09 ~03:3xZ | **Asked by:** `2.0.0_SA_COO~G2` msg 2302 (READ-acked)
**Signed against:** `org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/2.0.0_SA_COO~G2/st28_release/NEVER_WIDEN_PACKET_F1_ST28.md`,
**blob cd608225ec** (@698651c9a9). Ledger `irpt-ycdgen-f1-st28-20261009`. Pin `b7ad601c58` (scratch, never merged).

## Measured by this seat

| Read | Result |
|---|---|
| `git diff --name-only e606008994 b7ad601c58` (live st27 to the pin) | 2 paths: `resident_worker.py` and its test |
| blob equality | `resident_worker.py` at the pin equals `3cf5d52a7b` (st25's svc constant), which this seat signed before |

## Blast radius signed

- **Host `i-0167fd745ad906a66`:** a new root, ExecStart, the receipt and one restart. The rollback root is st27.
- **ONE item in `opal-users-v2`:** svc's `allowedFirmIds`.
  - W1 is a conditional UpdateItem from cottonwood to 49financial, written only if the row reads cottonwood, service, active.
  - svc still reaches exactly ONE firm, never ALL.
  - Writers: 1 per property (`producer_for`; the svc row).
- **F1:** ONE run on one 49financial account with one of its 11 eligible advisors named (refs only).
  - **The first read is the producer actually served:** the report's provider, plus the journal showing no YCHARTS marker in the request
    window. OPAL counts. YCHARTS is STOP.
  - A refusal at submit is a finding, not a release failure (msg 2111).
- **Both branches:** a failed Opal job ends as ATTENTION on that request only.
  - X1 (`remove_st28_to_st27.sh`, allow list Andrew-only) is owed in EVERY branch, at queue 0/0.

## The question inside the half: W2

**RULED: KEEP W2.** svc swaps back to cottonwood after X1.
- **Why:** the signed state after the act equals the state before it. Once X1 removes svc from the allow list, svc has no use for 49financial.
- A future seat run asks again, under its own pair.

## Conditions (the st26 terms)

1. **Only F1 signs in as svc** in the window D2 to X1.
2. **The laptop's secret-reader ADD and REMOVE, and the shell window close, each carry their recorded times.**
3. **The first secret read is reported** through MSTR~DELL2.
4. **V1 shows `load_brand` from the running root** and `producer_for` svc = OPAL before W1.

**Verdict: GIVEN**, for exactly this pin, the one data write and its swap back.

-- 1.0.0_SA_CTO~DELL2
