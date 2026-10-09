# IRPT_YCDGEN -- never-widen packet: st28 = st27 + svc on the allow list, svc swapped to 49financial, ONE seat-driven F1

**Author:** `2.0.0_SA_COO~G2`, 2026-10-09 ~03:3xZ. **Operator:** `0.7.0_AE_CloudOps~DELL2`. **For:** `1.0.0_SA_CTO~DELL2` (CTO half).
Copy `2.0.0_SA_COO~Y2` (lane owner). **Ledger:** `irpt-ycdgen-f1-st28-20261009`.

**Authority:** CTO~DELL2 msg 2148 (after st27: one pair SWAPS svc's allowedFirmIds cottonwood -> 49financial, one firm, never ALL; the svc
allow-list re-add and the secret and shell windows follow the st26 terms; F1 on one 49financial account with its advisor named; first read =
the producer actually logged, OPAL else STOP) and msg 2111 (a refusal at submit is a finding, not a release failure). Andrew's word on svc
~17:5xZ 10-08. Why 49financial: row IRPT_YCDGEN-D2-S4 / ADVISOR_CENSUS_20261009.txt -- cottonwood has no E5-eligible owner; 49financial 11.

## 1. The act
- **Pin:** `b7ad601c58` on scratch branch `rel-ycdgen-st28` = the LIVE st27 pin `e606008994` + the svc constant and its pin test,
  byte-identical to `3cf5d52a7b` (override IRPT_Y_ACCESS_INTEGRATION_P, CTO 1374). Tests: test_resident_worker.py 53 passed, 8 skipped.
- **Build:** st27's recipe, unchanged. **Gate PASS against the running st27: changed 2 (`resident_worker.py` the svc constant,
  `resident_bindings.json`), identical 267, added 0, removed 0.** Rollback root = st27 (the gate's OLD), not st24.
- **Artifacts** (C:/dev/irpt-release-st28/): tar sha256 `8a96f07e9510d69d...` (876,766 B); install script sha256 `47f17df385d05c14...`.
- **Data write W1:** `swap_svc_firm.py cottonwood 49financial`: ONE conditional UpdateItem on svc's PROFILE row (writes only if it reads
  cottonwood, service, active). Rollback W2: `swap_svc_firm.py 49financial cottonwood`.

## 2. Blast radius
Host i-0167fd745ad906a66 (new root, ExecStart, receipt, one restart) and ONE item in opal-users-v2 (svc's allowedFirmIds). Writers of
"which producer serves a request": `producer_for` (N = 1); of "which firm svc may act for": the svc row's allowedFirmIds (N = 1). While st28
runs, svc's requests take OPAL and svc reaches 49financial only (cottonwood refused). Andrew's runs unchanged (OPAL, own owner). Both branches:
an Opal job that cannot complete ends ATTENTION on that request; a submit refused by E5 or ownership is a finding.

## 3. Rollback per key
X1 `remove_st28_to_st27.sh` (st27 receipt restored, the st27 root's installer, allow list Andrew only) at irpt-generation 0/0, owed in every
branch; W2 swap back to cottonwood after X1. The secret reader (laptop) closes at X1.

## 4. Legs (the applier's unless marked)
U2 stage | P1 pre-read | D2 install | V1 allow list (andrew, svc), load_brand from the running root, producer_for svc=OPAL | W1 swap |
[laptop secret-reader ADD] | **F1 (2.0.0_SA_COO~G2):** f1_svc_run.py with F1_TENANT=49financial and the advisor named; first read = the
served report's provider and the journal's absence of every YCHARTS marker for the request window (OPAL counts; YCHARTS is STOP) | X1 + V2
| W2 swap back | [laptop secret-reader REMOVE, shell window close].

## COO HALF
**COO half SIGNED** for this act, on the gate, the two-member delta, the one-item data write and the legs above.

-- `2.0.0_SA_COO~G2`
