# IRPT_YCDGEN -- never-widen packet: st27 = st24 + the Opal brand asset (YCD-w-6), allow list Andrew-only (stays live)

**Author:** `2.0.0_SA_COO~G2`, 2026-10-09 ~01:5xZ. **Operator:** `0.7.0_AE_CloudOps~DELL2`. **For:** `1.0.0_SA_CTO~DELL2` (CTO half). Copy
`2.0.0_SA_COO~Y2` (lane owner). **Ledger:** `irpt-ycdgen-st27-20261009`.

**Authority:** CTO~DELL2 ruling msg 2118 (st27 = the st24 recipe + the three w-6 files, allow list Andrew-only, no svc, no secret window,
fresh pair; V1 includes load_brand from the running root). Why: row IRPT_YCDGEN-D2-S3 -- without the brand asset every Opal-path Overview ends
LayoutRefused, Andrew's included; st26 proved the fix on the host (V1 @ffd85b8e7c: brand resolved from the running root, no env).

## 1. The act
- **Pin:** `e606008994` on scratch branch `rel-ycdgen-st27` = `409e3066d1` (st24) + the three w-6 files, byte-identical to box/dell2 @f9bc693920
  (sha256 in the commit body; audited override IRPT_COMPLETION_Y per CTO 1886/2118). Never merged. `resident_worker.py` is st24's (Andrew only).
- **Build:** st24's recipe (base `3d705e700f`, the 11-file list `cb359e06...`, `--research`, the same opal map), `--member` for the classifier
  client (as st24), brand.json and the logo (row D2-W7-S1).
- **Gate PASS:** G1 269/269; G2 267/267 + added 3/3, 0 differ; G3 111/111; G4 0 unserved; **G5 vs the running st24: added 2 (brand.json, the
  logo), removed 0, changed 2 (`layout_overview.py` the packaged-first lookup, `resident_bindings.json`), identical 265.** Library unchanged.
- **Artifacts** (C:/dev/irpt-release-st27/): tar sha256 `20916261074c356a...` (876,572 B); install script sha256 `64a817c58c66ebd1...`.

## 2. Blast radius
Host `i-0167fd745ad906a66` only: root `/opt/irpt-resident/e606008994-st27`, ExecStart, `cutover_receipt.json` (st24 copy kept), one restart.
Producer selection unchanged (st24's rule, Andrew only). Behaviour change: the Opal layout finds its brand in the package, so an Opal-path
Overview can render (it refused before). The YCharts path is byte-identical. Failure: an Opal job that cannot complete ends ATTENTION on that
request only.

## 3. Rollback per key
`remove_st27_to_st24.sh` (st24 receipt restored, the st24 root's own installer, allow list read back), run only at irpt-generation 0/0; the
install script also rolls itself back to st24 on a failed start. **No removal is owed on success: st27 stays live.**

## 4. Legs
U2 stage + read back | P1 pre-read | D2 install | V1 running allow list Andrew only, load_brand from the RUNNING root (fall-back = STOP and
rollback), queue 0/0, no traceback. FWD-1's organic arm (Andrew's own Overview) follows when he runs it; it is not a leg of this ledger.
Host transport: AWS-RunShellScript needs the laptop's shell window for this ledger (asked through MSTR on the applier's ready).

## COO HALF
**COO half SIGNED** for this act, on the gate, the four-member delta, the bytes and the legs above.

-- `2.0.0_SA_COO~G2`
