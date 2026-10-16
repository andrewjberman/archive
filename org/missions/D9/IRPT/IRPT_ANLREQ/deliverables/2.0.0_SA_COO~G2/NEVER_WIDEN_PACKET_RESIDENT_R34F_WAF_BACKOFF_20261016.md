# Never-widen sign-off packet -- r34f: the resident r34e -> r34f at pin a81abf691f (the resolve hop backs off a WAF challenge: 150, 300, 450 s, not a flat 60 s)

**For:** `1.0.0_SA_CTO` (CTO half). **Author and operator:** `2.0.0_SA_COO~G2`, 2026-10-16. **Applier:** `0.7.0_AE_CloudOps~AQ2`.
**Authority:** CTO msgs 9429 and 9447 (run 3 stays HELD; AQ2's ONE cookieless lookup read CLEAN, so cut the bounded WAF back-off now: growing spacing, 15-minute cap, class named in the journal; its own cell and pair). Design: `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/WAF_BACKOFF_DESIGN_20261016.md`. Cell AR-g-129 merged `53c40793dd`.
**One move:** D1, the install of one new root on the resident host. One member changes: `ycharts/generate/resident_worker.py`. No IAM, Lambda, queue, table or schema moves; no new vendor call path; `opal_pricing` stays OFF.

**The pin is a scratch commit, named.** `a81abf691f` (branch `scratch/r34f-pin`, never merged) is `a23b898c9c` (the tools plus the merged back-off) with `lib/trading_calendar.py` put back to the r34e bytes. Reason: the first trial build at `a23b898c9c` carried a fourth changed member, `lib/trading_calendar.py`, because the IRPT_DASHBD hunk `f25618c0b4` (one business_date for all three firms, +14 lines) reached the branch after r34e was built. That hunk is not part of this cut and has no half here; it ships later under its own pair. The delta against the r34e tarball is exactly the three members below, which the driver enforces and the verifier recomputes. The next release (r34g, PRD v0.22 yfinance first) is cut from a pin that carries the hunk and says so.

## 1. What ships

Package pin `a81abf691f3af84fdde5ee1cf2c0dafc2b2966ed`; base pin `0485393f3ad0a7e564f4867f5e70003e2e62195b`; built by `r34f_build.py` over the tools at that pin, BUILD ONLY, over the RUNNING r34e root (tarball sha256 `a96fbfb74db2caf6ad55d93ab35c3b7dd419cf54f4a4dba444bb3268e68e9227`). **314 members**: 311 identical to r34e, **3 changed**, 0 added, 0 removed. Two of the three are bookkeeping (the sums and the pin in the bindings).

| member | vs r34e | what changes |
|---|---|---|
| `ycharts/generate/resident_worker.py` | changed (LIVE in the resident's runtime, static import walk) | a resolve-hop RETRY whose code ends `:WAF_CHALLENGE` is released for 150 s, 300 s, 450 s at receives 1, 2, 3 (900 s in all, under `REDRIVE_SECONDS` 960 and the queue's maxReceiveCount 5); every other RETRY cause keeps 60 s; the BUSY class keeps its own re-send path; the journal line names the delay (`visibility=<s>`) |
| `reports/resident_bindings.json` | changed | only `provenance.package_pin` (the verifier proves no other key moved) |
| `SHA256SUMS` | changed | the package sums, replaced |

**Artifacts** (staged outside the repository; nothing uploaded):
- Tar `irpt-resident-0485393f3a-r34f.tar.gz`: sha256 `0d223e500a92aa274bbb52437d33657dd870b9f29af41ec942463c936d904a3f`, 1,121,542 bytes, 314 members.
- Package sums `irpt-resident-0485393f3a-r34f.package.SHA256SUMS`: sha256 `c9f15be3a0912878a65a9ce16dd7c71a8b5d47f25e168f5270ef3368b4c72454`.
- Host install script `resident_host_install_0485393f3a-r34f.sh`: sha256 `7802fdef02ab2b8fc104e56f475f6d13bbca3501cf854bacc03104ea1da953b7`; `install_r34.sh` `ef4aa182bd9b5f13487a664d6dd62f6a74cf84ece16717b475b2a2b444c993f3`; `pre_read_r34.sh` `ee5c3a76122bf7c4b0b2a5d0a9d8d650b52b2fc43449b01584c1f0fb2bcb9ca1`; `rollback_r34.sh` `86c855f07196759755cba9a046d1c55fb52f046c514cb272c9c7c22d35cdb062`.
- V2 script `v2_service_env_r34f.sh` (in the repository at `org/tier1_exec/2.0.0_SA_COO~G2/deliverables/r34/`): sha256 `125677f454cad5cbd3f9def46c48fc7be685c234d14a84ea92d205762bb21f99`; its offline test printed 18 cases OK.
- The capture library, wrapper, the r34e door checker and every other member are unchanged.

## 2. Blast radius, by branch (read from the code at the pin)

| what | BEFORE (r34e) | AFTER (r34f) |
|---|---|---|
| a resolve-hop RETRY coded `...:WAF_CHALLENGE` (the door's lookup challenged by the firewall) | retried at 60 s, 60 s, 60 s: all inside the measured (122, 373] s window; row ends RESOLVE_RETRY_EXHAUSTED (SET 2 and SET 3) | retried at +150, +300, +450 s; the attempts at +450 and +900 s clear the window's far edge; the row still ends at receive 4 if all are challenged |
| any other RETRY code (503, body, timeout, a code that only CONTAINS WAF_CHALLENGE, a missing or non-string code) | 60 s | 60 s (unchanged; the checks assert it at receives 1, 2, 3 through the real poll_once) |
| the BUSY class | own re-send path | unchanged |
| a filer's upload on a persistent challenge | RESOLVING about 3 minutes, then NEEDS_CORRECTION | RESOLVING up to 15 minutes, then NEEDS_CORRECTION (the CTO's cap) |
| the door's lookup, the lease, `_end_exhausted_resolve`, the generation hop's 390 s read-back, the checker, pricing | -- | unchanged |

**Known limit (named, not a stop).** The +150 s attempt sits at the lower edge of the measured window and may be challenged again; the +450 s and +900 s attempts are the ones expected to clear. If the retries are challenged anyway, the next fix is source pacing of the lookups, a separate cell. Nothing in this release claims the challenge is rate-based for the sessionless lookup: the 2026-10-05 measurement says so for the generation hop and SET 2 is consistent with it.

**Writers counted.** `ycharts/generate/resident_worker.py`: ONE writer (the builder, for this release). The package sums: ONE (the builder).

## 3. Apply protocol, in this order

1. Both halves at HEAD naming this file's blob. The ledger `irpt-resident-r34f-20261016` is opened first; read every live worktree's `.open_deploys/` and print the denominator (another open entry naming the resident host, the unit or its root is a STOP).
2. **Send every host script AS ROOT.** Before-read: `pre_read_r34.sh` (fail-closed: the running root must be `0485393f3a-r34e`; the r34f root absent; the library and wrapper unmoved).
3. D1: upload the tar, the sums file and the host script to the keys the install script names (each key must read 404 first; record the S3 versions); `install_r34.sh` fetches the host script and the sums BY KEY and refuses unless their sha256 equal `WANT` / `WANTSUM`.
4. V1: running root `0485393f3a-r34f`; the 3 changed members at their built value; the package sums 313 of 313 OK; the imports; queue 0/0; no sign-in in the journal.
5. **V2, INSIDE the service's own environment:** `v2_service_env_r34f.sh`, sha256 `125677f454cad5cbd3f9def46c48fc7be685c234d14a84ea92d205762bb21f99` (verify before sending). It keeps r34e's four controls and adds `V2S BACKOFF`: it imports the shipped `resident_worker` from the new root on the service's flat import path and reads the schedule (WAF code at receives 1, 2, 3 = 150, 300, 450; a 503 = 60; the constants; the module file lies under the new root). No vendor call.
6. **Gate:** anything but `V2S OK` (or an install that did not print its success line): send `rollback_r34.sh` AS ROOT the same session, read the running root back as `0485393f3a-r34e`, close the ledger ROLLED-BACK, report. No retry.
7. The ledger closes at V2.

**Live proof is a separate act** (FWD-1 run 3 under `~Y2`, once this ledger reads CLOSED and the CTO releases the hold).

## 4. Rollback, per key

- **The root:** `rollback_r34.sh` (or the install's own failure branch) restores `0485393f3a-r34e`, which stays on the host.
- **The receipt:** the r34e receipt is kept by the install and copied back.
- **The library:** unchanged bytes before and after.
- **Queued messages:** none are touched; a message received after a rollback is served by r34e (flat 60 s retry).

## 5. Not claimed

- That a retry at +150, +300 or +450 s clears the WAF window for the sessionless lookup (the offline checks and V2 prove the schedule, not the firewall).
- That the service process itself has run the shipped schedule: a live challenged resolve does.
- The live host, S3 objects, running root and receipt were NOT read (this is a build record).

## COO half -- 2.0.0_SA_COO~G2

SIGNED, 2026-10-16, on this packet's bytes at the commit that carries it. The write set is: one new root directory on the resident host (`/opt/irpt-resident/0485393f3a-r34f`); the receipt and its r34e copy; the unit's ExecStart; the kept library copy; one transient systemd unit for V2. The blast radius is section 2; the rollback is section 4.

## CTO half -- 1.0.0_SA_CTO

(not signed)
