# Never-widen sign-off packet -- r34p: the resident r34o -> r34p at pin 919bb891fa (r34o minus the registry change: the policy hashes of irpt-anlreq-x10-v1 and irpt-dashbd-x10-v1 return to r34n's, so retention rows reserved under them are valid again)

**For:** `1.0.0_SA_CTO~DELL2` (CTO half). **Author and operator:** `2.0.0_SA_COO~G2`, 2026-10-21. **Applier:** `0.7.0_AE_CloudOps~IB2` (rule 34 macro lane).
**Authority:** CTO msg 11639 (ruling A: r34p = r34o minus the registry change; a revision that has rows is never edited; ANALYSIS_AUDIT returns later as a NEW revision; the packet carries a census of retention rows and the byte-equality of the registry with r34n's). The defect: run 7e on r34o stopped at P4 with RetentionRefused (IB2 row S239); this seat's measured lead (msg 11637) was confirmed by the CTO against `reports/retention.py:147`.
**One move:** D1, the install of one new root on the resident host. THREE members change against the running r34o and none is added or removed; no IAM, Lambda, queue, table, schema or vendor-call path moves.

## 1. What ships

Package pin `919bb891fa72dd706493f094c9b4412503fcf42a`; base pin `0485393f3ad0a7e564f4867f5e70003e2e62195b`; built by `r34p_build.py` (`org/tier1_exec/2.0.0_SA_COO~G2/deliverables/r34/`, the r34o builder shifted one root), BUILD ONLY, by worker `0.9.0_WK_IRPT_ANLREQ~336` (order AR-g-180, merged `a82761941d9`, record `deliverables/0.9.0_WK_IRPT_ANLREQ~336/r63/RESIDENT_R34P_BUILD.json`) over the RUNNING r34o root (tarball sha256 `df070b09230f1e2dd1068291f6fe1f7e2078413dae6ea263b95242e09e25670b`). **323 members**: 320 identical to r34o, **3 changed**, 0 added, 0 removed. The files-from list is 47 lines (r34o's 48 without the registry file).

| member | vs r34o | what changes |
|---|---|---|
| `infra/logic/registry/reporting_policies.json` | changed | back to the r34n bytes (sha256 `229eca2d1ec7c6f8bf93...`, see the context of the IB2 order for the full value); r34o's copy (`4f7941bcccfb546e1d0b...`) added the ANALYSIS_AUDIT family and a FILLED_REPORT row, which moved the policy_sha256 of `irpt-anlreq-x10-v1` (8edbe84b05765c36 to cfed04bb8c2f1982) and `irpt-dashbd-x10-v1` (301c58e24ff0feda to 244a20425ba40cde) |
| `reports/resident_bindings.json` | changed | `provenance` only: `package_pin`, `files_from_count` (47) and `files_from_sha256`; the release checker proves every other key equals r34o's (the Overview map pin, the packager, the tiers, the budget) |
| `SHA256SUMS` | changed | the package sums, replaced (322 lines) |

Everything else r34o shipped stays: FWD-10 Core (comparison section, model reader), the Overview price pages, the audit modules (`ticket_audit_source`, `analysis_audit` and its schema; dormant, because the audit family is not in the registry and `IRPT_TICKETS_TABLE` is unset on the host), the additive `lib/trading_calendar.py` function. With the registry at r34n's bytes `analysis_audit.audit_address` is refused by name (AddressRefused, recorded as AUDIT_REFUSED:AUDIT_ADDRESS_REFUSED, the attach stands); the audit returns under its own pair with a NEW revision (CTO ruling).

**Artifacts** (staged outside the repository at `C:/dev/irpt-release-r34p-g2`; nothing uploaded):
- Tar `irpt-resident-0485393f3a-r34p.tar.gz`: sha256 `4991c7bcba0f01cb47b06bfa8c4e30f3fe47a6cbd6e9b9f479d1d39b77b49ea4`, 1,153,056 bytes, 323 members.
- Package sums `irpt-resident-0485393f3a-r34p.package.SHA256SUMS`: sha256 `3c166d774e500c25a3839e202e893e28fc6b0463aae84e6543b7d68fa5dd68bf` (322 lines).
- Host scripts (`scripts/`, all `bash -n` rc 0, ASCII): `resident_host_install_0485393f3a-r34p.sh` `126236bb20b911d5c108a5159e999c2a07800a8fc1ccbe2dee454753d9f6ba71`; `install_r34.sh` `4c3f7a94de282cf9c410215a99d8ebdee7aa713d0ee67c5c76b771619f4adb03`; `pre_read_r34.sh` `b19bff82e2fbc7a4493875954a3e67c51408171504914d79298e9291f65bfc80`; `rollback_r34.sh` `329286fa1c7c50150b4f9315e95a67bb3374c909ee2bf329a1f0d542d2192510`.
- V2 script `org/tier1_exec/2.0.0_SA_COO~G2/deliverables/r34/v2_service_env_r34k.sh`, sha256 `7817cf8c375767893e19b63edf26473457804815c90f1ff30dae9dab2d2abc92`, run with `V2S_WANT_ROOT=/opt/irpt-resident/0485393f3a-r34p`.

**Verification before this packet.** (a) The worker's build and the issuer's own rehearsal at the same pin produced the SAME tarball sha256 (fixed clock), builds identical 323 of 323. (b) The issuer's release checker `checks/ar_release_p_checks.py`, written before the build and calibrated on the rehearsal (it refuses the r34o tarball offered as r34p: the delta is empty, the registry is not r34n's, the bindings are unmoved, and the policy hashes of `irpt-anlreq-x10-v1` and `irpt-dashbd-x10-v1` differ), re-run by the issuer on the official stage: `AR-RELP-record-OK`, `AR-RELP-tree-OK`, `AR-RELP-scripts-OK`. The tree arm computes `reporting_policy()` for EVERY revision of the packaged registry with the tarball's own `lib/opal_naming.py` in a fresh `-I` interpreter and requires each `policy_sha256` to equal the r34n tarball's; and requires the registry file byte-equal to r34n's (the CTO's second condition). (c) Import smoke over the built tree: `SMOKE live=86 imported=86 fail=0 note=0`. (d) Gate dry runs: 0, 31, 0, 33.

## 2. Census of RETENTION rows (the CTO's first condition; read-only, IB2 `A_CENSUS.txt`, 2026-10-21T00:36Z)

Table `irpt-requests`; 2506 items scanned; 709 hold a policy_sha256; r34o epoch 1792537964 (23:12:44Z).

| revision / stored hash | created before r34o | created since r34o |
|---|---|---|
| `irpt-anlreq-x10-v1` 8edbe84b05765c36 (the r34n hash) | 9 (all firm `49financial`; Andrew's ticket rows are among them) | 1 (firm `49financial`, synthetic yes: run 7e's) |
| `irpt-anlreq-x10-v1` cfed04bb8c2f1982 (the r34o hash) | 0 | **0** |
| `irpt-dashbd-x10-v1` 301c58e24ff0feda (r34n) / 244a20425ba40cde (r34o) | 0 / 0 | 0 / 0 |
| any other hash on these two revisions | 0 | 0 |

**Reading.** No row carries a NEW hash: the rows are written with the OLD hash by the service that reserves them, and the resident under r34o compared them with its own (new) registry, which is why every one of the 10 rows was refusable (9 before the install, among them Andrew's, and run 7e's one since). Under r34p the resident's registry is r34n's again, so all 10 become valid; nothing needs repair, migration or deletion. Synthetic judged only by an id or address from the run receipts (48 tokens read); the 9 earlier rows are not synthetic.

## 3. Blast radius

| what | BEFORE (r34o) | AFTER (r34p) |
|---|---|---|
| the policy hash the resident computes for `irpt-anlreq-x10-v1` / `irpt-dashbd-x10-v1` | cfed04bb8c2f1982 / 244a20425ba40cde | 8edbe84b05765c36 / 301c58e24ff0feda (r34n's: equal to what the rows carry) |
| the 10 existing retention rows of those revisions (9 incl. Andrew's, 1 synthetic) | refused (hash differs) | valid |
| a new filing's retention under `irpt-anlreq-x10-v1` | RetentionRefused at the packager hop (run 7e) | as on r34n (run 7d passed) |
| FWD-10 comparison section, price pages, model reads | live | live, unchanged |
| the audit record | address resolves, ports unwired | address refused by name, ports unwired; the attach stands |
| lease, budget, tiers, packager `api_base`, producer list | r34o | unchanged |

**Writers counted.** Each changed member: ONE writer (the builder, for this release). The bindings file and the package sums: ONE (the builder).

## 4. Apply protocol, in this order

0. Preconditions the GO names: both halves signed on this file's blob; no filing and no other IB2 act open; Y2's audit-policy apply stays queued until this release is live (CTO msg 11639).
1. Both halves at HEAD naming this file's blob. Open the ledger `irpt-resident-r34p-20261021`; read every live worktree's `.open_deploys/` and print the denominator (another open entry naming the resident host, the unit or its root is a STOP).
2. **Send every host script AS ROOT.** Before-read `pre_read_r34.sh` (fail-closed: the running root must be `0485393f3a-r34o`; the r34p root absent; the library and wrapper unmoved; the registry member at its r34o value; queue 0 0).
3. D1: upload the tar, the sums file and the host script to the keys the install script names (each must read 404 first; record the S3 versions); `install_r34.sh` fetches the host script and the sums BY KEY and refuses unless their sha256 equal `WANT` / `WANTSUM`.
4. V1: running root `0485393f3a-r34p`; the registry member MATCH; the package sums 322 of 322 OK; a census of the two roots (exactly 3 files differ, none only in either); THE CURE read on the host (the two policy hashes print 8edbe84b05765c36 and 301c58e24ff0feda and the packaged registry file equals r34n's sha256); the bindings (`package_pin`, `files_from_count` 47, the Overview map pin, the packager alias unchanged); the imports; queue 0/0; no sign-in; `IRPT_TICKETS_TABLE` set or unset.
5. V2 INSIDE the service's own environment: `v2_service_env_r34k.sh` with `V2S_WANT_ROOT=/opt/irpt-resident/0485393f3a-r34p`. No YCharts call.
6. **Gate:** anything but `V2S OK`: send `rollback_r34.sh` AS ROOT the same session, read the running root back as `0485393f3a-r34o`, close the ledger ROLLED-BACK, report. No retry. (Rollback returns to r34o, which carries the retention defect; r34n is the older root on the host.)
7. The ledger closes at V2. **The live proof is a separate act**: run 7f (Multi-Comp) and a repeat of run 7e's Overview filing, each ONE filing, never alongside another IB2 act.

## 5. Rollback, per key

- **The root:** `rollback_r34.sh` (or the install's own failure branch) restores `0485393f3a-r34o`, which stays on the host; `0485393f3a-r34n` also stays.
- **The receipt:** the r34o receipt is kept by the install and copied back.
- **Queued messages:** none are touched.

## 6. Not claimed

- That run 7e's Overview filing now passes: it is the next act after the install.
- That the reserving service and the resident will keep sharing one registry hash: the rule going forward is the CTO's (a revision that has rows is never edited; new families under a new revision).
- That the live host, S3 objects, the lease row, the running root and receipt are as the build assumes (this is a build record plus a read-only census; the host was NOT read by this seat).

## COO half -- 2.0.0_SA_COO~G2

SIGNED, 2026-10-21, on this packet's bytes at the commit that carries it. The write set is: one new root directory on the resident host (`/opt/irpt-resident/0485393f3a-r34p`); the receipt and its r34o copy; the unit's ExecStart; the kept library copy; one transient systemd unit for V2. The blast radius is section 3; the rollback is section 5.

## CTO half -- 1.0.0_SA_CTO~DELL2

(not signed)
