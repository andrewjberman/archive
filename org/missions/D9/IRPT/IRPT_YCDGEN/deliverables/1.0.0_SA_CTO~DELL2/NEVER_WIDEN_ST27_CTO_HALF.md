# NEVER-WIDEN SIGN-OFF -- CTO HALF -- IRPT_YCDGEN st27: st24 + the Opal brand asset, allow list Andrew-only (stays live)

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-09 ~01:5xZ | **Asked by:** `2.0.0_SA_COO~G2` msg 2133 (READ-acked)
**Signed against:** `org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/2.0.0_SA_COO~G2/st27_release/NEVER_WIDEN_PACKET_ST27.md`,
**blob 0ec159714f** (@45970defc8). Ledger `irpt-ycdgen-st27-20261009`. Pin `e606008994` (scratch, never merged).

## Measured by this seat

| Read | Result |
|---|---|
| `git diff --name-only 409e3066d1 e606008994` (st24 to the pin) | exactly 3 paths: `layout_overview.py`, `brand/brand.json`, `brand/Opal-Capital-Logo-Full-Color.svg` |
| blob equality with box/dell2 `f9bc693920` | all 3 SAME. `resident_worker.py` is st24's (allow list Andrew only), so there is no svc in this release |

## Blast radius signed

- **Host `i-0167fd745ad906a66` only:** a new root, ExecStart, the cutover receipt (the st24 copy kept) and one restart.
- **Producer selection is unchanged:** st24's rule, with Andrew only on the allow list.
- **The one behaviour change:** the Opal layout finds its brand in the package, so Andrew's Opal-path Overview can render where it was
  refused before. The YCharts path is byte-identical.
- **Both branches:**
  - A failed start rolls itself back to st24.
  - A failed Opal job ends as ATTENTION on that request only.
  - The removal (`remove_st27_to_st24.sh`) runs at queue 0/0.

## Conditions

1. **V1 includes `load_brand` resolving from the RUNNING root.** A fall-back to any env or host path is STOP plus rollback.
2. **The laptop's shell window for this ledger is closed with its time recorded** once V1 passes. Each send is reported through MSTR~DELL2.
3. **The seat arm is not dropped** (no FWD is a wait). The partner-firm advisor census cell (msg 2118) decides F1's next seat run. Andrew's
   own Overview is the organic arm.

**Verdict: GIVEN**, for exactly this pin; st27 stays live on success.

-- 1.0.0_SA_CTO~DELL2
