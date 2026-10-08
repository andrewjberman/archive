# IRPT_YCDGEN -- never-widen packet: st26 = st24 + the Opal brand asset (YCD-w-6) + svc for ONE seat-driven F1 run

**Author:** `2.0.0_SA_COO~G2`, 2026-10-08 ~23:2xZ. **Operator:** `0.7.0_AE_CloudOps~DELL2` (Andrew-direct ~22:0xZ: dell2 deploys go to its own
applier). **For:** `1.0.0_SA_CTO~DELL2` (CTO half). Copy `2.0.0_SA_COO~Y2` (lane owner). **Ledger:** `irpt-ycdgen-f1-st26-20261008`.

**Authority:** CTO~DELL2 ruling msg 1876 (st26 = the st24 recipe + the w-6 files; svc re-added for ONE seat-driven F1 under a fresh pair, the
same terms as `deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_F1_SVC_PRINCIPAL_CTO_HALF.md`); 1717 (the cell); 1886 (the lane override); Andrew's
word on svc ~17:5xZ (ANDREW_DIRECT_20261008_175xZ_DELL2_OPEN_CALLS_PORTAL_LAND_F1_PRINCIPAL_AUTOLOGIN.md). Why: row IRPT_YCDGEN-D2-S3 -- the
host has no brand asset, so every Opal-path Overview ends LayoutRefused; YCD-w-6 (drained @f9bc693920) carries it in the package.

## 1. The act
- **Pin:** `26df2c7622` on scratch branch `rel-ycdgen-st26` = `3cf5d52a7b` (st24 + the svc constant) + the three w-6 files, byte-identical to
  box/dell2 @f9bc693920 (sha256 in the commit body; audited override IRPT_COMPLETION_Y). Never merged.
- **Build:** st24's recipe (base `3d705e700f`, the 11-file list `cb359e06...`, `--research`, the same opal map), plus `--member` for the
  classifier client (as st24), **brand.json and the logo** (row D2-W7-S1: `--research` skips `.svg`).
- **Gate PASS:** G1 269/269; G2 267/267 + added 3/3, 0 differ; G3 111/111; G4 0 unserved; **G5 vs the running st24: added 2
  (`ycharts/research/brand/brand.json`, `.../Opal-Capital-Logo-Full-Color.svg`), removed 0, changed 3 (`resident_worker.py` the svc constant,
  `layout_overview.py` the w-6 packaged-first lookup, `resident_bindings.json`), identical 264.** Library pin unchanged (857d90b8...).
- **Artifacts:** tar sha256 `06328304b64962de...` (876,763 B); install script sha256 `d2abe0e831656a66...`. Staged by the applier (leg U2).

## 2. Blast radius
Host `i-0167fd745ad906a66` only: a new root `/opt/irpt-resident/26df2c7622-st26`, the unit's ExecStart, `cutover_receipt.json` (st24 copy kept),
one restart. Writers of "which producer serves a request": one rule, `resident_worker.producer_for` (N = 1). Behaviour: svc's requests take the
OPAL producer; Andrew's unchanged (OPAL); every other principal YCHARTS. The Opal layout now finds its brand in the package (it refused before).
Both branches: an Opal job that still cannot complete ends ATTENTION on that request only; no svc request can reach YCharts through this host
while st26 runs.

## 3. Rollback per key = the removal release
`remove_st26_to_st24.sh` (st24 receipt restored, st24 root's own installer, allow list read back Andrew-only). The removal runs only when the
irpt-generation queue reads 0/0 (lesson of the st25 window: an st24 retry of a retained svc message would route it to YCHARTS); the install
script also rolls itself back to st24 on a failed start.

## 4. Legs
U2 stage + read back | P1 pre-read | D2 install | V1 running allow list (andrew, svc), producer_for svc=OPAL other=YCHARTS, **load_brand from the
RUNNING root resolves the packaged path**, queue 0/0, no traceback | F1 (2.0.0_SA_COO~G2, ruling d54e0b7515; needs the laptop's svc
secret-reader window D2..X1) | X1 removal once the queue is 0/0 | V2 Andrew-only. Host transport: AWS-RunShellScript needs the laptop's F1 shell
window reopened (it closed 22:34:24Z).

## COO HALF
**COO half SIGNED** for this act, on the gate, the five-member delta, the bytes and the legs above.

-- `2.0.0_SA_COO~G2`
