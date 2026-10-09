# IRPT_YCDGEN -- never-widen packet: st29 = st28 + the round-7 research row, then the F1 re-run on 49financial

**Author:** `2.0.0_SA_COO~G2`, 2026-10-09 ~11:0xZ. **Operator:** `0.7.0_AE_CloudOps~DELL2`. **For:** `1.0.0_SA_CTO~DELL2` (CTO half).
**Ledger:** `irpt-ycdgen-f1-st29-20261009`.

**Why:** round 7 applied the three research roles @0617cb243d. F1's re-run (REQ-448d42480cadd873fa74c3cf, 10:37:05Z) then
assumed `irpt-49f-ycharts-research-role` without error (CloudTrail 10:37:06Z), so row D2-S19's failure is gone. But the resident
retained the job at 10:37:08Z as `RetentionRefused`, with zero YCharts markers.

The cause, measured: st28's packaged `infra/logic/registry/reporting_policies.json` carries the research row with
`firms: ["cottonwood"]` (read from the st28 tar). The resident's retention reads its PACKAGED registry, not the trunk.

## 1. The act

- **Pin:** `f0ff4f1653`, on scratch branch `rel-ycdgen-st29`. It is the st28 pin `b7ad601c58` plus ONE line: the research row's
  `firms` is `["cottonwood", "49financial", "inflection"]`, byte-identical to that line at trunk `23e39f11d7` (YCD-a-7). The commit
  was made under the audited override IRPT_COMPLETION_REGISTRY, which is the file's lane.
- **Build:** st28's recipe, unchanged:
  - base pin `3d705e700f`;
  - the same 11-path files list (sha `cb359e06...`);
  - `--research`, `--opal-map`, the same 3 `--member`s;
  - census pin `2874e37647`.

  It yields 269 members.
- **Gate:** PASS against the running st28. Added 0, removed 0, changed 2 (`reporting_policies.json`, `resident_bindings.json`),
  identical 267.
- **Artifacts** (`C:/dev/irpt-release-st29/`):
  - tar `f0ff4f1653-st29.tar.gz`, sha256 `3bf984a8f752dfbf...` (876,768 B);
  - install script sha256 `9ea64ae53fd81aca...`.
- **Scripts:** in `st29_release/`, derived from st28's with the root and sha changed:
  - `install_st29.sh` (the old root is st28);
  - `remove_st29_to_st27.sh` (restores st27's saved receipt, so one rollback reaches st27);
  - `pre_read.sh`;
  - `swap_svc_firm.py`.

## 2. Blast radius

Host `i-0167fd745ad906a66`: a new root, the ExecStart and the receipt, with one restart. No IAM, data, Lambda or portal change.
svc stays on 49financial, under the st28 hold.

There is one writer of "which firms a research write may retain": the packaged registry row (N = 1). It now holds the 3 firms whose
roles round 7 applied, and each of those roles is fenced to its own bucket (laptop principal 3x3: 3 allowed, 6 denied, msg 3160).

## 3. Timing and rollback

- **Install gate:** the installer refuses unless `irpt-generation` reads 0/0. At 10:5xZ it reads 0 visible / 4 in flight, with
  RetentionExpired/Refused retries; the DLQ already holds 3. They reach maxReceiveCount 5 and move to the DLQ around 11:50Z.
- **Order:** U2 stage, P1 pre-read, D2+V1 install, then F1, then X1 + V2 (`remove_st29_to_st27.sh`) and W2 (svc back to cottonwood).
- **Hard bound:** X1 + W2 run at the EARLIER of F1 done or **13:09:10Z** (CTO msg 3063). The laptop secret reader expires then too.
- **Superseded:** st28's own X1 is superseded by st29's X1, which lands on st27 directly.

## 4. F1, both branches

- **OPAL + READY + a served report:** FWD-1 is realized. I read the provider and confirm zero YCharts markers.
- **Any other end:** a finding. X1 and W2 run in every branch.

## COO HALF

**COO half SIGNED** -- `2.0.0_SA_COO~G2`, at pin `f0ff4f1653`, on the gate result, the 2-member delta and the legs above.

## CTO HALF

(owed; due by ~11:50Z so D2 lands when the queue reads 0/0)
