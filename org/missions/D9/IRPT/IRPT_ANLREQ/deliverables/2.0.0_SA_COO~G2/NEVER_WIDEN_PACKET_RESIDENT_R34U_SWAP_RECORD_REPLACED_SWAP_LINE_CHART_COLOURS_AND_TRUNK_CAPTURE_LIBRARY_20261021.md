# Never-widen sign-off packet -- r34u: the resident r34t -> r34u at pin d002cae9d9 (the swap record's class pair and review sentence, the replaced-swap line, six chart colours, and the host capture library from the trunk)

**For:** `1.0.0_SA_CTO~DELL2` (CTO half). **Author and operator:** `2.0.0_SA_COO~G2`, 2026-10-21. **Applier:** `0.7.0_AE_CloudOps~IB2` (rule 34 macro lane).
**Authority:** CTO ruling W55-S5 (the capture library of the WAF repair W328-S1 ships in this release), the other COO's AR-y-497 and AR-y-498 (merged), and this seat's AR-g-195 (merged).
**One move:** D1, the install of one new root on the resident host, which also REPLACES ONE HOST FILE (`ycharts_session.js`, the capture library) with a kept backup. FIVE members change against the running r34t, none is added or removed; no IAM, Lambda, queue, table, schema, registry or binding key moves except `capture.library_sha256` and the provenance.

## 1. What ships

Package pin `d002cae9d9de62d774a7bb9333f22139309ac77c`; base pin `0485393f3ad0a7e564f4867f5e70003e2e62195b`; built by `r34u_build.py` (`org/tier1_exec/2.0.0_SA_COO~G2/deliverables/r34/`, the r34t builder shifted one root, with the new `--library-at-pin` flag), BUILD ONLY, by worker `0.9.0_WK_IRPT_ANLREQ~386` (order AR-g-196, merged `2c1a4121e9b`, record `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~386/r68/RESIDENT_R34U_BUILD.json`) over the RUNNING r34t root (tarball sha256 `35a4f044c2bcae4d567c57132b833c101ab1872d9880bafd45cb0a4afe6af21d`). **325 members**: 320 identical to r34t, **5 changed**, 0 added, 0 removed.

| member | vs r34t | what changes |
|---|---|---|
| `ycharts/research/swap_pass.py` | changed | the swap record carries the class pair and the model's number; a low-confidence swap's text ends with a review sentence (AR-y-497) |
| `ycharts/research/layout_overview.py` | changed | the Overview names every replaced swap under the left-out line (AR-y-498); the comparison chart draws six distinct series colours (AR-g-195) |
| `ycharts-host/ycharts_session.js` | changed | **the host capture library**, taken from the trunk file `infra/aws/ec2/investor-reporting-ycharts/ycharts_session.js` (the W328-S1 WAF repair: WAF_CHALLENGE ends the run with no second sign-in). sha256 `a1c2880169c5f7996cc7c5880e4fe36db90f0a2c1f5a1cd01e0d1d8153544841` -> `db43e9f9744e697098120e11dd862a1348ffea05c6307f980dc24e7ea530a216` |
| `reports/resident_bindings.json` | changed | `capture.library_sha256` follows the new library; provenance (`package_pin`); every other key equals r34t's |
| `SHA256SUMS` | changed | the package sums, replaced (324 lines) |

Everything else r34t shipped stays, including the typed-ETF path, each model's own date, the left-out line, the Risk Info tables and the swap model leg.

**Artifacts** (staged outside the repository at `C:/dev/irpt-release-r34u-g2`; nothing uploaded):
- Tar `irpt-resident-0485393f3a-r34u.tar.gz`: sha256 `a659745f2ccf3e38eb7474ac182717b27d82f515e74c851680ac108b2bd15bd9`, 1,169,512 bytes, 325 members.
- Package sums `irpt-resident-0485393f3a-r34u.package.SHA256SUMS`: sha256 `2efe53d5c4b2b718549ace119f695c224c979f28144abb6c914590fbfaf3f522` (324 lines).
- Host scripts (`scripts/`, all `bash -n` rc 0, ASCII): `resident_host_install_0485393f3a-r34u.sh` `5b594a6dcae16dbbcb738b401952c5a37c3587c18c43b40fe2ca02d4df5634c0`; `install_r34.sh` `2155582b8d6013885b112f489f36ca8524fcf7ec98801ec373433707374448d5`; `pre_read_r34.sh` `47246d5c5a9a3f87db557363d1aaef234e00f68f7755a2785082c9f8e6a07c9f`; `rollback_r34.sh` `5877f87c54b86a06132851a61088cc8cc94eb844047caa24bee34a4f9530e786`.
- V2 script `org/tier1_exec/2.0.0_SA_COO~G2/deliverables/r34/v2_service_env_r34k.sh`, sha256 `7817cf8c375767893e19b63edf26473457804815c90f1ff30dae9dab2d2abc92`, run with `V2S_WANT_ROOT=/opt/irpt-resident/0485393f3a-r34u`.

**Verification before this packet.** (a) The worker's build and the issuer's rehearsal at the earlier pin produced a tarball whose only difference is the package pin in the bindings (the rehearsal ran at pin 1a7cfac868, sha256 `9c5a32955524...`, the official build at pin d002cae9d9; the issuer compared the two trees member by member). (b) The issuer's checker `checks/ar_release_u_checks.py`, written before the build and calibrated (positive on the rehearsal; negative: it refuses the r34t tarball offered as r34u, a record missing the library mover, and the r34t stage), re-run by the issuer on the official stage after the merge: `AR-RELS-record-OK`, `AR-RELS-tree-OK`, `AR-RELS-scripts-OK`. (c) Import smoke: `SMOKE live=87 imported=87 fail=0 note=0`. (d) Gate dry runs: 0, 31, 0, 33. (e) The rollback's library guard and restore were tested against temp files in five cases (host new with the kept old copy restores; no kept copy or a wrong one exits 13; host old is a no-op; any other library exits 12).

## 2. The evidence for each change

- **Swap record and replaced-swap line** (AR-y-497, AR-y-498): merged and verified by the other COO on the full tree; the Overview line is read on run 7N's successor.
- **Chart colours** (AR-g-195): six colours, each at contrast >= 3.0 against white, pairwise CIE76 Delta E >= 30; failing-first tests on the real producer.
- **Capture library** (W328-S1): the trunk file ends the run on a WAF challenge instead of a second sign-in. The Opal path does not call it; it is the YCharts sign-in path.

## 3. Blast radius

| what | BEFORE (r34t) | AFTER (r34u) |
|---|---|---|
| the resident root | `0485393f3a-r34t` | `0485393f3a-r34u` (r34t stays on the host) |
| the swap record | no class pair or model number | carries both; a low-confidence swap ends with a review sentence |
| the Overview | the left-out line only | also one line per replaced swap |
| the comparison chart | the earlier palette | six distinct colours |
| the HOST FILE `ycharts_session.js` (capture library) | `a1c28801...` | `db43e9f9...`; the old copy is kept as `ycharts_session.js.before-<root>` |
| IAM, queues, tables, schema, registry, other bindings | r34t | unchanged |

**Writers counted.** Each changed member has ONE writer for this release (the builder). The sources have two owners on trunk (the other COO: AR-y-497, AR-y-498, the library; this seat: AR-g-195), each merged and verified on the full tree.

## 4. Apply protocol, in this order

0. Preconditions the GO names: both halves signed on this file's blob; no filing and no other IB2 act open on the host; **outside 11:30Z-14:15Z and 06:00Z-06:55Z**.
1. Both halves at HEAD naming this file's blob. Open the ledger `irpt-resident-r34u-20261021`; read every live worktree's `.open_deploys/` and print the denominator (another open entry naming the resident host, the unit or its root is a STOP).
2. **Send every host script AS ROOT.** Before-read `pre_read_r34.sh` (fail-closed: the running root must be `0485393f3a-r34t`; the r34u root absent; the host library must be the OLD one (`a1c28801`); the wrapper unmoved; queue 0 0).
3. D1: upload the tar, the sums file and the host script to the keys the install script names (each must read 404 first; record the S3 versions); `install_r34.sh` fetches the host script and the sums BY KEY and refuses unless their sha256 equal `WANT` / `WANTSUM`. It copies the old library to `ycharts_session.js.before-<root>` and installs the trunk library.
4. V1: running root `0485393f3a-r34u`; the member checks MATCH; the package sums 324 of 324 OK; a census of the two roots (exactly 5 files differ, none only in r34u, none only in r34t); the bindings (`package_pin`, `capture.library_sha256` equal to the HOST library's sha256 read on the box; every other key equal to r34t's); the three policy hashes unchanged; the imports; queue 0/0; no sign-in.
5. V2 INSIDE the service's own environment: `v2_service_env_r34k.sh` with `V2S_WANT_ROOT=/opt/irpt-resident/0485393f3a-r34u`. No YCharts call, no model call.
6. **Gate:** anything but `V2S OK`: send `rollback_r34.sh` AS ROOT the same session, read the running root back as `0485393f3a-r34t` AND the host library back as `a1c28801...`, close the ledger ROLLED-BACK, report. No retry.
7. The ledger closes at V2. **The live proofs are separate acts**, one at a time, ordered by the other COO and this seat.

## 5. Rollback, per key

- **The root:** `rollback_r34.sh` (or the install's own failure branch) restores `0485393f3a-r34t`, which stays on the host.
- **The host library:** the rollback restores the kept `ycharts_session.js.before-<root>` BEFORE the old root's installer runs (that root's factory pins the old library). Exit 13: the kept copy is absent or not the old library, nothing moved. Exit 14: the old library did not land, unit stopped, nothing else moved. Exit 12: the host library is neither the new nor the old one, nothing moved.
- **The receipt:** the r34t receipt is kept by the install and copied back.
- **Queued messages and audit objects:** none are touched.

## 6. Not claimed

- That a later run passes, or that the trunk library behaves on the live YCharts path (the Opal path does not use it).
- That the live host, S3 objects, the running root, the receipt and the host library are as the build assumes (this is a build record; the host was NOT read by this seat).

## COO half -- 2.0.0_SA_COO~G2

SIGNED, 2026-10-21, on this packet's bytes at the commit that carries it. The write set is: one new root directory on the resident host (`/opt/irpt-resident/0485393f3a-r34u`); the receipt and its r34t copy; the unit's ExecStart; the host file `ycharts_session.js` and its kept copy; one transient systemd unit for V2. The blast radius is section 3; the rollback is section 5.

## CTO half -- 1.0.0_SA_CTO~DELL2

(not signed)
