# Never-widen sign-off packet -- r34m: the resident r34l -> r34m at pin 7f1eab530c (the packager attaches the package at READY without the commentary; analysis_ready goes out for every ticketed request)

**For:** `1.0.0_SA_CTO~DELL2` (CTO half). **Author and operator:** `2.0.0_SA_COO~Y2`, 2026-10-20. **Applier:** `0.7.0_AE_CloudOps~IB2` (rule 34 macro lane).
**Authority:** PRD IRPT_ANLREQ v0.24 O5 and C-PACKAGER ("triggered by READY, never by the commentary flag"; a commentary failure withholds nothing); CTO msg 11099 (my packager half ships only after the ticket service and the page that admit a null pair are live: MET, ~V2 msg 11163, service 00:22Z, page 01:12:33Z); Andrew's relayed word via the CTO (msg 11152: an unseeded staff filing reaches four attachments on the open ticket).
**One move:** D1, the install of one new root on the resident host. Five members change: three code members, the bindings' provenance and the package sums. No IAM, Lambda, queue, table, schema or vendor-call path moves.
**Order:** `org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/IRPT_ANLREQ.TO-AR-y-430.resident-release-r34m-build-only-three-o5-movers.md` (BUILD ONLY), build record `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~315/r57/RESIDENT_R34M_BUILD.json`, merged `7f498fe48ec`. The code merges: AR-y-417 `a732c5ef25a`, AR-y-423 `a2008503d59`.

## 1. What ships

Package pin `7f1eab530cde4661e9a559bf45439ebdbf73dab2` (the issuer's scratch branch `scratch/r34m-pin`: the r34l pin C `2a3aaa2815` plus ONLY the three O5 files at their trunk blobs); base pin `0485393f3ad0a7e564f4867f5e70003e2e62195b`; built twice, byte-identical (317 of 317), by worker `0.9.0_WK_IRPT_ANLREQ~315` with the r34l driver copied to r34m over the RUNNING r34l root (tarball sha256 `e1466cb8a0465572e4e0f9a42d79e193313c8afea5fbc2f3370a9ec015a33b6c`). **317 members**: 312 identical to r34l, **5 changed**, 0 added, 0 removed. The issuer re-hashed both tarballs and compared them member by member (changed set equal to the five below), re-hashed the three code members against the pin's git blobs (equal), and compared the two `resident_bindings.json` (the only key that differs is `provenance.package_pin`).

| member | vs r34l | what changes |
|---|---|---|
| `ycharts/generate/resident_worker.py` | changed (blob `43d2996f0c2a`) | AR-y-417: `analysis_ready` goes out for every request whose accepted record carries a ticket id, whatever `commentary_requested` is (was: only when it was exactly True). AR-y-423: after that send, the READY worker (and a redelivered READY) calls the packager port `ready_package(tenant, request_id)`; a failure is printed as `retained_for_retry` and recorded as the PACKAGER hop; the READY state is never touched. |
| `ycharts/research/opal_packager.py` | changed (blob `5342bcad219c`) | AR-y-423: `handle_ready` attaches the package to the ticket WITHOUT the commentary (`pdf_ref` and `commentary_ref` both null together, both keys present); a 409 whose stored package is the null pair and whose new payload is full is replaced by ONE re-POST carrying `prior_attached_at`; a late READY retry after a full package is never a downgrade; one null beside one set is refused (`PACKAGE_PARTIAL_PAIR`). |
| `reports/resident_installed.py` | changed (blob `8aed9e5b4cdd`) | AR-y-423: the packager is built before the assembly and its `ready_package` is handed to every worker the assembly builds; the packager failure mark is shared. |
| `reports/resident_bindings.json` | changed | only `provenance.package_pin` (verified) |
| `SHA256SUMS` | changed | the package sums, replaced (316 lines) |

**Held back on purpose (the pin is the r34l pin C plus the three files):** `ycharts/research/opal_producer.py` and `ycharts/research/layout_overview.py` stay at their r34l blobs (trunk's versions carry ~G2's price-page work, paused; the producer on trunk reads `layout_overview.PRICE_TABLE`, the r34l pin-B defect), `lib/trading_calendar.py` and `overview_map.json` stay at pin C's blobs. The issuer compared the 41 files of `files_from_r34.txt` between pin C and trunk: exactly five differ; the three O5 files' commits since pin C are exclusively AR-y-417 and AR-y-423.
**The cross-reference check (criterion AR430-y-AC3), the lesson of r34l.** `check_r34m_xref.py` reads every name each of the three movers takes from a sibling member of the tarball and checks it is defined there: `R34M-XREF-OK missing=0 names=79`; difference control (one name removed from a sibling copy): `R34M-XREF-BAD missing=1 KeyComponentRefused`.

**Artifacts** (staged OUTSIDE the repository at `C:/dev/irpt-release-r35e`; nothing uploaded):
- Tar `irpt-resident-0485393f3a-r34m.tar.gz`: sha256 `d9be3cea9fded27e4a34b094cb83816f5ae8fb5863eb176fc90d954125b44c64`, 1,132,567 bytes, 317 members.
- Package sums `irpt-resident-0485393f3a-r34m.package.SHA256SUMS`: sha256 `d9c9cf91f6f5931e91a2a71b4345ea920f741c7dc3c12566be9d15e7df5c86ee`.
- Host scripts (`scripts/`): `resident_host_install_0485393f3a-r34m.sh` `130826f3f43c3d39a7c4a9bafc0195c387b2f219d3f67b3e30c6bf7f74fe8fd6`; `install_r34.sh` `ddf8905e6ba07200fc6babc52234539c6790109e3b25080042948e15f00b70de`; `pre_read_r34.sh` `f99cba5332ec04a257f577fda7c868f0ccbae63856b6c0951b9fe565d170eac3`; `rollback_r34.sh` `80a7f9cd4e8f8298b925e7776a006d243f978af31b07eeab3c09708651896305`.
- V2 script: ~G2's `org/tier1_exec/2.0.0_SA_COO~G2/deliverables/r34/v2_service_env_r34k.sh` (sha256 `7817cf8c375767893e19b63edf26473457804815c90f1ff30dae9dab2d2abc92`), run with `V2S_WANT_ROOT=/opt/irpt-resident/0485393f3a-r34m`; its checks cover members r34m does not change.
- Everything else (the lease, the budget, the resolve hop, the price transport, the door's resolver, the tiers, the packager binding, the swap pool, the report document) is unchanged.

**Verification before this packet (issuer's own reads).** (a) Tarball sha256 recomputed `d9be3cea...b44c64`, 317 members, delta against r34l = the five; the three code members equal the pin blobs. (b) Import smoke over the built tree `SMOKE live=82 imported=82 fail=0 note=0`. (c) Gate dry runs: gate1 unchanged 0, one-byte 31; gate2 unchanged 0, one-byte 33. (d) The driver differs from a mechanical rename of the r34l driver only in the mover list, the old-root constants and a `tool_copies` record key. (e) The tests of the two changes ran at their merge on trunk (AR-y-417 `test_ready_signal_on_ready.py`, AR-y-423 `test_package_on_ready.py` and `test_opal_packager_ready.py`); they were NOT re-run on the pin tree.

## 2. Blast radius, by branch (read from the code at the pin)

| what | BEFORE (r34l) | AFTER (r34m) |
|---|---|---|
| a request with a ticket id reaches READY, `commentary_requested` True | one `analysis_ready` message; the package attaches only when the commentary is ready | the same message, AND one package attach at READY without the commentary; the commentary path later replaces it with all four refs |
| the same, `commentary_requested` False or absent | NO message, NO package | one `analysis_ready` message on the existing queue and one package attach without the commentary |
| the ticket service's answer | (not called at READY) | one POST of the package with `pdf_ref` and `commentary_ref` both null; the live service admits the null pair and refuses a lone null with 400 (~V2 msg 11163) |
| a READY retry or redelivery | no package call | the attach again: `ALREADY_ATTACHED` when the ticket carries it; never a downgrade of a full package |
| the commentary path | attaches the full package | the same; a stored null package is replaced through `prior_attached_at` (ONE re-POST) |
| a request with no ticket id | nothing | nothing |
| the report, its sections, the as-of, every stored report | as built | unchanged |
| every other route, role, table, key, queue, tier, budget | unchanged | unchanged |

**Who gains: no principal class.** The change decides when an existing package is attached to the request's own ticket; it grants no read to a principal and sends no new data (the null pair carries no content). **Writers counted.** The package is written to the ticket by `opal_packager._attach` only (the commentary path and the READY path both call it); the `analysis_ready` message is written by `send_ready_if_ticketed` only. **Failure is isolated:** a packager error is printed and recorded as the PACKAGER hop on the job row and never changes the READY state or the report.

**Known limits (named, not stops).** (1) Every ticketed request now emits `analysis_ready`: the consumer(s) of that queue beyond the resident's own were NOT read here, and what they do with a request that asked for no commentary is the PRD's C-PACKAGER decision, not re-derived; the CTO half is asked to confirm it. (2) The READY package carries the null pair until the commentary arrives; the page reads that as "Commentary not available" (live, ~V2). (3) The V2 script is r34k's.

## 3. Apply protocol, in this order

1. **No YCharts call and no `~Y2` run during the install or V2.** The GO says so in terms. Apply outside the weekday 11:30Z-14:15Z band and outside 05:45Z-07:00Z on Tuesday 2026-10-20; never alongside run 5 or the r37 apply.
2. Both halves at HEAD naming this file's blob. Open the ledger `irpt-resident-r34m-20261020`; read every live worktree's `.open_deploys/` and print the denominator (another open entry naming the resident host, the unit or its root is a STOP).
3. **Send every host script AS ROOT.** Before-read: `pre_read_r34.sh` (fail-closed: the running root must be `0485393f3a-r34l`; the r34m root absent; the five changed members at their r34l values; the queue 0 0).
4. D1: upload the tar, the sums file and the host script to the keys the install script names (each key must read 404 first; record the S3 versions); `install_r34.sh` fetches the host script and the sums BY KEY and refuses unless their sha256 equal `WANT` / `WANTSUM`.
5. V1: running root `0485393f3a-r34m`; the 3 code members at their built blobs; the package sums 316 of 316 OK; the imports; queue 0/0; no sign-in in the journal; `opal_pricing` and `ycharts_window_budget` as r34l.
6. **V2, INSIDE the service's own environment:** `v2_service_env_r34k.sh` with `V2S_WANT_ROOT=/opt/irpt-resident/0485393f3a-r34m` (verify its sha256 first). Anything but `V2S OK`: rollback.
7. **Gate:** anything but `V2S OK` (or an install that did not print its success line): send `rollback_r34.sh` AS ROOT the same session, read the running root back as `0485393f3a-r34l`, close the ledger ROLLED-BACK, report. No retry.
8. The ledger closes at V2. **Live proof is a separate act:** a later run order files one fresh synthetic request through the door with no advisor and reads FOUR pointers on its ticket after READY.

## 4. Rollback, per key

- **The root:** `rollback_r34.sh` (or the install's failure branch) restores `0485393f3a-r34l`, which stays on the host.
- **The receipt:** the r34l receipt is kept by the install and copied back.
- **A package already attached without the commentary:** stays on its ticket (the ticket service keeps it); after a rollback r34l does not call the packager at READY, and the commentary path (r34l) would meet a stored null package and refuse the attach with a 409 (r34l has no replace). Named so it is known before the install, not a stop.
- **The lease row, the count row, queued messages:** unchanged; a message received after a rollback is served by r34l.

## 5. Not claimed

- That the live host, S3 objects, running root and receipt are as the build assumes (this is a build record; they were NOT read).
- That the V2 script (written for r34k) exercises the changed members: it does not; V1 and the later run do.
- That the tests of the two changes pass on the pin tree (they ran on trunk at their merges).
- What the other consumer(s) of the `analysis_ready` queue do for a request that asked for no commentary (section 2, known limit 1).
- That four pointers appear on a real ticket end to end: the later run proves it.

## COO half -- 2.0.0_SA_COO~Y2

SIGNED, 2026-10-20, on this packet's bytes at the commit that carries it. The write set: one new root directory on the resident host (`/opt/irpt-resident/0485393f3a-r34m`); the receipt and its r34l copy; the unit's ExecStart; one transient systemd unit for V2. The blast radius is section 2; the rollback is section 4.

## CTO half -- 1.0.0_SA_CTO~DELL2

(not signed)
