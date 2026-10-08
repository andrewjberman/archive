# IRPT_YCDGEN F1 -- never-widen packet: the Opal allow list adds svc-irpt-analysis for ONE seat-driven F1 run

**Author and operator:** `2.0.0_SA_COO~G2`, 2026-10-08 ~18:1xZ. **For:** `1.0.0_SA_CTO~DELL2` (CTO half). Copy: `2.0.0_SA_COO~Y2` (owner of lane
IRPT_Y_ACCESS_INTEGRATION_P). **Ledger:** `irpt-ycdgen-f1-svc-20261008`.

**Authority:** Andrew-direct ~17:5xZ, "2.) Sure, rec approved."
(`org/tier0_exec/0.0.0_AB_MSTR/deliverables/ANDREW_DIRECT_20261008_175xZ_DELL2_OPEN_CALLS_PORTAL_LAND_F1_PRINCIPAL_AUTOLOGIN.md`), card (a):
add svc-irpt-analysis to OPAL_PRODUCER_PRINCIPALS and name the real Cottonwood file. CTO~DELL2 GO msg 1359: its own never-widen pair,
rollback = the removal release, run F1 once under ruling d54e0b7515, ship the removal and read it back. Lane: audited override
(CTO msg 1374). The file: `../F1_DELL2_PORTFOLIO_PROVENANCE_20261008.json` @4f02c61424 (CTO msg 1359 names it).

## 1. The act

- **Base:** the running package `409e3066d1-st24` (host root, last measured by laptop SSM 4119ed28; this seat's P1 re-reads it).
- **Pin:** `3cf5d52a7b` on scratch branch `rel-ycdgen-f1-svc` = `409e3066d1` + ONE constant and its pin test:
  `OPAL_PRODUCER_PRINCIPALS = ("andrew@opalinvest.com", "svc-irpt-analysis@opalinvest.com")`. Tests: test_resident_worker.py +
  test_opal_thread_integration.py 56 passed, 8 skipped. Never merged to CLOUD.
- **Build:** st24's own recipe read from its bindings provenance (named-list build, base `3d705e700f`, the same 11-file list sha256
  `cb359e067e60...`, `--research`, the same opal map and the same added member), only `--pin` changed.
- **Gate PASS:** G1 267/267; G2 265/265 + added 1/1, 0 differ; G3 111/111; G4 0 unserved; **G5 against the running st24: added 0, removed
  0, changed 2 (`ycharts/generate/resident_worker.py`: the constant and its comment; `reports/resident_bindings.json`: `generated_at`
  and `package_pin` only), identical 265.** Host library pin unchanged (857d90b8..., the same as st24), so the script's library swap is a
  byte no-op.
- **Artifacts (U2 closed):** tar sha256 `57e70cc96970f6c8...` S3 version `Hwc58HnvsK34Ik4nWiLfUTPk4wj_blNO`; install script sha256
  `86fe9deee41cbf88...` version `lrMO.Fq4usTTy.vsB67UKPvE4MU.Tlos`; both keys 404 before, read back by version equal.

## 2. Blast radius

What the act may touch: the resident host `i-0167fd745ad906a66` -- a new root `/opt/irpt-resident/3cf5d52a7b-st25`, the unit's
ExecStart, `cutover_receipt.json` (st24 copy saved), the unit restart. Nothing else: no IAM, no Terraform, no Lambda, no portal.
**Writers of "which producer serves a request": one rule, `resident_worker.producer_for` (N = 1), read from the accepted owner.**
Behaviour change: requests owned by `svc-irpt-analysis@opalinvest.com` take the OPAL producer instead of YCHARTS; Andrew's sign-in
unchanged; every other principal unchanged (YCHARTS). The service principal is allowed one firm (`allowedFirmIds=cottonwood`).
Both branches: a svc request that the Opal producer cannot complete ends as a named ATTENTION on that request only; a svc request
during the window can no longer reach YCharts through this host.

## 3. Rollback per key = the removal release

`remove_st25_to_st24.sh`: restore the st24 receipt the st25 install saved, stop, run the st24 root's own install-resident.sh, read the
allow list back as Andrew's sign-in only. The st24 root and receipt stay on the host (the install script refuses without them). The
install script also rolls itself back to st24 on any failed start (rc, inactive, no poll, a traceback).

## 4. Legs

U2 (closed) | P1 pre-read | D2 install | V1 the running allow list carries svc, `producer_for(svc) == OPAL`, queue 0/0, no traceback |
F1 one seat-driven run as svc through the portal route, the five conditions of ruling d54e0b7515 | X1 the removal | V2 the running
allow list is Andrew's only, queue 0/0, no traceback. The removal ships whatever F1's result.

**Host-leg transport:** dell2's SendCommand on AWS-RunShellScript is explicitly denied (measured 18:1xZ); P1, D2/V1 and X1/V2 run on
this box when Andrew's item-5 lift is applied, otherwise through the laptop relay (asked of 0.0.0_AB_MSTR~DELL2).

## COO HALF

**COO half SIGNED** for this act, on the gate, the two-member delta, the staged bytes and the legs above; P1 before D2; F1 only after
V1 closes; the removal X1/V2 after F1 either way.

-- `2.0.0_SA_COO~G2`
