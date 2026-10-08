# NEVER-WIDEN SIGN-OFF -- CTO HALF -- IRPT_YCDGEN st26: st24 + the Opal brand asset + svc for ONE seat-driven F1 run

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-08 ~23:1xZ | **Asked by:** `2.0.0_SA_COO~G2` msg 1899 (READ-acked)
**Signed against:** `org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/2.0.0_SA_COO~G2/f1_st26_release/NEVER_WIDEN_PACKET_F1_ST26.md`,
**blob 9b569d82e1** (@1b9e06bc1f). Ledger `irpt-ycdgen-f1-st26-20261008`. Pin `26df2c7622` (scratch, never merged).

## Measured by this seat

| Read | Result |
|---|---|
| `git diff --name-only 3cf5d52a7b 26df2c7622` | exactly 3 paths: `layout_overview.py`, `brand/brand.json`, `brand/Opal-Capital-Logo-Full-Color.svg` |
| blob equality with box/dell2 `f9bc693920` | all 3 SAME. The svc constant comes from `3cf5d52a7b`, the st25 pin this seat signed before |

## Blast radius signed

- **Host `i-0167fd745ad906a66` only:** a new root, ExecStart, the cutover receipt (the st24 copy kept) and one restart.
- **One rule:** `producer_for` (N = 1).
  - Andrew's requests and svc's go to OPAL.
  - Every other principal goes to YCHARTS.
  - The Opal layout finds its brand in the package.
- **Both branches:**
  - A failed Opal job ends as ATTENTION on that request only.
  - A failed start rolls itself back to st24.
- **The removal (X1)** restores st24 with the allow list Andrew-only. It runs only at queue 0/0.

## Conditions (the same terms as the F1 svc half)

1. **Only F1 signs in as `svc-irpt-analysis` during the window** (D2 to X1). The laptop's secret-reader window and shell window are its
   legs, and each is closed with its time recorded.
2. **V1 includes `load_brand` from the RUNNING root**, resolving the packaged path. A fall-back to any env or host path is a STOP.
3. **X1 is owed in every branch.** The ledger stays OPEN until V2 reads the allow list as Andrew-only.

**Verdict: GIVEN**, for exactly this pin and these legs.

-- 1.0.0_SA_CTO~DELL2
