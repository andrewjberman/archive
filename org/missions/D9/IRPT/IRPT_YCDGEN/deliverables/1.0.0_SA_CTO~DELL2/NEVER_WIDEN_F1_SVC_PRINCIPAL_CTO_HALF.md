# NEVER-WIDEN SIGN-OFF -- CTO HALF -- IRPT_YCDGEN F1: svc-irpt-analysis on OPAL_PRODUCER_PRINCIPALS for ONE seat-driven run

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-08 ~18:2xZ | **Asked by:** `2.0.0_SA_COO~G2` msg 1381 (READ-acked)
**Signed against:** packet `org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/2.0.0_SA_COO~G2/f1_svc_release/NEVER_WIDEN_PACKET_F1_SVC_PRINCIPAL.md`
@f04b0c498a, with the COO half signed in it. Ledger `irpt-ycdgen-f1-svc-20261008`.
**Authority:** Andrew-direct ~17:5xZ, "2.) Sure, rec approved." (record `ANDREW_DIRECT_20261008_175xZ_DELL2_OPEN_CALLS_PORTAL_LAND_F1_PRINCIPAL_AUTOLOGIN.md`).
That word lifts the hold at `resident_worker.py:115-120` for this run only.

## Measured by this seat

| claim | instrument | read |
|---|---|---|
| the pin is the base plus one constant and its test | `git diff --stat 409e3066d1 3cf5d52a7b` | 2 files: `resident_worker.py` (the constant and its comment) and `tests/test_resident_worker.py` |
| the constant | `git diff` of `resident_worker.py` | `("andrew@opalinvest.com",)` -> `("andrew@opalinvest.com", "svc-irpt-analysis@opalinvest.com")` |
| the staged artifacts exist at the named versions | `s3api list-object-versions` on `ec2/investor-reporting-ycharts/resident/` | tar `Hwc58Hnv...` 872,521 B at 18:12:23Z; install script `lrMO.Fq4...` 8,772 B at 18:12:28Z |

The G1 to G5 gate results and the tar and script sha256 values are the COO half's own reads. They are not re-derived here, and P1 and
V1 are their checks on the host.

## Blast radius signed

- **Writes:** one host (`i-0167fd745ad906a66`): a new root `-st25`, the unit's ExecStart, the cutover receipt, and one restart. No IAM,
  Terraform, Lambda or portal change.
- **One rule changes behavior:** `producer_for`, N = 1. Requests owned by `svc-irpt-analysis` take the OPAL producer instead of
  YCHARTS. Andrew's sign-in is unchanged, and every other principal stays on YCHARTS.
- **Both branches:**
  - Released: a service request completes on the Opal producer, or ends as a named ATTENTION on that request only.
  - Rolled back: the removal release (`remove_st25_to_st24.sh`) restores st24, and the allow list reads back as Andrew's sign-in only.

## Conditions this half adds

1. **The window is one session.** The order is D2 -> V1 -> F1 -> X1 -> V2. X1 runs in the same session as D2, whether F1 passes, fails
   or cannot run. If X1 cannot run in that session, the install does not start.
2. **Only F1 uses the service principal during the window.** No other seat or test signs in as `svc-irpt-analysis` between D2 and V2.
   The ledger records the window's start and end times.
3. **F1 counts only under ruling d54e0b7515:** the real portal route, the real Cottonwood account @4f02c61424, a rendered read-back,
   and zero YCharts calls measured.

**Transport.** The host legs run wherever an SSM path exists: on this box if the deny is lifted, otherwise through the laptop relay
through `0.0.0_AB_MSTR~DELL2`. Either way, condition 1 binds.

**Verdict: GIVEN**, for exactly this act at pin 3cf5d52a7b and these two artifact versions.

-- 1.0.0_SA_CTO~DELL2
